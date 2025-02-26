import sqlite3

def crear_conexion(db_file):
    """Crea una conexión a la base de datos SQLite especificada por db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def crear_tablas(conn):
    """Crea las tablas necesarias en la base de datos."""
    try:
        c = conn.cursor()
        # Tabla documentos
        c.execute('''
            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                contenido TEXT,
                resumen TEXT,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Tabla correos
        c.execute('''
            CREATE TABLE IF NOT EXISTS correos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remitente TEXT,
                asunto TEXT,
                contenido TEXT,
                fecha_envio DATETIME,
                resumen TEXT
            )
        ''')
        # Tabla logs de búsqueda
        c.execute('''
            CREATE TABLE IF NOT EXISTS logs_busqueda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consulta TEXT,
                fecha_busqueda DATETIME DEFAULT CURRENT_TIMESTAMP,
                resultados INTEGER
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    conn = crear_conexion("agice.db")
    if conn is not None:
        crear_tablas(conn)
        print("Base de datos y tablas creadas exitosamente.")
        conn.close()
    else:
        print("Error al crear la conexión a la base de datos.")
