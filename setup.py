from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mkdocs_bootprint_schema",
    version="0.0.1",
    description="A MkDocs plugin to ocnvert json schema files into html page using bootprint (out is MD page in order to permit mkdocs integration)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="mkdocs, schema, json, plugin",
    url="https://github.com/mysiki/mkdocs_bootprint_schema",
    author="mysiki",
    author_email="hoaxboy@wanadoo.fr",
    license="MIT",
    python_requires=">=3.6",
    install_requires=["mkdocs>=1.0.4"],
    packages=find_packages(),
    entry_points={
        "mkdocs.plugins": [
            "bootprint_schema = mkdocs_bootprint_schema.bootprint_schema:BootprintSchema"
        ]
    },
)
