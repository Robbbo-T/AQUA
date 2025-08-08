# ANNEX — SICOCA Insight Matrix (UTCS v12.3)

**Ruta:** `AQUA/domains/industry/supply_chain/algorithms/SICOCA/docs/annexes/ANNEX_SICOCA_INS.md`  
**Sistema:** SICOCA — *Sustainable Industrial Chains Optimisation Circuit Algorithm*  
**UTCS root (provisional):** `QOPT-954`  
**Versión del anexo:** v0.1.0 · 2025-08-08  
**Propietario:** AQUA Technologies S.L. — Quantum & Industry Division

> **Base conceptual:** La cadena de suministro es un **activo estratégico** en permacrisis; la IA debe ser **relevante, responsable y confiable**; cobertura **end-to-end** (diseño→operación), sensórica **IoT**, proveedores como **socios estratégicos**, y **anticipación** regulatoria/geopolítica mediante IA. :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}:contentReference[oaicite:2]{index=2}:contentReference[oaicite:3]{index=3}

---

## 0) Tabla de mapeo UTCS (resumen)

| INS | Insight base | UTCS (provisional) | Módulo SICOCA | Técnica principal | Objetivo |
|---|---|---|---|---|---|
| INS-01 | Supply chain = activo estratégico | `SC/STR/QOPT` | `core/graph.py`, `core/qaoa.py` | **QAOA** Max-Cut multiobjetivo | Particionado/rediseño de red para resiliencia y coste. :contentReference[oaicite:4]{index=4} |
| INS-02 | IA relevante/ responsable/ confiable | `AI/GOV/TRUST` | `core/governance.py` | Hamiltoniano con penalizaciones (políticas) | *Trust gate* previo a despliegue. :contentReference[oaicite:5]{index=5} |
| INS-03 | Planificación end-to-end + IoT | `SC/PLAN/DEM` | `core/qubo.py`, `core/qae.py` | **QUBO** + **QAE** | Reposición óptima, buffers y *stockout* prob. :contentReference[oaicite:6]{index=6} |
| INS-04 | Proveedores = socios estratégicos | `SC/SUP/NET` | `core/graph.py`, `core/qaoa.py` | SWAP test + QAOA selección | Cartera robusta y diversificada. :contentReference[oaicite:7]{index=7} |
| INS-05 | Gestión biónica (Human-in-the-Loop) | `AI/HIL/OPR` | `core/hil.py` | VQE/QAOA parametrizado | Inyectar preferencias humanas en el ansatz. :contentReference[oaicite:8]{index=8} |
| INS-06 | Anticipación regulatoria/geopolítica | `SC/RSK/FWD` | `core/risk.py`, `core/qae.py` | **Hybrid QMC** + **QAE** | Reconfiguración preventiva ante shocks. :contentReference[oaicite:9]{index=9} |
| INS-07 | Valor = ingresos, costes, riesgos | `FIN/KPI/Q` | `core/value.py` | Estado de valor + QAE | Decisión GO/REVISE por expectativa de valor. :contentReference[oaicite:10]{index=10} |

> Sustituir los códigos UTCS por las claves **canónicas** cuando el validador UTCS v12.3 publique la taxonomía final.

---

## 1) INS-01 — Red estratégica (QAOA Max-Cut Multiobjetivo)

**Base:** Tratar la cadena como **activo estratégico** en permacrisis; rediseño estructural aporta ventaja. :contentReference[oaicite:11]{index=11}

**Modelo:** Grafo \(G(V,E)\) con pesos combinados: coste, riesgo, CO₂, lead time.  
**Objetivo:** Maximizar resiliencia y reducir TCO/CO₂ con **particiones/segmentaciones** de la red.

**Pseudocódigo (estilo Qiskit):**
```python
# Construcción de grafo y coste compuesto
G = build_supply_graph(nodes, edges, weights={"cost":Wc,"risk":Wr,"co2":Wg})
def w_total(e): return λ1*Wc[e] + λ2*Wr[e] + λ3*Wg[e]

# QAOA Max-Cut multiobjetivo
qc = QuantumCircuit(len(G["nodes"]))
qc.h(range(len(G["nodes"])))
for l in range(p):
    for (i,j) in G["edges"]:
        qc.rzz(2*gamma[l]*w_total((i,j)), i, j)
    for i in range(len(G["nodes"])):
        qc.rx(2*beta[l], i)
result = sample_bitstrings(qc, shots=2048)
partition = decode_cut(result)
````

**KPIs:** *ResilienceIndex*, TCO, CO₂eq\_reduction.

---

## 2) INS-02 — Gobernanza algorítmica (Trust/Ethics Gate)

**Base:** La IA debe ser **relevante, responsable y confiable**; confianza como esencia del negocio.&#x20;

**Idea:** Añadir **penalizaciones** al Hamiltoniano (diversidad de proveedores, exposición país, límites ESG).
**Criterios:** estabilidad ≥ umbral; reproducibilidad; *model cards* y *datasheets*.

**Pseudocódigo (estilo Qiskit):**

```python
H_base = build_cost_hamiltonian(G, weights)
H_pen  = fairness_penalties(max_country_exposure=0.5, min_diversity=0.3, esg_floor=70)
H_tot  = H_base + μ * H_pen

qc = qaoa_from_hamiltonian(H_tot, p=2)
metrics = evaluate_trust(qc, seeds=[1,2,3], noise_models=["depol_stub"])
assert metrics["stability"] >= 0.80 and metrics["meets_threshold"]
```

**Salida:** `trust_report`, `stability_score`, `fairness_flags`.

---

## 3) INS-03 — Planificación DEM/INV + IoT (QUBO + QAE)

**Base:** Cobertura **end-to-end**, detección de **anomalías IoT** y planificación de demanda/inventario con visibilidad sin precedentes.&#x20;

**Idea:** Formulación **QUBO** multi-SKU; **QAE** para estimar prob. de *stockout*.

**Pseudocódigo (estilo Qiskit):**

```python
Q = build_inventory_qubo(demand_scenarios, holding_cost, backlog_cost, sla=0.95)
sol = solve_qaoa_qubo(Q, p=2)

state = encode_stock_state(current_stock, demand_mu, demand_sigma)
P_stockout = quantum_amplitude_estimation(state, event="stockout").estimate
policy = derive_policy(sol, P_stockout, risk_tolerance=0.15)
```

**KPIs:** *FillRate*, *StockoutProb*, *TotalCost*.

---

## 4) INS-04 — Proveedores como socios (SWAP + QAOA)

**Base:** Colocar a los proveedores en el **centro**; clasificar e integrar en un programa 360°.&#x20;

**Idea:**

1. **SWAP test** para similitud de perfiles (calidad, OTIF, ESG, riesgo).
2. **QAOA** para seleccionar cartera con máxima cobertura y mínima concentración.

**Pseudocódigo (estilo Qiskit):**

```python
sim = swap_test(encode_profile(S1), encode_profile(S2))  # |<ψ|φ>|^2
H = coverage_benefit() - α*concentration_penalty() - β*risk_penalty()
portfolio = qaoa_select(H, p=1)
```

**KPIs:** *SupplierDiversity*, *PortfolioRisk*, OTIF.

---

## 5) INS-05 — Gestión biónica (Human-in-the-Loop)

**Base:** *Bionic supply chain*: creatividad humana + tecnología digital para ir más rápido y mejor.&#x20;

**Idea:** Preferencias humanas $\rightarrow$ parámetros del **ansatz** (VQE/QAOA). *Loop* HIL con revisión.

**Pseudocódigo (estilo Qiskit):**

```python
θ = human_preferences_to_params(ui_sliders, policy_rules)
ansatz = build_param_ansatz(layout="problem-aware")
E = vqe(H_tot, ansatz, init_params=θ)

while not converged:
    feedback = human_review(top_k_solutions(E))
    θ = update_params(θ, feedback)
    E = vqe(H_tot, ansatz, init_params=θ)
```

**KPIs:** *TimeToDecision*, *AcceptanceRate*.

---

## 6) INS-06 — Anticipación de riesgo (Hybrid QMC + QAE)

**Base:** Anticiparse a presiones **regulatorias/geopolíticas** y diseñar estrategia bajo incertidumbre.&#x20;

**Idea:** Muestreo de **shocks** con *Quantum Monte Carlo* híbrido; **QAE** para $P(\text{loss} > L)$.

**Pseudocódigo (estilo Qiskit):**

```python
scenarios = generate_shock_scenarios(policy, geo, climate)
qc = quantum_monte_carlo_encode(scenarios, impact_model)
P_loss = quantum_amplitude_estimation(qc, event="loss>threshold").estimate

if P_loss > 0.2:
    plan = recommend_reconfiguration(routes, alt_suppliers, contracts)
```

**KPIs:** *ShockLossProb*, *ReconfigLeadTime*.

---

## 7) INS-07 — Aseguramiento de valor (Estado de valor + QAE)

**Base:** Lo que importa a CEO/CFO: **ingresos, costes, riesgos** (la tecnología es un medio).&#x20;

**Idea:** Estado con amplitudes proporcionales a $\Delta$ ingresos, $\Delta$ coste, $\Delta$ riesgo, $\Delta$ CO₂; **QAE** para expectativa de valor.

**Pseudocódigo (estilo Qiskit):**

```python
state = encode_value_components(delta_revenue, delta_cost, delta_risk, delta_co2)
E_value = quantum_amplitude_estimation(state, event="value>0").estimate
decision = "GO" if E_value > 0.0 else "REVISE"
```

**KPIs:** *NPV\_delta*, *TCO\_delta*, *Risk\_delta*, *CO2eq\_reduction*.

---

## 8) Datos, Integración y Validación

**Fuentes mínimas:** ERP/MES/WMS/TMS/SRM, IoT, contratos, riesgos país/clima.&#x20;
**Integración:** QAUDIT (ledger), DT-TRACE (*digital thread*), QPU-910/QAI-950/QSN-930 (ICDs).
**Validación (resumen):**

* **Unitarias:** Dimensión/condicionamiento Hamiltonianos/QUBO; sensibilidad $\lambda$.
* **Trust (INS-02):** estabilidad ≥ 0.80; reproducibilidad (≥ 3 *seeds*); *model cards* & *datasheets*.&#x20;
* **E2E:** *FillRate* ≥ 0.95 (INS-03), *ShockLossProb* ≤ 0.20 y reconfig ≤ 7 días (INS-06).

---

## 9) Enlaces UTCS y nomenclatura (ejemplos)

```yaml
utcs_binding_examples:
  - id: "SICOCA-INS-01"
    utcs_path: "SC/STR/QOPT"
    circuit: "QAOA-MO-MaxCut"
    kpis: ["ResilienceIndex", "TCO", "CO2eq_reduction"]
  - id: "SICOCA-INS-02"
    utcs_path: "AI/GOV/TRUST"
    circuit: "QAOA-with-penalties"
    kpis: ["Stability", "FairnessScore"]
  - id: "SICOCA-INS-03"
    utcs_path: "SC/PLAN/DEM"
    circuit: "QUBO-Inventory + QAE"
    kpis: ["FillRate", "StockoutProb", "TotalCost"]
  - id: "SICOCA-INS-04"
    utcs_path: "SC/SUP/NET"
    circuit: "SWAP-Similarity + QAOA-Selection"
    kpis: ["SupplierDiversity", "PortfolioRisk", "OTIF"]
  - id: "SICOCA-INS-05"
    utcs_path: "AI/HIL/OPR"
    circuit: "Param-Ansatz-VQE"
    kpis: ["TimeToDecision", "AcceptanceRate"]
  - id: "SICOCA-INS-06"
    utcs_path: "SC/RSK/FWD"
    circuit: "Hybrid-QMC + QAE"
    kpis: ["ShockLossProb", "ReconfigLeadTime"]
  - id: "SICOCA-INS-07"
    utcs_path: "FIN/KPI/Q"
    circuit: "ValueAggregator + QAE"
    kpis: ["NPV_delta", "TCO_delta", "Risk_delta", "CO2eq_reduction"]
```

---

## 10) Referencias

* Rol estratégico, confianza y 3 requisitos de IA (**relevante**, **responsable**, **confiable**).&#x20;
* Cobertura *end-to-end*, IoT y planificación/inspección.&#x20;
* Proveedores en el centro; *bionic supply chain*.&#x20;
* Anticipación regulatoria/geopolítica; permacrisis.&#x20;


