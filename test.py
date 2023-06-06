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