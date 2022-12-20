#%%
import os
import sqlalchemy
import pandas as pd
import datetime
from tqdm import tqdm

#%%
# FUNÇÃO PARA SELECIONAR O PERIODO DESEJADO, CRIANDO A DATA INICIO E FIM LENDO AS DATAS INPUTADAS...
# EM STRINGS E INTERPRETANDO

def dates_to_list(dt_start, dt_stop):
    date_start = datetime.datetime.strptime(dt_start, "%Y-%m-%d")
    date_stop = datetime.datetime.strptime(dt_stop, "%Y-%m-%d")
    days = (date_stop - date_start).days

    dates = [ (date_start+datetime.timedelta(i)).strftime("%Y-%m-%d") for i in range(days+1) ]


def backfill (query, engine, dt_start, dt_stop ):
    dates = dates_to_list(dt_start, dt_stop)
    for d in tqdm(dates):
        process_date(query, d, engine)

def import_query(path):
    with open(path, "r") as open_file:
        query = open_file.read()
    return query

def process_date(query, date, engine):
    delete = f"delete from tb_book_player where dtRef = '{date}'"
    engine.execute(delete)
    query = query.format(date = date)
    engine.execute(query)

#%%  

engine = sqlalchemy.create_engine("sqlite:///../data/gc.db")

query = import_query("query.sql")

dt_start = input("Entre com uma data de inicio: ")
dt_stop = input("Entre com uma data fim:")
backfill(query, engine, dt_start, dt_stop)

# %%
