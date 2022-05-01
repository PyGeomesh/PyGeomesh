from setuptools import setup

setup(
    name="geomesh",
    version="0.1.0",
    author="PuQing",
    author_email="me@puqing.work",
    packages=["geomesh"],
    description="Generate meshes for geometries",
    url="https://github.com/AndPuQing/Geomesh",
    download_url="https://pypi.python.org/pypi/geomesh",
    license="MIT",
    platforms="any",
    requires=[
        "numpy",
        "scipy",
        "matplotlib",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
)
