#%%
import pandas as pd
import sqlalchemy

from sklearn import model_selection
from sklearn import ensemble
from sklearn import pipeline
from sklearn import metrics


from feature_engine import imputation
from feature_engine import encoding


pd.set_option('display.max_columns', None)

#%%
#SAMPLE - Criar conexão com BD, criar variavel out off time de BD para treino e teste e 
#		  criar nossa base de treino e teste
""" Conexão com o dataset final """
con = sqlalchemy.create_engine("sqlite:///../../../data/gc.db")
con.table_names()
df = pd.read_sql_table("tb_abt_sub", con)

"""BAck teste - base deslocada fora da principal
 1- variavel out of time onde uso isin para selecionar o periodo e criar uma cópia
 2- váriavel train onde tambem uso o metodo isin para coletar o periodo e crio uma cópia  """

df_oot = df[df["dtRef"].isin(['2022-01-15', '2022-01-16'])].copy()
df_train = df[~df["dtRef"].isin(['2022-01-15', '2022-01-16'])].copy()

""" Definir aleatoriamente uma base de treino e teste """

""" for i in df_train.columns:
	print(i) """
features = df_train.columns.tolist()[2:-1]
target = 'flagSub'
# %%
""" Criar Base de Treino e Teste """
X_train, X_test, y_train, y_test = model_selection.train_test_split(df_train[features],
																	df_train[target],
																	random_state=42,
																	test_size=0.2)
																	
""" X_train.count() / df_train.count() """

# EXPLORE - PARTE EXPLORATORIA - Muito importe que a partir de agora iremos usar
#								 somente o X_train, primeiro separamos e depois
#								 avaliamos, esquece o dado original, 

#%%
X_train.head()
# %%
#Separar feature categorica e numericas em lugares diferentes - Um SET() é uma coleção de itens 
# únicos

cat_features = X_train.dtypes[X_train.dtypes=="object"].index.tolist()
num_features = list(set(X_train.columns) - set(cat_features))

# Verificar nas features numericas se possue missing
print("Missing numerico")
is_na = X_train[num_features].isna().sum()
print(is_na[is_na>0])

missing_0 = ["avgKDA",]

missing_1 = ["winRateTrain",   
			 "winRateNuke",     
			 "winRateInferno", 
			 "winRateAncient", 
			 "winRateDust2",   
			 "winRateMirage",  
			 "winRateOverpass",
			 "vlIdade",        
			 "winRateVertigo", ]

#%%
print("Missing numerico")
is_na = X_train[num_features].isna().sum()
print(is_na[is_na>0])
# %% 

#MODIFY - Definindo um objeto que ira fazer um imputação arbritaria em algumas variaves 
##		  no dataset

## Imputação de Dados
input_0 = imputation.ArbitraryNumberImputer(arbitrary_number=0, variables=missing_0)
input_1 = imputation.ArbitraryNumberImputer(arbitrary_number=-1, variables=missing_1)

## One Hot Encoding
onehot = encoding.OneHotEncoder(drop_last=True, variables=cat_features)

## MODELO

model = ensemble.RandomForestClassifier(n_estimators=200, min_samples_leaf=50, n_jobs=-1)

# Definir o Pipeline - Juntar todas as transformações em um único objeto

model_pipe = pipeline.Pipeline(steps = [("Imput 0", input_0),
									     ("Imput -1", input_1),
									     ("One Hot", onehot),
									     ("Modelo", model)])
										 
# %%
##TREINAR O MODELO

model_pipe.fit(X_train, y_train)
# %%
## METRICAS

### Escorar o Modelo
y_train_pred = model_pipe.predict(X_train)
y_train_prob = model_pipe.predict_proba(X_train)

### Medir o Modelo
acc_train = round(100*metrics.accuracy_score(y_train, y_train_pred),2)
roc_train = metrics.roc_auc_score(y_train, y_train_prob[:,1] )

print("acc_train", acc_train)
print("roc_train", roc_train)

#%%

print("Base Line: ",round((1-y_train.mean())*100,2))
print("Acuracia: ", acc_train)
# %%
