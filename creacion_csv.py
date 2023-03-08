import pandas as pd
#Recibir un dataframe
def convertir(df):
    df.to_csv("canales_noind.csv", index=False)
    return df

# df=archivo()
# print(convertir(df))
# notas="canales_noind.csv"
# try:
#     file = open(notas, "r")
#     content = file.read()
#     file.close()
# except FileNotFoundError:
#     print("El archivo no se pudo encontrar")
# except PermissionError:
#     print("No se tienen los permisos necesarios para acceder al archivo")
# except IOError:
#     print("Ocurrió un error de E/S al acceder al archivo")
# except Exception as e:
#     print("Ocurrió un error inesperado:", e)
# else:
#     print("El archivo se leyó correctamente")






