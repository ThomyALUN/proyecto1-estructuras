from lectura import leerCSV

listEtiquetas=[]
diccionarioEtiquetas={}

#crea las etiquetas 
def crearEtiquetas(nombreEtiqueta):
    listEtiquetas.append(nombreEtiqueta)
    return listEtiquetas

#modificar las etiquetas
def modificarEtiquetas(oldEtiqueta,newEtiqueta):
    listEtiquetas[listEtiquetas.index(oldEtiqueta)]=newEtiqueta
    return listEtiquetas

#eliminar las etiquetas
def eliminarEtiquetas(etiquetaEliminar):
    listEtiquetas.remove(etiquetaEliminar)
    return listEtiquetas

#llenar las etiquetas con los canales
def llenarEtiquetas(etiqueta,numeros):
    suscripciones=leerCSV("suscripciones.csv")[0]
    separarCanales=numeros.split(" ")
    #convierte la lista de strings a lista de numeros
    for a in range(len(separarCanales)):
        separarCanales[a]=int(separarCanales[a])  
        #llena un diccionario -> etiqueta(key) : canales(valores)
    diccionarioEtiquetas.update({etiqueta:suscripciones.loc[separarCanales,('URL del canal','Título del canal')]})
    return diccionarioEtiquetas

if __name__=="__main__":     
    print(crearEtiquetas('salud'))
    print(crearEtiquetas('cosina'))
    print(modificarEtiquetas('cosina','cocina'))
    print(eliminarEtiquetas('salud'))
    print(llenarEtiquetas('cocina','1 2 3 4'))