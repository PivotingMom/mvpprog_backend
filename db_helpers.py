from db_creds import *
import mariadb


def connect_db():
    conn = None
    cursor = None

    try:
        conn = mariadb.connect(host=host, port=port,database=database, user=user, password=password)
        cursor = conn.cursor()
        return (conn, cursor)
    except mariadb.OperationalError as e:
        print("got an operational error")
    if ("Access denied" in e.msg):
        print("failed to log in")
    disconnect_db()


def disconnect_db(conn, cursor):
    if (cursor != None):
        cursor.close()
    if (conn != None):
        conn.rollback()
        conn.close()


def run_query(statement, args=None):
    try:
        (conn, cursor) = connect_db()
        if statement.startswith("SELECT"):
            cursor.execute(statement, args)
            result = cursor.fetchall()
            print("Total of {} users".format(cursor.rowcount))
            return result
        else:
            cursor.execute(statement, args)
            if cursor.rowcount == 1:
                conn.commit()
                print("Query successful")
            else:
                print("Query Failed")
            if statement.startswith("INSERT"):
                return cursor.lastrowid
            #helps to return the id of what i inserted into my DB

    except mariadb.OperationalError as e:
        print("got an operational error")
        if ("Access denied" in e.msg):
            print("failed to log in")

    except mariadb.IntegrityError as e:
        print("Intergrity error")
        if ("CONSTRAINT `user_CHECK_username" in e.msg):
            print("Error, all usernames must start with the letter J")
        elif ("CONSTRAINT `user_CHECK_title" in e.msg):
            print("Error, text outside of the acceptable types")
        elif ("Duplicate entry" in e.msg):
            print("user already exist")
        else:
            print(e.msg)
    
    except RuntimeError as e:
        print("caught a runtime error")
        e.with_traceback

    except Exception as e:
        print(e)
            
    finally:
        disconnect_db(conn, cursor)