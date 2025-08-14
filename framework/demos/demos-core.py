"""
DeMOS - Dual-Engined Metrics Operational System Core
UTCS-MI Code: [198] DeMOS Core

Advanced metrics collection and operational monitoring system
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import statistics
import numpy as np

class MetricType(Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"
    QUANTUM_STATE = "quantum_state"
    QUANTUM_FIDELITY = "quantum_fidelity"

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class Metric:
    name: str
    type: MetricType
    value: Union[float, int, str, complex]
    timestamp: float
    labels: Dict[str, str] = field(default_factory=dict)
    unit: Optional[str] = None
    help_text: Optional[str] = None

@dataclass
class Alert:
    id: str
    metric_name: str
    severity: AlertSeverity
    message: str
    timestamp: float
    resolved: bool = False
    resolution_time: Optional[float] = None

@dataclass
class OperationalTarget:
    metric_name: str
    target_value: float
    tolerance: float
    critical_threshold: float
    unit: str

class DeMOSCore:
    """
    Core DeMOS metrics and operational monitoring system
    """
    
    def __init__(self):
        self.logger = logging.getLogger("DeMOS.Core")
        self.metrics: Dict[str, List[Metric]] = {}
        self.alerts: Dict[str, Alert] = {}
        self.operational_targets: Dict[str, OperationalTarget] = {}
        self.collectors: Dict[str, Any] = {}
        self.simulation_engine = None
        
        # Initialize core metrics
        self._initialize_core_metrics()
        
        # Initialize operational targets
        self._initialize_operational_targets()
        
    def _initialize_core_metrics(self):
        """Initialize core system metrics"""
        self.logger.info("Initializing DeMOS core metrics")
        
        core_metrics = [
            "system.boot_time",
            "system.uptime",
            "kernel.memory_usage",
            "kernel.cpu_usage",
            "kernel.process_count",
            "quantum.qubit_count",
            "quantum.gate_fidelity",
            "quantum.coherence_time",
            "platform.ampel360.health",
            "platform.caas.certification_rate",
            "platform.diqiaas.intelligence_accuracy",
            "platform.gaia.mission_success_rate",
            "framework.cqea.application_count",
            "framework.amores.compliance_score",
            "framework.wee.learning_rate",
            "security.threat_level",
            "security.encryption_strength"
        ]
        
        for metric_name in core_metrics:
            self.metrics[metric_name] = []
    
    def _initialize_operational_targets(self):
        """Initialize operational performance targets"""
        targets = [
            OperationalTarget("system.boot_time", 30.0, 5.0, 60.0, "seconds"),
            OperationalTarget("kernel.memory_usage", 50.0, 10.0, 90.0, "percent"),
            OperationalTarget("quantum.gate_fidelity", 99.0, 1.0, 95.0, "percent"),
            OperationalTarget("quantum.coherence_time", 100.0, 20.0, 50.0, "microseconds"),
            OperationalTarget("security.threat_level", 1.0, 0.5, 3.0, "level"),
            OperationalTarget("framework.amores.compliance_score", 95.0, 5.0, 80.0, "percent"),
        ]
        
        for target in targets:
            self.operational_targets[target.metric_name] = target
    
    async def collect_metric(self, name: str, value: Union[float, int, str, complex], 
                           metric_type: MetricType = MetricType.GAUGE, 
                           labels: Optional[Dict[str, str]] = None,
                           unit: Optional[str] = None) -> bool:
        """
        Collect a metric value
        """
        try:
            metric = Metric(
                name=name,
                type=metric_type,
                value=value,
                timestamp=time.time(),
                labels=labels or {},
                unit=unit
            )
            
            if name not in self.metrics:
                self.metrics[name] = []
            
            self.metrics[name].append(metric)
            
            # Keep only last 1000 data points per metric
            if len(self.metrics[name]) > 1000:
                self.metrics[name] = self.metrics[name][-1000:]
            
            # Check if this triggers any alerts
            await self._check_alerts(metric)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to collect metric {name}: {e}")
            return False
    
    async def _check_alerts(self, metric: Metric):
        """
        Check if a metric triggers any alerts
        """
        if metric.name in self.operational_targets:
            target = self.operational_targets[metric.name]
            
            if isinstance(metric.value, (int, float)):
                deviation = abs(float(metric.value) - target.target_value)
                
                if deviation > target.critical_threshold:
                    await self._create_alert(
                        metric.name,
                        AlertSeverity.CRITICAL,
                        f"Metric {metric.name} critically out of range: {metric.value} (target: {target.target_value})"
                    )
                elif deviation > target.tolerance:
                    await self._create_alert(
                        metric.name,
                        AlertSeverity.WARNING,
                        f"Metric {metric.name} out of tolerance: {metric.value} (target: {target.target_value})"
                    )
    
    async def _create_alert(self, metric_name: str, severity: AlertSeverity, message: str):
        """
        Create a new alert
        """
        alert_id = f"{metric_name}_{int(time.time())}"
        
        alert = Alert(
            id=alert_id,
            metric_name=metric_name,
            severity=severity,
            message=message,
            timestamp=time.time()
        )
        
        self.alerts[alert_id] = alert
        
        self.logger.warning(f"Alert created: {severity.value} - {message}")
        
        # Trigger alert handlers
        await self._handle_alert(alert)
    
    async def _handle_alert(self, alert: Alert):
        """
        Handle alert based on severity
        """
        if alert.severity == AlertSeverity.EMERGENCY:
            # Immediate action required
            await self._emergency_response(alert)
        elif alert.severity == AlertSeverity.CRITICAL:
            # Escalate to operators
            await self._critical_response(alert)
        elif alert.severity == AlertSeverity.WARNING:
            # Log and monitor
            await self._warning_response(alert)
    
    def get_metric_history(self, metric_name: str, 
                          duration_seconds: Optional[int] = None) -> List[Metric]:
        """
        Get historical data for a metric
        """
        if metric_name not in self.metrics:
            return []
        
        metrics = self.metrics[metric_name]
        
        if duration_seconds:
            cutoff_time = time.time() - duration_seconds
            metrics = [m for m in metrics if m.timestamp >= cutoff_time]
        
        return metrics
    
    def get_metric_statistics(self, metric_name: str, 
                            duration_seconds: int = 3600) -> Dict[str, float]:
        """
        Get statistical summary of a metric
        """
        history = self.get_metric_history(metric_name, duration_seconds)
        
        if not history:
            return {}
        
        numeric_values = [float(m.value) for m in history 
                         if isinstance(m.value, (int, float))]
        
        if not numeric_values:
            return {}
        
        return {
            "count": len(numeric_values),
            "mean": statistics.mean(numeric_values),
            "median": statistics.median(numeric_values),
            "std_dev": statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0.0,
            "min": min(numeric_values),
            "max": max(numeric_values),
            "latest": numeric_values[-1] if numeric_values else 0.0
        }
    
    def get_system_health_score(self) -> float:
        """
        Calculate overall system health score (0.0 - 1.0)
        """
        health_scores = []
        
        # Evaluate each operational target
        for metric_name, target in self.operational_targets.items():
            recent_metrics = self.get_metric_history(metric_name, 300)  # Last 5 minutes
            
            if recent_metrics:
                latest_value = recent_metrics[-1].value
                if isinstance(latest_value, (int, float)):
                    deviation = abs(float(latest_value) - target.target_value)
                    normalized_deviation = deviation / (target.target_value + 0.001)  # Avoid division by zero
                    score = max(0.0, 1.0 - normalized_deviation)
                    health_scores.append(score)
        
        return statistics.mean(health_scores) if health_scores else 0.0
    
    def get_operational_dashboard(self) -> Dict[str, Any]:
        """
        Get comprehensive operational dashboard data
        """
        dashboard = {
            "timestamp": time.time(),
            "system_health_score": self.get_system_health_score(),
            "active_alerts": len([a for a in self.alerts.values() if not a.resolved]),
            "metrics_summary": {},
            "recent_alerts": list(self.alerts.values())[-10:],  # Last 10 alerts
            "operational_targets": {}
        }
        
        # Add metrics summary
        for metric_name in self.metrics.keys():
            stats = self.get_metric_statistics(metric_name)
            if stats:
                dashboard["metrics_summary"][metric_name] = stats
        
        # Add operational targets status
        for target_name, target in self.operational_targets.items():
            recent_metrics = self.get_metric_history(target_name, 300)
            if recent_metrics:
                latest_value = recent_metrics[-1].value
                dashboard["operational_targets"][target_name] = {
                    "target": target.target_value,
                    "current": latest_value,
                    "status": self._evaluate_target_status(target, latest_value),
                    "unit": target.unit
                }
        
        return dashboard
    
    def _evaluate_target_status(self, target: OperationalTarget, current_value: Any) -> str:
        """
        Evaluate operational target status
        """
        if not isinstance(current_value, (int, float)):
            return "unknown"
        
        deviation = abs(float(current_value) - target.target_value)
        
        if deviation <= target.tolerance:
            return "optimal"
        elif deviation <= target.critical_threshold:
            return "acceptable"
        else:
            return "critical"
    
    async def start_simulation_engine(self):
        """
        Start the DeMOS simulation engine
        """
        from .simulation_engine import SimulationEngine
        
        self.simulation_engine = SimulationEngine(self)
        await self.simulation_engine.start()
        
        self.logger.info("DeMOS simulation engine started")
    
    def shutdown(self):
        """
        Shutdown DeMOS core
        """
        self.logger.info("DeMOS Core shutdown initiated")
        
        if self.simulation_engine:
            self.simulation_engine.stop()
        
        # Stop all collectors
        for collector in self.collectors.values():
            if hasattr(collector, 'stop'):
                collector.stop()
        
        self.logger.info("DeMOS Core shutdown complete")

# Global DeMOS instance
demos_core = None

def initialize_demos_system():
    """Initialize the global DeMOS system"""
    global demos_core
    demos_core = DeMOSCore()
    return demos_core

def get_demos_system() -> Optional[DeMOSCore]:
    """Get the global DeMOS system instance"""
    return demos_core