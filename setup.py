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
        'paste',
        'pastedeploy',
        'repoze.who<1.1',
        'repoze.who-friendlyform',
        'webtest',
        'sqlalchemy'
    ],
    setup_requires=[
    ],
    entry_points = {
        'paste.app_factory': [
            'main=helloworld.app:make_app',
        ],
        'paste.server_factory': [
            'native=helloworld.server:make_server',
        ],
    },
    zip_safe=False)

