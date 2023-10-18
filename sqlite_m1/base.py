from django.db.backends.sqlite3 import base
from django.utils.asyncio import async_unsafe


class DatabaseWrapper(base.DatabaseWrapper):
    @async_unsafe
    def get_new_connection(self, conn_params):
        con = super().get_new_connection(conn_params)
        con.execute("PRAGMA legacy_alter_table = OFF")
        return con
