import ioxdb;
import os

connection = ioxdb.connect(
    host = os.environ["HOST"],
    bucket = os.environ["BUCKET"],
    token = os.environ["TOKEN"]
)

cursor = connection.cursor()
sql = "SELECT x, time FROM ? WHERE time > (NOW() - interval'? seconds')::timestamp LIMIT ?"
cursor.execute(sql, ["vibrations",10, 10])

print(dir(ioxdb.DataTypes))
print(cursor.decscription)
print(cursor.fetchone())