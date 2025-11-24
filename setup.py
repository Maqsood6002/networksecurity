from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """Reads the requirements from a file and returns them as a list."""
    requirements_lst:List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            requirements = file.readlines()
            for req in requirements:
                requirement=req.strip()
                if requirement!="-e .":
                    requirements_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    return requirements_lst

setup(
    name='NetworkSecurityProject',
    version='0.1.0',
    author='Maqsood',
    author_email='maqsood6002@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)