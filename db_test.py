import mysql.connector as connector
import config_parser
from config_parser import config as conf
from mysql.connector import errorcode

TABLES = {}
TABLES['genres'] = "CREATE TABLE IF NOT EXISTS Genres (genre VARCHAR(50) PRIMARY KEY);"

def run_db():
    cnx = connector.connect(**conf['DB'])
    cursor = cnx.cursor()

    print TABLES

    for name, ddl in TABLES.iteritems():
        try:
            print("Creating table {}: ".format(name))
            cursor.execute(ddl)
        except connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()

if __name__ == '__main__':
    config_parser.read_config()
    run_db()