from flask_mysqldb import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="#aTestTest1", db="autoqa")
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    results = cursor.fetchone()
    print("Database version : %s " % results)

except MySQLdb.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))