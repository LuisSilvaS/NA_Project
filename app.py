import streamlit as st
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyvis.network import Network
from metrics import generate_adjacency_matrix
from metrics import calculate_diameter
from metrics import plot_degree_distribution
from metrics import visualize_measures
from metrics import calculate_assortativity
#from metrics import strongly_connected
#from metrics import weakly_connected



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

# Diâmetro da Rede
if st.sidebar.button("Diâmetro da Rede"):
    st.write(f'Diâmetro da rede: {calculate_diameter(G)}')

# Histograma de Distribuição Empírica de Grau
if st.sidebar.button("Histograma de Distribuição Empírica de Grau"):
    st.write(plot_degree_distribution(G))

# Conectados Fortemente
#if st.sidebar.button("Conectados Fortemente"):
    #st.write(strongly_connected(G))

# Conectados Fracamente
#if st.sidebar.button("Conectados Fracamente"):
    #st.write(weakly_connected(G))

# Grafo com Medidas
# visualization centrality measures
if st.sidebar.button("Grafo com Medidas"):
    st.write("Nesse Grafo é possivel visualizar para todos os nós: Degree centrality, Closeness centrality, Betweenness centrality, Eigenvector centrality e o Coeficiente de clustering Local e Global,")
    st.write(visualize_measures(G))

# Assortatividade Geral da Rede
if st.sidebar.button("Assortatividade Geral da Rede"):
    st.write("Assortatividade Geral da Rede")
    st.write(calculate_assortativity(G))


st.write("By Luis Carlos Silva")