from setuptools import setup, find_packages

setup(
    name="resumesniper",
    version="1.0.0",
    author="Rishabh Raj",
    author_email="rishabhraj74918@gmail.com",
    description="Autonomous ATS Gap Analyzer, Resume Tailorer & Cold Reachout Copilot",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Rishabhraj06/ResumeSniper",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pypdf>=4.0.0",
        "streamlit>=1.35.0",
    ],
    extras_require={
        "dev": ["pytest>=8.0.0"],
    },
    entry_points={
        "console_scripts": [
            "resumesniper=resumesniper.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
)
