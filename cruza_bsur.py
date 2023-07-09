# 6. Diseñe un código que calcule el porcentaje de transacciones de la base conciliable de BANSUR no cruzó 
# contra la liquidación de CLAP.

import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('datos.db')
c = conn.cursor()

# Obtener el número total de transacciones conciliables en BANSUR
c.execute("SELECT COUNT(*) FROM BANSUR WHERE TIPO_TRX IN ('PAGO', 'CANCELACION')")
total_bansur = c.fetchone()[0]

# Obtener el número de transacciones conciliables que no cruzaron con CLAP
c.execute("SELECT COUNT(*) FROM NuevaTabla WHERE Cruce = 'No cruzó'")
no_cruzadas = c.fetchone()[0]

# Calcular el porcentaje de transacciones no cruzadas
porcentaje = (no_cruzadas / total_bansur) * 100

# Imprimir el resultado
print("Porcentaje de transacciones no cruzadas: {:.2f}%".format(porcentaje))

# Cerrar la conexión a la base de datos
conn.close()