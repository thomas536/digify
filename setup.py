from distutils.core import setup

setup(
    name='Digify',
    version='0.1dev',
    packages=['digify',],
    package_dir={'': 'src'},
    license='BSD',
    description='Convert written out numbers to integers',
    long_description=open('README.txt').read(),
)
