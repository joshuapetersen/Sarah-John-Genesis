"""
SEMANTIC KNOWLEDGE GRAPH
Part of the Sarah Prime NeuralMesh Expansion.
Implements Evolution Roadmap Item #3: Connecting memories into a navigable web of logic.
"""

import networkx as nx
import numpy as np
import sys
import os
from typing import List, Dict, Any

# Ensure we can import our sibling modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from Semantic_Memory_Search import SemanticMemoryEngine
    from sklearn.metrics.pairwise import cosine_similarity
    DEPENDENCIES_MET = True
except ImportError:
    DEPENDENCIES_MET = False
    print("CRITICAL: Semantic Engine or sklearn not found. Knowledge Graph cannot be built.")

class KnowledgeGraphCore:
    """
    The Synaptic Web.
    Converts linear memory storage into a high-dimensional graph.
    """
    def __init__(self, db_path='genesis_core.db', similarity_threshold=0.6):
        self.graph = nx.Graph()
        self.threshold = similarity_threshold
        self.semantic_engine = None
        
        if DEPENDENCIES_MET:
            print("Initializing Semantic Knowledge Graph...")
            self.semantic_engine = SemanticMemoryEngine(db_path=db_path)
            self.build_graph()
        else:
            raise RuntimeError("Missing dependencies for Knowledge Graph.")

    def build_graph(self):
        """
        Construct the graph from semantic memories.
        Nodes = Memories
        Edges = Semantic Similarity > Threshold
        """
        memories = self.semantic_engine.memory_cache
        embeddings = self.semantic_engine.embeddings
        
        if not memories:
            print("No memories to graph.")
            return

        print(f"Building Knowledge Graph from {len(memories)} nodes...")
        
        # 1. Add Nodes
        for mem in memories:
            self.graph.add_node(
                mem['id'], 
                problem=mem['problem'], 
                tags=mem['tags'],
                type='memory'
            )
            
        # 2. Add Edges (Synapses)
        # Calculate similarity matrix
        sim_matrix = cosine_similarity(embeddings)
        np.fill_diagonal(sim_matrix, 0)
        
        edge_count = 0
        num_memories = len(memories)
        
        for i in range(num_memories):
            for j in range(i + 1, num_memories):
                score = sim_matrix[i][j]
                if score > self.threshold:
                    # Connect the nodes
                    id_i = memories[i]['id']
                    id_j = memories[j]['id']
                    self.graph.add_edge(id_i, id_j, weight=float(score))
                    edge_count += 1
                    
        print(f"Graph Constructed: {self.graph.number_of_nodes()} Nodes, {self.graph.number_of_edges()} Synapses.")

    def get_central_concepts(self, top_k=5):
        """
        Identify the most 'central' memories using PageRank.
        These are the core pillars of the system's knowledge.
        """
        if self.graph.number_of_nodes() == 0:
            return []
            
        pagerank = nx.pagerank(self.graph, weight='weight')
        sorted_nodes = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for node_id, score in sorted_nodes:
            node_data = self.graph.nodes[node_id]
            results.append({
                'id': node_id,
                'problem': node_data.get('problem', 'Unknown'),
                'importance': score
            })
        return results

    def find_connection(self, start_id, end_id):
        """
        Find the semantic path between two memories.
        "How did I get from A to B?"
        """
        try:
            path = nx.shortest_path(self.graph, source=start_id, target=end_id, weight='weight')
            return path
        except nx.NetworkXNoPath:
            return None

    def get_graph_stats(self):
        """Return vital statistics of the knowledge graph."""
        return {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'connected_components': nx.number_connected_components(self.graph)
        }

if __name__ == "__main__":
    kg = KnowledgeGraphCore()
    
    print("\n--- KNOWLEDGE GRAPH ANALYSIS ---")
    stats = kg.get_graph_stats()
    print(f"Nodes: {stats['nodes']}")
    print(f"Synapses: {stats['edges']}")
    print(f"Network Density: {stats['density']:.4f}")
    
    print("\n--- CORE CONCEPTS (PageRank) ---")
    core = kg.get_central_concepts()
    for c in core:
        print(f"[{c['importance']:.4f}] ID {c['id']}: {c['problem']}")
