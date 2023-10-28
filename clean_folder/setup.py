from setuptools import setup

setup(
    name='clean-folder',
    version='0.1',
    packages=['clean_folder'],
    install_requires=[],
    entry_points={
        'console_scripts': ['clean-folder=clean_folder.clean:main']
    },
)
