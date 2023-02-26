import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mpu_i2c_drivers",
    version="2.0.0",
    author="Jeferson Menegazzo",
    author_email="jmdev@outlook.com.br",
    description="I2C Drivers for MPU-9250, MPU-9255, MPU-9150, MPU-6500, MPU-6555, and MPU-6050",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jefmenegazzo/mpu-i2c-drivers-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: CC BY-ND 4.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)