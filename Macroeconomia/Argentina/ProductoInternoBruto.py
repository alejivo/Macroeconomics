import pandas as pd
import io
import requests
import json
import wbdata 

class ProductoInternoBruto:
    
    def __init__(self):
        pass
    
    def getPreciosCorrientesBase2004(self, periodo = "Anual"):
        """
        El PIB es el valor total de bienes y servicios FINALES producidos en
        un pais durante un periodo de tiempo determinado.
        
        Este PBI se encuentra calculado a precios de mercado lo que significa
        que incluye impuestos y subsidios.
        
        Este PIB toma los precios de bienes y servicios del año que se esta
        calculando ejemplo: el PIB Corriente el 2020 toma los precios del 2020
        
        Este tipo de PBI no es bueno para comparar, si se lo divide por el
        "Indice de Precios Implicitos" o "Deflactor del PBI" se obtiene el
        PBIPreciosConstantes
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual" o "Trimestral")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame()

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-producto-interno-bruto-precios-mercado-precios-corrientes-base-2004"
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
    
    def getPreciosCorrientesBase1996(self, periodo = "Anual"):
        """
        El PIB es el valor total de bienes y servicios FINALES producidos en
        un pais durante un periodo de tiempo determinado.
        
        Este PBI se encuentra calculado a precios de mercado lo que significa
        que incluye impuestos y subsidios.
        
        Este PIB toma los precios de bienes y servicios del año que se esta
        calculando ejemplo: el PIB Corriente en el 2020 toma los precios del 2020
        
        Este tipo de PBI no es bueno para comparar, si se lo divide por el
        "Indice de Precios Implicitos" o "Deflactor del PBI" se obtiene el
        PBIPreciosConstantes
        
        Contine datos desde 1996 hasta el 2012
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual" o "Trimestral")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame()

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-producto-interno-bruto-precios-mercado-precios-corrientes-base-1993"
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
    
    def getPreciosConstantesPerCapitaBase2004(self):
        """
        El PIB es el valor total de bienes y servicios FINALES producidos en
        un pais durante un periodo de tiempo determinado.
        
        Este PBI se encuentra calculado a precios de mercado lo que significa
        que incluye impuestos y subsidios.
        
        Este PIB toma los precios de bienes y servicios de un año base
        manteniendo los precios constantes de forma que solo impacten las
        variaciones en las cantidades.
        
        ES EL MEJOR INDICADOR DE EVOLUCION ECONOMICA.
        
        Se toma como base el año 2004 = 100
        
        Ejemplo: el PIB Corriente el 2020 toma los precios del 2004
        
        Solo es anual la poblacion es extraida del banco mundial

        Returns
        -------
        pd.DataFrame()

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-producto-interno-bruto-precios-mercado-precios-constantes-base-2004"
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
        df_temp['date'] = df_temp['indice_tiempo'].dt.date
        #set index
        df_temp.set_index('date', inplace=True)
        
        #traigo la poblacion
        indicators={"SP.POP.TOTL":"PoblacionTotal"}
        df_poblacion = wbdata.get_dataframe(indicators,country=['ARG'])
        df_poblacion = df_poblacion.iloc[::-1] #doy vuelta
        df_poblacion.reset_index(inplace=True) #reseto el indice
        df_poblacion['date'] = pd.to_datetime(df_poblacion['date'], format='%Y', errors='ignore') #formateo fecha
        df_poblacion.fillna(method='ffill', inplace = True) # relleno nulos
        df_poblacion['date'] = df_poblacion['date'].dt.date #transformo a fecha sin hora
        df_poblacion.set_index('date', inplace=True) #seteo el indice
        desde = df_temp.index[0]
        hasta = df_temp.index[-1]
        df_poblacion = df_poblacion.loc[desde : hasta]
        
        
        
        df_retornar = pd.DataFrame()
        df_retornar['PBIPreciosConstantesBase2004'] = df_temp['producto_interno_bruto_precios_mercado']*1000000 #ya que esta en millones
        df_retornar['PoblacionTotal'] = df_poblacion['PoblacionTotal']
        df_retornar['PBIPerCapitaPreciosConstantesBase2004'] = df_retornar['PBIPreciosConstantesBase2004']/df_poblacion['PoblacionTotal']
        
        return df_retornar
    
    def getPreciosConstantesBase2004(self, periodo = "Anual"):
        """
        El PIB es el valor total de bienes y servicios FINALES producidos en
        un pais durante un periodo de tiempo determinado.
        
        Este PBI se encuentra calculado a precios de mercado lo que significa
        que incluye impuestos y subsidios.
        
        Este PIB toma los precios de bienes y servicios de un año base
        manteniendo los precios constantes de forma que solo impacten las
        variaciones en las cantidades.
        
        ES EL MEJOR INDICADOR DE EVOLUCION ECONOMICA.
        
        Se toma como base el año 2004 = 100
        
        Ejemplo: el PIB Corriente el 2020 toma los precios del 2004
        
        Parameters
        ----------
        periodo : str, optional (puede ser "Anual" o "Trimestral")
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        pd.DataFrame()

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-producto-interno-bruto-precios-mercado-precios-constantes-base-2004"
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
    
    def getIndicePreciosImplicitosBase2004(self, periodo = "Anual"):
        """
        

        Parameters
        ----------
        periodo : TYPE, optional
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        None.

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-indice-precios-implicitos-producto-interno-bruto-ipi---pib-base-2004"
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
        TYPE
            DESCRIPTION.

        """
        return self.getIndicePreciosImplicitosBase2004(periodo)
    
    def getValorAgregadoBrutoCorrientesBase2004(self, periodo = "Anual"):
        """
        Retorna el Valor Agregado Bruto es todo lo que la empresa agrega a los
        insumos para fabricar un bien final (eje: horas hombre, uso de bienes
                                             de capital)
        
        Valor Agregado Bruto a precios básicos por rama de actividad económica 
        en millones de pesos a precios corrientes. Base 2004
        

        Parameters
        ----------
        periodo : TYPE, optional
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        None.

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-valor-agregado-bruto-precios-basicos-por-rama-actividad-economica"
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
    
    def getIngresoBrutoInternoCorrientesBase2004(self, periodo = "Anual"):
        """
        El Ingreso Bruto Interno (YIB) es el total de las retribuciones obtenidas
        por los factores de la produccion dentro del pais por su contribucion
        al proceso productivo.
        
        Dados que los componentes del YIB son las retribuciones a los factores
        de produccion y el VAIB es la retribucion a los factores pagados podemos
        decir que VAIB = YIB
        
        Debido a que el API no retorna el YIB se retorna el VAB

        Parameters
        ----------
        periodo : TYPE, optional
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        None.

        """
        return self.getValorAgregadoBrutoCorrienteBase2004(periodo)
    
    def getValorAgregadoBrutoConstanteBase2004(self, periodo = "Anual"):
        """
        Retorna el Valor Agregado Bruto es todo lo que la empresa agrega a los
        insumos para fabricar un bien final (eje: horas hombre, uso de bienes
                                             de capital)
        
        Valor Agregado Bruto a precios básicos por rama de actividad económica 
        en millones de pesos a precios constantes. Base 2004
        

        Parameters
        ----------
        periodo : TYPE, optional
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        None.

        """
        #Obtener la url de descarga del cvs
        urlPackage="https://datos.gob.ar/api/3/action/package_show?id=sspm-valor-agregado-bruto-precios-basicos-por-rama-actividad-economica"
        s=requests.get(urlPackage).content
        objJson = json.loads(s)
        resultado = objJson['result']['resources']
        selector = 5 if periodo == 'Trimestral' else 4 #si no es trimestral siempre es anual
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
    
    def getIngresoBrutoInternoConstanteBase2004(self, periodo = "Anual"):
        """
        El Ingreso Bruto Interno (YIB) es el total de las retribuciones obtenidas
        por los factores de la produccion dentro del pais por su contribucion
        al proceso productivo.
        
        Dados que los componentes del YIB son las retribuciones a los factores
        de produccion y el VAIB es la retribucion a los factores pagados podemos
        decir que VAIB = YIB
        
        CONOCIDO COMO PBI "DESDE EL INGRESO"
        
        Debido a que el API no retorna el YIB se retorna el VAB

        Parameters
        ----------
        periodo : TYPE, optional
            DESCRIPTION. The default is "Anual".

        Returns
        -------
        None.

        """
        return self.getValorAgregadoBrutoCorrienteBase2004(periodo)
    


