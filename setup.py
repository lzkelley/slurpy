from setuptools import setup
import version

readme = open('README.md').read()
version = open('VERSION').read().strip()
requirements = ['numpy', 'scipy', 'astropy', 'matplotlib']

requirements = []

setup(
    name="slurpy",
    version=version,
    author="Luke Zoltan Kelley",
    author_email="lkelley@cfa.harvard.edu",
    description=("Python wrapper for SLURM."),
    license="MIT",
    keywords="",
    url="https://github.com/lzkelley/slurpy",
    packages=['slurpy'],
    include_package_data=True,
    install_requires=requirements,
    long_description=readme,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
)
