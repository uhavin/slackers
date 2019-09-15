from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Niels van Huijstee",
    author_email="niels@huijs.net",
    classifier=["Intended Audience :: Developers"],
    descripion="Slack interactions web server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="slacken",
    packages=["slacken"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov", "pytest-mock"],
    url="https://github.com/uhavin/slacken",
    version="0.0.0",
)
