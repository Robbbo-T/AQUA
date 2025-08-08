#!/usr/bin/env python3
"""
Graph Builder for INS-01 Strategic Network
Document ID: AQUART-INDUSTRY-SUPL-CODE-INS01-graph_builder-v1.0
Classification: CONFIDENTIAL
"""

import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Optional
import json

class SupplyChainGraphBuilder:
    """
    Constructs supply chain network graphs with multiobj weights
    for QAOA Max-Cut optimization
    """
    
    def __init__(self):
        """Initialize graph builder"""
        self.node_types = {
            'supplier': {'risk_base': 0.2, 'cost_multiplier': 1.0},
            'manufacturer': {'risk_base': 0.3, 'cost_multiplier': 1.2},
            'distributor': {'risk_base': 0.15, 'cost_multiplier': 0.8},
            'retailer': {'risk_base': 0.1, 'cost_multiplier': 0.9}
        }
    
    def create_sample_network(self, 
                             num_nodes: int = 8,
                             connectivity: float = 0.4,
                             seed: int = 42) -> Tuple[List[Dict], List[Tuple], Dict[str, Dict]]:
        """
        Create a sample supply chain network
        
        Args:
            num_nodes: Number of network nodes
            connectivity: Network connectivity ratio
            seed: Random seed for reproducibility
        
        Returns:
            Tuple of (nodes, edges, weights)
        """
        np.random.seed(seed)
        
        # Generate nodes
        nodes = self._generate_nodes(num_nodes)
        
        # Generate edges with connectivity constraint
        edges = self._generate_edges(nodes, connectivity)
        
        # Generate weights for multiobj optimization
        weights = self._generate_weights(edges)
        
        return nodes, edges, weights
    
    def _generate_nodes(self, num_nodes: int) -> List[Dict]:
        """Generate supply chain nodes with attributes"""
        nodes = []
        node_types = list(self.node_types.keys())
        
        for i in range(num_nodes):
            node_type = np.random.choice(node_types)
            type_config = self.node_types[node_type]
            
            node = {
                'id': i,
                'attributes': {
                    'type': node_type,
                    'risk': type_config['risk_base'] + np.random.normal(0, 0.05),
                    'capacity': np.random.uniform(50, 200),
                    'location': {
                        'lat': np.random.uniform(-90, 90),
                        'lon': np.random.uniform(-180, 180)
                    },
                    'certifications': np.random.choice(['ISO9001', 'ISO14001', 'ISO45001']),
                    'esg_score': np.random.uniform(60, 95)
                }
            }
            nodes.append(node)
        
        return nodes
    
    def _generate_edges(self, nodes: List[Dict], connectivity: float) -> List[Tuple]:
        """Generate network edges based on connectivity ratio"""
        edges = []
        num_nodes = len(nodes)
        max_edges = num_nodes * (num_nodes - 1) // 2
        num_edges = int(max_edges * connectivity)
        
        # Ensure minimum spanning tree connectivity
        mst_edges = self._generate_mst(nodes)
        edges.extend(mst_edges)
        
        # Add additional edges for specified connectivity
        remaining_edges = num_edges - len(mst_edges)
        additional_edges = self._generate_additional_edges(nodes, mst_edges, remaining_edges)
        edges.extend(additional_edges)
        
        return edges
    
    def _generate_mst(self, nodes: List[Dict]) -> List[Tuple]:
        """Generate minimum spanning tree to ensure connectivity"""
        edges = []
        connected = {0}  # Start with node 0
        
        while len(connected) < len(nodes):
            min_distance = float('inf')
            best_edge = None
            
            for i in connected:
                for j in range(len(nodes)):
                    if j not in connected:
                        distance = self._calculate_distance(
                            nodes[i]['attributes']['location'],
                            nodes[j]['attributes']['location']
                        )
                        if distance < min_distance:
                            min_distance = distance
                            best_edge = (i, j)
            
            if best_edge:
                edges.append(best_edge)
                connected.add(best_edge[1])
        
        return edges
    
    def _generate_additional_edges(self, nodes: List[Dict], 
                                  existing_edges: List[Tuple],
                                  num_additional: int) -> List[Tuple]:
        """Generate additional edges beyond MST"""
        additional_edges = []
        existing_set = set(existing_edges)
        
        candidates = []
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                if (i, j) not in existing_set and (j, i) not in existing_set:
                    distance = self._calculate_distance(
                        nodes[i]['attributes']['location'],
                        nodes[j]['attributes']['location']
                    )
                    candidates.append(((i, j), distance))
        
        # Sort by distance and select closest edges
        candidates.sort(key=lambda x: x[1])
        for i in range(min(num_additional, len(candidates))):
            additional_edges.append(candidates[i][0])
        
        return additional_edges
    
    def _calculate_distance(self, loc1: Dict, loc2: Dict) -> float:
        """Calculate geographic distance between locations"""
        lat1, lon1 = np.radians(loc1['lat']), np.radians(loc1['lon'])
        lat2, lon2 = np.radians(loc2['lat']), np.radians(loc2['lon'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        # Earth radius in km
        r = 6371
        return r * c
    
    def _generate_weights(self, edges: List[Tuple]) -> Dict[str, Dict]:
        """Generate multiobj weights for edges"""
        weights = {
            'cost': {},
            'risk': {},
            'co2': {}
        }
        
        for i, j in edges:
            # Base weights with some randomness
            base_cost = np.random.uniform(50, 200)
            base_risk = np.random.uniform(0.1, 0.5)
            base_co2 = np.random.uniform(20, 100)
            
            # Store weights for both directions
            weights['cost'][(i, j)] = base_cost
            weights['cost'][(j, i)] = base_cost
            
            weights['risk'][(i, j)] = base_risk
            weights['risk'][(j, i)] = base_risk
            
            weights['co2'][(i, j)] = base_co2
            weights['co2'][(j, i)] = base_co2
        
        return weights
    
    def load_from_json(self, filepath: str) -> Tuple[List[Dict], List[Tuple], Dict[str, Dict]]:
        """
        Load network from JSON file
        
        Args:
            filepath: Path to JSON file
        
        Returns:
            Tuple of (nodes, edges, weights)
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        nodes = data['nodes']
        edges = [tuple(edge) for edge in data['edges']]
        weights = data['weights']
        
        return nodes, edges, weights
    
    def save_to_json(self, 
                     nodes: List[Dict],
                     edges: List[Tuple],
                     weights: Dict[str, Dict],
                     filepath: str) -> None:
        """
        Save network to JSON file
        
        Args:
            nodes: Network nodes
            edges: Network edges  
            weights: Edge weights
            filepath: Output file path
        """
        data = {
            'nodes': nodes,
            'edges': edges,
            'weights': weights,
            'metadata': {
                'num_nodes': len(nodes),
                'num_edges': len(edges),
                'connectivity': len(edges) / (len(nodes) * (len(nodes) - 1) / 2),
                'generator': 'INS-01 Graph Builder v1.0'
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def visualize_network(self, 
                         nodes: List[Dict],
                         edges: List[Tuple],
                         partition: Optional[Tuple[set, set]] = None) -> str:
        """
        Generate network visualization HTML
        
        Args:
            nodes: Network nodes
            edges: Network edges
            partition: Optional partition for coloring
        
        Returns:
            HTML string for visualization
        """
        # Create NetworkX graph for layout
        G = nx.Graph()
        for node in nodes:
            G.add_node(node['id'], **node['attributes'])
        
        for i, j in edges:
            G.add_edge(i, j)
        
        # Calculate layout
        pos = nx.spring_layout(G, seed=42)
        
        # Generate HTML
        html = self._generate_html_visualization(nodes, edges, pos, partition)
        
        return html
    
    def _generate_html_visualization(self,
                                   nodes: List[Dict],
                                   edges: List[Tuple],
                                   pos: Dict,
                                   partition: Optional[Tuple[set, set]]) -> str:
        """Generate HTML visualization code"""
        
        # Node colors based on partition
        node_colors = {}
        if partition:
            for node_id in partition[0]:
                node_colors[node_id] = '#ff6b6b'  # Red for partition 0
            for node_id in partition[1]:
                node_colors[node_id] = '#4ecdc4'  # Teal for partition 1
        else:
            for node in nodes:
                node_colors[node['id']] = '#95a5a6'  # Gray default
        
        html = '''
<!DOCTYPE html>
<html>
<head>
    <title>INS-01 Strategic Network Visualization</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .node { stroke: #fff; stroke-width: 2px; }
        .link { stroke: #999; stroke-opacity: 0.6; stroke-width: 2px; }
        .node-label { font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <h1>INS-01 Strategic Network</h1>
    <svg width="800" height="600"></svg>
    
    <script>
        const nodes = ''' + json.dumps([{
            'id': n['id'],
            'type': n['attributes']['type'],
            'x': pos[n['id']][0] * 300 + 400,
            'y': pos[n['id']][1] * 200 + 300,
            'color': node_colors[n['id']]
        } for n in nodes]) + ''';
        
        const links = ''' + json.dumps([{
            'source': edge[0],
            'target': edge[1]
        } for edge in edges]) + ''';
        
        const svg = d3.select("svg");
        
        // Draw links
        svg.selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("class", "link")
            .attr("x1", d => nodes.find(n => n.id === d.source).x)
            .attr("y1", d => nodes.find(n => n.id === d.source).y)
            .attr("x2", d => nodes.find(n => n.id === d.target).x)
            .attr("y2", d => nodes.find(n => n.id === d.target).y);
        
        // Draw nodes
        svg.selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("class", "node")
            .attr("cx", d => d.x)
            .attr("cy", d => d.y)
            .attr("r", 15)
            .attr("fill", d => d.color);
        
        // Add labels
        svg.selectAll("text")
            .data(nodes)
            .enter().append("text")
            .attr("class", "node-label")
            .attr("x", d => d.x)
            .attr("y", d => d.y + 5)
            .attr("text-anchor", "middle")
            .text(d => d.id + " (" + d.type.substring(0,3) + ")");
    </script>
</body>
</html>'''
        
        return html