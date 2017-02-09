import os.path
import setuptools

import sg

_APP_PATH = os.path.dirname(sg.__file__)

with open(os.path.join(_APP_PATH, 'resources', 'README.rst')) as f:
    long_description = f.read()

with open(os.path.join(_APP_PATH, 'resources', 'requirements.txt')) as f:
    install_requires = list(map(lambda s: s.strip(), f.readlines()))

setuptools.setup(
    name='synchronous_glacier',
    version=sg.__version__,
    description="Execute workflows against Glacier.",
    long_description=long_description,
    classifiers=[],
    keywords='aws glacier',
    author='Dustin Oprea',
    author_email='dustin@randomingenuity.com',
    url='https://github.com/dsoprea/PySynchronousGlacier',
    license='GPL 2',
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'sg': [
            'resources/README.rst',
            'resources/requirements.txt',
        ],
    },
    install_requires=install_requires,
    scripts=[
        'sg/resources/scripts/sg-vault-delete',
    ],
)
