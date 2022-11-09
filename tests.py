import unittest
import iox_dbapi
import os

class TestGlobals(unittest.TestCase):
    def test_globals(self):
        self.assertEqual("2.0",iox_dbapi.apilevel)
        self.assertEqual(0,iox_dbapi.threadsafety)
        self.assertEqual("qmark",iox_dbapi.paramstyle)

class TestCursors(unittest.TestCase):
    def test_create_cursor(self):
        connection = iox_dbapi.connect(
            host = os.environ["HOST"],
            org = os.environ["ORG"],
            bucket = os.environ["BUCKET"],
            token = os.environ["TOKEN"]
        )
        cursor = connection.cursor()

class TestTransactions(unittest.TestCase):
    def setUp(self):
        self.connection = iox_dbapi.connect(
            host = os.environ["HOST"],
            org = os.environ["ORG"],
            bucket = os.environ["BUCKET"],
            token = os.environ["TOKEN"]
        )

    def test_connection_noops(self):
        self.connection.commit()
        self.connection.close()
        self.connection.rollback()

if __name__ == '__main__':
    unittest.main()