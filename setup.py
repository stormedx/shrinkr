from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        print("\nIf the 'shrinkx' command is not available, add the following line to your shell's configuration file:")
        print('export PATH="$(python -m site --user-base)/bin:$PATH"\n')

setup(
    name='ShrinkX',
    version='1.5',
    py_modules=['shrinkx'],
    description='A Python tool for effortlessly compressing media files for sharing online.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Joshua Foroughi',
    author_email='stormedxx@icloud.com',
    url='https://github.com/stormedx/shrinkx',
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'shrinkx=shrinkx:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
)