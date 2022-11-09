import iox_dbapi;
import os

connection = iox_dbapi.connect(
    host = os.environ["HOST"],
    org = os.environ["ORG"],
    bucket = os.environ["BUCKET"],
    token = os.environ["TOKEN"]
)

cursor = connection.cursor()
sql = "SELECT x, time FROM vibrations WHERE time > (NOW() - interval'10 seconds')::timestamp LIMIT 10"
cursor.execute(sql)


print(cursor.fetchone())