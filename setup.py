from setuptools import setup, find_packages
import os

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="code-cleaner",
    version="0.1.0",
    description="A tool to remove comments and log statements from code files",
    author="Shreyash Singh",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=requirements,
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'code-cleaner=code_cleaner.cli:main',
            'code-cleaner-web=code_cleaner.web:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)