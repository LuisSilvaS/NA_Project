import networkx as nx
import matplotlib.pyplot as plt

def local_clustering_coefficient(G):
    clustering_coeffs = nx.clustering(G)
    return clustering_coeffs


def plot_clustering_coefficients(clustering_coeffs):
    nodes = list(clustering_coeffs.keys())
    coefficients = list(clustering_coeffs.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(nodes, coefficients)
    plt.xlabel("Node")
    plt.ylabel("Clustering Coefficient")
    plt.title("Local Clustering Coefficients")
    plt.show()


    import networkx as nx
from pyvis.network import Network
import streamlit as st

def visualize_centrality_measures(G):
    st.subheader("Medidas de Centralidade")
    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)
    clustering_coeffs = nx.clustering(G)  # Coeficiente de clusterização local

    # Add centrality measures as node attributes
    nx.set_node_attributes(G, degree_centrality, "degree_centrality")
    nx.set_node_attributes(G, closeness_centrality, "closeness_centrality")
    nx.set_node_attributes(G, betweenness_centrality, "betweenness_centrality")
    nx.set_node_attributes(G, eigenvector_centrality, "eigenvector_centrality")
    nx.set_node_attributes(G, clustering_coeffs, "clustering_coefficient")  # Atributo de clusterização local

    # Create a pyvis network
    nt = Network(notebook=True)

    # Add nodes and edges to the network
    for node in G.nodes():
        nt.add_node(node, title=f"Degree Centrality: {degree_centrality[node]}\n"
                              f"Closeness Centrality: {closeness_centrality[node]}\n"
                              f"Betweenness Centrality: {betweenness_centrality[node]}\n"
                              f"Eigenvector Centrality: {eigenvector_centrality[node]}\n"
                              f"Clustering Coefficient: {clustering_coeffs[node]}")  # Mostra o coeficiente de clusterização local

    for edge in G.edges():
        nt.add_edge(edge[0], edge[1])

    # Save the network as HTML file
    html_file = "centrality_measures.html"
    nt.show(html_file)

    # Display the graph using st.components.v1.html()
    with open(html_file, "r") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=500)

