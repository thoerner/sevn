"""
Setup configuration for the environment variable manager.
"""

from setuptools import setup, find_packages

setup(
    name="envault",
    version="1.0.0",
    description="Secure environment variable manager",
    author="Tim",
    author_email="tim@example.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "envault=cli.main:main",
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies required
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    package_data={
        "": ["py.typed"],
    },
) 