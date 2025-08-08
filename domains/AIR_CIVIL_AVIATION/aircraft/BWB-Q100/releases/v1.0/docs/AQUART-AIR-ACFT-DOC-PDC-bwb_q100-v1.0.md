# AMPEL360 BWB-Q100 — Program Definition & Concept (PDC) — v1.0

```yaml
UTCS:
  DOC_ID: AQUART-PROG-ACFT-BWB-Q100-SYS-PDC-0001-SDIG-30400010000/N-A-v1.0
  TITLE: Program Definition & Concept — AMPEL360 BWB-Q100
  TYPE: PDC
  VERSION: v1.0
  STATUS: Release
  DATE: 2025-08-08
  OWNER: AQUA Technologies S.L. — AMPEL360 Program Office
  PROGRAM: BWB-Q100 (100-passenger blended-wing-body)
  CLASSIFICATION: AQUA // Internal (export-controlled TBC)
  RELATED:
    - SRS: AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md
    - SAD: AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md
    - CCP: AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md
    - VVP: AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md
    - RTM: AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md
    - KPI: AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md
    - PSAC: ../plans/AQUART-AIR-ACFT-PLAN-DO178C-psac-v1.0.md
    - PHAC: ../plans/AQUART-AIR-ACFT-PLAN-DO254-phac-v1.0.md
  QAUDIT:
    LEDGER: AQUA/evidence/AQUART-EVID-CHAIN-DATA-LEDGER-qaudit_main-v1.0.jsonl
````

**Derived from:** AQUA INITIATIVE v19.0 — Axiom-Integrated Framework
**Vector:** LH₂ **fuel-cell electric** (PEM baseline)
**FCS @ EIS:** **Classical DAL-A primary**, **FbQW quantum augmentation only** *(no safety credit)*

---

## Document Control

* **Scope:** BWB-Q100 (100 pax) liquid-hydrogen fuel-cell electric aircraft; augmentation via FbQW quantum channel; MOS/MOI aligned.
* **Source Basis:** AQUA v19.0 Axioms I–V, MOS/MOI, and POCs (Flight Optimizer, Maintenance Automation).

---

## 1. Executive Abstract

BWB-Q100 is a **100-passenger** **LH₂ fuel-cell electric** blended-wing-body platform. At EIS, primary flight controls are **classical DAL-A**. A quantum channel (**FbQW**) provides **augmentation only** (advisory/estimation), with **no actuator authority** and **no safety credit**. The lifecycle is **digital-twin-first**; S1000D Issue 5.0 IETP is generated from authoritative configuration sources. Post-quantum security (PQC) and **QAUDIT** evidence anchoring apply end-to-end.

---

## 2. Alignment with AQUA v19.0

* **Axiom I — Systemic Integrity:** Single digital thread; RTM enforced; value velocity tied to integrity metrics.
* **Axiom II — Pattern:** *Imagine → Digitize → Physicalize → Embed → Extend → Entangle → Return*. This PDC anchors the **Physicalize** stage.
* **Axiom III — Geometry of Scaling:** Platform reuse across **AMPEL360** (design), **DiQIaaS** (ops), **CaaS** (cert), **RoBoT** (manufacturing), **GAIA** (mission/traffic).
* **Axiom IV — Interface Ontology:** MOI/M.IO entangled UIs for cockpit, maintenance, and certification evidence.
* **Axiom V — Ethos:** LH₂ fuel-cell electric path chosen for zero in-flight CO₂ and low local emissions.

Portfolio context retained: **Q-100** (BWB • 100 pax • LH₂ • 2033–2036 research).

---

## 3. Goals & Non-Goals

**Goals**

* Freeze **powertrain architecture** at:
  **LH₂ → vaporizer → PEM fuel-cell stacks → HVDC bus → inverters → distributed electric propulsors** *(PEM vs. alternative FC tech is evolvable)*.
* Treat **FbQW** as **augmentation only** at EIS; classical DAL-A remains primary.
* Establish initial **quantitative KPI set** (v1.0) and launch **PSAC/PHAC** skeletons.

**Non-Goals**

* Final performance numbers, propulsor count/diameter, and tank geometry — **TBR via trades**.

---

## 4. Stakeholders & Roles

* **Program Owner:** AQUA Technologies S.L.
* **Design Authority:** AMPEL360 platform teams (structures, propulsion/energy, controls, avionics/HMI).
* **Certification:** **CaaS**; EASA primary with FAA validation; early engagement on **SC-QS-001**.
* **Operations:** **DiQIaaS** (airline/MRO); **GAIA** for fleet/airspace coordination.
* **Manufacturing:** **RoBoT** (automated composites, stack integration, final assembly).

---

## 5. Concept of Operations (CONOPS)

* **Mission:** Short/medium-haul passenger service with LH₂ fuel-cell electric powertrain; distributed electric propulsors integrated into BWB.
* **Operational Environment:** Hydrogen ground infrastructure; digital MRO; sentient decision support.
* **Digital Twin:** Authoritative baseline for design, test, and operations; evidence source for certification artefacts.

---

## 6. Product Breakdown Structure (PBS) — v1.0

* **Airframe:** BWB primary box; aeroelastic control surfaces; LH₂ bay and crash-energy management.
* **Energy & Propulsion:** LH₂ tanks; vaporizer/regas; **PEM fuel-cell stacks**; **HVDC** bus *(nominal 1–3 kVdc, exact **TBR**)*; inverters; distributed electric propulsors.
* **Flight Controls:** Classical **DAL-A** control laws; **FbQW augmentation** channel with graceful fallback; integrity monitoring.
* **Avionics & HMI:** Modular avionics; deterministic networks (e.g., TSN); MOI/M.IO cockpit.
* **Thermal & Water:** Heat rejection loops; anti-icing; water management from fuel cells.
* **Security & Identity:** PQC + QAUDIT for provenance and attestation.
* **Manufacturing & Quality:** RoBoT cells; inline NDI; digital QA.
* **Support & MRO:** DiQIaaS predictive maintenance; S1000D IETP.

---

## 7. Architecture Overview (MOS/MOI Mapping)

```mermaid
graph TB
  subgraph "MOS Eight-Layer Stack for BWB-Q100"
    L8[Business & Strategy]
    L7[Digital-Industrial Ops (RoBoT/MRO)]
    L6[Digital Twin & Simulation]
    L5[AI/Agents & Sentient Models]
    L4[Robotics & Ground Ops]
    L3[Cyber-Physical (Sensors/Edge/TSN)]
    L2[Aerospace Integration (Avionics • FCS • Propulsion)]
    L1[Quantum/PQC Foundation (FbQW • QKD • PQC)]
  end
  L8-->L7-->L6-->L5-->L4-->L3-->L2-->L1
```

---

## 8. v1.0 Changes vs v0.9

* Fuel-cell electric path selected as **baseline** (was generic LH₂ conversion).
* **FbQW augmentation at EIS**; classical DAL-A primary clarified across **SRS/SAD/CCP**.
* Added **Quantitative KPI Set (v1.0)** and **PSAC/PHAC** skeletons.
* Expanded hydrogen safety and thermal/water management sections.

---

## 9. Roadmap (extract)

* **Pre-apps & SC-QS-001 engagement:** 2026-01 → 2026-12
* **PDR:** 2027-06 • **CDR:** 2029-06 • **First Flight:** 2032-01 • **EIS:** 2036-01

---

## 10. KPIs (Level-0 Summary, v1.0)

See full set → **KPI**: [AQUART-AIR-ACFT-DOC-KPI-initial\_targets-v1.0.md](AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md)

* **Safety:** Catastrophic ≤ **1×10⁻⁹ / FH** (aircraft level).
* **Dispatch reliability:** ≥ **99.5%** @ EIS+24; ≥ **99.7%** @ EIS+60.
* **Energy efficiency (cruise, tank→shaft):** **≥ 40%** (TBR 38–45%).
* **Crypto overhead (protected control paths):** **≤ 5%** of loop period.
* **Twin correlation (acceptance):** Prop power ±**5%**; dyn. response ±**10%**; thermal nodes ±**5 °C**.
* **Manufacturing yield (LRIP composites):** **≥ 85%** (≥95% at maturity).

---

## 11. Risks & Mitigations (Top-5)

| ID | Risk                                     | Impact | Likelihood |    Owner   | Mitigation                                                                                                                                           | Residual |
| -: | ---------------------------------------- | :----: | :--------: | :--------: | ---------------------------------------------------------------------------------------------------------------------------------------------------- | :------: |
| R1 | HVDC nominal not converged (1–3 kVdc)    |    H   |      M     | ENG-ENERGY | Time-box trade; shortlist 1.5/2.0/3.0 kVdc; freeze @ **PDR**                                                                                         |     L    |
| R2 | PEM thermal margin shortfall             |    H   |      M     |  ENG-THERM | Early thermal rig; +10% HX; derate curves; VVP cards ([VVP §Test Benches & Cards](AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md#test-benches--cards)) |     L    |
| R3 | PQC bursts exceed loop budget            |    M   |      M     |  ENG-AVSEC | Cap ≤5%; HW offload; budget tests; degrade to MAC-only where allowed                                                                                 |     L    |
| R4 | FbQW jitter reduces usefulness           |    M   |      M     |   ENG-FCS  | Async advisory bus; deadlines; drop-late policy; **no safety credit**                                                                                |     L    |
| R5 | LH₂ infra availability at pilot airports |    M   |      M     |     OPS    | Airport pilots; mobile tank farm; phased ops plan                                                                                                    |     M    |

*Trigger:* Red if **Impact=H** & **Likelihood≥M** for >2 sprints → escalate to Program Board.

---

## 12. Certification Posture & Compliance Map (v1.0)

* **Lifecycle:** ARP4754A development assurance; ARP4761 safety assessment (FHA → PSSA → SSA).
* **Software:** DO-178C up to **DAL-A** (primary FCS & monitors). See **PSAC** →
  [AQUART-AIR-ACFT-PLAN-DO178C-psac-v1.0.md — §Timing & Crypto Budgets](../plans/AQUART-AIR-ACFT-PLAN-DO178C-psac-v1.0.md#timing--crypto-budgets)
* **Hardware:** DO-254 up to **DAL-A** (FCC/complex logic). See **PHAC** →
  [AQUART-AIR-ACFT-PLAN-DO254-phac-v1.0.md — §Environmental & Derating (DO-160/EEE)](../plans/AQUART-AIR-ACFT-PLAN-DO254-phac-v1.0.md#environmental--derating-do-160eee)
* **Environmental:** DO-160 categories **TBR** per equipment location/mission.
* **Security:** DO-326A/ED-202A baseline; **PQC** profiles (`nist_l3` default; `nist_l5` roots-of-trust).
* **Hydrogen:** Early engagement on **SC-QS-001** (pre-apps); hazards in **CCP** →
  [AQUART-AIR-ACFT-DOC-CCP-easa\_plan-v1.0.md — §Hydrogen Safety Case](AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md#hydrogen-safety-case), evidence via **VVP** →
  [AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md — §Test Benches & Cards](AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md#test-benches--cards).
* **Quantum:** FbQW as **augmentation only** at EIS *(no actuator authority; no safety credit)*.

---

## 13. Interfaces (abbrev.) & ICD Refs

* **Energy chain:** LH₂ tanks → vaporizer/regas → **PEM stacks** (flow/press/temp) → **HVDC bus** (V/I/telemetry).
* **Propulsion control:** HVDC → inverters (command/telemetry) → motors.
* **Avionics/FCS:** Sensors/actuators over deterministic networks (AFDX/TSN/CAN-FD mix **TBR**), PQC wrappers per DO-326A.
* **FbQW channel:** Advisory vectors + confidence + deadlines on async bus; **no direct actuator path**.
* Full ICDs live in **SAD** annexes →
  [AQUART-AIR-ACFT-DOC-SAD-bwb\_q100-v1.0.md — §Interfaces & ICD Annexes](AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md#interfaces--icd-annexes)

---

## 14. Assumptions & Constraints

* **Regulatory:** EASA CS-25 base with H₂ special conditions **TBR**; FAA validation expected.
* **Ops profile:** Short/medium-haul; duty cycles **TBR**.
* **Infra:** LH₂ ground support at pilot airports; compliant storage/handling.
* **Supply:** Aviation-grade PEM stacks; dual-vendor strategy.
* **Schedule:** PDR 2027-06; CDR 2029-06; First Flight 2032-01; EIS 2036-01 (subject to change control).

---

## 15. Governance, Traceability & Evidence

* **UTCS** naming/headers across all artefacts.
* **RTM** maintains PDC→SRS→SAD→VVP links →
  [AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md](AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md)
* **QAUDIT** ledger anchors hashes/signatures →
  `AQUA/evidence/AQUART-EVID-CHAIN-DATA-LEDGER-qaudit_main-v1.0.jsonl`
* **Tool qual (DO-330):** declare **TQL** for safety-relevant tools in **PSAC/PHAC**.

---

## 16. Open TBR/TBD (extract)

|         ID | Item                       | Owner      | Needed by | Reference                                                                                                                                                                                           |
| ---------: | -------------------------- | ---------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TBR-01** | HVDC nominal (1–3 kVdc)    | ENG-ENERGY | **PDR**   | [SAD §Energy & Propulsion](AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md#energy--propulsion) · [PSAC §Timing & Crypto Budgets](../plans/AQUART-AIR-ACFT-PLAN-DO178C-psac-v1.0.md#timing--crypto-budgets) |
| **TBR-02** | Propulsor count/diameter   | ENG-PROP   | PDR       | [SAD §Propulsion (Distributed Electric)](AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md#propulsion-distributed-electric)                                                                                  |
| **TBR-03** | DO-160 categories per LRUs | ENG-ENV    | CDR       | [PHAC §Environmental & Derating (DO-160/EEE)](../plans/AQUART-AIR-ACFT-PLAN-DO254-phac-v1.0.md#environmental--derating-do-160eee)                                                                   |
| **TBR-04** | FbQW bench/HIL cards       | ENG-FCS    | PDR       | [VVP §Test Benches & Cards](AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md#test-benches--cards)                                                                                                       |
| **TBR-05** | PQC perf. budgets per link | ENG-AVSEC  | PDR       | [PSAC §Timing & Crypto Budgets](../plans/AQUART-AIR-ACFT-PLAN-DO178C-psac-v1.0.md#timing--crypto-budgets)                                                                                           |

---

## 17. References

* **Docs (this release):** PDC (this), SRS, SAD, KPI, VVP, RTM, CCP — all v1.0.
* **Standards:** ARP4754A, ARP4761, DO-178C, DO-254, DO-160, DO-326A/ED-202A, DO-330, S1000D Issue 5.0.
* **AQUA v19.0:** Axioms I–V, MOS/MOI, Ex-AGI rationale.

---

## Change Log

| Version | Date       | Author            | Notes                                                                                                                |
| :------ | :--------- | :---------------- | :------------------------------------------------------------------------------------------------------------------- |
| v1.0    | 2025-08-08 | A. Pelliccia (PO) | Baseline PDC. LH₂ fuel-cell baseline; **FbQW augmentation-only** @ EIS; KPIs seeded; PSAC/PHAC skeletons referenced. |

```

**Commit suggestion**
```

docs(bwb-q100): rewrite PDC v1.0 with hyperlinkable cross-refs and UTCS header

```

Want me to also add the **anchor-check CI** we drafted so PRs fail if someone renames a linked heading?
```
