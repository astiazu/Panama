# Diseñe un código que calcule el porcentaje de transacciones de la base conciliable de CLAP cruzó contra 
# la liquidación de BANSUR.

import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('datos.db')
c = conn.cursor()

# Obtener el número total de transacciones conciliables en CLAP
c.execute("SELECT COUNT(*) FROM CLAP WHERE TIPO_TRX IN ('PAGADA', 'CANCELADA')")
total_clap = c.fetchone()[0]

# Obtener el número de transacciones conciliables que cruzaron con BANSUR
c.execute("SELECT COUNT(*) FROM NuevaTabla WHERE Cruce = 'Cruzó'")
cruzadas = c.fetchone()[0]

# Calcular el porcentaje de transacciones cruzadas
porcentaje = (cruzadas / total_clap) * 100

# Imprimir el resultado
print("Porcentaje de transacciones cruzadas: {:.2f}%".format(porcentaje))

# Cerrar la conexión a la base de datos
conn.close()
