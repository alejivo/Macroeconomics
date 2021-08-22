# -*- coding: utf-8 -*-
import pandas as pd
import io
import requests
import json
import webbrowser
from Macroeconomia.Argentina.ProductoInternoBruto import ProductoInternoBruto

class IndicadoresDeCrecimiento:
    
    __PIB = ProductoInternoBruto()
    
    def __init__(self):
        pass
    
    
    def getPIB(self):
        return self.__PIB
    
    def getInformeDeAvanceDeNivelDeActividad(self):
        """
        Es un informe que emite el INDEC con informacion basica con retraso de
        tres meses en ellos se encontrara con base 2004:
            * Estimador del PBI
            * Informes globales
            * Inversion bruta y fija
            * Estimacion del PBI a precios corrientes
            * Indice de precios implicitos

        """
        print("Debe buscar el informe en la página del INDEC")
        webbrowser.open('https://www.indec.gob.ar/indec/web/Institucional-Indec-InformesTecnicos', new=2)
        
        
    def getEstimadorMensualDeActividad(self, periodo = "Anual"):
        """
        Es un anticipo mensual muy provisorio de la variacion del PBI trimestral
        con un rezago de 2 meses, es un estimador muy parcial por lo que con cada 
        informe de actividad se ajusta
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual", "Trimestral", "Mensual")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-estimador-mensual-actividad-economica-emae-base-2004"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        if periodo == 'Mensual': 
            selector = 2
        elif periodo == 'Trimestral': 
            selector = 1
        else:
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
        
    def getIndiceProduccionIndustrial(self):
        """
        Es un indicador de coyuntura que mide la evolucion del la produccion
        en terminos fisicos (se basa en encuestas a camaras y organismos)
        
        Es un indice mensual

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-indice-produccion-industrial-manufacturero-ipi"
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
    
    def getEstadisticasServiciosPublicos(self, periodo = "Anual"):
        """
        Indicador de evolucion mensual del consumo global de servicios publicos 
        en volumen fisico con base a 2004.
        Esta conformado por:
            * Electricidad y agua 39.6%
            * Transporte de pasajeros 29.3
            * Transporte de cargas 4,1%
            * Peajes 4.4%
            * Telefonia (incluye movil) 22.6%
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual", "Mensual", "Semanal")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-estadisticas-servicios-publicos"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        if periodo == 'Semanal': 
            selector = 2
        elif periodo == 'Mensual': 
            selector = 1
        else:
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
    
    def getVentasTotalesAutoservicios(self):
        """
        Ventas totales en autoservicios mayoristas a valores corrientes y 
        constantes y evolución por canal de venta, medio de pago y grupos de 
        artículos
        
        Los datos de la serie son mensuales.

        Returns
        -------
        pd.DataFrame().

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-ventas-autoservicios-mayoristas"
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
    