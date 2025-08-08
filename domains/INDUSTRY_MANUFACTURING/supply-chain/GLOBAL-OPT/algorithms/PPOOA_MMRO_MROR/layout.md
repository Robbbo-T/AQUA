```
├── README.md
├── UTCS_binding_MRO-961.yaml
├── architecture/
│   ├── system_design.md
│   └── integration_matrix.yaml
├── mmro/
│   ├── sensors/quantum_sensors.py
│   ├── data_pipeline/stream_processor.py
│   └── digital_twin/state_estimator.py
├── ppooa/
│   ├── classical/predictive_models.py
│   ├── quantum/qaoa_scheduler.py                # stub QAOA (sim)
│   └── hybrid/quantum_classical_loop.py         # lazo híbrido
├── mror/
│   ├── optimization/recycling_optimizer.py
│   ├── marketplace/value_calculator.py
│   └── compliance/environmental_standards.yaml  # (vacío por ahora)
├── integration/
│   ├── sicoca_bridge.py
│   ├── ampel360_connector.py
│   ├── diqiaas_interface.py
│   └── qaudit_logger.py
├── validation/
│   ├── classical/
│   │   ├── lifecycle_simulator.py
│   │   ├── performance_validator.py
│   │   └── outputs/                # artefactos
│   └── quantum/                    # (placeholder)
└── docs/
    └── api_specification.yaml
