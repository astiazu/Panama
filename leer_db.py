import sqlite3

def leer_registros(tabla):
    # Conectar 
    conn = sqlite3.connect('datos.db')
    c = conn.cursor()

    # Obtener los primeros diez registros de la tabla
    c.execute(f"SELECT * FROM {tabla} LIMIT 10")
    registros = c.fetchall()

    # Imprimir los registros
    print(f"Registros de la tabla {tabla}:")
    for registro in registros:
        print(registro)

    # Cerrar la conexión
    conn.close()

# Leer los primeros diez registros de la tabla "clap"
leer_registros("clap")

# Leer los primeros diez registros de la tabla "bansur"
leer_registros("bansur")