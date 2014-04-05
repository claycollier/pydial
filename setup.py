from setuptools import setup


setup(
    name='PyDial',
    version='0.0.1',
    license='MIT',
    url='https://github.com/claycollier/pydial',
    author='Clay Collier',
    author_email='clay.collier@gmail.com',
    description='Simple DIAL protocol client and server for Python.',
    packages=['pydial'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=['requests'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
