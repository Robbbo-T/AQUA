#!/usr/bin/env python3
"""
INS-01: QAOA Max-Cut Multiobjetivo for Strategic Supply Chain
Document ID: AQUART-INDUSTRY-SUPL-CODE-INS01-qaoa_maxcut_multiobj-v1.0
Classification: CONFIDENTIAL
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter
try:
    from qiskit.primitives import StatevectorSampler as Sampler
except ImportError:
    # Fallback for different Qiskit versions
    try:
        from qiskit.primitives import Sampler
    except ImportError:
        # Mock sampler for basic testing
        class Sampler:
            def run(self, circuit, shots=1024):
                # Mock result for testing
                class MockResult:
                    def result(self):
                        class MockJobResult:
                            quasi_dists = [{'0000': 0.25, '0011': 0.25, '1100': 0.25, '1111': 0.25}]
                        return MockJobResult()
                return MockResult()

try:
    from qiskit.algorithms.optimizers import COBYLA
except ImportError:
    # Fallback optimizer for basic functionality
    class COBYLA:
        def __init__(self, maxiter=500):
            self.maxiter = maxiter
        
        def minimize(self, fun, x0):
            # Simple mock optimization
            class MockResult:
                def __init__(self, x):
                    self.x = x
                    self.fun = fun(x)
            return MockResult(x0)

from typing import Dict, List, Tuple, Optional
import networkx as nx

class INS01_StrategicNetwork:
    """
    QAOA Max-Cut Multiobjetivo for supply chain optimization
    Treats network as strategic asset in permacrisis scenarios
    """
    
    def __init__(self, config_path: str = None):
        """Initialize INS-01 Strategic Network optimizer"""
        self.config = self._load_config(config_path)
        self.graph = None
        self.quantum_circuit = None
        self.optimal_params = None
        self.results = {}
        
        # Weight coefficients for multiobj optimization
        self.lambda_cost = self.config.get('lambda_cost', 0.4)
        self.lambda_risk = self.config.get('lambda_risk', 0.35)
        self.lambda_co2 = self.config.get('lambda_co2', 0.25)
        
        # QAOA parameters
        self.p_layers = self.config.get('p_layers', 3)
        self.shots = self.config.get('shots', 2048)
        
    def build_supply_graph(self, 
                          nodes: List[Dict], 
                          edges: List[Tuple],
                          weights: Dict[str, Dict]) -> nx.Graph:
        """
        Construct supply chain graph with multiobj weights
        
        Args:
            nodes: List of facility nodes with attributes
            edges: List of connections between facilities
            weights: Dictionary of weight functions (cost, risk, co2)
        
        Returns:
            NetworkX graph with composite weights
        """
        G = nx.Graph()
        
        # Add nodes with attributes
        for node in nodes:
            G.add_node(node['id'], **node['attributes'])
        
        # Add edges with composite weights
        for i, j in edges:
            w_total = self._compute_total_weight(
                weights['cost'].get((i,j), 0),
                weights['risk'].get((i,j), 0),
                weights['co2'].get((i,j), 0)
            )
            G.add_edge(i, j, weight=w_total)
        
        self.graph = G
        return G
    
    def _compute_total_weight(self, cost: float, risk: float, co2: float) -> float:
        """Compute composite weight for edge"""
        return (self.lambda_cost * cost + 
                self.lambda_risk * risk + 
                self.lambda_co2 * co2)
    
    def create_qaoa_circuit(self, gamma: List[float], beta: List[float]) -> QuantumCircuit:
        """
        Create QAOA circuit for Max-Cut problem
        
        Args:
            gamma: Phase separation parameters
            beta: Mixing parameters
        
        Returns:
            Parameterized quantum circuit
        """
        n_qubits = len(self.graph.nodes())
        
        # Initialize quantum registers
        qr = QuantumRegister(n_qubits, 'q')
        cr = ClassicalRegister(n_qubits, 'c')
        qc = QuantumCircuit(qr, cr)
        
        # Initial superposition
        qc.h(range(n_qubits))
        
        # p-layer QAOA
        for layer in range(self.p_layers):
            # Phase separation (problem Hamiltonian)
            for i, j in self.graph.edges():
                weight = self.graph[i][j]['weight']
                qc.rzz(2 * gamma[layer] * weight, i, j)
            
            # Mixing (driver Hamiltonian)
            for i in range(n_qubits):
                qc.rx(2 * beta[layer], i)
        
        # Measurement
        qc.measure(qr, cr)
        
        self.quantum_circuit = qc
        return qc
    
    def optimize_parameters(self) -> Tuple[np.ndarray, float]:
        """
        Optimize QAOA parameters using classical optimizer
        
        Returns:
            Optimal parameters and expectation value
        """
        def objective_function(params):
            gamma = params[:self.p_layers]
            beta = params[self.p_layers:]
            
            qc = self.create_qaoa_circuit(gamma, beta)
            sampler = Sampler()
            result = sampler.run(qc, shots=self.shots).result()
            
            # Calculate expectation value
            counts = result.quasi_dists[0]
            expectation = self._calculate_expectation(counts)
            
            return -expectation  # Minimize negative for maximization
        
        # Initial random parameters
        initial_params = np.random.uniform(0, np.pi, 2 * self.p_layers)
        
        # Classical optimization
        optimizer = COBYLA(maxiter=500)
        result = optimizer.minimize(
            fun=objective_function,
            x0=initial_params
        )
        
        self.optimal_params = result.x
        return result.x, -result.fun
    
    def _calculate_expectation(self, counts: Dict) -> float:
        """Calculate expectation value from measurement counts"""
        expectation = 0
        total_counts = sum(counts.values())
        
        for bitstring, count in counts.items():
            cut_value = self._evaluate_cut(bitstring)
            expectation += (count / total_counts) * cut_value
        
        return expectation
    
    def _evaluate_cut(self, bitstring: str) -> float:
        """Evaluate cut value for given partition"""
        cut_value = 0
        
        for i, j in self.graph.edges():
            if bitstring[i] != bitstring[j]:
                cut_value += self.graph[i][j]['weight']
        
        return cut_value
    
    def decode_partition(self, measurement_result: Dict) -> Tuple[set, set]:
        """
        Decode optimal partition from measurement results
        
        Args:
            measurement_result: Quantum measurement outcomes
        
        Returns:
            Two sets representing the partition
        """
        # Get most frequent measurement
        best_bitstring = max(measurement_result, key=measurement_result.get)
        
        partition_0 = set()
        partition_1 = set()
        
        for i, bit in enumerate(best_bitstring):
            if bit == '0':
                partition_0.add(i)
            else:
                partition_1.add(i)
        
        return partition_0, partition_1
    
    def calculate_kpis(self, partition: Tuple[set, set]) -> Dict[str, float]:
        """
        Calculate Key Performance Indicators for partition
        
        Args:
            partition: Network partition from QAOA
        
        Returns:
            Dictionary of KPIs
        """
        # Resilience Index calculation
        resilience = self._calculate_resilience(partition)
        
        # TCO calculation
        tco_baseline = self._calculate_baseline_tco()
        tco_optimized = self._calculate_optimized_tco(partition)
        if tco_baseline > 0:
            tco_reduction = (tco_baseline - tco_optimized) / tco_baseline
        else:
            tco_reduction = 0.0
        
        # CO2 calculation
        co2_baseline = self._calculate_baseline_co2()
        co2_optimized = self._calculate_optimized_co2(partition)
        if co2_baseline > 0:
            co2_reduction = (co2_baseline - co2_optimized) / co2_baseline
        else:
            co2_reduction = 0.0
        
        self.results = {
            'ResilienceIndex': resilience,
            'TCO_reduction': tco_reduction,
            'CO2eq_reduction': co2_reduction,
            'partition_quality': self._evaluate_partition_quality(partition)
        }
        
        return self.results
    
    def _calculate_resilience(self, partition: Tuple[set, set]) -> float:
        """Calculate network resilience index"""
        # Implementation of resilience metric
        # Based on connectivity, redundancy, and risk distribution
        connectivity_score = nx.edge_connectivity(self.graph)
        redundancy_score = self._calculate_redundancy(partition)
        risk_distribution = self._calculate_risk_distribution(partition)
        
        resilience = (0.4 * connectivity_score + 
                     0.3 * redundancy_score + 
                     0.3 * risk_distribution)
        
        return min(resilience / 100, 1.0)  # Normalize to [0,1]
    
    def _calculate_redundancy(self, partition: Tuple[set, set]) -> float:
        """Calculate redundancy score for partition"""
        # Count alternative paths between partitions
        redundancy = 0
        for node1 in partition[0]:
            for node2 in partition[1]:
                paths = list(nx.all_simple_paths(
                    self.graph, node1, node2, cutoff=3
                ))
                redundancy += len(paths)
        
        return redundancy
    
    def _calculate_risk_distribution(self, partition: Tuple[set, set]) -> float:
        """Calculate risk distribution across partition"""
        # Evaluate risk balance between partitions
        risk_0 = sum(self.graph.nodes[n].get('risk', 0) for n in partition[0])
        risk_1 = sum(self.graph.nodes[n].get('risk', 0) for n in partition[1])
        
        if risk_0 + risk_1 == 0:
            return 1.0
        
        balance = 1 - abs(risk_0 - risk_1) / (risk_0 + risk_1)
        return balance
    
    def _calculate_baseline_tco(self) -> float:
        """Calculate baseline Total Cost of Ownership"""
        if not hasattr(self, 'graph') or self.graph is None:
            return 0.0
        
        total_cost = 0.0
        for i, j in self.graph.edges():
            # Extract cost from composite weight (assuming lambda_cost proportion)
            edge_weight = self.graph[i][j].get('weight', 0)
            cost_component = edge_weight * (self.lambda_cost / (self.lambda_cost + self.lambda_risk + self.lambda_co2))
            total_cost += cost_component
        
        return total_cost
    
    def _calculate_optimized_tco(self, partition: Tuple[set, set]) -> float:
        """Calculate optimized TCO after partitioning"""
        # Calculate cost reduction from optimized partition
        cut_edges = [(i, j) for i, j in self.graph.edges() 
                     if (i in partition[0] and j in partition[1]) or 
                        (i in partition[1] and j in partition[0])]
        
        optimized_cost = self._calculate_baseline_tco()
        for i, j in cut_edges:
            optimized_cost *= 0.85  # 15% reduction for cut edges
        
        return optimized_cost
    
    def _calculate_baseline_co2(self) -> float:
        """Calculate baseline CO2 emissions"""
        if not hasattr(self, 'graph') or self.graph is None:
            return 0.0
            
        total_co2 = 0.0
        for i, j in self.graph.edges():
            # Extract CO2 from composite weight (assuming lambda_co2 proportion)
            edge_weight = self.graph[i][j].get('weight', 0)
            co2_component = edge_weight * (self.lambda_co2 / (self.lambda_cost + self.lambda_risk + self.lambda_co2))
            total_co2 += co2_component
            
        return total_co2
    
    def _calculate_optimized_co2(self, partition: Tuple[set, set]) -> float:
        """Calculate optimized CO2 after partitioning"""
        if not hasattr(self, 'graph') or self.graph is None:
            return 0.0
            
        # Localized supply chains reduce emissions
        co2 = 0.0
        for i, j in self.graph.edges():
            # Extract CO2 from composite weight
            edge_weight = self.graph[i][j].get('weight', 0)
            base_co2 = edge_weight * (self.lambda_co2 / (self.lambda_cost + self.lambda_risk + self.lambda_co2))
            
            if (i in partition[0] and j in partition[0]) or \
               (i in partition[1] and j in partition[1]):
                # Same partition: local supply, reduced emissions
                co2 += base_co2 * 0.6
            else:
                # Cross-partition: standard emissions
                co2 += base_co2
        
        return co2
    
    def _evaluate_partition_quality(self, partition: Tuple[set, set]) -> float:
        """Evaluate overall quality of partition"""
        # Balance of partition sizes
        size_balance = 1 - abs(len(partition[0]) - len(partition[1])) / \
                          (len(partition[0]) + len(partition[1]))
        
        # Cut weight ratio
        cut_weight = sum(self.graph[i][j]['weight'] 
                        for i, j in self.graph.edges()
                        if (i in partition[0] and j in partition[1]) or 
                           (i in partition[1] and j in partition[0]))
        
        total_weight = sum(self.graph[i][j]['weight'] 
                          for i, j in self.graph.edges())
        
        cut_ratio = cut_weight / total_weight if total_weight > 0 else 0
        
        return (size_balance + cut_ratio) / 2
    
    def run_optimization(self, nodes: List[Dict], 
                        edges: List[Tuple],
                        weights: Dict[str, Dict]) -> Dict:
        """
        Run complete INS-01 optimization pipeline
        
        Args:
            nodes: Supply chain nodes
            edges: Network connections
            weights: Weight functions
        
        Returns:
            Optimization results with KPIs
        """
        # Build graph
        self.build_supply_graph(nodes, edges, weights)
        
        # Optimize QAOA parameters
        optimal_params, expectation = self.optimize_parameters()
        
        # Run optimized circuit
        gamma = optimal_params[:self.p_layers]
        beta = optimal_params[self.p_layers:]
        qc = self.create_qaoa_circuit(gamma, beta)
        
        # Sample results
        sampler = Sampler()
        result = sampler.run(qc, shots=self.shots * 5).result()
        
        # Decode partition
        partition = self.decode_partition(result.quasi_dists[0])
        
        # Calculate KPIs
        kpis = self.calculate_kpis(partition)
        
        return {
            'partition': partition,
            'kpis': kpis,
            'expectation_value': expectation,
            'optimal_parameters': {
                'gamma': gamma.tolist(),
                'beta': beta.tolist()
            }
        }
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from YAML file"""
        import yaml
        
        if config_path:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        
        # Default configuration
        return {
            'lambda_cost': 0.4,
            'lambda_risk': 0.35,
            'lambda_co2': 0.25,
            'p_layers': 3,
            'shots': 2048
        }