from setuptools import setup, find_packages

setup(
    name='house_findisc',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'httpx~=0.7.8',
        'pdfplumber~=0.5.14',

    ]
)
