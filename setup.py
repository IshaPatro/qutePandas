from setuptools import setup, find_packages

setup(
    name="qutePandas",
    version="1.1.0",
    packages=find_packages(),
    package_data={
        'qutePandas': ['*.q'],
    },
    install_requires=[
        'pykx>=2.0.0',
        'pandas>=1.3.0',
        'numpy>=1.20.0',
        'pyarrow>=10.0.0',
    ],
    author="Isha Patro",
    author_email="ishapatro21@gmail.com",
    description="A pandas-like library for kdb+/q using pykx",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://ishapatro.github.io/qutePandas/",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Database",
    ],
    python_requires='>=3.7',
    license_files=[],
)