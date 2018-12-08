import psycopg2
import json

print('Connecting to database...')

connection = psycopg2.connect(dbname='car-search',
                              user='root',
                              password='Ek9z32CDUg5xXOmoLYdo',
                              host='db',
                              port='5432')

cursor = connection.cursor()

print('Created database structure...')

cursor.execute("""
    CREATE TABLE IF NOT EXISTS public.cars
    (
    "brand" varchar(255),
    "year" int,
    "color" varchar(255),
    "plate-number" varchar(255) PRIMARY KEY,
    "bookmarked" boolean
    );
    """)

connection.commit()


print('Checking if data has been already imported...')

cursor.execute("""SELECT COUNT(*) FROM public.cars;""")

result = cursor.fetchone()
if result[0] > 0:
    print('Database has been already initialized, skipping import...')
    cursor.close()
    connection.close()
    quit(0)


print('Reading data...')

file = open('data.json', 'r')
cont = file.read()
data = json.loads(cont)

print('Importing data...')
for car in data:
    plateNumber = car['n']
    year = car['y']
    brand = car['br']
    color = car['col']

    print(f'inserting car {plateNumber}...')

    cursor.execute("""
        INSERT INTO public.cars ("plate-number", "brand", "year", "color") VALUES (%s, %s, %s, %s);    
    """, (plateNumber, brand, year, color))

    connection.commit()


cursor.close()
connection.close()

print('Database initialized...')
