import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="async_event_bus",
    version="0.0.1",
    author="Linus Basig",
    author_email="linus@basig.me",
    description="A simple event in process event bus based on asyncio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linuxbasic/async_event_bus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)