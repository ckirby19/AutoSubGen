import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autosubgen", # Replace with your own username
    version="1.0.0",
    author="Conor Kirby",
    author_email="conorkirby1@gmail.com",
    description="Generates SRT subtitles for a video using Google Speech Recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ckirby19/auto-sub-gen",
    packages=setuptools.find_packages(),
    install_requires=[
        "certifi>=2020.6.20",
        "DateTime>=4.3",
        "ffmpeg-python>=0.2.0",
        "future>=0.18.2",
        "PyAudio>=0.2.11",
        "pydub>=0.24.1",
        "pytz>=2020.1",
        "SpeechRecognition>=3.8.1",
        "wincertstore>=0.2",
        "zope.interface>=5.1.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)