# UTCS v12.3 — Binding Metadata for SICOCA
meta:
  name: "SICOCA UTCS Binding"
  system: "SICOCA"
  description: "Quantum–AI optimisation for industrial supply chains"
  utcs_version: "v12.3"
  utcs_code_root: "QOPT-954"         # provisional; confirmar en registro UTCS
  realidad: "SDIG"                   # Synchronous Digital
  version: "0.1.0"
  owner: "AQUA Technologies S.L. — Quantum & Industry Division"
  status: "DRAFT"
  last_update: "2025-08-08"
  artifact_id_proposed: "AQUART-ALGO-IND-SC-SICOCA-QOPT-0954-<UTCS_PATH>-SDIG-v0.1.0"

classification:
  domain: "Industry/SupplyChain/Algorithms"
  # Confirmar códigos canónicos del árbol UTCS en el validador oficial
  utcs_paths:
    - "SC/STR/QOPT"   # INS-01 Red estratégica (QAOA MaxCut MO)
    - "AI/GOV/TRUST"  # INS-02 Gobernanza algorítmica
    - "SC/PLAN/DEM"   # INS-03 Demanda/Inventario (QUBO+QAE)
    - "SC/SUP/NET"    # INS-04 Red de proveedores (SWAP+QAOA)
    - "AI/HIL/OPR"    # INS-05 Human-in-the-Loop (VQE/QAOA)
    - "SC/RSK/FWD"    # INS-06 Anticipación riesgo (QMC+QAE)
    - "FIN/KPI/Q"     # INS-07 Aseguramiento de valor

modules:
  - id: "INS-01"
    name: "Strategic Network Partitioning"
    utcs_path: "SC/STR/QOPT"
    module_path: "src/sicoca/core/{graph.py,qaoa.py}"
    technique: "QAOA Max-Cut multiobjective"
    inputs: ["ERP/MES/WMS", "cost_matrix", "risk_matrix", "co2_weights"]
    outputs: ["partition", "cut_edges", "sensitivity_lambda"]
    kpis: ["ResilienceIndex", "TCO", "CO2eq_reduction"]
  - id: "INS-02"
    name: "Algorithmic Governance Gate"
    utcs_path: "AI/GOV/TRUST"
    module_path: "src/sicoca/core/governance.py"
    technique: "Hamiltonian penalties + policy checks"
    inputs: ["solution_candidate", "policy_rules"]
    outputs: ["trust_report", "stability_score", "fairness_flags"]
    kpis: ["Stability", "FairnessScore", "Reproducibility"]
  - id: "INS-03"
    name: "Demand & Inventory Planning"
    utcs_path: "SC/PLAN/DEM"
    module_path: "src/sicoca/core/{qubo.py,qae.py}"
    technique: "QUBO (inventory) + QAE (stockout)"
    inputs: ["ts_demand", "inventory_levels", "lead_times", "sla_targets"]
    outputs: ["reorder_policy", "buffer_levels", "P_stockout"]
    kpis: ["FillRate", "StockoutProb", "TotalCost"]
  - id: "INS-04"
    name: "Supplier Portfolio Robustness"
    utcs_path: "SC/SUP/NET"
    module_path: "src/sicoca/core/{graph.py,qaoa.py}"
    technique: "SWAP similarity + QAOA selection"
    inputs: ["supplier_profiles", "esg_scores", "geo_risk"]
    outputs: ["supplier_set", "concentration_index", "alt_map"]
    kpis: ["SupplierDiversity", "PortfolioRisk", "OTIF"]
  - id: "INS-05"
    name: "Bionic HIL Optimisation"
    utcs_path: "AI/HIL/OPR"
    module_path: "src/sicoca/core/hil.py"
    technique: "Parametrised ansatz (VQE/QAOA) with human preferences"
    inputs: ["ui_preferences", "policy_rules", "objective_weights"]
    outputs: ["theta_params", "accepted_solution"]
    kpis: ["TimeToDecision", "AcceptanceRate"]
  - id: "INS-06"
    name: "Forward Risk Anticipation"
    utcs_path: "SC/RSK/FWD"
    module_path: "src/sicoca/core/{risk.py,qae.py}"
    technique: "Hybrid Quantum Monte Carlo + QAE"
    inputs: ["scenarios_geo", "regulatory_events", "climate_signals"]
    outputs: ["shock_loss_prob", "reconfig_plan", "prebuy_orders"]
    kpis: ["ShockLossProb", "ReconfigLeadTime"]
  - id: "INS-07"
    name: "Value Assurance Aggregator"
    utcs_path: "FIN/KPI/Q"
    module_path: "src/sicoca/core/value.py"
    technique: "Value-state encoding + amplitude estimation"
    inputs: ["delta_revenue", "delta_cost", "delta_risk", "delta_co2"]
    outputs: ["E_value", "decision_gate"]
    kpis: ["NPV_delta", "TCO_delta", "Risk_delta", "CO2eq_reduction"]

governance:
  trust_gate:
    min_stability: 0.80                 # varianza entre seeds/noise-models
    reproducibility_runs: 3
    fairness_constraints:
      max_country_exposure: 0.50        # límite de concentración por país
      min_supplier_diversity: 0.30      # Herfindahl inverso / share mínimo
    privacy:
      pii_allowed: false
      encryption_at_rest: "PQC-READY (placeholder)"
      encryption_in_transit: "TLS 1.3+"
    auditability:
      model_cards: true
      datasheets: true

validation:
  unit_tests:
    - "tests/test_qubo.py"
    - "tests/test_qaoa.py"
    - "tests/test_governance.py"
  integration_tests:
    datasets:
      inventory: "data/examples/inventory_sample.csv"
      suppliers: "data/examples/suppliers_sample.csv"
    checks:
      - name: "Stockout probability sanity"
        expect: "0.0 <= P_stockout <= 1.0"
      - name: "Governance stability threshold"
        expect: "stability >= 0.80"
  acceptance_criteria:
    INS-01:
      ResilienceIndex_min: 0.05         # Δ resiliencia mínima aceptable
    INS-03:
      FillRate_min: 0.95
      TotalCost_delta_max: 0.00         # no aumentar coste total
    INS-06:
      ShockLossProb_max: 0.20
      ReconfigLeadTime_max_days: 7
    INS-07:
      E_value_min: 0.0                  # >0 ⇒ GO; ≤0 ⇒ REVISE

runtime:
  backend: "simulator"                  # simulator | qpu
  qpu_provider: "<QPU_PROVIDER_PLACEHOLDER>"
  shots: 2048
  seed: 1234
  noise_models: ["depoloarising_stub"]  # placeholder
  performance:
    max_runtime_seconds: 600
    max_qubits_hint: 64                 # guía para selección de problemas

data_interfaces:
  schemas:
    inventory: "data/schemas/inventory.schema.json"
    suppliers: "data/schemas/suppliers.schema.json"
  streams:
    qsn_930: ["telemetry.iot", "market.feeds", "logistics.events"]
  retention:
    raw_days: 30
    features_days: 365

audit_traceability:
  qaudit:
    enabled: true
    stream: "SICOCA/optimizations"
    fields: ["run_id","utcs_module","commit_hash","config_hash","kpis","decision"]
  dt_trace:
    enabled: true
    link_template: "dttrace://sicoca/{run_id}"

security:
  classification: "Internal — Confidential"
  secrets_management: "External vault (no secrets in repo)"
  sbom: false                           # habilitar cuando se integre

icd:
  qpu_910:
    endpoint: "<QPU_ENDPOINT_PLACEHOLDER>"
    contract: "ICD-QPU-910-v1"
  qai_950:
    endpoint: "<QAI_ENDPOINT_PLACEHOLDER>"
    contract: "ICD-QAI-950-v1"
  qsn_930:
    endpoint: "<QSN_ENDPOINT_PLACEHOLDER>"
    contract: "ICD-QSN-930-v1"

kpis:
  ResilienceIndex: "Prob. de mantener servicio ≥ SLA bajo disrupciones simuladas"
  TCO: "Total Cost of Ownership del flujo logístico"
  CO2eq_reduction: "Reducción de emisiones en equivalente CO₂"
  StockoutProb: "Probabilidad de rotura de stock por SKU"
  ShockLossProb: "Probabilidad de pérdida > umbral bajo shocks"
  ReconfigLeadTime: "Tiempo para reconfigurar red tras shock"
  NPV_delta: "Variación del NPV estimado del plan"
  Risk_delta: "Variación de riesgo agregado (normalizado 0–1)"

change_control:
  semver: "0.1.0"
  reviewers: ["UTCS Custodian","QAUDIT Lead","SICOCA Core"]
  notes: "Sustituir utcs_paths y utcs_code_root por claves canónicas tras validación."

contacts:
  tech_owner: "Amedeo Pelliccia"
  email: "contact@aqua.example"         # actualizar
