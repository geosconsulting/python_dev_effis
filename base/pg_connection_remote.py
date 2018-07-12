import psycopg2
from sshtunnel import SSHTunnelForwarder

try:

    with SSHTunnelForwarder(
        ("127.0.0.1", 22),
        #ssh_private_key="</path/to/private/ssh/key>",
        ### in my case, I used a password instead of a private key
        ssh_username="jrc",
        ssh_password="Only4jrc",
        remote_bind_address=('localhost', 5432)) as server:

        server.start()
        print "Server connected"

        params = {
            'database': 'pagila',
            'user': 'postgres',
            'password': 'antarone',
            'host': 'localhost',
            'port': 5432
            }

        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print "Database connected"

        cur.execute("SELECT * FROM actor ORDER BY last_update LIMIT 10;")
        rows = cur.fetchall()

        for row in rows:
            print "First Name = ", row[1],"Last Name = ", row[2]

        print "Operation done successfully"
        conn.close()

except:
    print "Connection Failed"