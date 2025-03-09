from setuptools import setup, find_packages
from pathlib import Path

from conf import VERSION

DIR = Path(__file__).parent

with open(str(DIR / 'requirements.txt'), 'r') as fp:
    lines = fp.read().splitlines()
    REQUIREMENTS = lines if lines else []

setup(
    name='passlock',
    version=VERSION,
    author='roysmanfo',
    url='https://github.com/roysmanfo/PassLock',
    install_requires=REQUIREMENTS,
    packages=find_packages(include=['src']),
    entry_points={
        'console_scripts': ['passlock=src.main:main']
    }
)
