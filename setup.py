from setuptools import find_packages, setup

setup(
    name='thelocals',
    version='0.1.0',
    author='Timofey Kukushkin',
    author_email='tima@kukushkin.me',
    description='Поиск жилья на сайте http://thelocals.ru',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'aiohttp',
        'aiotg',
        'asyncio-redis',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'thelocals=thelocals.cli:cli',
        ],
    },
)
