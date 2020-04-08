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
        'click',
        'celery',
        'fasttext',  
        'Flask',
        'flask_cors',
        'flask_limiter',
        'gunicorn',
        'mkdocs',
        'praw',
        'progress',
        'pyfiglet', 
        'redis',
        'seaborn',  
        'SQLAlchemy',
        'tenacity',
        'StringGenerator'
    ],
    entry_points={
        'console_scripts': [
            'crossmod = crossmod.__main__:main'
        ]
    },
)
