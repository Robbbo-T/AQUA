# AMPEL360 BWB-Q100 — Plans (v1.0)

**Vector:** LH₂ **fuel-cell electric** (PEM baseline)  
**FCS @ EIS:** **Classical DAL-A primary**, **FbQW quantum augmentation only** (no safety credit)

This folder contains the **certification planning skeletons**:

- **PSAC (DO-178C)** — [`AQUART-AIR-ACFT-PLAN-DO178C-psac-v1.0.md`](AQUART-AIR-ACFT-PLAN-DO178C-psac-v1.0.md)  
  Software lifecycle, DALs, verification, CM, SQA, tools (DO-330).
- **PHAC (DO-254)** — [`AQUART-AIR-ACFT-PLAN-DO254-phac-v1.0.md`](AQUART-AIR-ACFT-PLAN-DO254-phac-v1.0.md)  
  Hardware lifecycle, DALs, verification (sim/formal/bench), CM/QA, environmental/derating.

---

## Reading order
1. **PSAC (DO-178C)**  
2. **PHAC (DO-254)**

Keep the `docs/` set open while reading:
- **PDC** — [`../docs/AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md)  
- **SRS** — [`../docs/AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md)  
- **SAD** — [`../docs/AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md)  
- **CCP** — [`../docs/AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md)  
- **VVP** — [`../docs/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md)  
- **RTM** — [`../docs/AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md)  
- **KPI** — [`../docs/AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md)

---

## Dependencies (trace-in / trace-out)

| Plan | Pulls from (inputs) | Pushes evidence to (outputs) |
|:--|:--|:--|
| **PSAC** | SRS · SAD · VVP · CCP · RTM | `../tests/` · `../evidence/` · QAUDIT ledger |
| **PHAC** | SAD · VVP · CCP | `../tests/` · `../evidence/` · QAUDIT ledger |

QAUDIT ledger: `AQUA/evidence/AQUART-EVID-CHAIN-DATA-LEDGER-qaudit_main-v1.0.jsonl`

---

## Deliverables produced by these plans
- DO-178C / DO-254 **compliance matrices** (objective → evidence).
- **SOI** schedule (DO-178C) / **stage reviews** (DO-254).
- **Configuration baselines** & reproducible builds (hashes into QAUDIT).
- **Anomaly management** workflow tied to RTM closure.

---

## Fill-next (v1.0 → v1.1)
**PSAC**
- Finalize DALs per SSA; lock toolchain & TQL (DO-330).
- Define verification budgets (MC/DC for DAL-A, etc.) and independence.
- Timing/crypto benches to enforce **≤ 5%** loop budget on protected paths.
- FbQW stays **DAL-E** (advisory only, no actuator authority).

**PHAC**
- Confirm HW items & DALs (e.g., FCC-FPGA DAL-A).
- HDL standards (CDC/resets/safe states) & coverage targets (sim/formal/element).
- DO-160 categories; HVDC creepage/clearance; partial discharge testing.
- Tool assessment (lint/CDC/formal, synthesis/P&R, simulators) + TQL/confidence.

---

## Quick links
↩︎ [Back to v1.0 root](..) · [docs](../docs/) · [models](../models/) · [tests](../tests/) · [evidence](../evidence/) · [s1000d](../s1000d/)

---

## File index
```

plans/
├─ AQUART-AIR-ACFT-PLAN-DO178C-psac-v1.0.md
└─ AQUART-AIR-ACFT-PLAN-DO254-phac-v1.0.md

```

**Maintainer:** Program Certification Lead · **Owner:** Amedeo Pelliccia
