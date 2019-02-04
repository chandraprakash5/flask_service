import sqlalchemy
from sqlalchemy.orm import sessionmaker


class PostgresDBHandler(object):
    """Configuration for Postgres database connections using sqlalchemy."""
    HOST = 'host'
    USER = 'user'
    PASSWORD = 'password'
    DATABASE = 'database'
    POOL_SIZE = 'pool_size'
    PORT = 'port'
    INIT_OPTS = 'init_opts'
    STATEMENT_TIMEOUT = 'statement_timeout'
    CONNECT_TIMEOUT = 'connect_timeout'

    def __init__(self, config):
        """Create a PostgresDB handler object. It can take ConfigObj or dictionary as
        constructor parameter.
        :param dict of (str, str) config: Settings for connecting to the database.
        :rtype: PostgresDBHandler
        """
        metadata = sqlalchemy.schema.MetaData()

        pool_size = int(config.get(PostgresDBHandler.POOL_SIZE, 5))
        connect_timeout = int(config.get(PostgresDBHandler.CONNECT_TIMEOUT, 10)) # seconds
        statement_timeout = int(config.get(PostgresDBHandler.STATEMENT_TIMEOUT, 20000)) # milliseconds
        port = int(config.get(PostgresDBHandler.PORT, 5432))
        host = config[PostgresDBHandler.HOST]
        password = config[PostgresDBHandler.PASSWORD]
        username = config[PostgresDBHandler.USER]
        database = config[PostgresDBHandler.DATABASE]

        db_url = sqlalchemy.engine.url.URL("postgresql", username=username, password=password,
                                           host=host, port=port, database=database)
        self.engine = engine = sqlalchemy.create_engine(
            db_url, pool_size=pool_size,
            connect_args={'connect_timeout': connect_timeout,
                          'options': '-c statement_timeout=%s' % statement_timeout})
        # this increases memory footprint by a couple of MBs.
        # also doubles the init time to ~ 2s, but provides
        # huge simplicity in creating the sqlalchemy Table objects
        # down the line, so embracing this with all smiles !
        if PostgresDBHandler.INIT_OPTS in config and \
                        'reflect_metadata' in config[PostgresDBHandler.INIT_OPTS]:
            metadata.reflect(bind=engine, views=True)

    def getEngine(self):
        """Get database engine.
        :rtype: sqlalchemy.engine.Engine
        """
        return self.engine

    def getSession(self, expire_on_commit=True, auto_flush=True):
        """Starts a new session with the current engine and returns it  to the caller.
        It is responsibility of the callee to appropriately close the session.
        :param boolean expire_on_commit:
        :param boolean auto_flush:
        :rtype: sqlalchemy.orm.session.Session
        """
        session = sessionmaker(bind=self.getEngine(), autoflush=auto_flush,
                               expire_on_commit=expire_on_commit)
        return session()

