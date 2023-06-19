import streamlit as st
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gzip
from pyvis.network import Network
import seaborn as sns
from metrics import generate_adjacency_matrix
from metrics import calculate_diameter
from metrics import plot_degree_distribution
from metrics import visualize_measures
from metrics import calculate_assortativity
from metrics import measures_heatmap
from metrics import calcular_componentes_fortemente_conectados
from metrics import calcular_componentes_fracamente_conectados

# Carregar os dados da rede a partir do arquivo CSV
got_data = pd.read_csv("data/stormofswords.csv")

# Criar um objeto NetworkX a partir dos dados
G = nx.from_pandas_edgelist(got_data, 'Source', 'Target')

# Criar um objeto Network do pyvis a partir do objeto NetworkX
nt = Network(notebook=True)
nt.from_nx(G)

# Configurar o layout da visualização
nt.barnes_hut()

# Criar o aplicativo Streamlit
st.title("Rede de Game of Thrones")
st.write("Análise de redes em Game of Thrones.")
st.sidebar.title("Introdução")
if st.sidebar.button("DataFrame"):
    st.write(got_data)

if st.sidebar.button("História dos Dados"):
    st.write("A base de dados em questão apresenta uma estrutura composta por três colunas: Source (fonte), Target (alvo) e Weight (peso), podemos analisar as informações disponíveis a fim de compreender o contexto. Com base no diâmetro da rede, que é igual a 6, e no valor de assortatividade geral de -0.13076253169826765, é possível inferir algumas características relevantes acerca da rede. O diâmetro da rede se refere à distância máxima entre quaisquer dois nós presentes na rede. No caso dessa base de dados, o diâmetro igual a 6 indica que o caminho mais longo entre quaisquer duas entidades conectadas possui seis conexões. Já a assortatividade geral da rede, cujo valor é negativo (-0.13076253169826765), sugere que a rede tem uma tendência a conectar nós com características distintas. Isso significa que entidades portadoras de atributos específicos têm maior probabilidade de se conectar a outras entidades que possuam atributos diferentes, em vez de se agruparem com base em características semelhantes. Essa diversidade nas conexões pode indicar a existência de diversos tipos de relacionamentos ou interações entre as entidades representadas pelos nós.")

# Exibir o grafo
st.subheader("Grafo")
viz_file = "html_files/network.html"
nt.show(viz_file)
with open(viz_file, "r") as f:
    html_content = f.read()
st.components.v1.html(html_content, height=500)

# Definindo a barra lateral
st.sidebar.title("Métricas")

# Matriz de adjacência
if st.sidebar.button("Matriz de adjacência"):
    st.write("Matriz de adjacência")
    st.write(generate_adjacency_matrix(G))

# Histograma de Distribuição Empírica de Grau
if st.sidebar.button("Histograma de DEG"):
    st.write(plot_degree_distribution(G))

#Conectados Fortemente
if st.sidebar.button("Conectados Fortemente"):
    st.write(calcular_componentes_fortemente_conectados(G), figsize=(28, 24), title='componentes fortemente conectados:')

#Conectados Fracamente
if st.sidebar.button("Conectados Fracamente"):
    st.write(calcular_componentes_fracamente_conectados(G), figsize=(28, 24), title='componentes fracamente conectados')

# Grafo com Medidas
if st.sidebar.button("Grafo com Medidas"):
    st.write("Nesse Grafo é possivel visualizar para todos os nós: Degree centrality, Closeness centrality, Betweenness centrality, Eigenvector centrality e o Coeficiente de clustering Local e Global onde é possivel visualizar a distribuição de cada medida nos Nós")
    st.write(visualize_measures(G))

#heatmap
#if st.sidebar.button("Grafo heatmap"):
st.subheader("Medidas de Centralidade")
st.write("Nesse Grafo é possivel visualizar para todos os nós: Degree centrality, Closeness centrality, Betweenness centrality, Eigenvector centrality e o Coeficiente de clustering Local e Global, represntados em forma de heatmap")
measures_heatmap(G)

# Diâmetro da Rede
st.write(f'Diâmetro da rede: {calculate_diameter(G)}')

# Assortatividade Geral da Rede
st.write("Assortatividade Geral da Rede")
st.write(calculate_assortativity(G))

st.write("By Luis Carlos Silva")