import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Remove Emojis
long_description = long_description.replace(":information_source: ", "")
long_description = long_description.replace(":warning: ", "")
long_description = long_description.replace(":exclamation: ", "")

setuptools.setup(
    name="mpu9250_jmdev",
    version="2.0.0",
    author="Jeferson Menegazzo",
    author_email="jef.menegazzo@outlook.com",
    description="MPU 9250, 9150, 6500, 6050 I2C Driver in Python for Raspbery PI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CC BY-NC-ND 4.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)