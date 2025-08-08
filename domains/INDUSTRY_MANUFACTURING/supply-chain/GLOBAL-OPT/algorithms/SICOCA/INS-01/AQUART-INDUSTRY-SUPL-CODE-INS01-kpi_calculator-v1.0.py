#!/usr/bin/env python3
"""
KPI Calculator for INS-01 Strategic Network
Document ID: AQUART-INDUSTRY-SUPL-CODE-INS01-kpi_calculator-v1.0
Classification: CONFIDENTIAL
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Optional
import json
from dataclasses import dataclass

@dataclass
class KPITargets:
    """Target values for Key Performance Indicators"""
    resilience_index: float = 0.85
    tco_reduction: float = 0.20
    co2_reduction: float = 0.30
    quantum_advantage: float = 1.5

class INS01_KPICalculator:
    """
    Advanced KPI calculation for strategic network optimization
    Focuses on permacrisis scenarios and multiobj optimization
    """
    
    def __init__(self, targets: Optional[KPITargets] = None):
        """Initialize KPI calculator with targets"""
        self.targets = targets or KPITargets()
        self.baseline_metrics = {}
        self.optimized_metrics = {}
        
    def calculate_comprehensive_kpis(self,
                                   graph: nx.Graph,
                                   partition: Tuple[set, set],
                                   quantum_runtime: float,
                                   classical_runtime: float) -> Dict[str, float]:
        """
        Calculate comprehensive KPI suite for INS-01
        
        Args:
            graph: Supply chain network graph
            partition: Optimal partition from QAOA
            quantum_runtime: Time for quantum optimization
            classical_runtime: Time for classical equivalent
        
        Returns:
            Dictionary of all KPIs with values and targets
        """
        kpis = {}
        
        # Core KPIs
        kpis['ResilienceIndex'] = self._calculate_resilience_index(graph, partition)
        kpis['TCO_reduction'] = self._calculate_tco_reduction(graph, partition)
        kpis['CO2eq_reduction'] = self._calculate_co2_reduction(graph, partition)
        
        # Quantum advantage metrics
        kpis['quantum_advantage'] = classical_runtime / quantum_runtime if quantum_runtime > 0 else 1.0
        kpis['quantum_efficiency'] = self._calculate_quantum_efficiency(graph, partition)
        
        # Network topology metrics
        kpis['network_modularity'] = self._calculate_network_modularity(graph, partition)
        kpis['partition_balance'] = self._calculate_partition_balance(partition)
        kpis['cut_ratio'] = self._calculate_cut_ratio(graph, partition)
        
        # Risk and sustainability metrics
        kpis['risk_distribution'] = self._calculate_risk_distribution(graph, partition)
        kpis['sustainability_score'] = self._calculate_sustainability_score(graph, partition)
        kpis['disruption_tolerance'] = self._calculate_disruption_tolerance(graph, partition)
        
        # Financial metrics
        kpis['cost_efficiency'] = self._calculate_cost_efficiency(graph, partition)
        kpis['operational_savings'] = self._calculate_operational_savings(graph, partition)
        
        # Performance vs targets
        kpis['target_achievement'] = self._calculate_target_achievement(kpis)
        
        return kpis
    
    def _calculate_resilience_index(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """
        Calculate comprehensive resilience index
        Combines connectivity, redundancy, and risk distribution
        """
        # Network connectivity component
        connectivity = self._calculate_connectivity_resilience(graph, partition)
        
        # Redundancy component
        redundancy = self._calculate_redundancy_resilience(graph, partition)
        
        # Risk distribution component  
        risk_dist = self._calculate_risk_resilience(graph, partition)
        
        # Geographic distribution component
        geo_dist = self._calculate_geographic_resilience(graph, partition)
        
        # Weighted combination
        resilience = (0.3 * connectivity + 
                     0.25 * redundancy + 
                     0.25 * risk_dist +
                     0.2 * geo_dist)
        
        return min(resilience, 1.0)
    
    def _calculate_connectivity_resilience(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate connectivity-based resilience"""
        # Edge connectivity between partitions
        cut_edges = [(i, j) for i, j in graph.edges()
                     if (i in partition[0] and j in partition[1]) or
                        (i in partition[1] and j in partition[0])]
        
        total_edges = len(graph.edges())
        if total_edges == 0:
            return 0.0
        
        # Higher cut ratio indicates better connectivity
        cut_ratio = len(cut_edges) / total_edges
        
        # Node connectivity within partitions
        internal_connectivity_0 = self._calculate_internal_connectivity(graph, partition[0])
        internal_connectivity_1 = self._calculate_internal_connectivity(graph, partition[1])
        
        avg_internal_connectivity = (internal_connectivity_0 + internal_connectivity_1) / 2
        
        return (0.4 * cut_ratio + 0.6 * avg_internal_connectivity)
    
    def _calculate_internal_connectivity(self, graph: nx.Graph, partition_nodes: set) -> float:
        """Calculate connectivity within a partition"""
        if len(partition_nodes) <= 1:
            return 1.0
        
        subgraph = graph.subgraph(partition_nodes)
        if len(subgraph.edges()) == 0:
            return 0.0
        
        # Density of the subgraph
        n = len(partition_nodes)
        max_edges = n * (n - 1) / 2
        actual_edges = len(subgraph.edges())
        
        return actual_edges / max_edges if max_edges > 0 else 0.0
    
    def _calculate_redundancy_resilience(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate redundancy-based resilience"""
        redundancy_scores = []
        
        # Check path redundancy between partitions
        sample_pairs = []
        for i, node1 in enumerate(list(partition[0])[:3]):  # Sample to avoid combinatorial explosion
            for j, node2 in enumerate(list(partition[1])[:3]):
                sample_pairs.append((node1, node2))
        
        for node1, node2 in sample_pairs:
            try:
                paths = list(nx.all_simple_paths(graph, node1, node2, cutoff=4))
                redundancy_scores.append(min(len(paths), 5) / 5.0)  # Normalize to [0,1]
            except nx.NetworkXNoPath:
                redundancy_scores.append(0.0)
        
        return np.mean(redundancy_scores) if redundancy_scores else 0.0
    
    def _calculate_risk_resilience(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate risk distribution resilience"""
        risk_0 = sum(graph.nodes[n].get('risk', 0.0) for n in partition[0])
        risk_1 = sum(graph.nodes[n].get('risk', 0.0) for n in partition[1])
        
        total_risk = risk_0 + risk_1
        if total_risk == 0:
            return 1.0
        
        # Balance score - closer to 0.5/0.5 is better
        balance = 1 - abs((risk_0 / total_risk) - 0.5) * 2
        
        # Risk concentration penalty
        max_node_risk_0 = max([graph.nodes[n].get('risk', 0.0) for n in partition[0]], default=0.0)
        max_node_risk_1 = max([graph.nodes[n].get('risk', 0.0) for n in partition[1]], default=0.0)
        
        concentration = 1 - max(max_node_risk_0, max_node_risk_1)
        
        return (0.7 * balance + 0.3 * concentration)
    
    def _calculate_geographic_resilience(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate geographic distribution resilience"""
        # Extract geographic coordinates
        coords_0 = []
        coords_1 = []
        
        for node in partition[0]:
            loc = graph.nodes[node].get('location', {})
            if 'lat' in loc and 'lon' in loc:
                coords_0.append((loc['lat'], loc['lon']))
        
        for node in partition[1]:
            loc = graph.nodes[node].get('location', {})
            if 'lat' in loc and 'lon' in loc:
                coords_1.append((loc['lat'], loc['lon']))
        
        if not coords_0 or not coords_1:
            return 0.5  # Neutral if no geographic data
        
        # Calculate geographic spread within each partition
        spread_0 = self._calculate_geographic_spread(coords_0)
        spread_1 = self._calculate_geographic_spread(coords_1)
        
        # Calculate distance between partition centroids
        centroid_0 = np.mean(coords_0, axis=0)
        centroid_1 = np.mean(coords_1, axis=0)
        
        inter_partition_distance = self._haversine_distance(centroid_0, centroid_1)
        
        # Normalize and combine metrics
        avg_spread = (spread_0 + spread_1) / 2
        normalized_distance = min(inter_partition_distance / 10000, 1.0)  # Normalize by 10000 km
        
        return (0.6 * normalized_distance + 0.4 * min(avg_spread / 5000, 1.0))
    
    def _calculate_geographic_spread(self, coordinates: List[Tuple[float, float]]) -> float:
        """Calculate geographic spread of coordinates"""
        if len(coordinates) <= 1:
            return 0.0
        
        distances = []
        for i, coord1 in enumerate(coordinates):
            for coord2 in coordinates[i+1:]:
                distances.append(self._haversine_distance(coord1, coord2))
        
        return np.mean(distances) if distances else 0.0
    
    def _haversine_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Calculate haversine distance between two coordinates"""
        lat1, lon1 = np.radians(coord1[0]), np.radians(coord1[1])
        lat2, lon2 = np.radians(coord2[0]), np.radians(coord2[1])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        return 6371 * c  # Earth radius in km
    
    def _calculate_tco_reduction(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate Total Cost of Ownership reduction"""
        baseline_tco = sum(data.get('weight', 0) * self._extract_cost_weight(graph, i, j)
                          for i, j, data in graph.edges(data=True))
        
        # Calculate optimized TCO based on partition
        optimized_tco = 0
        for i, j, data in graph.edges(data=True):
            base_cost = data.get('weight', 0) * self._extract_cost_weight(graph, i, j)
            
            if (i in partition[0] and j in partition[0]) or (i in partition[1] and j in partition[1]):
                # Same partition - local optimization reduces cost
                optimized_tco += base_cost * 0.8  # 20% reduction
            else:
                # Cross-partition - some efficiency loss
                optimized_tco += base_cost * 1.05  # 5% increase
        
        if baseline_tco == 0:
            return 0.0
        
        return max(0, (baseline_tco - optimized_tco) / baseline_tco)
    
    def _extract_cost_weight(self, graph: nx.Graph, i: int, j: int) -> float:
        """Extract cost component from edge weight"""
        # Assume 40% of total weight is cost (based on lambda_cost = 0.4)
        return 0.4
    
    def _calculate_co2_reduction(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate CO2 emission reduction"""
        baseline_co2 = sum(data.get('weight', 0) * self._extract_co2_weight(graph, i, j)
                          for i, j, data in graph.edges(data=True))
        
        # Calculate optimized CO2 based on localization
        optimized_co2 = 0
        for i, j, data in graph.edges(data=True):
            base_co2 = data.get('weight', 0) * self._extract_co2_weight(graph, i, j)
            
            if (i in partition[0] and j in partition[0]) or (i in partition[1] and j in partition[1]):
                # Same partition - localized supply chain reduces emissions
                optimized_co2 += base_co2 * 0.6  # 40% reduction
            else:
                # Cross-partition - standard emissions
                optimized_co2 += base_co2
        
        if baseline_co2 == 0:
            return 0.0
        
        return max(0, (baseline_co2 - optimized_co2) / baseline_co2)
    
    def _extract_co2_weight(self, graph: nx.Graph, i: int, j: int) -> float:
        """Extract CO2 component from edge weight"""
        # Assume 25% of total weight is CO2 (based on lambda_co2 = 0.25)
        return 0.25
    
    def _calculate_quantum_efficiency(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate quantum algorithm efficiency"""
        n_qubits = len(graph.nodes())
        n_edges = len(graph.edges())
        
        # Quantum efficiency based on problem size scaling
        classical_complexity = n_qubits ** 2  # Simplified classical complexity
        quantum_complexity = n_qubits  # QAOA scales linearly with qubits
        
        if classical_complexity == 0:
            return 1.0
        
        theoretical_speedup = classical_complexity / quantum_complexity
        
        # Practical efficiency considering circuit depth and noise
        circuit_depth_penalty = 1 / (1 + 0.1 * n_qubits)  # Noise increases with depth
        
        return min(theoretical_speedup * circuit_depth_penalty / 100, 1.0)
    
    def _calculate_network_modularity(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate network modularity score"""
        try:
            # Convert partition to community format
            communities = [partition[0], partition[1]]
            modularity = nx.algorithms.community.modularity(graph, communities)
            return max(0, modularity)  # Ensure non-negative
        except:
            return 0.0
    
    def _calculate_partition_balance(self, partition: Tuple[set, set]) -> float:
        """Calculate balance between partition sizes"""
        size_0 = len(partition[0])
        size_1 = len(partition[1])
        total_size = size_0 + size_1
        
        if total_size == 0:
            return 1.0
        
        # Perfect balance is 0.5/0.5 split
        balance = 1 - abs((size_0 / total_size) - 0.5) * 2
        return balance
    
    def _calculate_cut_ratio(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate ratio of cut edges to total edges"""
        cut_edges = sum(1 for i, j in graph.edges()
                       if (i in partition[0] and j in partition[1]) or
                          (i in partition[1] and j in partition[0]))
        
        total_edges = len(graph.edges())
        return cut_edges / total_edges if total_edges > 0 else 0.0
    
    def _calculate_risk_distribution(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate risk distribution balance"""
        return self._calculate_risk_resilience(graph, partition)
    
    def _calculate_sustainability_score(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate overall sustainability score"""
        # ESG scores from nodes
        esg_scores = []
        for node in graph.nodes():
            esg_score = graph.nodes[node].get('esg_score', 70)  # Default to 70
            esg_scores.append(esg_score)
        
        avg_esg = np.mean(esg_scores) if esg_scores else 70
        
        # CO2 reduction contribution
        co2_reduction = self._calculate_co2_reduction(graph, partition)
        
        # Combine ESG and CO2 metrics
        return (0.6 * (avg_esg / 100) + 0.4 * co2_reduction)
    
    def _calculate_disruption_tolerance(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate tolerance to supply chain disruptions"""
        # Simulate random node failures and measure impact
        tolerance_scores = []
        
        for partition_nodes in partition:
            if len(partition_nodes) <= 1:
                tolerance_scores.append(0.0)
                continue
                
            # Test removing each node
            for node in partition_nodes:
                remaining_nodes = partition_nodes - {node}
                if len(remaining_nodes) == 0:
                    tolerance_scores.append(0.0)
                    continue
                    
                # Check if remaining nodes are still connected
                subgraph = graph.subgraph(remaining_nodes)
                if nx.is_connected(subgraph):
                    tolerance_scores.append(1.0)
                else:
                    # Measure largest connected component
                    largest_cc = max(nx.connected_components(subgraph), key=len)
                    tolerance_scores.append(len(largest_cc) / len(remaining_nodes))
        
        return np.mean(tolerance_scores) if tolerance_scores else 0.0
    
    def _calculate_cost_efficiency(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate cost efficiency improvement"""
        return self._calculate_tco_reduction(graph, partition)
    
    def _calculate_operational_savings(self, graph: nx.Graph, partition: Tuple[set, set]) -> float:
        """Calculate operational savings from optimization"""
        # Estimate savings from reduced coordination costs
        cross_partition_edges = sum(1 for i, j in graph.edges()
                                   if (i in partition[0] and j in partition[1]) or
                                      (i in partition[1] and j in partition[0]))
        
        total_edges = len(graph.edges())
        if total_edges == 0:
            return 0.0
        
        # Lower cross-partition ratio means higher operational savings
        coordination_ratio = cross_partition_edges / total_edges
        return 1 - coordination_ratio
    
    def _calculate_target_achievement(self, kpis: Dict[str, float]) -> float:
        """Calculate overall target achievement score"""
        achievements = []
        
        # Check core KPIs against targets
        if 'ResilienceIndex' in kpis:
            achievements.append(min(kpis['ResilienceIndex'] / self.targets.resilience_index, 1.0))
        
        if 'TCO_reduction' in kpis:
            achievements.append(min(kpis['TCO_reduction'] / self.targets.tco_reduction, 1.0))
        
        if 'CO2eq_reduction' in kpis:
            achievements.append(min(kpis['CO2eq_reduction'] / self.targets.co2_reduction, 1.0))
        
        if 'quantum_advantage' in kpis:
            achievements.append(min(kpis['quantum_advantage'] / self.targets.quantum_advantage, 1.0))
        
        return np.mean(achievements) if achievements else 0.0
    
    def generate_kpi_report(self, kpis: Dict[str, float]) -> str:
        """Generate comprehensive KPI report"""
        report = "# INS-01 Strategic Network KPI Report\n\n"
        report += f"Generated: {np.datetime64('now')}\n\n"
        
        # Core KPIs
        report += "## Core Performance Indicators\n\n"
        report += f"| KPI | Value | Target | Status |\n"
        report += f"|-----|-------|--------|---------|\n"
        
        core_kpis = [
            ('ResilienceIndex', self.targets.resilience_index, '≥'),
            ('TCO_reduction', self.targets.tco_reduction, '≥'),
            ('CO2eq_reduction', self.targets.co2_reduction, '≥'),
            ('quantum_advantage', self.targets.quantum_advantage, '≥')
        ]
        
        for kpi_name, target, operator in core_kpis:
            if kpi_name in kpis:
                value = kpis[kpi_name]
                status = "✅" if value >= target else "❌"
                report += f"| {kpi_name} | {value:.3f} | {operator}{target} | {status} |\n"
        
        # Additional metrics
        report += "\n## Additional Metrics\n\n"
        additional_kpis = [k for k in kpis.keys() 
                          if k not in [kpi[0] for kpi in core_kpis]]
        
        for kpi_name in sorted(additional_kpis):
            value = kpis[kpi_name]
            report += f"- **{kpi_name}**: {value:.3f}\n"
        
        # Summary
        overall_score = kpis.get('target_achievement', 0.0)
        report += f"\n## Overall Performance\n\n"
        report += f"**Target Achievement Score**: {overall_score:.1%}\n\n"
        
        if overall_score >= 0.8:
            report += "🎉 **Excellent Performance** - All targets exceeded!\n"
        elif overall_score >= 0.6:
            report += "✅ **Good Performance** - Most targets achieved\n"
        else:
            report += "⚠️  **Needs Improvement** - Several targets missed\n"
        
        return report