from distutils.core import setup
from setuptools import find_packages

setup(
    name='expremigen',
    version='0.0.1',
    packages=find_packages(exclude=['build', 'dist', 'tests']),
    install_requires=['vectortween', 'MIDIUtil', 'textX'],
    url='https://github.com/shimpe/expremigen',
    python_requires='>=3',
    license='GPLv3+',
    author='stefaan himpe',
    author_email='stefaan.himpe@gmail.com',
    description='Expressive Midi Generation',
    long_description='Expressive Midi Generation',
    classifiers=["Development Status :: 3 - Alpha",
                 "Intended Audience :: Other Audience",
                 "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 3 :: Only",
                 "Topic :: Artistic Software",
                 "Topic :: Multimedia :: Sound/Audio :: MIDI",
                 "Topic :: Software Development :: Libraries :: Python Modules"]
)
