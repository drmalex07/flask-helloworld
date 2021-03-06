from setuptools import setup, find_packages

setup(
    name='helloworld',
    version=open('VERSION').read(),
    description='Hello World',
    url='http://github.com/drmalex07/helloworld',
    author='Michail Alexakis',
    author_email='malex@example.com',
    license='MIT',
    packages=find_packages(),
    package_data={
        'helloworld': [
            'templates/*.html'],
    },
    install_requires=[
        # Moved to requirements.txt
    ],
    setup_requires=[
    ],
    entry_points = {
        'paste.app_factory': [
            'main=helloworld.app:make_app',
        ],
        'paste.filter_factory': [
            'session=helloworld.filters:make_session_filter',
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

