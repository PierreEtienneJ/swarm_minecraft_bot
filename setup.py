from setuptools import setup, find_packages
  
setup(
    name='swarm_minecraft_bot',
    version='0.1',
    description='A Python package to make a swarm minecraft bots',
    author='Pierre-Etienne',
    install_requires=[
        'javascript',
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True
)