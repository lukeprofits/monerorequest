from setuptools import setup

setup(
    name='monerorequest',
    version='2.1.0',
    author="Luke Profits",
    description="monerorequest is an easy way to create/decode Monero Payment Requests.",
    url="https://github.com/lukeprofits/monerorequest",
    packages=['monerorequest'],
    package_dir={'monerorequest': 'src/monerorequest'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
