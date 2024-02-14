from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation."""
    def run(self):
        install.run(self)
        print("\nTo make 'shrinkx' available as a command, add the following line to your .bashrc or .zshrc file:")
        print('export PATH="$(python -m site --user-base)/bin:$PATH"\n')

setup(
    name='shrinkx',
    version='1.1',
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
