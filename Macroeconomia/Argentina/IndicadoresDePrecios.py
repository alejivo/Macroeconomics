# -*- coding: utf-8 -*-
import pandas as pd
import io
import requests
import json
import webbrowser
from Macroeconomia.Argentina.ProductoInternoBruto import ProductoInternoBruto

class IndicadoresDePrecios:
    
    def __init__(self):
        """
        Inicializa
        """
        self.__PIB = ProductoInternoBruto()
    
    def getPIB(self):
        return self.__PIB
    
    def getDeflactorBase2004(self, periodo = "Anual"):
        """
        Se puede utilizar como un indicador de precio, tiene mayor cobertura
        que el IPC pero no incluye bienes intermedios.
    
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual" o "Trimestral")
            DESCRIPTION. The default is "Anual".
    
        Returns
        -------
        pd.DataFrame()
    
        """
        return self.__PIB.getIndicePreciosImplicitosBase2004(periodo)
    
    def getIndicePreciosAlConsumidorCordobaBaseJulio2012(self):
        """
        Se elabora en la mayoria de los paises mensualmente, mide las 
        variaciones de los precios de un conjunto de bienes y servicios para 
        un tiempo determinado con una base determinada (en este caso el año 2016)
        
        El IPC Cordoba solo tiene en cuenta la provincia de cordoba.
        Esta solo disponible como serie mensual.
    
        Returns
        -------
        pd.DataFrame()
    
        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-indice-precios-al-consumidor-provincia-cordoba-base-2014-100"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 0
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
    
    def getIndicePreciosAlConsumidor(self, periodo = "Mensual"):
        """
        Se elabora en la mayoria de los paises mensualmente, mide las 
        variaciones de los precios de un conjunto de bienes y servicios para 
        un tiempo determinado con una base determinada (en este caso el año 2016)
        
        El IPC Nacional esta formado por:
            * Gran Buenos Aires 44%
            * Pampeana 34.2%
            * Nordeste 6.9%
            * Cuyo 5.6%
            * Patagonia 4.6%
    
        Parameters
        ----------
        periodo : str, optional (puede ser "Mensual" o "Trimestral")
            DESCRIPTION. The default is "Mensual".
    
        Returns
        -------
        pd.DataFrame()
    
        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-indice-precios-al-consumidor-nacional-ipc-base-diciembre-2016"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 1 if periodo == 'Trimestral' else 0 #si no es trimestral siempre es anual
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
    
    def getCoeficienteEstabilizacionDeReferencia(self):
        """
        Tambien llamado CER
        Es un indicador de ajuste diario elaborado por el BCRA en base al IPC
        
        Se usa para ajustar  determinados titulos publicos y otros instrumentos
        financieros.
        
        Es una serie mensual
        
        Base 2002M1
    
        Returns
        -------
        pd.DataFrame().
    
        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-cer-uva-uvi"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 0
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
    
    def getIndiceDeConfianzaDelConsumidor(self):
        """
        El índice de confianza del consumidor es un indicador económico que 
        mide el grado de optimismo que los consumidores sienten sobre la 
        evolución del estado en general de la economía, y sobre su situación 
        financiera personal.
    
        Returns
        -------
        pd.DataFrame()
    
        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-indice-confianza-consumidor"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        longitudResultado = len(resultado)-1
        ultimoResultado = resultado[longitudResultado]
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
    
    def getBaseMonetaria(self):
        """
        Como la inflacion tambien puede ser por un fenomeno monetario
        hay que ver la evolucion de la base monetaria.
        
        Esta serie es mensual.
    
        Returns
        -------
        pd.DataFrame().
    
        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-factores-explicacion-base-monetaria"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 0
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
    
    def getIndicePreciosInternosAlPorMayorBase2015(self):
        """
        La evolucion de los precios a los cuales productor o importador directo 
        vende los productos al mercado interno (excluyendo las exportaciones)
        por lo cual tiene incluido el IVA, impuestos internos, ITI y subsidios 
        sus componentes son:
            * Productos primarios 19.36%
            * Productos manufacturados y energia 73.35%
            * Productos importados 7.29%
            
        Esta serie es mensual.
        
        La base es: Dic-2015 = 100
    
        Returns
        -------
        pd.DataFrame().
    
        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-indice-precios-internos-basicos-al-por-mayor-dic-2015-100"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 0
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
    

    
objIndicadoresDePrecios = IndicadoresDePrecios()
df = IndicadoresDePrecios.getIndicePreciosInternosAlPorMayorBase2015("")
