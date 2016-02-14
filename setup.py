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
        'pastedeploy',
        'pastescript',
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
        'paste.paster_command': [
            'init-db=helloworld.commands:InitDatabase',
        ]
    },
    zip_safe=False)

