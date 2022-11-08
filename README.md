This is an implementation of Python's dbapi2. See:

https://peps.python.org/pep-0249/

It provides a standard interface for IOx-backed InfluxDB organizations.

Use just like any dbapi v2 - 
```Python
import iox_dbapi;

connection = iox_dbapi.connect(
    host = "",
    org = "",
    bucket = "",
    token = ""
)

cursor = connection.cursor()
sql = "SELECT * FROM TABLE WHERE time > (NOW() - interval'10 seconds')::timestamp LIMIT 10"
cursor.execute(sql)


print(cursor.fetchone())
```

This code is raw and incomplete. You will need an IOx organization in InfluxDB Cloud to use it.