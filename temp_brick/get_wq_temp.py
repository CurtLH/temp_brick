import psycopg2

conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="apassword",
                        host="192.168.0.104") 

conn.autocommit = True
cur = conn.cursor()

cur.execute("""SELECT condition -> 'current_observation' -> 'temp_f' FROM arlington_weather_condition
               WHERE id = (SELECT MAX(id) FROM arlington_weather_condition)""")

print([i[0] for i in cur][0])
