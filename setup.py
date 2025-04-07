from setuptools import setup, find_packages
from pathlib import Path

from passlock.conf import VERSION

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
    packages=find_packages(include=['passlock']),
    package_dir={"": "."},
    package_data={
        "passlock": [".conf"],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': ['passlock=passlock.main:main']
    }
)
