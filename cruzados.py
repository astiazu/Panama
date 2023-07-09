import sqlite3

# Conectar 
conn = sqlite3.connect('datos.db')
c = conn.cursor()

# Eliminar la tabla
c.execute("DROP TABLE IF EXISTS NuevaTabla")

# Crear una nueva tabla 
c.execute('''CREATE TABLE IF NOT EXISTS NuevaTabla (
                TARJETA INTEGER,
                FECHA_TRANSACCION TEXT,
                MONTO REAL,
                TIPO_TRX TEXT,
                TARJETA_BANSUR INTEGER,
                FECHA_TRANSACCION_BANSUR TEXT,
                MONTO_BANSUR REAL,
                TIPO_TRX_BANSUR TEXT,
                Cruce TEXT,
                ID_Conciliacion INTEGER
            )''')

# Ejecutar la consulta SQL y guardar
query = '''
INSERT INTO NuevaTabla
SELECT
    CLAP.TARJETA,
    CLAP.FECHA_TRANSACCION,
    CLAP.MONTO,
    CLAP.TIPO_TRX,
    BANSUR.TARJETA,
    BANSUR.FECHA_TRANSACCION,
    BANSUR.MONTO,
    BANSUR.TIPO_TRX,
    CASE
        WHEN CLAP.TARJETA = BANSUR.TARJETA AND CLAP.FECHA_TRANSACCION = BANSUR.FECHA_TRANSACCION THEN 'Cruzó'
        ELSE 'No cruzó'
    END,
    ROW_NUMBER() OVER (ORDER BY CLAP.FECHA_TRANSACCION, CLAP.TARJETA)
FROM
    CLAP
JOIN
    BANSUR ON CLAP.TARJETA = BANSUR.TARJETA
WHERE
    (CLAP.MONTO = BANSUR.MONTO OR ABS(CLAP.MONTO - BANSUR.MONTO) <= 0.99)
    AND CLAP.TIPO_TRX IN ('PAGADA', 'CANCELADA')
    AND BANSUR.TIPO_TRX = 'PAGO'
'''

c.execute(query)

# Abrir la tabla para ver los datos
c.execute("SELECT * FROM NuevaTabla LIMIT 100")
rows = c.fetchall()

# Imprimir los datos
for row in rows:
    print(row)


# Guardar commit
conn.commit()

# Cerrar 
conn.close()