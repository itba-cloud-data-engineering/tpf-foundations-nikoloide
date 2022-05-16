DROP TABLE if exists P_SALARIES.LK_FECHA cascade;
DROP TABLE if exists P_SALARIES.FT_SALARIOS_ACTIVIDAD cascade;
DROP TABLE if exists P_SALARIES.CLAES cascade;
DROP TABLE if exists P_SALARIES.IPC_MES cascade;
DROP TABLE if exists P_SALARIES.USD_MES cascade;

drop schema if exists P_SALARIES;
create schema P_SALARIES;

drop table if exists P_SALARIES.LK_FECHA; 
create table P_SALARIES.LK_FECHA (
    FECHA TEXT PRIMARY KEY,
    MONTH INT,
	DAY INT,
	YEAR INT,
	QUARTER INT
);


drop table if exists P_SALARIES.FT_SALARIOS_ACTIVIDAD; 
create table P_SALARIES.FT_SALARIOS_ACTIVIDAD (
    FECHA TEXT,
    CLAE6 SERIAL,
	W_MEDIAN DECIMAL(22,4)
);

drop table if exists P_SALARIES.CLAES; 
create table P_SALARIES.CLAES (
    CLAE6 SERIAL NOT NULL PRIMARY KEY,
    CLAE6_DESC TEXT,
	CLAE3 INT,
	CLAE3_DESC TEXT,
	CLAE2 INT,
	CLAE2_DESC TEXT,
	LETRA TEXT,
	LETRA_DESC TEXT
);



drop table if exists P_SALARIES.IPC_MES; 
create table P_SALARIES.IPC_MES (
    indice_tiempo  TEXT NOT NULL  PRIMARY KEY ,
    ipc_ng_nacional DECIMAL(18,1),
	ipc_ng_gba DECIMAL(18,1),
    ipc_ng_pampeana DECIMAL(18,1),
    ipc_ng_nea DECIMAL(18,1),
    ipc_ng_noa DECIMAL(18,1),
    ipc_ng_cuyo DECIMAL(18,1),
    ipc_ng_patagonia DECIMAL(18,1),
    ipc_ng_nacional_tasa_variacion_mensual DECIMAL(18,18),
    ipc_ng_gba_tasa_variacion_mensual DECIMAL(18,18),
    ipc_ng_pampeana_tasa_variacion_mensual DECIMAL(18,18),
    ipc_ng_nea_tasa_variacion_mensual DECIMAL(18,18),
    ipc_ng_noa_tasa_variacion_mensual DECIMAL(18,18),
    ipc_ng_cuyo_tasa_variacion_mensual DECIMAL(18,18),
    ipc_ng_patagonia_tasa_variacion_mensual DECIMAL(18,18),
    ipc_ng_nacional_tasa_variacion_acumulada_dic_ano_anterior DECIMAL(18,18),
    ipc_ng_gba_tasa_variacion_acumulada_dic_ano_anterior DECIMAL(18,18),
    ipc_ng_pampeana_tasa_variacion_acumulada_dic_ano_anterior DECIMAL(18,18),
    ipc_ng_nea_tasa_variacion_acumulada_dic_ano_anterior DECIMAL(18,18),
    ipc_ng_noa_tasa_variacion_acumulada_dic_ano_anterior DECIMAL(18,18),
    ipc_ng_cuyo_tasa_variacion_acumulada_dic_ano_anterior DECIMAL(18,18),
    ipc_ng_patagonia_tasa_variacion_acumulada_dic_ano_anterior DECIMAL(18,18)
);


drop table if exists P_SALARIES.USD_MES; 
create table P_SALARIES.USD_MES (
    indice_tiempo TEXT NOT NULL PRIMARY KEY ,
    dolar_tipo_unico DECIMAL(18,1),
	dolar_finan_esp_compra DECIMAL(18,4),
    dolar_finan_esp_venta DECIMAL(18,4),
    dolar_financiero_compra DECIMAL(18,4),
    dolar_financiero_venta DECIMAL(18,4),
    dolar_libre_compra DECIMAL(18,4),
    dolar_libre_venta DECIMAL(18,4),
    dolar_oficial_compra DECIMAL(18,4),
    dolar_oficial_venta DECIMAL(18,4),
    dolar_estadounidense DECIMAL(18,1),
    dolar_referencia_com_3500 DECIMAL(18,4)
);

alter table P_SALARIES.FT_SALARIOS_ACTIVIDAD add foreign key (CLAE6) REFERENCES P_SALARIES.CLAES(CLAE6);
alter table P_SALARIES.FT_SALARIOS_ACTIVIDAD add foreign key (FECHA) REFERENCES P_SALARIES.LK_FECHA(FECHA);
alter table P_SALARIES.IPC_MES add foreign key (indice_tiempo) REFERENCES P_SALARIES.LK_FECHA(FECHA);
alter table P_SALARIES.USD_MES add foreign key (indice_tiempo) REFERENCES P_SALARIES.LK_FECHA(FECHA);
