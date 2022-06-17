from setuptools import setup, find_packages

setup(
    name='manimate',
    version='0.1.0',
    packages=find_packages(include=['src', 'src.fsm', 'src.file', 'src.controllers', 'src.intermediate','src.scene','src.view']),
    install_requires=[
        'bidict>=0.21.4',
        'manim==0.15.2',
        'moderngl==5.6.4',
        'moderngl_window==2.4.1',
        'numpy>=1.22.1',
        'PySide6==6.3.0',
        'PySide2==5.15.2.1',
        'ipython==8.0.1',
    ],
    entry_points={
        'console_scripts': ['manimate=src.main:main']
    },
    author='Kevin Cen',
    description='Interactive Animation Builder for Manim',
)