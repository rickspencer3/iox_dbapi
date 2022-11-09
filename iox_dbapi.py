from influxdb_client import InfluxDBClient

apilevel = "2.0"
threadsafety = 0
paramstyle = "qmark"

def connect(host=None, token=None, org=None, bucket=None):
    return IOxConnection(host=host, token=token, bucket=bucket)

class IOxConnection:
    def __init__(self, host=None, token=None, org=None, bucket=None):
        self.host = host
        self.token = token
        self.org = org
        self.bucket = bucket

    def cursor(self):
        self.name = "iox"
        return IOxCursor(connection = self)
        
    #IOx is not a transactional database and does not hold a connection open.
    #Therefor the following interface functions are noops
    def close(self):
        pass
    def commit(self):
        pass
    def rollback(self):
        pass

class IOxCursor:
    def __init__(self, connection):
        self._closed = False
        self._connection = connection
        self._query_api = InfluxDBClient(url=self._connection.host, 
                                                token=self._connection.token, 
                                                org=self._connection.org).query_api()
        self._reset_results()
        self._arraysize = 1
        self._result = None

    def _reset_results(self):
        self._record_index = 0
        self._table_index = 0

    @property
    def arraysize(self):
        return self._arraysize

    @arraysize.setter
    def arraysize(self, value):
        self._arraysize = value

    @property
    def decscription(self):
        desc = []
        if self._result is None:
            return None
        else:
            for column in self._result[self._table_index].columns:
                desc.append((column.label,column.data_type,None,None,None,None,None))
        return desc
        
    @property
    def rowcount(self):
        if self._result is None:
            return -1
        else:
            return len(self._result[self._table_index].records)

    def close(self):
        self._closed = True

    def nextset(self):
        self._table_index += 1
        self._record_index = 0

        if self._table_index >= len(self._result):
            return None
        return True

    def fetchone(self):
        if self._result is None:
            return None

        if len(self._result) == 0:
            return None

        if self.rowcount == self._record_index:
            return None

        record = self._result[self._table_index].records[self._record_index]
        self._record_index += 1
        return tuple(record.values.values())

    def fetchall(self):
        results = []
        while self._record_index < self.rowcount:
            record = self._result[self._table_index].records[self._record_index]
            self._record_index += 1
            results.append(tuple(record.values.values()))
        return results         

    def fetchmany(self, size=None):
        results = []
        if size is None:
            size = self.arraysize
        for i in range(size):
            if self.rowcount == self._record_index:
                break
            record = self._result[self._table_index].records[self._record_index]
            self._record_index += 1
            results.append(tuple(record.values.values()))
        return results
            
    def execute(self, statement):
        flux = f"""import "experimental/iox"
iox.sql(bucket: "{self._connection.bucket}", query: "{statement}") """
        self._result = self._query_api.query(flux, org=self._connection.org)
        self._reset_results()