import networkx as nx
from datetime import datetime, timedelta
import random

class TransactionAnalyzer:
    def __init__(self):
        self.graph = nx.DiGraph()
    
    def build_network_graph(self, wallet_address, depth=2):
        self.graph.clear()
        self._generate_transaction_network(wallet_address, depth)
        
        nodes = []
        edges = []
        
        for node in self.graph.nodes(data=True):
            nodes.append({
                'id': node[0],
                'label': node[0][:8] + '...',
                'type': node[1].get('type', 'unknown'),
                'volume': node[1].get('volume', 0),
                'suspicious': node[1].get('suspicious', False)
            })
        
        for edge in self.graph.edges(data=True):
            edges.append({
                'source': edge[0],
                'target': edge[1],
                'amount': edge[2].get('amount', 0),
                'timestamp': edge[2].get('timestamp', '')
            })
        
        centrality = nx.degree_centrality(self.graph)
        
        return {
            'nodes': nodes,
            'edges': edges,
            'centrality': centrality,
            'total_nodes': len(nodes),
            'total_edges': len(edges)
        }
    
    def _generate_transaction_network(self, root_address, depth, current_depth=0):
        if current_depth >= depth:
            return
        
        self.graph.add_node(root_address, 
                           type='target' if current_depth == 0 else 'wallet',
                           volume=random.randint(10000, 1000000),
                           suspicious=random.random() > 0.7)
        
        num_connections = random.randint(2, 5)
        for i in range(num_connections):
            connected_address = f"0x{random.randint(10000000, 99999999):08x}{random.randint(10000000, 99999999):08x}"
            
            if connected_address not in self.graph:
                self.graph.add_node(connected_address,
                                   type='mixer' if random.random() > 0.8 else 'wallet',
                                   volume=random.randint(5000, 500000),
                                   suspicious=random.random() > 0.6)
                
                self.graph.add_edge(root_address, connected_address,
                                   amount=random.randint(100, 50000),
                                   timestamp=self._random_timestamp())
                
                if current_depth < depth - 1:
                    self._generate_transaction_network(connected_address, depth, current_depth + 1)
    
    def _random_timestamp(self):
        days_ago = random.randint(0, 90)
        timestamp = datetime.now() - timedelta(days=days_ago)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    def analyze_timeline(self, wallet_address):
        timeline_data = []
        
        for i in range(20):
            days_ago = 90 - (i * 4)
            timestamp = datetime.now() - timedelta(days=days_ago)
            
            timeline_data.append({
                'date': timestamp.strftime('%Y-%m-%d'),
                'transaction_count': random.randint(1, 50),
                'volume': random.randint(1000, 100000),
                'mixer_detected': random.random() > 0.85,
                'risk_score': random.uniform(0, 1)
            })
        
        return sorted(timeline_data, key=lambda x: x['date'])
