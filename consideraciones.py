import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('datos.db')
c = conn.cursor()

# Obtener el número total de transacciones en CLAP
c.execute("SELECT COUNT(*) FROM CLAP")
total_clap = c.fetchone()[0]
print(total_clap)
# Obtener el número total de transacciones en BANSUR
c.execute("SELECT COUNT(*) FROM BANSUR")
total_bansur = c.fetchone()[0]
print (total_bansur)

# Obtener el número de transacciones conciliables en CLAP y BANSUR
c.execute('''SELECT COUNT(*)
             FROM CLAP
             INNER JOIN BANSUR ON CLAP.TARJETA = BANSUR.TARJETA
             WHERE CLAP.TIPO_TRX IN ('PAGADA', 'CANCELADA')
             AND BANSUR.TIPO_TRX = 'PAGO'
             AND (CLAP.MONTO = BANSUR.MONTO OR ABS(CLAP.MONTO - BANSUR.MONTO) <= 0.99)''')
total_conciliables = c.fetchone()[0]

# Calcular porcentaje de transacciones conciliables
porcentaje_conciliables = (total_conciliables / total_clap) * 100

# Obtener el número de transacciones no cruzadas en BANSUR
c.execute('''SELECT COUNT(*)
             FROM BANSUR
             LEFT JOIN CLAP ON CLAP.TARJETA = BANSUR.TARJETA
             WHERE CLAP.TARJETA IS NULL''')
total_no_cruzadas = c.fetchone()[0]

# Calcular porcentaje de transacciones no cruzadas
porcentaje_no_cruzadas = (total_no_cruzadas / total_bansur) * 100

# Calcular la variación de montos conciliables
c.execute('''SELECT COUNT(*)
             FROM CLAP
             INNER JOIN BANSUR ON CLAP.TARJETA = BANSUR.TARJETA
             WHERE CLAP.TIPO_TRX IN ('PAGADA', 'CANCELADA')
             AND BANSUR.TIPO_TRX = 'PAGO'
             AND ABS(CLAP.MONTO - BANSUR.MONTO) <= 0.99''')
total_variacion_montos = c.fetchone()[0]

# Calcular porcentaje de variación de montos conciliables
porcentaje_variacion_montos = (total_variacion_montos / total_conciliables) * 100

# Obtener el número de transacciones conciliables con estado "PAGADA"
c.execute('''SELECT COUNT(*)
             FROM (SELECT TARJETA, MAX(FECHA_TRANSACCION) AS MAX_FECHA_TRANSACCION
                   FROM CLAP
                   WHERE TIPO_TRX = 'PAGADA'
                   GROUP BY TARJETA) AS A
             INNER JOIN CLAP ON CLAP.TARJETA = A.TARJETA AND CLAP.FECHA_TRANSACCION = A.MAX_FECHA_TRANSACCION
             INNER JOIN BANSUR ON CLAP.TARJETA = BANSUR.TARJETA
             WHERE BANSUR.TIPO_TRX = 'PAGO' ''')
total_pagadas = c.fetchone()[0]

# Calcular porcentaje de transacciones conciliables pagadas
porcentaje_pagadas = (total_pagadas / total_conciliables) * 100

# Imprimir los resultados
print("Porcentaje de transacciones conciliables: {:.2f}%".format(porcentaje_conciliables))
print("Porcentaje de transacciones no cruzadas: {:.2f}%".format(porcentaje_no_cruzadas))
print("Porcentaje de variación de montos conciliables: {:.2f}%".format(porcentaje_variacion_montos))
print("Porcentaje de transacciones conciliables pagadas: {:.2f}%".format(porcentaje_pagadas))

# Cerrar la conexión a la base de datos
conn.close()