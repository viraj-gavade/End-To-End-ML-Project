from setuptools import setup , find_packages
from typing import List

def get_requirements(file_Path : str )->List[str]:
    "This function is responsible for getting all the necessary packages"
    requirements = []

    with open(file_Path) as file : 
        requirements = file.readlines()
        requirements = [req.replace("/n" , " ")for req in requirements]

        if "-e." in requirements :
            requirements.remove("-e.")
    return requirements


setup(
    name='machine-learning-project',
    version='0.0.1',
    author='Viraj Gavade',
    author_email='vrajgavade17@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
