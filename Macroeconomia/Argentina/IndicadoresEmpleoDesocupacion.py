import pandas as pd
import io
import requests
import json

class IndicadoresEmpleoDesocupacion:
    
    def __init__(self):
        """
        Los indicadores de empleo y desocupacion se basan en gran medida en la
        EPC (encuesta permanente de hogares)  en 31 aglomeraciones urbanas.

        """
        pass

    
    def getTasaActividad(self, periodo = "Anual"):
        """
        La tasa de actividad es PEA/PoblacionTotal
        
        Se considera como una tasa indicadora de la oferta laboral por parte
        de los trabajadores.
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual", "Trimestral")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-principales-variables-ocupacionales-eph-continua-actividad"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 1 if periodo == "Trimestral" else 0 #si no es trimestral siempre es anual
            
        ultimoResultado = resultado[selector]
        urlDescarga = ultimoResultado['url']
        descripcion = ultimoResultado['description']
        print("Descargando: {}".format(descripcion))
        print("Archivo: {}".format(urlDescarga))
        
        #Descargar la url con cvs y generar pandas dataframe
        contenidoCVS = requests.get(urlDescarga).content
        flujoCVS = io.StringIO(contenidoCVS.decode('utf-8'))
        df_temp = pd.read_csv(flujoCVS)
        
        #transform string to datetime
        df_temp['indice_tiempo'] = pd.to_datetime(df_temp['indice_tiempo'], format='%Y-%m-%d', errors='ignore')
        df_temp['indice_tiempo'] = df_temp['indice_tiempo'].dt.date
        #set index
        df_temp.set_index('indice_tiempo', inplace=True)
        
        return df_temp
    
    def getTasaEmpleo(self, periodo = "Anual"):
        """
        La tasa de empleo se calcula como poblacion ocupada/poblacion total
        
        Se concidera como una tasa representativa de la demanda laboral ejercida
        por la empresas.
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual", "Trimestral")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-principales-variables-ocupacionales-eph-continua-empleo"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 1 if periodo == "Trimestral" else 0 #si no es trimestral siempre es anual
            
        ultimoResultado = resultado[selector]
        urlDescarga = ultimoResultado['url']
        descripcion = ultimoResultado['description']
        print("Descargando: {}".format(descripcion))
        print("Archivo: {}".format(urlDescarga))
        
        #Descargar la url con cvs y generar pandas dataframe
        contenidoCVS = requests.get(urlDescarga).content
        flujoCVS = io.StringIO(contenidoCVS.decode('utf-8'))
        df_temp = pd.read_csv(flujoCVS)
        
        #transform string to datetime
        df_temp['indice_tiempo'] = pd.to_datetime(df_temp['indice_tiempo'], format='%Y-%m-%d', errors='ignore')
        df_temp['indice_tiempo'] = df_temp['indice_tiempo'].dt.date
        #set index
        df_temp.set_index('indice_tiempo', inplace=True)
        
        return df_temp
    
    def getTasaDesocupacion(self, periodo = "Anual"):
        """
        Se calcula como: poblacion desocupada/PEA
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual", "Trimestral")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-principales-variables-ocupacionales-eph-continua-desempleo"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 1 if periodo == "Trimestral" else 0 #si no es trimestral siempre es anual
            
        ultimoResultado = resultado[selector]
        urlDescarga = ultimoResultado['url']
        descripcion = ultimoResultado['description']
        print("Descargando: {}".format(descripcion))
        print("Archivo: {}".format(urlDescarga))
        
        #Descargar la url con cvs y generar pandas dataframe
        contenidoCVS = requests.get(urlDescarga).content
        flujoCVS = io.StringIO(contenidoCVS.decode('utf-8'))
        df_temp = pd.read_csv(flujoCVS)
        
        #transform string to datetime
        df_temp['indice_tiempo'] = pd.to_datetime(df_temp['indice_tiempo'], format='%Y-%m-%d', errors='ignore')
        df_temp['indice_tiempo'] = df_temp['indice_tiempo'].dt.date
        #set index
        df_temp.set_index('indice_tiempo', inplace=True)
        
        return df_temp
    
    def getTasaSubocupacionDemandante(self, periodo = "Anual"):
        """
        Se calcula como poblacion desocupada demandante/PEA
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual", "Trimestral")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-principales-variables-ocupacionales-eph-continua-subocupacion-demandante"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 1 if periodo == "Trimestral" else 0 #si no es trimestral siempre es anual
            
        ultimoResultado = resultado[selector]
        urlDescarga = ultimoResultado['url']
        descripcion = ultimoResultado['description']
        print("Descargando: {}".format(descripcion))
        print("Archivo: {}".format(urlDescarga))
        
        #Descargar la url con cvs y generar pandas dataframe
        contenidoCVS = requests.get(urlDescarga).content
        flujoCVS = io.StringIO(contenidoCVS.decode('utf-8'))
        df_temp = pd.read_csv(flujoCVS)
        
        #transform string to datetime
        df_temp['indice_tiempo'] = pd.to_datetime(df_temp['indice_tiempo'], format='%Y-%m-%d', errors='ignore')
        df_temp['indice_tiempo'] = df_temp['indice_tiempo'].dt.date
        #set index
        df_temp.set_index('indice_tiempo', inplace=True)
        
        return df_temp
    
    def getTasaSubocupacionNoDemandante(self, periodo = "Anual"):
        """
        Se calcula como poblacion desocupada NO demandante/PEA
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual", "Trimestral")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-principales-variables-ocupacionales-eph-continua-subocupacion-no-demandante"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 1 if periodo == "Trimestral" else 0 #si no es trimestral siempre es anual
            
        ultimoResultado = resultado[selector]
        urlDescarga = ultimoResultado['url']
        descripcion = ultimoResultado['description']
        print("Descargando: {}".format(descripcion))
        print("Archivo: {}".format(urlDescarga))
        
        #Descargar la url con cvs y generar pandas dataframe
        contenidoCVS = requests.get(urlDescarga).content
        flujoCVS = io.StringIO(contenidoCVS.decode('utf-8'))
        df_temp = pd.read_csv(flujoCVS)
        
        #transform string to datetime
        df_temp['indice_tiempo'] = pd.to_datetime(df_temp['indice_tiempo'], format='%Y-%m-%d', errors='ignore')
        df_temp['indice_tiempo'] = df_temp['indice_tiempo'].dt.date
        #set index
        df_temp.set_index('indice_tiempo', inplace=True)
        
        return df_temp
    
    def getIndiceSalariosBase2016(self):
        """
        Es un indice que estima la evolucion de los salarios de la economia
        Base octubre 2016

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-indice-salarios-base-octubre-2016"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 0 #si no es trimestral o mensual siempre es anual
            
        ultimoResultado = resultado[selector]
        urlDescarga = ultimoResultado['url']
        descripcion = ultimoResultado['description']
        print("Descargando: {}".format(descripcion))
        print("Archivo: {}".format(urlDescarga))
        
        #Descargar la url con cvs y generar pandas dataframe
        contenidoCVS = requests.get(urlDescarga).content
        flujoCVS = io.StringIO(contenidoCVS.decode('utf-8'))
        df_temp = pd.read_csv(flujoCVS)
        
        #transform string to datetime
        df_temp['indice_tiempo'] = pd.to_datetime(df_temp['indice_tiempo'], format='%Y-%m-%d', errors='ignore')
        df_temp['indice_tiempo'] = df_temp['indice_tiempo'].dt.date
        #set index
        df_temp.set_index('indice_tiempo', inplace=True)
        
        return df_temp
    