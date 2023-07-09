# 2. Escriba el código de SQL que le permite conocer el monto y la cantidad de las transacciones que SIMETRIK 
# considera como conciliables para la base de BANSUR

import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('datos.db')
c = conn.cursor()

# Eliminar la tabla
c.execute("DROP TABLE IF EXISTS conciliables")

# Crear la tabla conciliables
c.execute('''CREATE TABLE IF NOT EXISTS conciliables (
                TARJETA INTEGER,
                FECHA_TRANSACCION TEXT,
                MONTO REAL,
                TIPO_TRX TEXT
            )''')

# Obtener los registros conciliables
c.execute('''SELECT clap.TARJETA, clap.FECHA_TRANSACCION, clap.MONTO, clap.TIPO_TRX
             FROM clap
             JOIN bansur ON clap.TARJETA = bansur.TARJETA
             WHERE clap.FECHA_TRANSACCION = bansur.FECHA_TRANSACCION
             AND (clap.MONTO = bansur.MONTO OR abs(clap.MONTO - bansur.MONTO) <= 0.99)
             AND bansur.TIPO_TRX IN ('PAGO', 'CANCELACION')
             ORDER BY clap.FECHA_TRANSACCION DESC''')

# Insertar los registros conciliables en la tabla conciliables
rows = c.fetchall()
c.executemany('INSERT INTO conciliables VALUES (?, ?, ?, ?)', rows)

# Contar las transacciones conciliables
c.execute('SELECT COUNT(*) FROM conciliables')
count = c.fetchone()[0]

# Imprimir el resultado
print("Número de transacciones conciliables: ", count)

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()