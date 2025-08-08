

# SICOCA — Sustainable Industrial Chains Optimisation Circuit Algorithm
**Path:** `AQUA/domains/industry/supply_chain/algorithms/SICOCA`  
**UTCS Code:** `QOPT-954` *(provisional; ver sección “UTCS Binding”)*  
**AQUA V. Domain:** Industry → Supply Chain → Quantum Optimisation  
**TRL:** 3 → en transición a TRL 4  
**Status:** Development / Integration Testing  

---

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Repository Layout](#repository-layout)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Python API (stubs)](#python-api-stubs)
- [UTCS Binding](#utcs-binding)
- [Testing](#testing)
- [Performance Metrics](#performance-metrics)
- [Resource Allocation](#resource-allocation)
- [Security & Compliance](#security--compliance)
- [License](#license)
- [Citation](#citation)
- [Contributing](#contributing)

---

## Overview

SICOCA es un **framework de optimización híbrido cuántico–clásico** para modelar, optimizar y **adaptar continuamente** cadenas de suministro industriales mediante **circuitos cuánticos**. 

### Conceptual Overview
```mermaid
mindmap
  root((SICOCA))
    Core Features
      Quantum Optimization
        QAOA
        QUBO
        Hybrid Loop
      Multi-Objective
        Cost
        CO2
        Resilience
        Geo-Risk
      Real-Time Adaptation
        Disruption handling
        Market changes
    Architecture
      Input Layer
        Validation
        Schemas
      Processing Layer
        Graph Model
        QUBO Formulation
        Quantum Solver
      Output Layer
        Reports
        Dashboards
        Audit Trail
    Integration
      AQUA V.
        QPU 910
        QAI 950
        QSN 930
        QAUDIT 970
      UTCS
        QOPT-954
        SC/STR/QOPT
        AI/GOV/TRUST
    Compliance
      Governance
        Trust evaluation
        Policy enforcement
      Security
        Data protection
        Audit trails
      Standards
        UTCS v12.3
        ICD compliance
```

**Mapeo conceptual:**
- **Nodos** (fábricas, almacenes, proveedores, distribuidores) → **Qubits**  
- **Flujos** (materiales, energía, datos) → **Puertas de entrelazamiento**  
- **Coste multiobjetivo** (CO₂, residuos, tiempo, resiliencia, riesgo geopolítico) → **Términos del Hamiltoniano de coste**  

**Ventajas:**
- Exploración de **espacios de configuración exponenciales** en superposición  
- Adaptación en tiempo real a **disrupciones** y cambios de mercado  
- Integración de **economía circular** para planificación *sustainability‑first*  
- Acoplamiento con sistemas **AQUA V.**:  
  - **QPU (910):** ejecución de circuitos  
  - **QAI (950):** analítica predictiva y modelos de riesgo  
  - **QSN (930):** *feeds* logísticos en tiempo real  
  - **QAUDIT (970):** trazabilidad segura y gobernanza  

---

## Key Features

### Feature Prioritization
```mermaid
quadrantChart
    title SICOCA Feature Prioritization
    x-axis Low Complexity --> High Complexity
    y-axis Low Impact --> High Impact
    quadrant-1 Quick Wins: 
      Schema validation
      Basic reporting
    quadrant-2 Major Projects: 
      Quantum integration
      Real-time optimization
    quadrant-3 Fill Ins: 
      UI enhancements
      Additional metrics
    quadrant-4 Strategic Initiatives: 
      Multi-objective optimization
      Global supply chain
```

- **Quantum-Enhanced Optimisation** con QAOA/QUBO y QAE  
- **Hybrid Iterative Loop (HIL):** realimentación entre heurística clásica y circuitos cuánticos  
- **Optimización Multiobjetivo:** CO₂, coste, tiempo, resiliencia, geo‑risk  
- **Entradas validadas por esquema** para reproducibilidad  
- **Topologías configurables:** lineal, distribuida, circular  
- **Integración UTCS/ICD:** metadatos listos para sistemas AQUA V.  

---

## Repository Layout

### System Architecture
```mermaid
graph TD
    subgraph "SICOCA System"
        UI[User Interface]
        API[API Layer]
        CORE[Core Engine]
        QPU[Quantum Processing]
        STORAGE[Data Storage]
    end
    
    subgraph "External Systems"
        QPU910[QPU 910]
        QAI950[QAI 950]
        QSN930[QSN 930]
        QAUDIT[QAUDIT 970]
    end
    
    UI --> API
    API --> CORE
    CORE --> QPU
    CORE --> STORAGE
    QPU --> QPU910
    CORE --> QAI950
    CORE --> QSN930
    CORE --> QAUDIT
```

```plaintext
AQUA/domains/industry/supply_chain/algorithms/SICOCA/
├── README.md
├── pyproject.toml
├── CITATION.cff
├── CHANGELOG.md
├── CODEOWNERS
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE-CODE
├── LICENSE-DOCS
├── .gitignore
├── configs/
│   ├── utcs.meta.yaml
│   └── sicoca.config.yaml
├── src/
│   └── sicoca/
│       ├── __init__.py
│       └── core/
│       ├── graph.py
│       ├── qubo.py
│       ├── qaoa.py
│       ├── qae.py
│       ├── hil.py
│       ├── governance.py
│       ├── risk.py
│       └── value.py
├── data/
│   ├── schemas/
│   │   ├── inventory.schema.json
│   │   └── suppliers.schema.json
│   └── examples/
│       ├── inventory_sample.csv
│       └── suppliers_sample.csv
├── docs/
│   ├── api/
│   │   └── index.md
│   └── annexes/
│       └── ANNEX_SICOCA_INS.md
├── scripts/
│   └── run_demo.py
└── tests/
    ├── test_qubo.py
    ├── test_qaoa.py
    └── test_governance.py
```

---

## Architecture

### Workflow Sequence
```mermaid
sequenceDiagram
    participant User as User/Script
    participant Validator as Schema Validator
    participant Graph as Graph Builder
    participant QUBO as QUBO Formulator
    participant QAOA as QAOA Solver
    participant HIL as Hybrid Iterative Loop
    participant Gov as Governance Module
    participant Risk as Risk Module
    participant Value as Value Module
    participant QPU as QPU 910
    participant QAI as QAI 950
    participant QSN as QSN 930
    participant Output as Output Generator
    participant QAUDIT as QAUDIT Ledger

    User->>Validator: Load inventory & supplier data
    Validator->>Validator: Validate against schemas
    Validator-->>Graph: Validated data
    Graph->>Graph: Build supply chain graph
    Graph-->>QUBO: Graph model
    
    QUBO->>QUBO: Formulate QUBO problem
    QUBO-->>QAOA: QUBO formulation
    
    QAOA->>QPU: Execute quantum circuit
    QPU-->>QAOA: Quantum computation results
    QAOA->>HIL: Send results for feedback
    HIL->>QAI: Request predictive analytics
    QAI-->>HIL: Risk assessment & predictions
    HIL->>QSN: Get real-time logistics data
    QSN-->>HIL: Current logistics state
    HIL->>QAOA: Feedback for refinement
    QAOA->>QAOA: Refined computation
    
    QAOA-->>Gov: Optimisation results
    Gov->>Gov: Evaluate trust & compliance
    Gov-->>Risk: Results for risk analysis
    Risk->>Risk: Calculate risk metrics
    Risk-->>Value: Risk-adjusted results
    Value->>Value: Compute sustainability metrics
    Value-->>Output: Final results
    
    Output->>Output: Generate reports & dashboards
    Output-->>QAUDIT: Audit trail entry
    QAUDIT->>QAUDIT: Record in blockchain ledger
    Output-->>User: Optimisation results
```

### Code Structure
```mermaid
classDiagram
    class GraphModel {
        +build_graph(data)
        +get_nodes()
        +get_edges()
    }
    
    class QuboFormulator {
        +formulate_qubo(graph)
        +set_objectives()
        +add_constraints()
    }
    
    class QaoaSolver {
        +solve_qubo(qubo)
        +set_parameters(p)
        +get_results()
    }
    
    class QaeEstimator {
        +estimate_stockout()
        +calculate_probability()
    }
    
    class HybridLoop {
        +classical_feedback()
        +quantum_refinement()
        +convergence_check()
    }
    
    class Governance {
        +evaluate_trust()
        +check_compliance()
        +apply_policies()
    }
    
    class Risk {
        +calculate_risk()
        +geo_risk_analysis()
        +disruption_impact()
    }
    
    class Value {
        +sustainability_metrics()
        +cost_analysis()
        +kpi_aggregation()
    }
    
    GraphModel --> QuboFormulator
    QuboFormulator --> QaoaSolver
    QaoaSolver --> HybridLoop
    HybridLoop --> QaeEstimator
    QaoaSolver --> Governance
    Governance --> Risk
    Risk --> Value
```

---

## Installation

### User Journey
```mermaid
journey
    title SICOCA Installation Journey
    section Installation
      User: 5: Install package
      User: 3: Configure environment
    section Configuration
      User: 4: Validate config file
      User: 3: Prepare data schemas
    section Execution
      User: 5: Run optimization
      System: 2: Process quantum computation
      System: 3: Generate results
    section Analysis
      User: 4: Review reports
      User: 3: Check sustainability metrics
    section Audit
      User: 2: Export audit trail
      User: 3: Share results
```

> Requisitos: **Python 3.10+**. Para ejecución cuántica real, añadir dependencias de Qiskit u otro *SDK* y configurar acceso al backend QPU.

### With Poetry
```bash
git clone <REPO_URL_PLACEHOLDER>
cd AQUA/domains/industry/supply_chain/algorithms/SICOCA
poetry install
```

### With pip
```bash
git clone <REPO_URL_PLACEHOLDER>
cd AQUA/domains/industry/supply_chain/algorithms/SICOCA
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

---

## Quickstart

### Demo Execution Process
```mermaid
flowchart TD
    A[Start: Load Config] --> B{Data Valid?}
    B -->|Yes| C[Build Graph Model]
    B -->|No| D[Log Error & Exit]
    C --> E[Formulate QUBO]
    E --> F{Quantum Available?}
    F -->|Yes| G[Execute QAOA]
    F -->|No| H[Classical Approximation]
    G --> I[Hybrid Loop]
    H --> I
    I --> J{Converged?}
    J -->|No| K[Adjust Parameters]
    K --> I
    J -->|Yes| L[Generate Results]
    L --> M[Audit Trail]
    M --> N[Output Reports]
    N --> O[End]
```

**Demo** con datos de ejemplo (stubs):
```bash
python scripts/run_demo.py
```

> Ejemplo de salida (demo, no contractual):
``` 
[INFO] Building supply chain graph with 2 SKUs 
[INFO] Formulating QUBO... 
[INFO] Executing QAOA on simulator backend (p=2) 
[INFO] Optimisation complete — sample objective: 1.234 
[INFO] P(stockout) ~ 0.31 
```

---

## Configuration

### Data Schema Relationships
```mermaid
erDiagram
    INVENTORY {
        string sku PK
        string name
        int quantity
        float cost
        string location
    }
    
    SUPPLIER {
        string id PK
        string name
        string country
        float reliability_score
        string certification
    }
    
    REPORT {
        string id PK
        timestamp created_at
        json optimization_results
        float total_cost
        float co2_emissions
    }
    
    QAUDIT_LEDGER {
        string tx_id PK
        timestamp timestamp
        string report_id FK
        string operation
        string user_id
        string hash
    }
    
    INVENTORY }|--|| REPORT : contains
    SUPPLIER }|--|| REPORT : references
    REPORT }|--|| QAUDIT_LEDGER : generates
```

Archivo: `configs/sicoca.config.yaml` (ejemplo)
```yaml
runtime:
  backend: "simulator" # simulator | qpu
  shots: 2048
  seed: 1234
policies:
  risk_tolerance: 0.15
  sla_min: 0.95
paths:
  data: "data/examples"
  outputs: "outputs"
```

**Esquemas de datos** (validación):
* `data/schemas/inventory.schema.json`
* `data/schemas/suppliers.schema.json`

---

## Python API (stubs)

### Algorithm State Machine
```mermaid
stateDiagram-v2
    [*] --> Initialization
    Initialization --> DataValidation
    DataValidation --> GraphBuilding
    GraphBuilding --> QUBOFormulation
    QUBOFormulation --> QuantumExecution
    QuantumExecution --> ClassicalFeedback
    ClassicalFeedback --> ConvergenceCheck
    ConvergenceCheck --> ResultsGeneration
    ResultsGeneration --> AuditTrail
    AuditTrail --> [*]
    
    QuantumExecution --> ErrorHandling
    ErrorHandling --> ClassicalFeedback
```

```python
from sicoca.core.qubo import build_inventory_qubo
from sicoca.core.qaoa import solve_qaoa_qubo
from sicoca.core.qae import estimate_stockout_prob
from sicoca.core.governance import evaluate_trust

Q = build_inventory_qubo(
    demand_scenarios=[120, 100, 140],
    holding_cost=0.8,
    backlog_cost=1.5,
    sla=0.95
)
result = solve_qaoa_qubo(Q, p=2)
p_stockout = estimate_stockout_prob(
    current_stock=110,
    demand_mu=120,
    demand_sigma=15
)
trust = evaluate_trust(result, min_stability=0.8)
print(result, p_stockout, trust)
```

---

## UTCS Binding

### Deployment Architecture
```mermaid
graph TB
    subgraph "Cloud Infrastructure"
        LB[Load Balancer]
        API1[API Server 1]
        API2[API Server 2]
        DB[(Database)]
        CACHE[Redis Cache]
    end
    
    subgraph "Quantum Infrastructure"
        QPU[Quantum Processor]
        QCTRL[Quantum Controller]
    end
    
    subgraph "Monitoring"
        PROM[Prometheus]
        GRAF[Grafana]
    end
    
    LB --> API1
    LB --> API2
    API1 --> DB
    API2 --> DB
    API1 --> CACHE
    API2 --> CACHE
    API1 --> QCTRL
    QCTRL --> QPU
    PROM --> API1
    PROM --> API2
    GRAF --> PROM
```

* **Código raíz provisional:** `QOPT-954`  
* **Claves por módulo (pendientes de validación UTCS v12.3):**  

| INS | Módulo | UTCS (provisional) | Técnica |  
|------|-------------------------------|------------------|------------------------------------------|  
| INS‑01 | `core/graph.py`, `core/qaoa.py` | `SC/STR/QOPT` | QAOA Max‑Cut multiobjetivo |  
| INS‑02 | `core/governance.py` | `AI/GOV/TRUST` | Penalización/constraints en Hamiltoniano |  
| INS‑03 | `core/qubo.py`, `core/qae.py` | `SC/PLAN/DEM` | QUBO inventario + QAE (*stockout*) |  
| INS‑04 | `core/graph.py`, `core/qaoa.py` | `SC/SUP/NET` | SWAP similitud + QAOA selección |  
| INS‑05 | `core/hil.py` | `AI/HIL/OPR` | VQE/QAOA parametrizado (human‑in‑the‑loop) |  
| INS‑06 | `core/risk.py`, `core/qae.py` | `SC/RSK/FWD` | Hybrid Quantum Monte Carlo + QAE |  
| INS‑07 | `core/value.py` | `FIN/KPI/Q` | Agregador de valor + QAE |  

> Sustituir por rutas UTCS canónicas en `configs/utcs.meta.yaml` cuando estén aprobadas.

---

## Testing

### Test Status Board
```mermaid
kanban
    title SICOCA Testing Board
    section Todo
      Core architecture design
      QUBO formulation
      QAOA implementation
    section In Progress
      Hybrid loop development
      Risk module integration
      UTCS binding
    section Testing
      Unit tests for QAOA
      Integration tests
      Performance benchmarks
    section Done
      Schema validation
      Graph model implementation
      Documentation
```

```bash
pytest -q
```
Carpetas de prueba: `tests/`

---

## Performance Metrics

### Performance Comparison
```mermaid
radarChart
    title SICOCA Performance Metrics
    axis Speed, Accuracy, Scalability, Usability, Security
    "Current" : [85, 90, 75, 80, 95]
    "Target" : [95, 95, 90, 85, 98]
```

---

## Resource Allocation

### Development Resources
```mermaid
pie title SICOCA Development Resource Allocation
    "Quantum Algorithms" : 35
    "Classical Computing" : 25
    "Data Processing" : 20
    "UI/UX" : 10
    "Testing & QA" : 10
```

---

## Security & Compliance

### Compliance Timeline
```mermaid
timeline
    title SICOCA Compliance Milestones
    section Q4 2023
      Security Audit : Initial assessment
      UTCS Integration : Metadata binding
    section Q1 2024
      Penetration Testing : Security validation
      Certification : UTCS compliance
    section Q2 2024
      Production Release : Full deployment
      Continuous Monitoring : Ongoing compliance
```

* **Responsible Disclosure:** ver `SECURITY.md`  
* **Trazabilidad & Auditoría:** integración con **QAUDIT/DT‑TRACE** (hooks pendientes)  
* **Datos sensibles:** no incluir ni *committear* secretos; gestionar en *vaults*  

---

## License
* **Código:** MIT — ver `LICENSE-CODE`  
* **Documentación:** CC BY‑SA 4.0 — ver `LICENSE-DOCS`  

---

## Citation

Si utilizas SICOCA en investigación u operaciones:
```bibtex
@software{sicoca_2025,
  title = {SICOCA — Sustainable Industrial Chains Optimisation Circuit Algorithm},
  author = {AQUA V. Quantum & Industry Division},
  year = {2025},
  url = {<REPO_URL_PLACEHOLDER>},
  note = {UTCS QOPT-954 (provisional), v0.1.0}
}
```

---

## Contributing

Ver `CONTRIBUTING.md` y `CODEOWNERS`. Alinea PRs con:  
* Validación UTCS (`configs/utcs.meta.yaml`)  
* Calidad de código (ruff, mypy)  
* Tests (pytest) y *benchmarks* básicos

