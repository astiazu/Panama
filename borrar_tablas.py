import sqlite3

# Conectar 
conn = sqlite3.connect('datos.db')
c = conn.cursor()

# Eliminar la tabla
c.execute("DROP TABLE IF EXISTS Tabla_Resultados")
c.execute("DROP TABLE IF EXISTS Resultados_Clap")
c.execute("DROP TABLE IF EXISTS Resultados_Bsur")
c.execute("DROP TABLE IF EXISTS Resultados")