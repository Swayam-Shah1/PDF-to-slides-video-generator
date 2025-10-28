"""
Setup script for Visual Explanation Prototype
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="visual-explanation-prototype",
    version="1.0.0",
    author="Swayam Shah",
    description="Convert PDF to PowerPoint slides and animated videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/infoware/visual-explanation-prototype",
    packages=find_packages(where="."),
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pdfplumber>=0.7.0",
        "PyPDF2>=3.0.0",
        "nltk>=3.8.0",
        "python-pptx>=0.6.21",
        "pillow>=10.0.0",
        "moviepy>=1.0.0",
        "imageio-ffmpeg>=0.4.0",
        "pyttsx3>=2.90",
        "pyyaml>=6.0.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.4",
            "pytest-cov==4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pdf-to-slides=src.cli.run_pipeline:main",
        ],
    },
)

