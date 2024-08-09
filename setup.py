import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='axp',
    version='1.0.0',
    author="zukixa",
    author_email="56563509+zukixa@users.noreply.github.com",
    description="Proxy scraper for further use",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zukixa/axp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['lxml', 'aiohttp']
)
