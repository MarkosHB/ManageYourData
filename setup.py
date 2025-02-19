from setuptools import setup, find_packages

setup(
    name='manageyourdata',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
        'openpyxl',
        'fpdf'
    ],
    entry_points={
        'console_scripts': [
            'manageyourdata = manageyourdata.main:main',
        ],
    },
)