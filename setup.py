from 
setuptools import setup, find_packages

setup(
    name="ByteMe",
    version="0.1.0",
    description="Educational Ransomware Simulator",
    author="Neriya Jacobsen",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pycryptodome==3.17"
    ],
    entry_points={
        "console_scripts": [
            "byteme = byte_me.main:main"
        ]
    },
    python_requires=">=3.7",
)
