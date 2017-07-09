from distutils.core import setup

setup(
    name='expremigen',
    version='0.0.1',
    packages=['tests', 'expremigen', 'expremigen.io', 'expremigen.patterns', 'expremigen.musicalmappings'],
    install_requires=['vectortween', 'MIDIUtil'],
    url='https://github.com/shimpe/expremigen',
    license='GPL v3',
    author='stefaan himpe',
    author_email='stefaan.himpe@gmail.com',
    description='Expressive Midi Generation'
)
