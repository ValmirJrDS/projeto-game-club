# %%
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt

from sklearn import model_selection
from sklearn import ensemble
from sklearn import tree
from sklearn import linear_model



from sklearn import pipeline
from sklearn import metrics


from feature_engine import imputation
from feature_engine import encoding

import scikitplot as skplt


pd.set_option('display.max_columns', None)

# %%
""" # SAMPLE - Criar conexão com BD, criar variavel out off time de BD para treino e teste e
#criar nossa base de treino e teste """
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

""" EXPLORE - PARTE EXPLORATORIA - Muito importe que a partir de agora iremos usar
#somente o X_train, primeiro separamos e depois avaliamos, esquece o dado original, """

# %%
X_train.head()
# %%
""" Separar feature categórica e numericas em lugares diferentes - Um SET() é uma coleção de itens
únicos """

cat_features = X_train.dtypes[X_train.dtypes == "object"].index.tolist()
num_features = list(set(X_train.columns) - set(cat_features))

"""Verificar nas features numericas se possuem missing """

print("Missing numerico")
is_na = X_train[num_features].isna().sum()
print(is_na[is_na > 0])

missing_0 = ["avgKDA", ]

missing_1 = ["winRateTrain",
             "winRateNuke",
             "winRateInferno",
             "winRateAncient",
             "winRateDust2",
             "winRateMirage",
             "winRateOverpass",
             "vlIdade",
             "winRateVertigo", ]

# %%
print("Missing numerico")
is_na = X_train[num_features].isna().sum()
print(is_na[is_na > 0])
# %%

"""MODIFY - Definindo um objeto que ira fazer um imputação arbitraria em algumas variaves
no dataset

Imputação de Dados """

input_0 = imputation.ArbitraryNumberImputer(
    arbitrary_number=0, variables=missing_0)
input_1 = imputation.ArbitraryNumberImputer(
    arbitrary_number=-1, variables=missing_1)

""" One Hot Encoding """

onehot = encoding.OneHotEncoder(drop_last=True, variables=cat_features)

""" MODELOS - TUNNING """

""" Random Forest """

rf_clf = ensemble.RandomForestClassifier(n_estimators=200,
					 min_samples_leaf=50,
					 n_jobs=-1,
					 random_state=42)
									

""" Ada Boost """

ada_clf = ensemble.AdaBoostClassifier(n_estimators = 200,
				      learning_rate = 0.8,
				      random_state = 42)

""" Arvore de Decisão """

dt_clf = tree.DecisionTreeClassifier(max_depth = 15,
				     min_samples_leaf=50,
			       	     random_state = 42)

""" Regressão Logistica """

rl_clf = linear_model.LogisticRegressionCV(cv=4, n_jobs=-1)

""" Definir o Pipeline - Juntar todas as transformações em um único objeto

Depois dos testes o Random Forest se saiu melhor, iremos comentar os outros

na origem do código e Tunnar o Random."""

""" Pipeline Random Forest """

""" GridSearchCV """
params = {"n_estimators":[50,100,150,200],
		  "min_samples_leaf": [5,10,20,50] }

grid_search = model_selection.GridSearchCV(rf_clf, params,n_jobs=1, cv=4,scoring='roc_auc',verbose=3,refit=True)

pipe_rf = pipeline.Pipeline(steps = [("Imput 0", input_0),
                                     ("Imput -1", input_1),
                                     ("One Hot", onehot),
                                     ("Modelo", grid_search)])
# %%
""" Funçao responsavel para realizar o treinamento do Modelo o que faz 
o usuario assinar nos proximos 15dd usando as estatisticas dos ulimos 30dd"""

def train_test_report( model, X_train, y_train, X_test, y_test, key_metric, is_prob=True):
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)
    metric_result = key_metric(y_test, prob[:,1]) if is_prob else key_metric(y_test, pred)
    return metric_result
#%%
""" For para treinar todos os algoritimos. Após o treino o Random Forest se saiu melhor
"""

""" for d,m in models.items():
	result = train_test_report(m, X_train, y_train, X_test, y_test, metrics.roc_auc_score)
	print(f"{d}: {result}") """

#%%
# TREINAR O MODELO - Tunar o modelo Random Forest

pipe_rf.fit(X_train, y_train)
# %%
""" Verificar Qual o melhor Modelo """

pd.DataFrame(grid_search.cv_results_).sort_values(by="rank_test_score")


#%%
# METRICAS

# Escorar o Modelo
y_train_pred = pipe_rf.predict(X_train)
y_train_prob = pipe_rf.predict_proba(X_train)

# Medir o Modelo
acc_train = round(100*metrics.accuracy_score(y_train, y_train_pred), 2)
roc_train = metrics.roc_auc_score(y_train, y_train_prob[:, 1])

print("acc_train", acc_train)
print("roc_train", roc_train)

# %%

print("Base Line: ", round((1-y_train.mean())*100, 2))
print("Acuracia: ", acc_train)
# %%
# TESTAR O MODELO
 
y_test_pred = pipe_rf.predict(X_test)
y_test_prob = pipe_rf.predict_proba(X_test)

# Medir o Modelo
acc_test = round(100*metrics.accuracy_score(y_test, y_test_pred), 2)
roc_test = metrics.roc_auc_score(y_test, y_test_prob[:, 1])

print("Base Line: ", round((1-y_test.mean())*100, 2))
print("acc_test", acc_test)
print("roc_test", roc_test)
#%%

skplt.metrics.plot_roc(y_train, y_train_prob)
plt.show()
# %%
skplt.metrics.plot_ks_statistic(y_train, y_train_prob)
plt.show()
# %%
skplt.metrics.plot_precision_recall(y_train, y_train_prob)
plt.show()
# %%
""" Melhor grafico, pois ele mostra quantas vezes mais a porcentagem de quem vai assinar 
	realmente assinar """
skplt.metrics.plot_lift_curve(y_train, y_train_prob)
plt.show()


# %%

skplt.metrics.plot_roc(y_test, y_test_prob)
plt.show()

# %%

""" A métrica do KS Statistic te sugeri o ponto de corte na 
	probabilidade para separar, nesse caso, quem vai assinar ou não
	onde esta mostrando 0.10 """
skplt.metrics.plot_ks_statistic(y_test, y_test_prob)
plt.show()

# %%

skplt.metrics.plot_precision_recall(y_test, y_test_prob)
plt.show()

# %%

""" Melhor grafico, pois ele mostra quantas vezes mais a porcentagem de quem vai assinar 
	realmente assinar """
skplt.metrics.plot_lift_curve(y_test, y_test_prob)
plt.show()

# %%
skplt.metrics.plot_cumulative_gain(y_test, y_test_prob)
plt.show()

""" Nesse Grafico de Ganho Acumulativo consigo verificar
que 15% da Base já tenho todos que seriam assinates """
# %%

""" Com o modelo testado verificando a Base OOT(out off time),
ou Base Fora do Tempo """

X_oot, y_oot = df_oot[features], df_oot[target]

y_prob_oot = pipe_rf.predict_proba(X_oot)

roc_oot = metrics.roc_auc_score(y_oot, y_prob_oot[:,1] )
print("roc_train", roc_oot)

#%%
""" Metricas da Base Fora do Tempo(OOT) """

skplt.metrics.plot_roc(y_oot, y_prob_oot)
plt.show()
#%%

skplt.metrics.plot_lift_curve(y_oot, y_prob_oot)
plt.show()

# %%
skplt.metrics.plot_cumulative_gain(y_oot, y_prob_oot)
plt.show()

""" Agora na Curva de Ganho para chegar a 100% tenho que abordar 
40%, mais se pegar 20% pegando 88% de assinantes não está ruim. Se perceber
10% da Base sobe 80% de assinantes, metrica muito boa """

# %%
