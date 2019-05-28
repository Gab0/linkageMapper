#!/bin/python

from setuptools import setup, find_packages
#from distutils.core import setup


entry_points = {
    'console_scripts': [
        "lmpline=linkageMapper.Pipeline:main",
        "lmview=linkageMapper.walkChromosomeResult:main",
        "lmdownload=linkageMapper.fetchDataNCBI:main",
        "lmprimer=linkageMapper.initializePrimerFile:main"
        ]
}

requirements = list(open("requirements.txt").readlines())
setup(
    name='linkageMapper',
    version='0.8',
    description='Genomic similarities per region',
    author='Gabriel Araujo',
    author_email='gabriel_scf@hotmail.com',
    url='https://www.github.com/Gab0/linkageMapper',
    #packages=find_packages(),
    setup_requires=["numpy"],
    install_requires=requirements,
    packages=[
        'linkageMapper',
        'linkageMapper.walkChromosome',
        'linkageMapper.PrimerEngine',
        'linkageMapper.DrawGraphics',
        'linkageMapper.Database'
    ],
    platforms='any',
    entry_points=entry_points
)
