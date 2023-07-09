import sqlite3
import csv

def crear_base_datos():
    # Crear una conexión a la base de datos
    conn = sqlite3.connect('datos.db')
    c = conn.cursor()

    # Crear tabla para los datos de clap.csv
    c.execute('''CREATE TABLE IF NOT EXISTS clap (
                    INICIO6_TARJETA INTEGER,
                    FINAL4_TARJETA INTEGER,
                    campo TEXT,
                    TARJETA INTEGER,
                    TIPO_TRX TEXT,
                    MONTO REAL,
                    FECHA_TRANSACCION DATE,
                    HORA_TRANSACCION DATETIME,
                    CODIGO_AUTORIZACION TEXT,
                    ID_BANCO INTEGER,
                    FECHA_RECEPCION_BANCO DATE
                )''')

    # Crear tabla para los datos de bansur.csv
    c.execute('''CREATE TABLE IF NOT EXISTS bansur (
                    TARJETA INTEGER,
                    TIPO_TRX TEXT,
                    MONTO REAL,
                    FECHA_TRANSACCION DATE,
                    CODIGO_AUTORIZACION TEXT,
                    ID_ADQUIRIENTE INTEGER,
                    FECHA_RECEPCION DATE
                )''')

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

def cargar_datos_csv():
    # Conectar a la base de datos
    conn = sqlite3.connect('datos.db')
    c = conn.cursor()

    # Cargar datos de clap.csv
    with open('clap.csv', 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Saltar la primera fila si contiene encabezados
        c.executemany('INSERT INTO clap VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', csv_data)

    # Cargar datos de bansur.csv
    with open('bansur.csv', 'r') as file:
        csv_data = csv.reader(file)
        next(csv_data)  # Saltar la primera fila si contiene encabezados
        c.executemany('INSERT INTO bansur VALUES (?, ?, ?, ?, ?, ?, ?)', csv_data)

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

# Crear la base de datos
crear_base_datos()

# Cargar los datos de los archivos CSV en la base de datos
cargar_datos_csv()