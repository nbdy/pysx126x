from setuptools import setup, find_packages


setup(
    long_description=open("README.md", "r").read(),
    name="sx126x",
    version="1.0",
    description="lora sx126x rx/tx library",
    author="Pascal Eberlein",
    author_email="pascal@eberlein.io",
    url="https://github.com/nbdy/pysx126x",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'sx126xtool = sx126x.__main__:main'
        ]
    },
    install_requires=["pyserial"],
    keywords="sx126x",
    packages=find_packages(),
    long_description_content_type="text/markdown"
)
