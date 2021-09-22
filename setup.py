import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname("__file__"))

version = {}
with open(os.path.join(here, "transposonmapper", "__version__.py")) as f:
    exec(f.read(), version)


with open("README.rst") as readme_file:
    readme = readme_file.read()

setup(
    name="transposonmapper",
    version=version["__version__"],
    description="A libray for processing sequencing data for SAturated Transposon Analysis in Yeast (SATAY)",
    long_description=readme,
    long_description_content_type='text/x-rst',
    url="https://github.com/SATAY-LL/Transposonmapper",
    author="Liedewij Laan Lab",
    author_email="L.M.InigoDeLaCruz@tudelft.nl",
    license="Apache Software License 2.0",
    packages=find_packages(exclude=["*tests*"]),
    package_data={"transposonmapper": ["data_files/*"]},
    key_words=["transposon-mapping", "Saccharomyces Cerevisiae",],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Unix Shell",
    ],
    test_suite="tests",
    install_requires=["numpy", "matplotlib", "scipy","pandas"],
    extras_require={
        "dev": [
            "bump2version",
            "pysam",
            "pytest",
            "pytest-cov",
            "jupyter-book>=0.7.0",
            "sphinx-click",
            "sphinx-tabs",
            "sphinxext-rediraffe",
            "sphinx_inline_tabs",
            "ghp-import"

        ],
        "linux":[
            "pysam"

        ]

    },
)
