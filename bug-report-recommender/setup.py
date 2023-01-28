from setuptools import find_packages, setup

setup(
    name='bugreportrecommender',
    packages=find_packages(),
    version='1.0.0',
    description='Similar Bug Reports Recommender',
    author='Guilherme de Melo Carneiro',
    license='MIT',
    install_requires=['pymongo']
)