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
        'pastescript',
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
        'paste.filter_factory': [
            'session=helloworld.filters:make_session_filter',
            'who=helloworld.filters:make_who_filter',
            'static=helloworld.filters:make_static_filter',
        ],
        'paste.server_factory': [
            'native=helloworld.servers:make_server',
        ],
        'paste.paster_command': [
            'init-db=helloworld.commands:InitDatabase',
        ]
    },
    zip_safe=False)

