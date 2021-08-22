#Funciones para operar sobre un dataframe de forma gener generica
import pandas as pd
import numpy as np
import datetime as dt
import copy
import logging
from urllib.request import urlopen
import json
from dateutil.relativedelta import relativedelta

#------------------------------------------------------------------------------
#                           INICIO DE LA CONFIGURACION
#------------------------------------------------------------------------------
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='(%(threadName)-10s) %(message)s'
# )


#------------------------------------------------------------------------------
#                             FIN DE LA CONFIGURACION
#------------------------------------------------------------------------------

def MultiplicarDataframe(DF,numero):
    """
    Descripción:
    -----------
    Multiplica un dataframe por un escalar
    La multiplicación solo se aplica a las columnas de tipo float64 o int64
    

    Parametros
    ----------
    df :  pandas dataframe, obligatorio
        Dataframe a ser multiplicado por un escalora
    numero : int, obligatorio
        Escalar por el que se van a multiplicar todas las columnas.

    Returns
    -------
    Dataframe con las columnas multiplicadas por el escalar.

    """
    df = DF.copy()
    for columna in df.columns:
        #solo mitiplico si el contenido es float o integer
        if(df[columna].dtype == np.float64 or df[columna].dtype == np.int64):
            #df[columna] = df[columna].apply(lambda x: x*numero) #version labda
            df.loc[:, columna] = df[columna] * numero
    return df

def DividirDataframe(DF,numero):
    """
    Descripción:
    -----------
    Divide un dataframe por un escalar
    La division solo se aplica a las columnas de tipo float64 o int64
    

    Parametros
    ----------
    df :  pandas dataframe, obligatorio
        Dataframe a ser multiplicado por un escalora
    numero : int, obligatorio
        Escalar por el que se van a dividir todas las columnas.

    Returns
    -------
    Dataframe con las columnas divididas por el escalar.

    """
    df = DF.copy()
    for columna in df.columns:
        #solo mitiplico si el contenido es float o integer
        if(df[columna].dtype == np.float64 or df[columna].dtype == np.int64):
            #df[columna] = df[columna].apply(lambda x: x*numero) #version labda
            df.loc[:, columna] = df[columna] / numero
    return df

def NormalizarSerie(SR):
    """
    Descripción:
    -----------
    Normaliza una serie basandose en maximo y minimo
    Haciendo que la misma se encuentre entre 0 y 1
    
    Un ejemplo de uso seria normalizar el DPO y operar 
    en 0.2 para la compra y 0.5 para la venta (estrategia comprado)
    

    Parametros
    ----------
    SR :  pandas serie, obligatorio
        Dataframe a ser multiplicado por un escalora
        
    Uso
    -------
    from DataframeUtils import NormalizarSerie \n
    df_stocks["GGAL"]["DPO_NORMALIZADO"] = NormalizarSerie(df_stocks["GGAL"]["DPO"])\n
    

    Returns
    -------
    Serie normalizada

    """
    sr = SR.copy()
    sr_norm =(sr - sr.min())/(sr.max()-sr.min()) 
    return sr_norm    

def DataframeDesde(DF,dias):
    """
    Descripción:
    -----------
    Retorna un dataframe desde cierta fecha en el pasado
    la fecha se calcula a partir de 'dias' es decir 365 sera un año

    Parametros
    ----------
    df :  pandas dataframe, obligatorio
        Dataframe debe tener un indice datetime
    dias : int, obligatorio
        Escalar que representa los dias a calcular la fecha

    Returns
    -------
    Dataframe con las filas desde la fecha calculada

    """
    df = DF.copy()
    df = df.reset_index()
    desde = df.iloc[-1,0] - pd.Timedelta(days=dias)
    hasta = dt.datetime.now()
    mask = (DF.index > desde) & (DF.index <= hasta)
    return DF.loc[mask]

def DataframeHasta(DF,dias):
    """
    Descripción:
    -----------
    Retorna un dataframe con la catidad de dias que se le pida

    Parametros
    ----------
    df :  pandas dataframe, obligatorio
        Dataframe debe tener un indice datetime
    dias : int, obligatorio
        Escalar que representa los dias a calcular la fecha

    Returns
    -------
    Dataframe con las filas desde la fecha calculada

    """
    df = copy.deepcopy(DF)
    df = df.reset_index()
    desde = df.iloc[0,0]
    hasta = df.iloc[0,0] + pd.Timedelta(days=dias)
    mask = (DF.index > desde) & (DF.index <= hasta)
    return DF.loc[mask]

def Log(cadena: str):
    """
    Descripcion
    -----------
    Permite imprimir datos en pantala o almacenarlas en
    un archivo, por default  sale por pantalla, ver el __init_.py de
    DataframeUtils para modificar la configuracion
    

    Parametros
    ----------
    cadena : str, obligatorio
        Cadena que saldra por pantalla

    """  
    logging.debug(cadena)
    
def GetParsedJSONData(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.
    Recibe una url y parsea el resultado como JSON retornando un objeto de tipo dic

    Parametros
    ----------
    url : str

    Retuorna
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def DicEliminarSobreMedia(dic,n_medias =1):
    """
    Descripción:
    -----------
    Recorre un diccionario de dataframes y elimina todos los
    dataframes cuya longitud sea mayor a N veces la media del diccionario
    
    Sirve para no contar con tickers que sean salgan mucho del rango
    medio alternando la performance general de la estrategia

    Parametros
    ----------
    dic : diccionario de pandas dataframe, obligatorio
        Diccionaroio con keys por tickers y dataframe debe tener un indice datetime
    n_medias : int, opcional
        Escalar que representa la cantidad de veces que se multiplicara
        la media a la hora de comparar, por defecto es 1

    Returns
    -------
    Dataframe con los tickers que superaron n veces la media eliminados

    """
    longitud = {}
    for ticker in dic:
        longitud[ticker] = len(dic[ticker].index)
    
    pd_longitud = pd.DataFrame()
    pd_longitud['longitud'] = pd.Series(longitud)
    media = pd_longitud['longitud'].mean()
    
    tickers_a_eliminar = []
    n_medias = 1 if n_medias == 0 else n_medias #no permitimos 0
    for ticker in dic:
        if len(dic[ticker].index) > media*n_medias: tickers_a_eliminar.append(ticker)
    
    return_dic = copy.deepcopy(dic)
    for ticker in tickers_a_eliminar:
        print("Se elimina el ticker {t} ya que supera {n} veces la media de {m}".format(t=ticker,m=media,n=n_medias))
        del return_dic[ticker]
    
    return return_dic

def SeleccionarDeDiccionario(dic,tickers):
    """
    Descripción:
    -----------
    Permite seleccionar ciertos tickers de un diccionario

    Parametros
    ----------
    dic : diccionario de pandas dataframe, obligatorio
        Diccionaroio con keys por tickers y dataframe debe tener un indice datetime
    tickers : [], opcional
        Lista de tickers que se desea seleccionar

    Returns
    -------
    Diccionario con los tickers seleccionados

    """    
    return {k:dic[k] for k in tickers if k in dic}

def ComprimirDataframe(df, periodo:str = 'A'):
    """
    Descripción:
    -----------
    Permite comprimir un dataframe en un marco temporal mas grande
    Tener en cuenta que el solicitado NO DEBE SER MENOR.

    Parametros
    ----------
    df : dataframe, obligatorio
        dataframe con una serie temporal como compresor
    periodo : str, opcional
        Representa al periodo a comprimir, por defecto es anual
        Los periodos son:
            * B: días hábiles
            * C: días hábiles personalizados
            * D: l día calendario
            * W: frecuencia semanal
            * M: fin de mes
            * SM: fin de mes semestral (15 y fin de mes)
            * BM: fin de mes comercial
            * CBM: fin de mes comercial personalizada
            * MS: inicio del mes
            * SMS: inicio semestral (1º y 15º)
            * BMS: inicio del mes laboral
            * CBMS:inicio del mes comercial personalizado
            * Q: cuarto de final
            * BQ: cierre del trimestre comercial
            * QS: inicio de un cuarto
            * BQS: inicio del trimestre comercial
            * A, Y: fin de año
            * BA, BY: fin de año comercial
            * AS, YS: inicio del año
            * BAS, BYS: inicio del año comercial
            * BH: horario comercial
            * H: hotas
            * T, min: minutos
            * S: segundos
            * L, ms: milisegundos
            * U, us: microsegundos
            * N: nanosegundos

    Returns
    -------
    Dataframe con los datos resampleados en un marco temporal mayor
    al pasado por parametro

    """ 
    df.reset_index(inplace= True)
    df =  df.groupby(pd.Grouper(key='Date',freq=periodo)).agg(\
                                {'Date': 'first',
                                'Open': 'first',
                                'High': 'max',
                                'Low': 'min',
                                'Close': 'last',
                                'Volume': sum })
    df.set_index('Date')
    return df

def ComprimirDiccionario(dic, periodo:str = 'A'):
    """
    Descripción:
    -----------
    Permite comprimir un diccionario con dataframes, cada
    dataframe debe estar en un marco temporal inferior al solicitado
    Tener en cuenta que el solicitado NO DEBE SER MENOR.

    Parametros
    ----------
    dic : diccionario de dataframe, obligatorio
        dataframe con series temporaless a ser comprimidas
    periodo : str, opcional
        Representa al periodo a comprimir, por defecto es anual
        Los periodos son:
            * B: días hábiles
            * C: días hábiles personalizados
            * D: l día calendario
            * W: frecuencia semanal
            * M: fin de mes
            * SM: fin de mes semestral (15 y fin de mes)
            * BM: fin de mes comercial
            * CBM: fin de mes comercial personalizada
            * MS: inicio del mes
            * SMS: inicio semestral (1º y 15º)
            * BMS: inicio del mes laboral
            * CBMS:inicio del mes comercial personalizado
            * Q: cuarto de final
            * BQ: cierre del trimestre comercial
            * QS: inicio de un cuarto
            * BQS: inicio del trimestre comercial
            * A, Y: fin de año
            * BA, BY: fin de año comercial
            * AS, YS: inicio del año
            * BAS, BYS: inicio del año comercial
            * BH: horario comercial
            * H: hotas
            * T, min: minutos
            * S: segundos
            * L, ms: milisegundos
            * U, us: microsegundos
            * N: nanosegundos

    Returns
    -------
    Diccionario con dataframes en un marco temporal mayor
    al pasado por parametro

    """ 
    for ticker in dic:
        dic[ticker] = ComprimirDataframe(dic[ticker], periodo)
    

def DataFrameDesdeFecha(df, fecha):
    """
    Esta funcion sirve para recortar un dataframe desde una fecha
    hasta la fecha actual.

    Parameters
    ----------
    df : dataframe, obligatorio
        dataframe con una serie temporal como index
    fecha : str o date, obligatorio
        fecha desde la cual se obtendra informacion, todos los
        registros antes de la misma seran eliminados

    Returns
    -------
    Dataframe con todos los registros desde la fecha original
    hasta la fecha actual

    """
    hoy = dt.datetime.now()
    #df.loc['2015-2-16':'2015-2-20']
    mask = (df.index > fecha) & (df.index <= hoy)
    return df.loc[mask]

def DataFrameRecortarAnos(df, anos:int = 1):
    """
    Esta funcion sirve para obtener un dataframe con los ultimos
    x años pasados por parametro, ejemplo: si años = 2 y el años es 
    2022 retornara un dataframe condatos desde el 2020
    
    Por defecto es 1.

    Parameters
    ----------
    df : dataframe, obligatorio
        dataframe con una serie temporal como index
    años : int, opcional
        candidad de años a los cuales remontara el punto de origen del
        dataframe

    Returns
    -------
    Dataframe con todos los registros desde x cantidad de años hacia
    atras. Retortna NaN si el tipo no es dataframe

    """
    hasta = dt.datetime.now()
    desde = hasta - relativedelta(years=anos)
    hasta_str = hasta.strftime("%Y-%m-%d")
    desde_str = desde.strftime("%Y-%m-%d")
    if isinstance(df, pd.DataFrame) == True :
        return df.query("'{}' < `index` < '{}' ".format(desde_str,hasta_str))
    else:
        return np.NaN

def DicRecortarAnos(dic, anos:int = 1):
    """
    Esta funcion sirve para obtener un diccionario de dataframe con los ultimos
    x años pasados por parametro, ejemplo: si años = 2 y el años es 
    2022 retornara un dataframe condatos desde el 2020
    
    Por defecto es 1.

    Parameters
    ----------
    dic : diccionario de dataframe, obligatorio
        diccionario de dataframes con serie temporal como index
    anos : int, opcional
        candidad de años a los cuales remontara el punto de origen del
        dataframe

    Returns
    -------
    Retorna un diccionario con todos los dataframes recortados x años
    hacia atras, si el tipo del registro no es dataframe el mismo sera 
    eliminado.

    """
    hasta = dt.datetime.now()
    desde = hasta - relativedelta(years=anos)
    hasta_str = hasta.strftime("%Y-%m-%d")
    desde_str = desde.strftime("%Y-%m-%d")
    nuevo_dic = {}
    for ticker in dic:
        if isinstance(dic[ticker], pd.DataFrame) == True :
            nuevo_dic[ticker] = dic[ticker].query("'{}' < `index` < '{}' ".format(desde_str,hasta_str))
    return nuevo_dic

def DicGetTickerFechaOHLC(dic : dict, ticker: str, fecha, exact = True):
    """
    Permite obtener el Open, High, Low, Close, Volume de una fecha especifica

    Parametros
    ----------
    dic : dict, obligatorio
        Diccionario de tickers que contiene dataframes ohlc.
    ticker : str o datetime, obligatorio
        Ticker que se encuentra en el diccionario.
    fecha : str, obligatorio
        Fecha en la que se buscaran los precios en formato Año-Mes-Dia
    exact : TYPE, opcional
        Indica si sera la fecha exacta o mas cercana . Por defecto es True.

    Retorna
    -------
    Una serie con los datos Open, High, Low, Close, Volume de una fecha especifica
    Eje:
        sr_fecha = DicGetTickerFechaOHLC(dic_merval,'PEP','2016-01-16',excact = False)
        print("Open el dia 16/01/2016: {}".format(sr_fecha['Open']))

    """
    #formateamos fecha si no es cadena
    if isinstance(fecha, str) == True:
        fecha_str = fecha
    else:
        fecha_str = fecha.strftime("%Y-%m-%d")
    #buscamos el id del ohlc
    if exact == False : 
        ohlc_fecha = dic[ticker].index.get_loc(fecha_str,method='nearest')
        return dic[ticker].iloc[ohlc_fecha]
    else:
        return dic[ticker].loc[fecha_str]
    
    
def ListaAnadirSinRepetir(primera_lista , segunda_lista):
    """
    Esta funcion permite unir listas sin que los elementos se repitan

    Parameters
    ----------
    primera_lista : [], obligatorio
        Lista con los primeros elements.
    segunda_lista : [], ogligatorio
        Lista con los segundos elementos.

    Returns
    -------
    []
        Lista unida sin que los elementos se repitan .

    """
    en_primera = set(primera_lista)
    en_segunda = set(segunda_lista)
    
    en_segunda_pero_no_en_primera = en_segunda - en_primera
    
    return primera_lista + list(en_segunda_pero_no_en_primera)
    
def DicDatetimePrimeraFecha(dic, fecha, dias):
    """
    Esta funcion permite obtener el primer registro que aparesca para una fecha
    dada entre n dias, por ejemplo: fecha=18-01-2021 dias=1 buscara el primer registro
    que encuentre entre el 17-01-2021 y el 19-01-2021
    
    SOLO FUNCIONA EN BASE DIARIA

    Parameters
    ----------
    dic : dictionary
        Diccionario de dataframes cuya llave es datetime.
    fecha : datetime, obligatorio
        Fecha a buscar.
    dias : int, obligatorio
        Dias +/- aproximados sobre los que buscar

    Returns
    -------
    Registro de un diccionario, puede ser dataframe o cualquier objeto.

    """
    desde = fecha - relativedelta(days=5)
    hasta = fecha + relativedelta(days=5)
    
    fechas = list(pd.date_range(start=desde, end=hasta)) #obtenemos fechas
    
    #convertimos a un formato comun
    fechas = [item.strftime('%Y-%m-%d') for item in fechas] 
    dic_keys = [item.strftime('%Y-%m-%d') for item in dic.keys()]

    for i in range(len(dic_keys)-1):
        
        if dic_keys[i] in fechas: 
            keys = list(dic.keys())
            return dic[keys[i]]