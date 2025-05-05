"""
This module contains the ButtonActions class, which defines methods for
performing various actions related to button clicks in the DemonLab dashboard.
The class includes methods for deleting rows from the Federation resync table.
"""

import asyncpg
import psycopg2
from psycopg2 import extensions
from textual.app import ComposeResult, on
from textual.widgets import Button

import demonlab_dashboard.database as db


class ButtonActions:

    @on(Button.Pressed)
    def but01_action(self) -> None:
        """
        Delete rows stuck in Federation resync table in the Synapse database.i
        """
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM device_lists_remote_resync;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]

    def but02_action(self) -> None:
        """ """
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM device_lists_remote_resync;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]

    def but03_action(self) -> None:
        """ """
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM device_lists_remote_resync;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]

    def but04_action(self) -> None:
        """ """
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM device_lists_remote_resync;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]

    def but05_action(self) -> None:
        """ """
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM device_lists_remote_resync;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]

    def but06_action(self) -> None:
        """ """
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM device_lists_remote_resync;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]

    def but07_action(self) -> None:
        """ """
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute(";")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]

    def but08_action(self) -> None:
        """ """
        conn = psycopg2.connect(
            dbname="synapse",
            user="synapse_user",
            password="synapse",
            host="10.99.10.128",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute(";")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [row[0] for row in rows]
