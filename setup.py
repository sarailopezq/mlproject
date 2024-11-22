from setuptools import find_packages, setup #will look for all packages we used in our directory
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path: str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open('requirements.txt') as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements] #dealing with backslashes between the elements of the list
        #-e . will automatically trigger setup.py
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
name = 'mlproject',
version = '0.0.1',
author = 'Sarailq',
author_email = 's.lopezq12@gmail.com',
packages = find_packages(),
#install_requires = ['pandas', 'numpy', 'seaborn'] #usual method
install_requires = get_requirements('requirements.txt')
)