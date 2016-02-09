from setuptools import setup

setup(
    name='helloworld',
    version='0.1',
    description='Hello World',
    url='http://github.com/drmalex07/helloworld',
    author='Michail Alexakis',
    author_email='malex@example.com',
    license='MIT',
    packages=['helloworld'],
    install_requires=[
        'jinja2',
        'flask',
        'beaker',
        'repoze.who<1.1',
        'repoze.who-friendlyform',
        'webtest',
    ],
    setup_requires=[
    ],
    zip_safe=False)

