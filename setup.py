from setuptools import setup, find_packages

setup(
    name='manimate',
    version='1.0.0',
    packages=find_packages(include=['src', 'src.fsm', 'src.file', 'src.controllers', 'src.intermediate','src.scene','src.view']),
    entry_points={
        'console_scripts': ['manimate=src.main:main']
    },
    author='Kevin Cen',
    description='Interactive Animation Builder for Manim',
)