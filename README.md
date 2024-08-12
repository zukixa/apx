# TODO:

- put on pip
- polish the github repo

# AsyncProxier: Asynchronous Free Proxy Fetcher

[![PyPI](https://img.shields.io/pypi/v/asyncproxier)](https://pypi.org/project/apx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AsyncProxier is a Python library that fetches and validates free proxies asynchronously. It scrapes proxies from multiple sources, checks their validity, and provides you with a working proxy that matches your specified criteria.

## Features

- **Asynchronous:** Uses `aiohttp` and `asyncio` for fast and efficient proxy fetching.
- **Multiple Sources:** Scrapes proxies from various websites, including sslproxies.org, us-proxy.org, free-proxy-list.net, proxyscrape.com, and proxy-list.download.
- **Filtering:** Filter proxies by country, anonymity level (elite/anonymous), Google support, and HTTPS support.
- **Validation:** Verifies that the returned proxy is working by connecting to a specified URL (defaults to google.com).
- **Easy to Use:** Simple and intuitive API for fetching and updating proxies.

## Installation

```bash
pip install apx
```

## Usage

```python
from apx import AsyncProxier
import asyncio
import httpx

async def main():
    # Initialize the proxier with desired settings
    proxier = AsyncProxier(country_id=['US'], https=True, anonym=True)

    # Get an initial working proxy
    proxy = await proxier.get()
    print(f"Initial working proxy: {proxy}")

    # Main usage of this client.
    for i in range(80):
        # Perform the HTTP request using the last working proxy.
        async with httpx.AsyncClient(proxies=(await proxier.update())) as sesh:
            try:
                response = await sesh.get('https://www.google.com')
                if response.status_code == 200:
                    # Request was successful, other code possible.
                    print("Request successful!")
                else:
                    # Request failed, raise an exception to try again with a new proxy
                    raise Exception('Proxy Error')
            except Exception as e:
                # Request failed, print the error message and continue to the next attempt with new proxy.
                print(f"Request failed: {str(e)}")
                await proxier.update(True) # Updating the proxy is necessary at an error.
                continue

if __name__ == "__main__":
    asyncio.run(main())
```

## Parameters

The `AsyncProxier` class accepts the following parameters:

- `country_id` (list, optional): A list of country codes to filter proxies by. Defaults to None (no country filter).
- `timeout` (float, optional): The timeout for proxy validation in seconds. Defaults to 0.5.
- `anonym` (bool, optional): Whether to only return anonymous or elite proxies. Defaults to False.
- `elite` (bool, optional): Whether to only return elite proxies. Defaults to False.
- `google` (bool, optional): Whether to only return proxies that support Google. Defaults to None (no Google filter).
- `https` (bool, optional): Whether to only return HTTPS proxies. Defaults to False.
- `verify_url` (str, optional): The URL to use for proxy validation. Defaults to 'www.google.com'.

## Inspiration and Continuation

This project is inspired by the [free-proxy](https://github.com/jundymek/free-proxy) repository, but it serves as an asynchronous continuation and expansion. The original source is unmaintained and lacks features like asynchronous operation and support for multiple proxy sources. AsyncProxier addresses these limitations and provides a more robust and efficient solution for fetching free proxies.

```

```
