import networkx as nx
import json

class GraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def add_wallet_node(self, address, node_type='wallet', **kwargs):
        self.graph.add_node(address, type=node_type, **kwargs)
    
    def add_transaction_edge(self, from_addr, to_addr, amount, **kwargs):
        self.graph.add_edge(from_addr, to_addr, amount=amount, **kwargs)
    
    def get_graph_data(self):
        return {
            'nodes': [{'id': node, **data} for node, data in self.graph.nodes(data=True)],
            'edges': [{'source': u, 'target': v, **data} for u, v, data in self.graph.edges(data=True)]
        }
    
    def calculate_centrality(self):
        return nx.degree_centrality(self.graph)
    
    def detect_communities(self):
        if len(self.graph.nodes()) > 0:
            undirected = self.graph.to_undirected()
            communities = list(nx.community.greedy_modularity_communities(undirected))
            return [list(community) for community in communities]
        return []
    
    def get_shortest_path(self, source, target):
        try:
            return nx.shortest_path(self.graph, source, target)
        except nx.NetworkXNoPath:
            return None
