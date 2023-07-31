import setuptools

VERSION = "0.1.0"

NAME = "st_owm_connection"

INSTALL_REQUIRES = [
    "streamlit>=1.22",
    "requests"
]


setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Streamlit Connection for OpenWeatherMap API.",
    url="https://github.com/1407arjun/streamlit-owm-connection",
    project_urls={
        "Source Code": "https://github.com/1407arjun/streamlit-owm-connection",
    },
    author="Arjun Sivaraman",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
    packages=["st_owm_connection"]
)
