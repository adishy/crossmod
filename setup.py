"""
Crossmod python package configuration.

"""

from setuptools import setup

setup(
    name='crossmod',
    version='0.0.2',
    packages=['crossmod'],
    include_package_data=True,
    install_requires=[
        'fasttext==0.9.1',  
        'Flask==1.1.1',
        'mkdocs==1.0.4',
        'praw==6.4.0',
        'seaborn==0.9.0',  
        'SQLAlchemy==1.3.12',
        'tenacity==6.0.0',
        'flask_cors',
        'flask_limiter',
        'click',
        'gunicorn',
        'progress',
        'pyfiglet'  
    ],
    entry_points={
        'console_scripts': [
            'crossmod = crossmod.ml.crossmod:main'
        ]
    },
)
