from setuptools import find_packages, setup

setup(
    name='bugreportrecommender',
    packages=find_packages(),
    version='0.0.1',
    description='Similar Bug Reports Recommender',
    author='Guilherme de Melo Carneiro',
    license='MIT',
    install_requires=['pandas', 'nltk', 'scikit-learn', 'sentence-transformers']
)