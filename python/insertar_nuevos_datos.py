import pandas as pd
import mysql.connector

#configuracion de la conexion
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="TU_CONTRASEÑA_AQUI",
    database="ventas_costos"
)
cursor = conn.cursor()

# Funcion para insertar datos desde CVS sin sobrescribir las PK
def insert_csv_to_mysql(csv_file, table_name, columns):
    df = pd.read_csv(csv_file)

    # Crear la consulta SQL de insercion ignorando duplicados
    placeholders = ",".join(["%s"]*len(columns))
    # Construir la parte ON DUPLICATE KEY UPDATE correctamente
    update_fields = ", ".join([f"{col} = VALUES({col})" for col in columns])
    sql = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {update_fields}"

    # Convertir los valores a tuplas e insertarlos
    values = [tuple(row) for row in df.values]
    cursor.executemany(sql, values)
    conn.commit()
    print(f"Datos insertados en {table_name}: {len(values)} filas")


# Insertar datos en cada tabla
insert_csv_to_mysql("data/nuevas_sucursales.csv", "sucursales", ["id_sucursal", "nombre_sucursal", "ciudad", "region", "gerente"])
insert_csv_to_mysql("data/nuevos_productos.csv", "productos", ["id_producto", "nombre_producto", "categoria", "precio_venta", "costo_unitario"])
insert_csv_to_mysql("data/nuevas_ventas.csv", "ventas", ["id_venta", "id_sucursal", "id_producto", "fecha_venta", "cantidad_vendida", "total_venta"])
insert_csv_to_mysql("data/nuevos_costos.csv", "costos", ["id_costo", "id_sucursal", "id_producto", "fecha_costo", "cantidad_comprada", "total_costo"])

#cerrar conexion
cursor.close()
conn.close()
print("insercion de nuevos datos finalizada con exito")

