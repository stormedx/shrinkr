from setuptools import setup, find_packages

setup(
    name='ShrinkX',
    version='0.1',
    packages=find_packages(),
    description='A Python tool for effortlessly compressing media files for sharing online.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Joshua Foroughi',
    author_email='stormedxx@icloud.com',
    url='https://github.com/stormedx/shrinkx',
    install_requires=[
        'os',
        'sys',
        'subprocess',
        'argparse',
        'time',
        'itertools',
    ],
)

setup(
    # ...
    entry_points={
        'console_scripts': [
            'shrinkx=shrinkx:main',
        ],
    },
    # ...
)