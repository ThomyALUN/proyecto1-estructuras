import pandas as pd

# Esta función lee el archivo CSV especificado por la ruta y devuelve un dataframe de pandas
# en caso de los datos se encuentren con el formato deseado y no se presenten problemas al
# abrir el archivo. También devuelve un valor booleano que permite identificar si el dataframe
# es válido y utilizable o no.

def leerCSV(ruta):
    try:
        valido=True
        df=pd.read_csv(ruta)
        primeraFila=df.iloc[1]                                      #Se recuperan los datos del primer registro del archivo
        primeraColumna=primeraFila[0]
        segundaColumna=primeraFila[1]
        if segundaColumna[:4]=="http" and len(df.columns)==3:       #Se comprueba si el archivo tiene enlaces en la segunda columna
            print("Es un archivo sin modificaciones")
        elif primeraColumna[:4]=="http" and len(df.columns)==3:     #Se comprueba si el archivo ya tiene las clasificaciones de los canales
            print("El archivo ya contiene las clasificaciones")     
        else:
            print("El archivo no tiene un formato válido.")
            print("...finalizando programa...")
            valido=False
            df=None
    except:
        print("El archivo no tiene un formato válido.")
        print("...finalizando programa...")
        valido=False
        df=None
    return df, valido

if __name__=="__main__":
    leerCSV("suscripciones.csv")