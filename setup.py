from setuptools import setup, find_packages

setup(
    name="cpp2xml",
    version="0.1.0",
    description="Parse C++ header files and generate XML documentation",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "libclang>=16.0",
        "tomli-w>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cpp2xml=cpp2xml.cli:main",
        ],
    },
    python_requires=">=3.10",
)
