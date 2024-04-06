from setuptools import setup, find_packages

setup(
    name="nfce-scraper",
    version="1.1.0",
    description="A python web scraper for Brazilian eletronic invoice",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="AGPL-3.0",
    author="Yuri Silveira",
    author_email="ypereirars@gmail.com",
    url="https://github.com/ypereirars/nfcescraper",
    packages=["nfce"] + ["nfce." + pkg for pkg in find_packages("nfce")],
    install_requires=open("requirements.txt").read().split("\n"),
    setup_requires=["flake8", "wheel"],
)
