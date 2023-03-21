import pandas as pd

from funciones import *

# Clase diseñada para facilitar el manejo de los datos de los canales y etiquetas mediante la estructura de datos "DataFrame" del módulo pandas
class ManejoDF():

    def __init__(self, ruta):
        self.listaEtiquetas=[]      # Se inicia una lista donde se almacena el nombre de todas las etiquetas creadas
        self.diccEtiquetas={}       # Se inicia un diccionario donde se almacenan todas las etiquetas y sus canales asociados. key: nombre de la etiqueta, value: sublista de canales
        self.listaCanales=[]        # Se inicia una lista donde se almacena el nombre de todos los canales registrados
        self.leerCSV(ruta)          # Se lee el archivo CSV


    # Lee el archivo CSV
    def leerCSV(self, ruta):    
        # Esta función lee el archivo CSV especificado por la ruta y devuelve un dataframe de pandas
        # en caso de los datos se encuentren con el formato deseado y no se presenten problemas al
        # abrir el archivo. Devuelve como segundo valor un booleano que permite identificar si el dataframe
        # es válido y utilizable o no. Y como último valor devuelve el tipo de archivo identificado.

        # El tipo de archivo #1 se refiere a archivos recién descargados desde Google Takeout
        # El tipo de archivo #2 se refiere a archivos modificados/creados durante el uso de la aplicación                                              
        try:                                                            # Se tiene un control sobre los problemas que se pueden presentar al intentar abrir el archivo o interactuar con él
            valido=True
            extension=ruta[-3:]                                         # Se obtiene la extensión del archivo
            if extension!="csv":
                # Se comprueba que la extensión del archivo sea .csv
                raise ValueError(f"La extensión del archivo es inválida: {extension}")
            df=pd.read_csv(ruta)
            primeraFila=df.iloc[1]                                      # Se recuperan los datos del primer registro del archivo
            primeraColumna=primeraFila[0]                               # Se toma el valor de la celda ubicada en: (fila: 1, columna: 1)
            segundaColumna=primeraFila[1]                               # Se toma el valor de la celda ubicada en: (fila: 1, columna: 2)
            if segundaColumna[:4]=="http" and len(df.columns)==3:       
                # Se comprueba si el archivo tiene enlaces en la segunda columna, en caso de ser así se asume que es un archivo recién obtenido del servicio de Google Takeout
                tipo=1
                df=df.drop(df.columns[0], axis="columns")               # Se elimina la primera columna ya que no contiene información útil
                df=df.assign(Etiqueta=None)                             # Se crea una nueva columna que contendrá el valor de la etiqueta asignada por el usuario
            elif primeraColumna[:4]=="http" and len(df.columns)==3:     
                # Se comprueba si el archivo ya tiene las clasificaciones de los canales, en caso de ser así se asume que es un archivo con etiquetas por lo cual se procede a una precarga
                tipo=2 
                df=df.fillna(value=0)
                nombreColEtiqueta=df.columns[2]
                df[nombreColEtiqueta].replace(0, None, inplace=True)
                self.listaEtiquetas=df[nombreColEtiqueta].unique()          # Se devuelve un arreglo de numpy con el nombre de las etiquetas
                self.listaEtiquetas=list(self.listaEtiquetas)               # Se transforma en una lista
                self.listaEtiquetas.remove(None)                            # Se elimina el valor nulo/por defecto de las etiquetas de la lista con el nombre de las etiquetas
                for etiqueta in self.listaEtiquetas:
                    # Se buscan todos los canales que tengan una etiqueta determinada y se introducen al diccionario de etiquetas
                    miniDF=df[df[nombreColEtiqueta]==etiqueta]
                    self.diccEtiquetas[etiqueta]=miniDF
            else:                                                       
                # Se detecta si el archivo no presenta errores durante su interacción pero su formato es inválido
                mensaje=f"{ruta} es un archivo que no tiene un formato válido"
                valido=False

        except FileNotFoundError:                                                         
            #Se detecta si han habido problemas a durante la carga o interacción con el archivo
            mensaje=f"El archivo: {ruta} no existe."
            valido=False
        except Exception as e:
            mensaje=f"Hubo un error durante la ejecución. {e}"
            valido=False

        self.valido=valido # Se almacena un booleano que describe si el archivo se pudo leer y acceder 

        # Se comprueba si la lectura fue exitosa
        if valido:
            self.tabla=df                                                       # Se asignan los datos leídos al atributo tabla
            self.tipo=tipo                                                      # Se almacena el tipo de archivo leído
            self.nombreColURL=self.tabla.columns[0]                             # Se almacena el nombre de la columna con la URL
            self.nombreColTitulo=self.tabla.columns[1]                          # Se almacena el nombre de la columna con el Título del canal 
            self.listaCanales=list(self.tabla.loc[:,self.nombreColTitulo])      # Se actualiza la lista con el nombre de los canales
        else:
            # En caso de que la lectura fracase, se devuelve el mensaje de error correspondiente
            self.tabla=None                                                     # Se asignan valores nulos a los atributos                    
            self.tipo=None  
            return mensaje

    # Exporta el archivo CSV resultante
    def crearCSV(self, ruta="archivosCSV/canalesClasificados.csv"):
        #Se intenta exportar el archivo
        try:
            self.tabla.to_csv(ruta, index=False)
        except Exception as error:
            #En caso de que no funciona la exportación, se reporta el error al usuario
            return f"No se pudo guardar el archivo -> {error}"

    # Añade una etiqueta
    def crearEtiqueta(self, nombreEtiqueta):
        # Se revisa si la etiqueta ya existe
        if nombreEtiqueta in self.listaEtiquetas:
            return 'La etiqueta ya existe'
        else:
            # Si la etiqueta no existe, se agrega a la lista de etiquetas y en el diccionario de etiquetas se le asigna un DataFrame vacío
            self.listaEtiquetas.append(nombreEtiqueta)
            self.diccEtiquetas[nombreEtiqueta]=pd.DataFrame()

    # Edita el nombre de una etiqueta (incluyendo el nombre de la etiqueta de los canales asociados)
    def modificarEtiqueta(self, oldEtiqueta, newEtiqueta):
        # Se comprueba que la etiqueta a cambiar se encuentra en la lista de etiquetas actual
        if oldEtiqueta in self.listaEtiquetas:
            # Se comprueba si la etiqueta nueva se encuentra en la lista de etiquetas actual 
            if(newEtiqueta in self.listaEtiquetas):
                return f'La etiqueta {newEtiqueta} ya existe'
            else:
                subTabla=self.diccEtiquetas.pop(oldEtiqueta)                                # Se elimina la subtabla que hay en el diccionario de etiquetas y se retorna a una variable
                self.listaEtiquetas[self.listaEtiquetas.index(oldEtiqueta)]=newEtiqueta     # Se cambia el nombre de la etiqueta antigua por el nombre de la etiqueta nueva
                if subTabla.empty:
                    # Se comprueba si el DataFrame eliminado estaba vacío                                                          
                    self.diccEtiquetas[newEtiqueta]=pd.DataFrame()                          # En caso de que el DF este vacío, no es necesario modificar las etiquetas de los canales 
                else:
                    indices=subTabla.index                                                  # Se obtienen los índices de los canales que estaban relacionados con la etiqueta antigua
                    self.diccEtiquetas[newEtiqueta]=subTabla                                # Se introduce la subtabla en el diccionario como valor de la llave con el nombre de la nueva etiqueta
                    for i in indices:
                        # Se actualiza la etiqueta de todos los canales relacionados
                        nombreCanal=subTabla.loc[i, self.nombreColTitulo]
                        self.actualizarEtqCanal(newEtiqueta, nombreCanal)
        else:
            return 'La etiqueta no existe'

    # Eliminar una etiqueta en específico
    def eliminarEtiqueta(self, etiquetaEliminar):
        # Se comprueba si la etiqueta existe en la lista de etiquetas
        if etiquetaEliminar in self.listaEtiquetas:
            subTabla=self.diccEtiquetas[etiquetaEliminar]               # Se recupera la subtabla de la etiqueta a eliminar
            indices=subTabla.index                                      # Se obtienen los índices de los canales 
            for i in indices:
                # Se itera sobre los canales que tenían la etiqueta a eliminar y se les pone el valor por defecto: None
                nombreCanal=subTabla.loc[i, self.nombreColTitulo]
                self.actualizarEtqCanal(None, nombreCanal)
            self.listaEtiquetas.remove(etiquetaEliminar)                # Se elimina la etiqueta de la lista
            self.diccEtiquetas.pop(etiquetaEliminar)                    # Se elimina la etiqueta del diccionario
        else:
            return f'La etiqueta {etiquetaEliminar} no existe'

    # Le agrega la etiqueta a un canal
    def clasificarCanal(self, etiqueta, nombreCanal):
        # Se comprueba que el canal este registrado
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        # Se comprueba que la etiqueta exista
        elif etiqueta not in self.listaEtiquetas:
            return f"La etiqueta {etiqueta} no existe"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal] # Se recuperan todos los datos del canal
        indice=canal.index[0]                                           # Se obtiene el índice del canal
        # Se comprueba si el canal esta clasificado. El valor None viene por defecto en los canales no clasificados
        if canal.loc[indice, "Etiqueta"]==None:
            if self.diccEtiquetas[etiqueta].empty:
                self.diccEtiquetas[etiqueta]=canal  #Si la etiqueta no tiene canales, se agrega el primero directamente
            else:
                self.diccEtiquetas[etiqueta]=pd.concat([self.diccEtiquetas[etiqueta],canal])  #Si la etiqueta ya tiene canales, se agregan los nuevos al final
            self.actualizarEtqCanal(etiqueta, nombreCanal)
        else:
            return f"El canal {nombreCanal} ya está clasificado"

    # Cambia la etiqueta asociada a un canal (no es un boton)
    def actualizarEtqCanal(self, etiqueta, nombreCanal):
        # Se comprueba que el canal este registrado
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        self.tabla.loc[indice, "Etiqueta"]=etiqueta                         # Se actualiza el valor de la etiqueta en la tabla principal
        self.diccEtiquetas[etiqueta].loc[indice, "Etiqueta"]=etiqueta       # Se actualiza el valor de la etiqueta en la subtabla de la etiqueta

    # Cambia la etiqueta asociada a un canal, lo elimina de la subtabla de la etiqueta actual y lo agrega a la subtabla de la nueva etiqueta
    def modificarEtqCanal(self, newEtiqueta, nombreCanal):
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        elif newEtiqueta not in self.listaEtiquetas:
            return f"La etiqueta {newEtiqueta} no existe"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        etqAntigua=self.tabla.loc[indice, "Etiqueta"]                       # Se recupera la etiqueta actual del canal
        if etqAntigua!=None:
            self.diccEtiquetas[etqAntigua].drop(indice, inplace=True)       # Si el canal ya tenía clasificación, se elimina de la subtabla correspondiente
        # Se comprueba que el canal no se encuentre en la subtabla de la nueva etiqueta
        if indice not in self.diccEtiquetas[newEtiqueta].index:
            self.diccEtiquetas[newEtiqueta]=pd.concat([self.diccEtiquetas[newEtiqueta],canal])
        self.tabla.loc[indice, "Etiqueta"]=newEtiqueta                       
        self.diccEtiquetas[newEtiqueta].loc[indice, "Etiqueta"]=newEtiqueta # Se actualiza el valor de la etiqueta en la tabla ppal y en la subtabla

    # Quita la etiqueta asociada a un canal. La pone en el valor por defecto: None
    def quitarEtqCanal(self, nombreCanal):
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        etqAntigua=self.tabla.loc[indice, "Etiqueta"]                   # Se recupera la etiqueta actual del canal
        if etqAntigua!=None:
            # Si la etiqueta actual no es el valor por defecto, se elimina de la subtabla correspondiente
            self.diccEtiquetas[etqAntigua].drop(indice, inplace=True)
        self.tabla.loc[indice, "Etiqueta"]=None     # Se actualiza el valor de la etiqueta en la tabla ppal

    # Añade un nuevo canal manualmente. Es opcional registrar el canal con su clasificación
    def registrarCanal(self, urlCanal, nombreCanal, etiqueta=None):
        if nombreCanal in self.listaCanales:
            return f"El canal {nombreCanal} ya esta registrado"
        elif urlCanal=="":
            return f"La URL:{urlCanal} tiene un formato inválido"
        elif etiqueta!=None and etiqueta not in self.listaEtiquetas:
            return f"La etiqueta {etiqueta} no existe"
        nuevaFila=pd.DataFrame([[urlCanal, nombreCanal, None]], columns=[self.nombreColURL, self.nombreColTitulo, "Etiqueta"])  # Se genera un DF con una sola fila, con los datos suministrados para el nuevo canal
        self.tabla=pd.concat([self.tabla,nuevaFila], ignore_index=True) # Se añade el nuevo canal al final de la tabla principal
        self.listaCanales.append(nombreCanal)                           # Se agrega el nombre del canal a la lista de canales
        
        
        if etiqueta!=None:
            # Se clasifica el canal en caso de que se haya enviado una etiqueta                             
            self.clasificarCanal(etiqueta, nombreCanal)

    # Elimina un canal
    def eliminarCanal(self, nombreCanal):
        # Se comprueba que el canal este registrado
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        etiqueta=canal.loc[indice,"Etiqueta"]   # Se recupera la etiqueta actual del canal
        if etiqueta!=None:
            # Si la etiqueta no es el valor por defecto, se elimina del canal de la subtabla correspondiente
            self.diccEtiquetas[etiqueta].drop(indice, inplace=True)
        self.tabla.drop(indice, inplace=True)   # Se elimina el canal de la tabla ppal
        self.listaCanales.remove(nombreCanal)   # Se elimina el nombre del canal de la lista de canales

    # Devuelve el nombre de todos los canales registrados en una lista
    def getListaCanales(self):
        return self.listaCanales

    # Devuelve el nombre de todas las etiquetas registradas en una lista
    def getListaEtiquetas(self):
        return self.listaEtiquetas
    
    # Devuelve los canales asociados a una etiqueta en específico. Devuelve una subtabla, es decir, un DataFrame de pandas
    def getCanalesEtiqueta(self, etiqueta):
        if etiqueta not in self.listaEtiquetas:
            return f"La etiqueta {etiqueta} no existe"
        else:
            subtabla=self.diccEtiquetas[etiqueta]                   # Se recupera el subdataframe con los canales relacionados a una etiqueta
            canalesSubtabla=subtabla.loc[:,self.nombreColTitulo]    # Se separa el nombre de los canales solamente
            canalesSubtabla=list(canalesSubtabla)                   # Se transforman los datos a una lista de python
            return canalesSubtabla
        
    # Devuelve los datos de un canal mediante su nombre. Devuelve una lista con dos valores: la URL y la etiqueta asignada
    def getDatosCanal(self, nombreCanal):
        if nombreCanal not in self.listaCanales:
            return f"El canal {nombreCanal} no esta registrado"
        canal=self.tabla[self.tabla[self.nombreColTitulo]==nombreCanal]
        indice=canal.index[0]
        url=canal.loc[indice,self.nombreColURL]
        etiqueta=canal.loc[indice,"Etiqueta"]
        return [url,etiqueta]


if __name__=="__main__":

    """
    ruta="archivosCSV/canalesClasificados.csv"
    valido=archivoAccesible(ruta)
    if valido:
        print("El archivo es accesible")
    else:
        exit()
    
    objetoDF=ManejoDF(ruta)
    print(objetoDF.listaCanales)
    print(objetoDF.tabla)
    print(objetoDF.listaEtiquetas)
    mostrarDiccEtq(objetoDF.diccEtiquetas)
    """

    ruta="archivosCSV/suscripciones.csv"
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

    print(objetoDF.clasificarCanal('salud', 'Quiero Cupcakes'))
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

    print(objetoDF.getCanalesEtiqueta("Salud"))

    mostrarDiccEtq(objetoDF.diccEtiquetas)

    objetoDF.crearCSV()
