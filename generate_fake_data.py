from faker import Faker
import pymysql
import random

fake = Faker()

# Conexión a la base de datos MySQL
connection = pymysql.connect(
    host='localhost',  # O la IP de tu contenedor Docker
    user='myuser',
    password='mypassword',
    database='mydatabase'
)

cursor = connection.cursor()

# 1. Crear 20 sedes
sede_ids = []
for _ in range(20):
    name = fake.company()
    location = fake.city()
    cursor.execute("INSERT INTO sede (name, location) VALUES (%s, %s)", (name, location))
    sede_ids.append(cursor.lastrowid)  # Guardamos el ID de la sede insertada

# 2. Crear 200 empleados, asignando a una sede aleatoria
roles = ["Trainer", "Nutricionista", "Administrador"]
for _ in range(200):
    name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.phone_number()
    email = fake.email()
    salary = random.uniform(1500, 5000)
    type_role = random.choice(roles)
    sede_id = random.choice(sede_ids)  # Asigna una sede aleatoria

    cursor.execute("""
        INSERT INTO employee (name, last_name, phone, email, salary, type, sede_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, last_name, phone, email, salary, type_role, sede_id))

# Commit para guardar los cambios
connection.commit()

# Cerrar la conexión
cursor.close()
connection.close()