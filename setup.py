from setuptools import setup

__author__ = 'Giuseppe De Marco'

setup(
    name="abstorage",
    version='v0.4.0',
    description="Abstract Storage System",
    author=__author__,
    author_email="giuseppe.demarco@unical.it",
    license="Apache 2.0",
    packages=["abstorage", "abstorage/storages"],
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    install_requires=["sqlalchemy"],
    #tests_require=['pytest'],
    #zip_safe=False,
    #extras_require={
        #'testing': tests_requires,
        #'docs': ['Sphinx', 'sphinx-autobuild', 'alabaster'],
        #'quality': ['isort'],
    #},
)
