#%%
import pandas as pd
import sqlalchemy

#%%
#SAMPLE

con = sqlalchemy.create_engine("sqlite:///../../../data/gc.db")
con.table_names()
df = pd.read_sql_table("tb_abt_sub", con)

""" BASE OF TIME - DESCOLADA FORA DO TEMPO DO TRINO
 NA COLUNA DTREF PEGUE OS DADOS ENTRE AS DATAS E COPIE 
 CRIAR UMA VARIAVEL TREINO COM OS DADOS ENTRE AS DATAS """

df_oot = df[df["dtRef"].isin(['2022-01-15', '2022-01-16'])].copy()
df_train = df[~df["dtRef"].isin(['2022-01-15', '2022-01-16'])].copy()

""" DEFINIR ALEATORIAMENTE UMA BASE DE TREINO E UMA DE TESTE """

""" for i in df_train.columns:
	print(i) """
features = df_train.columns.tolist()[2:-1]
target = 'flagSub'

