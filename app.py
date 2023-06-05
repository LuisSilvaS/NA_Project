import streamlit as st
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyvis.network import Network
from metrics import generate_adjacency_matrix
from metrics import calculate_diameter
from metrics import plot_degree_distribution
from metrics import local_clustering_coefficient
from metrics import visualize_centrality_measures
from metrics import calculate_assortativity
from metrics import strongly_connected_graph
from metrics import weakly_connected_graph


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
st.write("DataSet: github.com/pupimvictor/NetworkOfThrones/blob/master/stormofswords.csv .")


# Exibir o grafo
st.subheader("Grafo")
viz_file = "html_files/network.html"
nt.show(viz_file)
with open(viz_file, "r") as f:
    html_content = f.read()
st.components.v1.html(html_content, height=500)

# Matriz de adjacência
if st.button("Matriz de adjacência"):
    st.write(generate_adjacency_matrix(G))

# Diâmetro da rede e periferia
if st.button("Diâmetro da Rede"):
    st.write(calculate_diameter(G))

# Histograma de distribuição empírica de grau
if st.button("Histograma de Distribuição Empírica de Grau"):
    st.write(plot_degree_distribution(G))

# Coeficiente de clustering local
if st.button("Coeficiente de Clustering Local"):
    st.write(local_clustering_coefficient(G))
    
# Componentes Conectados Fortemente
if st.button("Conectados Fortemente"):
    st.write(strongly_connected_graph(G)) 

#Componentes Conectados Fracamente
if st.button("Conectados Fracamente"):
    st.write(weakly_connected_graph(G))

# Medidas de Centralidade 
if st.button("Grafo com Medias de Centralidade"):
    st.write(visualize_centrality_measures(G))

# Assortatividade Geral da Rede
if st.button("Assortatividade Geral da Rede"):
    st.write(calculate_assortativity(G))

st.write("By Luis Carlos Silva")