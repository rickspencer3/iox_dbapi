import unittest
import ioxdb
import os

class TestGlobals(unittest.TestCase):
    def test_globals(self):
        self.assertEqual("2.0",ioxdb.apilevel)
        self.assertEqual(0,ioxdb.threadsafety)
        self.assertEqual("qmark",ioxdb.paramstyle)

class TestCursors(unittest.TestCase):
    def test_create_cursor(self):
        connection = ioxdb.connect(
            host = os.environ["HOST"],
            bucket = os.environ["BUCKET"],
            token = os.environ["TOKEN"]
        )
        cursor = connection.cursor()

class TestTransactions(unittest.TestCase):
    def setUp(self):
        self.connection = ioxdb.connect(
            host = os.environ["HOST"],
            bucket = os.environ["BUCKET"],
            token = os.environ["TOKEN"]
        )

    def test_connection_noops(self):
        self.connection.commit()
        self.connection.close()
        self.connection.rollback()

if __name__ == '__main__':
    unittest.main()