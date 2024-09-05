from setuptools import setup, find_packages
from pathlib import Path

CONF = {}
DIR = Path(__file__).parent
with open(str(DIR / 'src' / '.conf'), 'r') as fp:
    lines = fp.read().splitlines()
    # if additional info is added in .conf the logic should change
    CONF['version'] = lines[0][len('version='):]

with open(str(DIR / 'requirements.txt'), 'r') as fp:
    lines = fp.read().splitlines()
    CONF['requirements'] = lines if lines else []

setup(
    name='passlock',
    version=CONF['version'],
    author='roysmanfo',
    url='https://github.com/roysmanfo/PassLock',
    install_requires=CONF['requirements'],
    packages=find_packages(include=['src']),
    entry_points={
        'console_scripts': ['passlock=src.main:main']
    }
)
