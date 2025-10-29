"""
Setup script for GenAnim
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="genanim",
    version="1.0.0",
    author="GenAnim Team",
    author_email="team@genanim.example.com",
    description="HooRii Agent Character Animation Generation System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/GenAnim",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies (minimal for base functionality)
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "video": [
            "opencv-python>=4.8.0",
            "pillow>=10.0.0",
            "numpy>=1.24.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "genanim=examples.basic_usage:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.txt"],
    },
)
