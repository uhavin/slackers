from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Niels van Huijstee",
    author_email="niels@huijs.net",
    classifiers=["Intended Audience :: Developers"],
    description="Slack interactions web server.",
    install_requires=[
        "environs>=5.2.1,<6",
        "fastapi",
        "pyee>=6,<7",
        "python-multipart>=0.0.5",
        "requests",
        "uvicorn",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="slackers",
    packages=["slackers"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov", "pytest-mock"],
    url="https://github.com/uhavin/slackers",
    version="0.0.0",
)
