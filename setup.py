from setuptools import setup, find_packages

setup(
    name='helloworld',
    version='0.1',
    description='Hello World',
    url='http://github.com/drmalex07/helloworld',
    author='Michail Alexakis',
    author_email='malex@example.com',
    license='MIT',
    packages=find_packages(),
    package_data={
        'helloworld': ['templates/*.html'],
    },
    install_requires=[
        'jinja2',
        'flask',
        'beaker',
        'webtest',
    ],
    setup_requires=[
    ],
    zip_safe=False)

