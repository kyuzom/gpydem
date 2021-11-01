import setuptools

setuptools.setup(
    name="gpydem",
    version="0.0.1",
    author="KyuzoM",
    author_email="99549950+kyuzom@users.noreply.github.com",
    description="GPy modem",
    long_description="GPy modem - 3G GSM USB modem handler.",
    url="https://github.com/kyuzom/gpydem",
    license="MIT",
    packages=[
        "gpydem",
    ],
    package_data={
        "gpydem": ["**/*"],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
)
