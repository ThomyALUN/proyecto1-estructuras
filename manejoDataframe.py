import pandas as pd

from archivoAccesible import *

def mostrarDiccEtq(dicc):
    for etiqueta in dicc.keys():
        subtabla=dicc[etiqueta]
        print(f"La subtabla de la etiqueta {etiqueta} es:\n{subtabla}\n")

class ManejoDF():

    def __init__(self, ruta):
        self.leerCSV(ruta)
        self.listaEtiquetas=[]
        self.diccEtiquetas={}

    # Lee el archivo CSV
    def leerCSV(self, ruta):    
        # Esta función lee el archivo CSV especificado por la ruta y devuelve un dataframe de pandas
        # en caso de los datos se encuentren con el formato deseado y no se presenten problemas al
        # abrir el archivo. Devuelve como segundo valor un booleano que permite identificar si el dataframe
        # es válido y utilizable o no. Y como último valor devuelve el tipo de archivo identificado.

        # El tipo de archivo #1 se refiere a archivos recién descargados desde Google Takeout
        # El tipo de archivo #2 se refiere a archivos modificados/creados durante el uso de la aplicación                                              
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
        self.tabla=df
        self.valido=valido
        self.tipo=tipo
        if valido:
            self.nombreColURL=self.tabla.columns[0]
            self.nombreColTitulo=self.tabla.columns[1]
            self.listaCanales=list(self.tabla.loc[:,self.nombreColTitulo])

    # Exporta el archivo CSV resultante
    def crearCSV(self):
        try:
            self.tabla.to_csv("canalesClasificados.csv", index=False)
        except Exception as error:
            return f"No se pudo guardar el archivo -> {error}"

    # Añade una etiqueta
    def crearEtiqueta(self, nombreEtiqueta):
        if nombreEtiqueta in self.listaEtiquetas:
            return 'La etiqueta ya existe'
        else:
            self.listaEtiquetas.append(nombreEtiqueta)
            self.diccEtiquetas[nombreEtiqueta]=pd.DataFrame()

    # Edita el nombre de una etiqueta (incluyendo el nombre de la etiqueta de los canales asociados)
    def modificarEtiqueta(self, oldEtiqueta, newEtiqueta):
        if oldEtiqueta in self.listaEtiquetas:
            if (newEtiqueta in self.listaEtiquetas):
                return f'La etiqueta {newEtiqueta} ya existe'
            else:
                subTabla=self.diccEtiquetas.pop(oldEtiqueta)
                self.listaEtiquetas[self.listaEtiquetas.index(oldEtiqueta)]=newEtiqueta
                if subTabla.empty:
                    self.diccEtiquetas[newEtiqueta]=pd.DataFrame()
                else:
                    indices=subTabla.index
                    self.diccEtiquetas[newEtiqueta]=subTabla
                    for i in indices:
                        nombreCanal=subTabla.loc[i, self.nombreColTitulo]
                        self.actualizarEtqCanal(newEtiqueta, nombreCanal)
        else:
            return 'La etiqueta que desea modificar no existe'

    # Eliminar una etiqueta en específico
    def eliminarEtiqueta(self, etiquetaEliminar):
        if etiquetaEliminar in self.listaEtiquetas:
            subTabla=self.diccEtiquetas[etiquetaEliminar]
            indices=subTabla.index
            self.diccEtiquetas[etiquetaEliminar]=subTabla
            for i in indices:
                nombreCanal=subTabla.loc[i, self.nombreColTitulo]
                self.actualizarEtqCanal(None, nombreCanal)
            self.listaEtiquetas.remove(etiquetaEliminar)
            self.diccEtiquetas.pop(etiquetaEliminar)
        else:
            return 'La etiqueta que desea eliminar no existe'

    # Le agrega la etiqueta a un canal
    def clasificarCanal(self, etiqueta, nombreCanal):
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        elif etiqueta not in self.listaEtiquetas:
            return f"La etiqueta {etiqueta} no existe"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        if canal.loc[indice, "Etiqueta"]==None:
            if self.diccEtiquetas[etiqueta].empty:
                self.diccEtiquetas[etiqueta]=canal  #Si la etiqueta no tiene canales, se agrega el primero directamente
            else:
                self.diccEtiquetas[etiqueta]=pd.concat([self.diccEtiquetas[etiqueta],canal])  #Si la etiqueta ya tiene canales, se agregan los nuevos al final
            self.actualizarEtqCanal(etiqueta, nombreCanal)
        else:
            return f"El canal {canal} ya está clasificado"

    # Cambia la etiqueta asociada a un canal
    def actualizarEtqCanal(self, etiqueta, nombreCanal):
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        self.tabla.loc[indice, "Etiqueta"]=etiqueta
        self.diccEtiquetas[etiqueta].loc[indice, "Etiqueta"]=etiqueta

    # Cambia la etiqueta asociada a un canal, lo elimina de la subtabla de la etiqueta actual y lo agrega a la subtabla de la nueva etiqueta
    def modificarEtqCanal(self, newEtiqueta, nombreCanal):
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        elif newEtiqueta not in self.listaEtiquetas:
            return f"La etiqueta {newEtiqueta} no existe"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        etqAntigua=self.tabla.loc[indice, "Etiqueta"]
        if etqAntigua!=None:
            self.diccEtiquetas[etqAntigua].drop(indice, inplace=True)
        if indice not in self.diccEtiquetas[newEtiqueta].index:
            self.diccEtiquetas[newEtiqueta]=pd.concat([self.diccEtiquetas[newEtiqueta],canal])
        self.tabla.loc[indice, "Etiqueta"]=newEtiqueta
        self.diccEtiquetas[newEtiqueta].loc[indice, "Etiqueta"]=newEtiqueta

    # Quita la etiqueta asociada a un canal
    def quitarEtqCanal(self, nombreCanal):
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        etqAntigua=self.tabla.loc[indice, "Etiqueta"]
        if etqAntigua!=None:
            self.diccEtiquetas[etqAntigua].drop(indice, inplace=True)
        self.tabla.loc[indice, "Etiqueta"]=None

    # Añade un nuevo canal manualmente
    def registrarCanal(self, urlCanal, nombreCanal, etiqueta=None):
        if nombreCanal in self.listaCanales:
            return f"El canal {nombreCanal} ya esta registrado"
        elif urlCanal=="":
            return f"La URL:{urlCanal} tiene un formato inválido"
        elif etiqueta!=None and etiqueta not in self.listaEtiquetas:
            return f"La etiqueta {etiqueta} no existe"
        nuevaFila=pd.DataFrame([[urlCanal, nombreCanal, None]], columns=[self.nombreColURL, self.nombreColTitulo, "Etiqueta"])
        self.tabla=pd.concat([self.tabla,nuevaFila], ignore_index=True)
        self.listaCanales.append(nombreCanal)
        if etiqueta!=None:
            self.clasificarCanal(etiqueta, nombreCanal)

    # Elimina un canal
    def eliminarCanal(self, nombreCanal):
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        etiqueta=canal.loc[indice,"Etiqueta"]
        if etiqueta!=None:
            self.diccEtiquetas[etiqueta].drop(indice, inplace=True)
        self.tabla.drop(indice, inplace=True)
        self.listaCanales.remove(nombreCanal)

    # Devuelve el nombre de todos los canales registrados
    def getListaCanales(self):
        return self.listaCanales

    # Devuelve el nombre de todas las etiquetas registradas
    def getListaEtiquetas(self):
        return self.listaEtiquetas
    
    # Devuelve los canales asociados a una etiqueta en específico
    def getCanalesEtiqueta(self, etiqueta):
        if etiqueta not in self.listaEtiquetas:
            return f"La etiqueta {etiqueta} no existe"
        else:
            return self.diccEtiquetas[etiqueta]
        
    # Devuelve los datos de un canal mediante su nombre
    def getDatosCanal(self, nombreCanal):
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        url=canal.loc[indice,self.nombreColURL]
        etiqueta=canal.loc[indice,"Etiqueta"]
        return [url,etiqueta]


if __name__=="__main__":
    ruta="suscripciones.csv"
    valido=archivoAccesible(ruta)
    if valido:
        print("El archivo es accesible")
    else:
        exit()
    
    objetoDF=ManejoDF(ruta)
    objetoDF.crearEtiqueta('salud')
    objetoDF.crearEtiqueta('cosina')
    objetoDF.crearEtiqueta('depirtes')
    print(objetoDF.listaEtiquetas)

    objetoDF.modificarEtiqueta('cosina','cocina')
    objetoDF.modificarEtiqueta('depirtes','deportes')
    print(objetoDF.listaEtiquetas)

    objetoDF.eliminarEtiqueta('salud')
    print(objetoDF.listaEtiquetas)

    objetoDF.crearEtiqueta('salud')
    print(objetoDF.listaEtiquetas)

    objetoDF.clasificarCanal('salud', 'Quiero Cupcakes')
    mostrarDiccEtq(objetoDF.diccEtiquetas)

    objetoDF.clasificarCanal('salud', 'Yuya')    
    mostrarDiccEtq(objetoDF.diccEtiquetas)

    objetoDF.clasificarCanal('salud', 'DoctorBlog')
    mostrarDiccEtq(objetoDF.diccEtiquetas)

    objetoDF.modificarEtiqueta('salud','Salud')
    print(objetoDF.listaEtiquetas)
    mostrarDiccEtq(objetoDF.diccEtiquetas)

    objetoDF.modificarEtqCanal('deportes','Yuya')
    print(objetoDF.listaEtiquetas)
    mostrarDiccEtq(objetoDF.diccEtiquetas)

    objetoDF.registrarCanal("...", "Auronplay", "Salud")
    print(objetoDF.tabla)
    mostrarDiccEtq(objetoDF.diccEtiquetas)

    print(objetoDF.getDatosCanal("Auronplay"))

    print(objetoDF.listaCanales)
    objetoDF.eliminarCanal('Quiero Cupcakes')
    print(objetoDF.tabla)
    print(objetoDF.listaCanales)

    mostrarDiccEtq(objetoDF.diccEtiquetas)
