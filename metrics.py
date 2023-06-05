import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from pyvis.network import Network
import streamlit as st
import plotly.graph_objects as go

def generate_adjacency_matrix(G):
    adj_matrix = nx.to_numpy_array(G)
    return adj_matrix

def calculate_diameter(G):
    diameter = nx.diameter(G)
    periphery = nx.periphery(G)
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


    clustering_coeffs = nx.clustering(G)
    for node in selected_nodes:
        st.write(f"Node: {node}")
        if node in clustering_coeffs:
            st.write(f"Clustering Coefficient: {clustering_coeffs[node]}")
        else:
            st.write("Node not found in the graph.")

def local_clustering_coefficient(G):
    clustering_coeffs = nx.clustering(G)
    return clustering_coeffs

def strongly_connected_graph(G):
    st.subheader("Componentes Conectados Fortemente")
    strongly_connected = list(nx.connected_components(G.to_undirected()))

    # Create a subgraph with strongly connected components
    subgraph_nodes = [node for component in strongly_connected for node in component]
    subgraph = G.subgraph(subgraph_nodes)

    # Plot the subgraph
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.title("Connected Components")
    plt.axis('off')

    # Display the graph
    st.pyplot(plt.gcf())

    # Display the connected components
    st.write(strongly_connected)

def weakly_connected_graph(G):
    st.subheader("Componentes Conectados Fracamente")
    weakly_connected = list(nx.connected_components(G))

    # Create a subgraph with weakly connected components
    subgraph_nodes = [node for component in weakly_connected for node in component]
    subgraph = G.subgraph(subgraph_nodes)

    # Plot the subgraph
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.title("Weakly Connected Components")
    plt.axis('off')

    # Display the graph
    st.pyplot(plt.gcf())

    # Display the weakly connected components
    st.write(weakly_connected)

def visualize_centrality_measures(G):

    # Calculate centrality measures
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    eigenvector_centrality = nx.eigenvector_centrality(G)

    # Add centrality measures as node attributes
    nx.set_node_attributes(G, degree_centrality, "degree_centrality")
    nx.set_node_attributes(G, closeness_centrality, "closeness_centrality")
    nx.set_node_attributes(G, betweenness_centrality, "betweenness_centrality")
    nx.set_node_attributes(G, eigenvector_centrality, "eigenvector_centrality")

    # Create a pyvis network
    nt = Network(notebook=True)

    # Add nodes and edges to the network
    for node in G.nodes():
        nt.add_node(node, title=f"Degree Centrality: {degree_centrality[node]}\n"
                              f"Closeness Centrality: {closeness_centrality[node]}\n"
                              f"Betweenness Centrality: {betweenness_centrality[node]}\n"
                              f"Eigenvector Centrality: {eigenvector_centrality[node]}")

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