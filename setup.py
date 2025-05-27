from setuptools import setup, find_packages

setup(
    name="text-to-speech",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pyttsx3>=2.90',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'text-to-speech=src.text_to_speech:main',
        ],
    },
    python_requires='>=3.6',
)