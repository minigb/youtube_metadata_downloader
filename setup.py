from setuptools import setup, find_packages

def load_requirements(filename = 'requirements.txt'):
    with open(filename, 'r') as file:
        return file.read().splitlines()

setup(
    name='yt_search_topk',
    version='0.1',
    packages=find_packages(),
    install_requires=load_requirements(),
)