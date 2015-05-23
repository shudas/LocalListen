import mysql.connector as connector

cnx = connector.connect(user='root', password='mysqlpass',
                        host='localhost',
                        database='locallisten')



cnx.close()