import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="en16931",
    version="0.2",
    author="Invinet Sistemes",
    author_email="jtorrents@ingent.net",
    description="A Python 3 package to parse, generate and manage the EN16931 Invoice format",
    long_description=long_description,
    url="https://github.com/invinet/python-en16931",
    packages=setuptools.find_packages(),
    package_data={
        'en16931': ['templates/*'],
    },
    install_requires=[
        "requests",
        "py-money",
        "Jinja2",
        "lxml",
    ],
    classifiers=(
	"Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
)
