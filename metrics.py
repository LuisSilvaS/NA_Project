import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from pyvis.network import Network
import streamlit as st
import plotly.graph_objects as go
import seaborn as sns
import gzip

def generate_adjacency_matrix(G):
    adj_matrix = nx.to_numpy_array(G)
    return adj_matrix

def calculate_diameter(G):
    diameter = nx.diameter(G)
    return diameter

def plot_degree_distribution(G):
    degrees = [G.degree(node) for node in G.nodes()]
    hist, bins = np.histogram(degrees, bins=10, density=True)

    fig = go.Figure(
        data=[go.Bar(x=bins[:-1], y=hist, marker_color='lightblue', marker_line_color='gray')],
        layout=go.Layout(
            title="Histograma de Distribuição Empírica de Grau",
            xaxis=dict(title="Grau"),
            yaxis=dict(title="Densidade"),
            bargap=0.1
        )
    )
    st.plotly_chart(fig)

def visualize_measures(G):
    st.subheader("Medidas de Centralidade")
    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)
    clustering_coefficient = nx.average_clustering(G)  # Coeficiente de clusterização global
    clustering_coeffs = nx.clustering(G)  # Coeficiente de clusterização local

    # Add centrality measures as node attributes
    nx.set_node_attributes(G, degree_centrality, "degree_centrality")
    nx.set_node_attributes(G, closeness_centrality, "closeness_centrality")
    nx.set_node_attributes(G, betweenness_centrality, "betweenness_centrality")
    nx.set_node_attributes(G, eigenvector_centrality, "eigenvector_centrality")
    nx.set_node_attributes(G, clustering_coefficient, "clustering_coefficient")  # Atributo de clusterização global
    nx.set_node_attributes(G, clustering_coeffs, "clustering_coefficients")  # Atributo de clusterização local

    # Create a pyvis network
    nt = Network(notebook=True)

    # Add nodes and edges to the network
    for node in G.nodes():
        nt.add_node(node, title=f"Degree Centrality: {degree_centrality[node]}\n"
                              f"Closeness Centrality: {closeness_centrality[node]}\n"
                              f"Betweenness Centrality: {betweenness_centrality[node]}\n"
                              f"Eigenvector Centrality: {eigenvector_centrality[node]}\n"
                              f"Clustering Coefficient: {clustering_coefficient}\n"
                              f"Local Clustering Coefficient: {clustering_coeffs[node]}")  # Mostra os coeficientes de clusterização global e local

    for edge in G.edges():
        nt.add_edge(edge[0], edge[1])

    # Save the network as HTML file
    html_file = "centrality_measures.html"
    nt.show(html_file)

    # Display the graph using st.components.v1.html()
    with open(html_file, "r") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=500)

def calculate_assortativity(G):
    assortativity = nx.degree_assortativity_coefficient(G)
    st.write(assortativity)

def measures_heatmap(G):
    st.write("Selecione a medida de centralidade:")

    centrality_measures = {
        "Degree Centrality": nx.degree_centrality,
        "Closeness Centrality": nx.closeness_centrality,
        "Betweenness Centrality": nx.betweenness_centrality,
        "Eigenvector Centrality": nx.eigenvector_centrality,
        "Clustering Coefficient": nx.clustering
    }

    selected_measure = st.selectbox("Medida de Centralidade", list(centrality_measures.keys()))

    # Calculate selected centrality measure
    measure_function = centrality_measures[selected_measure]
    centrality = measure_function(G)

    # Create a list of centralities for each node
    centralities = [centrality.get(node, 0) for node in G.nodes()]

    # Create a colormap for the centralities
    cmap = plt.cm.get_cmap("hot")
    norm = plt.Normalize(vmin=min(centralities), vmax=max(centralities))

    # Create a list of colors for each node based on centrality
    node_colors = [cmap(norm(c)) for c in centralities]

    # Diminuir a escala do grafo
    pos = nx.random_layout(G)

    # Ajustar parâmetros da figura e do plano de fundo
    fig, ax = plt.subplots(figsize=(32, 28), dpi=150, facecolor='#D6EAF8')  # Define a cor azul clara como plano de fundo

    node_sizes = [200, 300, 150]  # Lista de tamanhos dos nós

    # Desenhar o grafo com as novas configurações
    nx.draw_networkx(G, pos, node_color=node_colors, cmap=cmap, with_labels=True, ax=ax, font_weight='bold', font_color='blue', font_size=16)

    # Function to handle mouse movement event
    def hover(event):
        if event.inaxes == ax:
            for node in G.nodes():
                x, y = pos[node]
                if x - 0.05 <= event.xdata <= x + 0.05 and y - 0.05 <= event.ydata <= y + 0.05:
                    ax.annotate(node, xy=(x, y), xytext=(5, 5), textcoords="offset points", fontsize=10, color="blue", fontweight="bold")
                else:
                    ax.annotate("", xy=(x, y), xytext=(5, 5), textcoords="offset points", fontsize=10, color="blue", fontweight="bold")

            fig.canvas.draw_idle()

    # Connect the hover function to the mouse movement event
    fig.canvas.mpl_connect("motion_notify_event", hover)

    # Create a colorbar for the centralities
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # An empty array is required for the colorbar to work
    plt.colorbar(sm)
    
    # Mostrar o gráfico com a nova escala
    plt.title(selected_measure)
    plt.axis("off")
    st.pyplot(fig)

def calcular_componentes_fortemente_conectados(G, figsize=(28, 24), title=''):
    # Verificar se o grafo é direcionado
    if not nx.is_directed(G):
        # Converter o grafo em um digrafo
        G = nx.DiGraph(G)

    # Calcula os componentes fortemente conectados
    componentes = list(nx.strongly_connected_components(G))

    # Mostra o número de componentes e os nós em cada componente
    #st.write("Número de componentes fortemente conectados:", len(componentes))
    for i, componente in enumerate(componentes):
        #st.write(f"Componente {i+1}: {componente}")

        # Cria um subgrafo apenas com os nós do componente atual
        subgrafo = G.subgraph(componente)

        # Calcula a posição dos nós
        pos = nx.spring_layout(subgrafo)

        # Cria a figura com o tamanho especificado
        fig, ax = plt.subplots(figsize=figsize)

        # Desenha o subgrafo sem rótulos nos nós
        nx.draw(subgrafo, pos=pos, with_labels=False, ax=ax)

        # Adiciona os rótulos ao lado dos nós
        labels = {node: node for node in subgrafo.nodes}
        nx.draw_networkx_labels(subgrafo, pos, labels=labels, font_color='black', ax=ax, font_weight='bold')

        # Define o título do gráfico
        ax.set_title(title)

        # Exibe o gráfico no Streamlit
        st.pyplot(fig)

def calcular_componentes_fracamente_conectados(G, figsize=(28, 24), title=''):
    # Verificar se o grafo é direcionado
    if not nx.is_directed(G):
        # Converter o grafo em um digrafo
        G = nx.DiGraph(G)

    # Calcula os componentes fracamente conectados
    componentes = list(nx.weakly_connected_components(G))

    # Mostra o número de componentes e os nós em cada componente
    #st.write("Número de componentes fracamente conectados:", len(componentes))
    for i, componente in enumerate(componentes):
        #st.write(f"Componente {i+1}: {componente}")

        # Cria um subgrafo apenas com os nós do componente atual
        subgrafo = G.subgraph(componente)

        # Calcula a posição dos nós
        pos = nx.spring_layout(subgrafo)

        # Cria a figura com o tamanho especificado
        fig, ax = plt.subplots(figsize=figsize)

        # Desenha o subgrafo sem rótulos nos nós
        nx.draw(subgrafo, pos=pos, with_labels=False, ax=ax)

        # Adiciona os rótulos ao lado dos nós
        labels = {node: node for node in subgrafo.nodes}
        nx.draw_networkx_labels(subgrafo, pos, labels=labels, font_color='black', ax=ax, font_weight='bold')

        # Define o título do gráfico
        ax.set_title(title)

        # Exibe o gráfico no Streamlit
        st.pyplot(fig)

        