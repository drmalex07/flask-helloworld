import os
import logging
import paste.deploy
from paste.script import command

class InitDatabase(command.Command):

    # Describe positional arguments    
    max_args = 1
    min_args = 0

    usage = "CONFIG-FILE" # positional argumants
    summary = "Initialize database"
    group_name = 'helloworld'

    # Describe optional (getopt-style) arguments
    parser = command.Command.standard_parser(verbose=True)
    parser.add_option('--recreate', '-r', action='store_true', dest='recreate',
        help="Create database from scratch")
    parser.add_option("--name", "-n", dest='app_name', default='main')
    
    def command(self):

        # Read configuration 

        config_file = self.args[0] if len(self.args) else os.environ['CONFIG_FILE']
        config_file = os.path.realpath(config_file)
        if not os.path.exists(config_file):
            logging.error('Expected configuration at %s', config_file)
            self.parser.print_help()
            return
        
        logging.info('Using configuration from %s', config_file)
        config_uri = 'config:%s#%s' % (config_file, self.options.app_name)

        if self.verbose:
            logging.basicConfig(level=logging.INFO)

        # Import command-specific modules

        import sqlalchemy

        import helloworld.model as model

        # Load app configuration

        config = paste.deploy.appconfig(config_uri)
        database_url = config['database.url']

        # Create database schema

        engine = sqlalchemy.create_engine(database_url, echo=self.verbose)
        logging.info('Connecting to %s', database_url)

        if self.options.recreate:
            model.Base.metadata.drop_all(bind=engine)

        model.Base.metadata.create_all(bind=engine)
        
        logging.info('Tables were created successfully')
        return
       
