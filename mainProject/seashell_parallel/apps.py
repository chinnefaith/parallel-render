from django.apps import AppConfig
from django.db.backends.signals import connection_created


def configure_sqlite_connection(sender, connection, **kwargs):
    if connection.vendor != 'sqlite':
        return
    with connection.cursor() as cursor:
        cursor.execute('PRAGMA journal_mode=WAL;')
        cursor.execute('PRAGMA synchronous=NORMAL;')
        cursor.execute('PRAGMA busy_timeout=30000;')


class SeashellParallelConfig(AppConfig):
    name = 'seashell_parallel'

    def ready(self):
        connection_created.connect(
            configure_sqlite_connection,
            dispatch_uid='seashell_parallel.sqlite_config',
        )
