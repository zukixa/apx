from curl_cffi.requests import AsyncSession
import aiohttp
import asyncio
import re
import random
import lxml.html as lh

class AsyncProxier:
    def __init__(self, country_id=None, timeout=0.5, anonym=False, elite=False, google=None, https=False, verify_url=None):
        self.country_id = country_id
        self.timeout = timeout
        self.anonym = anonym
        self.elite = elite
        self.google = google
        self.schema = 'https' if https else 'http'
        self.verify_url = 'www.google.com' if not verify_url else verify_url.split('://')[1]
        self.current_proxy = None
        
    async def __check_if_proxy_is_working(self, session, proxies):
        url = f'{self.schema}://{self.verify_url}'
        try:
            async with session.get(url, proxy=proxies[self.schema], timeout=self.timeout) as response:
                if response.status == 200:
                    if response.connection:
                        pattern = r"URL\('(.+?)'\)"
                        match = re.search(pattern, str(response.connection))
                        if match:
                            return proxies[self.schema]
                        else:
                            pass
        except asyncio.TimeoutError:
            pass
        except aiohttp.ClientError:
            pass

        return None
    def __criteria(self, row_elements):
        country_criteria = True if not self.country_id else row_elements[2].text_content(
        ) in self.country_id
        elite_criteria = True if not self.elite else 'elite' in row_elements[4].text_content(
        )
        anonym_criteria = True if (
                                        not self.anonym) or self.elite else 'anonymous' == row_elements[4].text_content()
        switch = {'yes': True, 'no': False}
        google_criteria = True if self.google is None else self.google == switch.get(
            row_elements[5].text_content())
        https_criteria = True if self.schema == 'http' else row_elements[6].text_content(
        ).lower() == 'yes'
        return country_criteria and elite_criteria and anonym_criteria and google_criteria and https_criteria
    async def freeproxy(self):
        urls = [
            'https://www.sslproxies.org/',
            'https://free-proxy-list.net/uk-proxy.html',
            'https://www.us-proxy.org',
            'https://free-proxy-list.net'
        ]
        async with aiohttp.ClientSession() as session:
            r = await session.get(random.choice(urls))
            doc = lh.fromstring(await r.text())
            tr_elements = doc.xpath('//*[@id="list"]//tr')
            proxies = [f'{tr_elements[i][0].text_content()}:{tr_elements[i][1].text_content()}'
                        for i in range(1, len(tr_elements)) if self.__criteria(tr_elements[i])]
            return proxies

    async def proxyscrape(self):
        params = {
            'request': 'displayproxies',
            'protocol': self.schema,
            'timeout': self.timeout * 1000 if self.timeout else '10000',
            'country': self.country_id if self.country_id else 'all',
            'ssl': 'all',
            'anonymity': 'elite' if self.anonym else 'all'
        }
        async with aiohttp.ClientSession() as session:
            r = await session.post('https://api.proxyscrape.com/v2/', params=params)
            return (await r.text()).strip().replace('\r', '').split('\n')

    async def proxylist(self):
        params = {
            'type': self.schema,
            'country': self.country_id if self.country_id else 'none',
            'anonymity': 'elite' if self.anonym else 'none'
        }
        async with aiohttp.ClientSession() as session:
            r = await session.get('https://www.proxy-list.download/api/v1/get', params=params)
            return (await r.text()).strip().replace('\r', '').split('\n')

    async def get(self):
        """Returns a working proxy that matches the specified parameters."""
        ps = await self.proxyscrape()
        pl = await self.proxylist()
        fp = await self.freeproxy()
        proxy_list = ps + pl + fp
        random.shuffle(proxy_list)
        working_proxy = None
        async with aiohttp.ClientSession() as session:
            for proxy_address in proxy_list:
                proxies = {self.schema: f'http://{proxy_address}'}
                try:
                    working_proxy = await self.__check_if_proxy_is_working(session, proxies)
                    if working_proxy:
                        self.current_proxy = working_proxy
                        return working_proxy
                except:
                    continue
        raise Exception('There are no working proxies at this time.')
    
    async def update(self, refresh_needed=False):
        if refresh_needed or not self.current_proxy:
            self.current_proxy = await self.get()
        return self.current_proxy
    