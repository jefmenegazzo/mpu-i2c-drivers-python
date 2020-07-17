import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpu9250_jmdev",
    version="1.0.11",
    author="Jeferson Menegazzo",
    author_email="jef.menegazzo@outlook.com",
    description="MPU-9250 (MPU-6500 + AK8963) I2C Driver in Python for Raspbery PI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)