from setuptools import setup, find_packages

setup(
    name="nbcmdio",
    version="1.8.1",
    author="Cipen",
    author_email="faithyxp@foxmail.com",
    description="A powerful tool for terminal output and input.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YXPHOPE/NbCmdIO",
    packages=find_packages(),      # 自动发现包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)