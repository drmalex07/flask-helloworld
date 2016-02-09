import os
import ConfigParser as configparser


def config_from_file(path):
    global config
    
    parser = configparser.ConfigParser(defaults={
        'here': os.path.dirname(path)
    })
    parser.read(path)

    config.update(dict(parser.items('DEFAULT')))
    
    app_name = config.get('app', 'main')
    config['app'] = dict(parser.items('app:%s' % (app_name)))
   
    server_name = config.get('server', 'main')
    config['server'] = dict(parser.items('server:%s' % (server_name)))


config = {}
