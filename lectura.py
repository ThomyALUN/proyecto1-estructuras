import pandas as pd

# Esta función lee el archivo CSV especificado por la ruta y devuelve un dataframe de pandas
# en caso de los datos se encuentren con el formato deseado y no se presenten problemas al
# abrir el archivo. Devuelve como segundo valor un booleano que permite identificar si el dataframe
# es válido y utilizable o no. Y como último valor devuelve el tipo de archivo identificado.

# El tipo de archivo #1 se refiere a archivos recién descargados desde Google Takeout
# El tipo de archivo #2 se refiere a archivos modificados/creados durante el uso de la aplicación

def leerCSV(ruta):                                                  
    try:                                                            #Se tiene un control sobre los problemas que se pueden presentar al intentar abrir el archivo o interactuar con él
        valido=True
        extension=ruta[-3:]                                         #Se obtiene la extensión del archivo
        if extension!="csv":
            raise RuntimeError
        df=pd.read_csv(ruta)
        primeraFila=df.iloc[1]                                      #Se recuperan los datos del primer registro del archivo
        primeraColumna=primeraFila[0]
        segundaColumna=primeraFila[1]
        if segundaColumna[:4]=="http" and len(df.columns)==3:       #Se comprueba si el archivo tiene enlaces en la segunda columna
            tipo=1
            df=df.drop(df.columns[0], axis="columns")               #Se elimina la primera columna ya que no contiene información útil
            df=df.assign(Etiqueta=None)
            print(f"{ruta} es un archivo válido sin modificaciones.")
        elif primeraColumna[:4]=="http" and len(df.columns)==3:     #Se comprueba si el archivo ya tiene las clasificaciones de los canales
            tipo=2 
            print(f"{ruta} es un archivo válido que ya contiene las clasificaciones.")    
        else:                                                       #Se detecta si el archivo no presenta errores durante su interacción pero su formato es inválido
            print(f"{ruta} es un archivo que no tiene un formato válido.")
            valido=False
            df=None
            tipo=None
    except FileNotFoundError:                                                         #Se detecta si han habido problemas a durante la carga o interacción con el archivo
        print(f"El archivo: {ruta} no existe.")
        valido=False
        df=None
        tipo=None
    except:
        print(f"Hubo un error durante la ejecución")
        valido=False
        df=None
        tipo=None
    return df, valido, tipo

if __name__=="__main__":
    df, valido, tipo=leerCSV("suscripciones.csv")
    if valido:
        print(f"\nEl dataframe recuperado es el siguiente:\n{df}")
    else:
        print("\n...finalizando programa...")