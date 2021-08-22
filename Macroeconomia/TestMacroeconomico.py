# # -*- coding: utf-8 -*-
import wbdata 
import pandas as pd                            
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

# #wbdata.get_country(300) # to see list of countries
# LAMcountries=['ARG','BLZ','BOL','BRA','CHL','COL','CRI','CUB','SLV','GTM','GUY','HTI','HND',
#           'JAM','MEX','NIC','PAN','PRY','PER','PRI','SUR','URY','VEN']
# NAMcountries=['USA','CAN']
# #regions=['LCN','WLD','NAC'] #WORLD = WLD; LAT AM AND CARRIBEAN = LCN; NAC=North America
# regions=['NAC','WLD','LCN']
# allcountries=LAMcountries+NAMcountries
# allregions=allcountries+regions

pais_seleccionado = 'ARG'
desde = "2006"
hasta = "2020"


#Obtener el nombre del pais
ctry = wbdata.get_country() #lista paises
for i in range(len(ctry)-1):
    val = ctry[i]
    if val['id'] == pais_seleccionado:
        nombrePais = val['name']
        break
# #listar topicos
# wbdata.get_topic()
# Origenes
# wbdata.get_source()
# #listar indicadores de un topico
# wbdata.get_indicator(topic=10)
# wbdata.get_indicator(source=2)


#PBI
#Esto midel el crecimiento desde la demanada
indicators={
        "NY.GDP.MKTP.CN": "PIBCorrienteBase2004",
        "NY.GDP.MKTP.KN": "PIBConstanteBase2004",
        "NY.GDP.PCAP.CN" : "PIBPerCapitaCorrienteBase2004",
        "NY.GDP.PCAP.KN":"PIBPerCapitaConstanteBase2004",
        "SP.POP.TOTL":"PoblacionTotal"} 


df=wbdata.get_dataframe(indicators,country=pais_seleccionado)
df = df.iloc[::-1]
df["PIBConstanteBase2004MM9"] = df["PIBConstanteBase2004"].rolling(window=9).mean()
df["PIBConstanteBase2004MM20"] = df["PIBConstanteBase2004"].rolling(window=20).mean()
df["PIBPerCapitaConstanteBase2004MM9"] = df["PIBPerCapitaConstanteBase2004"].rolling(window=9).mean()
df["PIBPerCapitaConstanteBase2004MM20"] = df["PIBPerCapitaConstanteBase2004"].rolling(window=20).mean()
df = df.loc[desde:hasta]


plt.figure(figsize=[8.4, 4.8])
plt.plot(df["PIBConstanteBase2004"], color='blue', \
         label= "PIB Constante")
plt.plot(df["PIBConstanteBase2004MM9"], color='red', \
         label= "Media movil 9")
plt.plot(df["PIBConstanteBase2004MM20"], color='green', \
         label= "Media movil 20")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Evolucion del PBI de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Valor Monetario")
plt.xlabel("Fechas")
plt.show()

#PBI Per Capita

plt.figure(figsize=[8.4, 4.8])
plt.plot(df["PIBPerCapitaConstanteBase2004"], color='blue', \
         label= "PIB Per Capita Constante")
plt.plot(df["PIBPerCapitaConstanteBase2004MM9"], color='red', \
         label= "Media movil 9")
plt.plot(df["PIBPerCapitaConstanteBase2004MM20"], color='green', \
         label= "Media movil 20")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("PBI Per capita de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Valor Monetario")
plt.xlabel("Fechas")
plt.show()

#YBI - Ingreso interno bruto
#Esto mide el crecimiento desde el punto de vista del ingreso
indicador={"NY.GDY.TOTL.KN": "IngresoInternoBrutoConstante", 
           "SP.POP.TOTL":"PoblacionTotal"}
df =wbdata.get_dataframe(indicador,country=pais_seleccionado)
df = df.iloc[::-1]
df["IngresoInternoBrutoConstantePerCapita"] = df["IngresoInternoBrutoConstante"]/df["PoblacionTotal"]
df["IngresoInternoBrutoConstantePerCapitaMM9"] = df["IngresoInternoBrutoConstantePerCapita"].rolling(window=9).mean()
df["IngresoInternoBrutoConstantePerCapitaMM20"] = df["IngresoInternoBrutoConstantePerCapita"].rolling(window=20).mean()
df = df.loc[desde:hasta]

plt.figure(figsize=[8.4, 4.8])
plt.plot(df["IngresoInternoBrutoConstantePerCapita"], color='blue', \
         label= "YIB Per Capita Constante")
plt.plot(df["IngresoInternoBrutoConstantePerCapitaMM9"], color='red', \
         label= "Media movil 9")
plt.plot(df["IngresoInternoBrutoConstantePerCapitaMM20"], color='green', \
         label= "Media movil 20")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("YIB Per capita de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Valor Monetario")
plt.xlabel("Fechas")
plt.show()

#PBI Oferta (per capita)
#Sumando los VAIB (valores agregados de ingresos brutos) tenemos el PBI Oferta
indicador={"SP.POP.TOTL":"PoblacionTotal",
           "NY.GDP.MKTP.KN": "PIBDemanda",
           "NV.IND.TOTL.KN" : "ValorAgregadoConstanteIndustrial",
           "NV.AGR.TOTL.KN": "ValorAgregadoConstanteAgro",
           "NV.SRV.TOTL.KN": "ValorAgregadoConstanteServicios" }
df =wbdata.get_dataframe(indicador,country=pais_seleccionado)
df = df.iloc[::-1]
df["PIBOferta"] = df["ValorAgregadoConstanteIndustrial"]+ df["ValorAgregadoConstanteAgro"]+df["ValorAgregadoConstanteServicios"]
df["PIBOfertaPC"] = df["PIBOferta"]/ df["PoblacionTotal"]
df["PIBOfertaPCMM9"] = df["PIBOfertaPC"].rolling(window=9).mean()
df["PIBOfertaPCMM20"] = df["PIBOfertaPC"].rolling(window=20).mean()
df = df.loc[desde:hasta]

plt.figure(figsize=[8.4, 4.8])
plt.plot(df["PIBOfertaPC"], color='blue', \
         label= "PIB Oferta Per Capita Constante")
plt.plot(df["PIBOfertaPCMM9"], color='red', \
         label= "Media movil 9")
plt.plot(df["PIBOfertaPCMM20"], color='green', \
         label= "Media movil 20")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("PIB Oferta Per capita de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Valor Monetario")
plt.xlabel("Fechas")
plt.show()

#PBI Oferta Vs PBI Demanda
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["PIBOferta"], color='blue', \
         label= "PIB Oferta Per Capita Constante")
plt.plot(df["PIBDemanda"], color='red', \
         label= "PIBD emanda")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("PBI Oferta Vs PBI Demanda de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Valor Monetario")
plt.xlabel("Fechas")
plt.show()

#Comparacion de los 3 VAIB
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["ValorAgregadoConstanteIndustrial"], color='blue', \
         label= "VAIB Industrial")
plt.plot(df["ValorAgregadoConstanteAgro"], color='red', \
         label= "VAIB Agro")
plt.plot(df["ValorAgregadoConstanteServicios"], color='green', \
         label= "VAIB Servicios")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Comparativa VAIB de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Valor Monetario")
plt.xlabel("Fechas")
plt.show()

#PRECIOS ---------------------

indicador={"FP.CPI.TOTL.ZG":"InflacionBienesPct",
           "NY.GDP.DEFL.KD.ZG" : "DeflactorPibPorc"}
df =wbdata.get_dataframe(indicador,country=pais_seleccionado)
df = df.iloc[::-1]
df.fillna(method="ffill", inplace=True)
df["IPCPorcentaje"] = df["InflacionBienesPct"]/100
df["DeflactorPorcentaje"] = df["DeflactorPibPorc"]/100
df = df.loc[desde:hasta]

plt.figure(figsize=[8.4, 4.8])
plt.plot(((1+df["IPCPorcentaje"]).cumprod()-1)*100, 
         color='red', 
         label= "IPC Nacional % Acumulado")
plt.plot(((1+df["DeflactorPorcentaje"]).cumprod()-1)*100, 
         color='blue', 
         label= "Deflactor PIB % Acumulado")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("IPC Consumo vs Deflactor PIB en % Acumulado de {}".format(nombrePais))
plt.ylabel("Porcentaje")
plt.xlabel("Fechas")
plt.show()

#EMPLEO Y Desocupacion -----------------------------------------------
indicador={"SL.TLF.CACT.NE.ZS": "TasaActividad",          #Labor force participation rate, total (% of total population ages 15+) (national estimate)
           "SL.TLF.ACTI.1524.NE.ZS":"TasaActividadSub25", #Labor force participation rate for ages 15-24, total (%) (national estimate)
           "SL.UEM.TOTL.NE.ZS" : "TasaDesocupados",       #Unemployment, total (% of total labor force) (national estimate)
           "SL.UEM.1524.NE.ZS" : "TasaDesocupadosSub25",  #Unemployment, youth total (% of total labor force ages 15-24) (national estimate)
           "SL.TLF.TOTL.IN" : "PEA",                      #Labor force, total
           "SP.POP.TOTL" : "PoblacionTotal",
           "SL.EMP.TOTL.SP.NE.ZS" : "TasaEmpleo"}         #Employment to population ratio, 15+, total  
df =wbdata.get_dataframe(indicador,country=pais_seleccionado)
df = df.iloc[::-1]
df.fillna(method="ffill", inplace=True)
df = df.loc[desde:hasta]

#evolucion de la pea
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["PEA"], color='blue', \
         label= "PEA")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Evolucion de la Poblacion Economicamente Activa \n de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Poblacion")
plt.xlabel("Fechas")
plt.show()

#evolucion de la pea vs poblacion total
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["TasaActividad"], color='blue', \
         label= "Tasa de Actividad (oferta laboral)")
plt.plot(df["TasaEmpleo"], color='orange', \
         label= "Tasa de Empleo (demanda laboral)")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Evolucion de la TasaActividad vs Tasa Empleo \n de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Poblacion")
plt.xlabel("Fechas")
plt.show()

#ocupacion
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["TasaActividad"], color='blue', \
         label= "Tasa de actividad")
plt.plot(df["TasaActividadSub25"], color='red', \
         label= "Tasa de actividad sub 25")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Tasa de Actividad de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Tasa")
plt.xlabel("Fechas")
plt.show()

#desocupados
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["TasaDesocupados"], color='blue', \
         label= "Tasa de desocupados")
plt.plot(df["TasaDesocupadosSub25"], color='red', \
         label= "Tasa desocupados sub 25")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Tasa de Desocupacion de {} datos del Banco Mundial".format(nombrePais))
plt.ylabel("Tasa")
plt.xlabel("Fechas")
plt.show()



# ---------------------------------------------------------------------------------
#                       MISMO ANALISIS VIA DATOS DEL INDEC
# ---------------------------------------------------------------------------------


# MACROECONOMIA - CRECIMIENTO 
from Macroeconomia.Argentina.IndicadoresDeCrecimiento import IndicadoresDeCrecimiento
from Macroeconomia.Argentina.IndicadoresEmpleoDesocupacion import IndicadoresEmpleoDesocupacion
from Macroeconomia.Argentina.IndicadoresDePrecios import IndicadoresDePrecios
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd 

#Configuracion
desde = dt.datetime.strptime("2006", '%Y').date()
hasta = dt.datetime.strptime("2022", '%Y').date()
objIndicadoresDeCrecimiento = IndicadoresDeCrecimiento()
objIndicadoresDePrecios = IndicadoresDePrecios()
objIndicadoresEmpleoDesocupacion = IndicadoresEmpleoDesocupacion()
objPBI = objIndicadoresDeCrecimiento.getPIB()

#PBI Per Capita
df = objPBI.getPreciosConstantesPerCapitaBase2004()
df["PBIPerCapitaPreciosConstantesBase2004MM9"] = df["PBIPerCapitaPreciosConstantesBase2004"].rolling(window=5).mean()

plt.figure(figsize=[8.4, 4.8])
plt.plot(df["PBIPerCapitaPreciosConstantesBase2004"], color='blue', \
         label= "PIB Per Capita Constante")
plt.plot(df["PBIPerCapitaPreciosConstantesBase2004MM9"], color='red', \
         label= "Media movil 5")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("PBI Per capita de Argentina (INDEC)")
plt.ylabel("Valor Monetario")
plt.xlabel("Fechas")
plt.show()

#EMAE
df = objIndicadoresDeCrecimiento.getEstimadorMensualDeActividad("Mensual")
df["EMAEDesestacionalizado4MM9"] = df["emae_desestacionalizada"].rolling(window=20).mean()
df = df.loc[desde:hasta]

plt.figure(figsize=[8.4, 4.8])
plt.plot(df["emae_desestacionalizada"], color='blue', \
         label= "EMAE Desestacionalizado")
plt.plot(df["EMAEDesestacionalizado4MM9"], color='red', \
         label= "Media movil 20")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Estimador Mensual de Actividad Economica (INDEC)")
plt.ylabel("Valor")
plt.xlabel("Fechas")
plt.show()

#IPI
df = objIndicadoresDeCrecimiento.getIndiceProduccionIndustrial()
df["IPIEDesestacionalizado4MM20"] = df["serie_desestacionalizada"].rolling(window=20).mean()
df = df.loc[desde:hasta]

plt.figure(figsize=[8.4, 4.8])
plt.plot(df["serie_desestacionalizada"], color='blue', \
         label= "IPI Desestacionalizado")
plt.plot(df["IPIEDesestacionalizado4MM20"], color='red', \
         label= "Media movil 20")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Indice de Produccion Industrial (INDEC)")
plt.ylabel("Valor")
plt.xlabel("Fechas")
plt.show()

#INDICADORES DE PRECIOS ---------------------------------------

#IPC Cordoba
dfc = objIndicadoresDePrecios.getIndicePreciosAlConsumidorCordobaBaseJulio2012()
dfc['IPC'] = dfc['nivel_general']
dfc['IPCPorcentaje'] = dfc['nivel_general'].pct_change()
dfc = dfc.loc[desde:hasta]

#Grafico IPC Cordoba
plt.figure(figsize=[8.4, 4.8])
plt.plot(dfc["IPC"], color='blue', label= "IPC Cordoba")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("IPC Cordoba")
plt.ylabel("Valor")
plt.xlabel("Fechas")
plt.show()

#IPC Nacion
df = objIndicadoresDePrecios.getIndicePreciosAlConsumidor()
df['IPC'] = df['ipc_ng_nacional']
df['IPC_GBA'] = df['ipc_ng_gba']
df['IPC_PAMP'] = df['ipc_ng_pampeana']
df['IPC_NEA'] = df['ipc_ng_nea']
df['IPC_NOA'] = df['ipc_ng_noa']
df['IPC_CUYO'] = df['ipc_ng_cuyo']
df['IPC_PATA'] = df['ipc_ng_cuyo']
df['IPCPorcentaje'] = df['ipc_ng_nacional'].pct_change()
df = df.loc[desde:hasta]

#Grafico IPC Nacion
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["IPC"], color='blue', label= "IPC Nacional")
plt.plot(df["IPC_GBA"], color='red', label= "IPC Gran BsAs")
plt.plot(df["IPC_PAMP"], color='pink', label= "IPC Pampeano")
plt.plot(df["IPC_NEA"], color='green', label= "IPC NEA")
plt.plot(df["IPC_NOA"], color='yellow', label= "IPC NOA")
plt.plot(df["IPC_CUYO"], color='black', label= "IPC Cuyo")
plt.plot(df["IPC_PATA"], color='orange', label= "IPC Patagonia")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("IPC Nacionl (INDEC)")
plt.ylabel("Valor")
plt.xlabel("Fechas")
plt.show()

#Grafico IPC Cordoba Porcentaje
plt.figure(figsize=[8.4, 4.8])
plt.plot((1+dfc["IPCPorcentaje"]).cumprod()-1, 
         color='red', 
         label= "IPC Cordoba % Acumulado")
plt.plot((1+df["IPCPorcentaje"]).cumprod()-1, 
         color='blue', 
         label= "IPC Nacional % Acumulado")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("IPC Cordoba vs Nacion en % Acumulado")
plt.ylabel("Porcentaje 1 = 100%")
plt.xlabel("Fechas")
plt.show()

df = objIndicadoresDePrecios.getIndiceDeConfianzaDelConsumidor()
df['IConfianzaConsumidor'] = df['icc_nacional']
df['IConfianzaConsumidorPorcentaje'] = df['icc_nacional'].pct_change()
df = df.loc[desde:hasta]

#Grafico ICConsumidor
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["IConfianzaConsumidor"], color='red', 
         label= "ICC")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Indice de confianza del consumidor (INDEC)")
plt.ylabel("Valor")
plt.xlabel("Fechas")
plt.show()

#DESOCUPACION / OCUPACION ----------------------------------------
df1 = objIndicadoresEmpleoDesocupacion.getTasaActividad().loc[desde:hasta]
df2 = objIndicadoresEmpleoDesocupacion.getTasaEmpleo().loc[desde:hasta]
df3 = objIndicadoresEmpleoDesocupacion.getTasaDesocupacion().loc[desde:hasta]
df = pd.DataFrame()
df['TasaActividad'] = df1['eph_continua_tasa_actividad_total']
df['TasaEmpleo'] = df2['eph_continua_tasa_empleo_total']
df['TasaDesempleo'] = df3['eph_continua_tasa_desempleo_total']

#evolucion de la pea vs poblacion total
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["TasaActividad"], color='blue', \
         label= "Tasa de Actividad (oferta laboral)")
plt.plot(df["TasaEmpleo"], color='orange', \
         label= "Tasa de Empleo (demanda laboral)")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Evolucion de la TasaActividad vs Tasa Empleo (INDEC)")
plt.ylabel("Tasa")
plt.xlabel("Fechas")
plt.show()

#desocupados
plt.figure(figsize=[8.4, 4.8])
plt.plot(df["TasaDesempleo"]*100, color='blue', \
         label= "Tasa de desocupacion")
plt.gcf().autofmt_xdate()
plt.legend(loc="upper left") #muestra las etiquetas
plt.title("Tasa de Desocupacion (INDEC)")
plt.ylabel("Tasa")
plt.xlabel("Fechas")
plt.show()


