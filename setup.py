import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto-sub-gen-ckirby19", # Replace with your own username
    version="1.0.0",
    author="Conor Kirby",
    author_email="conorkirby1@gmail.com",
    description="Generates SRT subtitles for a video using Google Speech Recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ckirby19/auto-sub-gen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)