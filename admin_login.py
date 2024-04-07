# admin_login.py

import psycopg2

def admin_login(cursor, username, password):
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname='FinalProjectDBMS',
            user='postgres',
            password='salonraut',
            host='localhost',
            port=5432
        )

        # Execute query to check user credentials
        cursor.execute("SELECT * FROM admin_credentials WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            return True
        else:
            return False

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
        return False
    finally:
        # Close database connection
        if 'conn' in locals():
            cursor.close()
            conn.close()
