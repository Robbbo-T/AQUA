# AMPEL360 BWB-Q100 — Models (v1.0)

**Vector:** LH₂ **fuel-cell electric** (PEM baseline)  
**FCS @ EIS:** **Classical DAL-A primary**, **FbQW quantum augmentation only** (no safety credit)

This folder contains **analysis stubs** used for early trades and V&V planning.  
> ⚠️ Non-flight, non-production code. Results are indicative only and must be validated per VVP.

---

## Contents
- **Aerodynamic model (stub, MATLAB/Octave)** — [`AQUART-AIR-ACFT-CODE-MODEL-aerodynamic-v1.0.m`](AQUART-AIR-ACFT-CODE-MODEL-aerodynamic-v1.0.m)  
  Parametric BWB lift/drag/moment surfaces & trim sweeps (coarse fidelity).
- **Propulsion simulation (stub, Python)** — [`AQUART-AIR-ACFT-CODE-SIM-propulsion-v1.0.py`](AQUART-AIR-ACFT-CODE-SIM-propulsion-v1.0.py)  
  LH₂→PEM→HVDC→inverter→motor chain; efficiencies, thermal placeholders.

---

## Run quickstarts

### 1) Aerodynamic model (`.m`)
MATLAB **o** GNU Octave:
```matlab
% from repo root or this folder
cd('AQUA/domains/AIR_CIVIL_AVIATION/aircraft/BWB-Q100/releases/v1.0/models');
results = AQUART_AIR_ACFT_CODE_MODEL_aerodynamic_v1_0();  % returns struct
save('out/aero_stub_v1.0.mat','results');  % optional
````

### 2) Propulsion sim (`.py`)

Python 3.10+:

```bash
cd AQUA/domains/AIR_CIVIL_AVIATION/aircraft/BWB-Q100/releases/v1.0/models
python3 AQUART-AIR-ACFT-CODE-SIM-propulsion-v1.0.py --export out/propulsion_stub_v1.0.json
```

> Dependencias mínimas; si usas el repo global: `pip install -r AQUA/AQUART-MGMT-PY-CONF-REQUIREMENTS-dependencies-v3.2.txt`

**Outputs (suggested):** write to local `out/` (git-ignored) and reference selected artefacts in `../evidence/` per VVP.

---

## Interfaces & assumptions (v1.0)

* **Aero stub:** quasi-steady, ISA std, cruise/TO/LD configs (TBR), simple BWB polars.
* **Propulsion stub:** scalar chain efficiencies; HVDC envelope **1.5–3.0 kVdc (TBR)**; PEM thermal nodes placeholders; crypto overhead budget **≤ 5%** loop on protected paths (ref. KPI).

---

## Where this is used

* **SAD** trades & ICD sanity.
* **VVP** test card scaffolding and acceptance thresholds.
* **RTM** links from SRS L0/L1 to preliminary analyses.

Keep the `docs/` set open:

* **PDC** — [`../docs/AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md)
* **SRS** — [`../docs/AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md)
* **SAD** — [`../docs/AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md)
* **VVP** — [`../docs/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md)
* **RTM** — [`../docs/AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md)
* **KPI** — [`../docs/AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md`](../docs/AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md)

---

## Versioning & evidence

* UTCS IDs embedded in filenames; update `-vX.Y` on changes.
* Anchor hashes/signatures in **QAUDIT**:
  `AQUA/evidence/AQUART-EVID-CHAIN-DATA-LEDGER-qaudit_main-v1.0.jsonl`

---

## Quick checks

* [ ] Scripts run and produce deterministic outputs with fixed seeds.
* [ ] Assumptions documented in SAD; thresholds aligned to KPI.
* [ ] Any figures/tables exported to `../evidence/` and referenced in VVP cards.

---

## File index

```
models/
├─ AQUART-AIR-ACFT-CODE-MODEL-aerodynamic-v1.0.m
├─ AQUART-AIR-ACFT-CODE-SIM-propulsion-v1.0.py
└─ README.md
```

**Maintainer:** Systems Analysis Lead · **Owner:** Amedeo Pelliccia

```

---

### Commit
```

docs(bwb-q100): add models/README.md (aero model + propulsion sim stubs)

````
```bash
git add AQUA/domains/AIR_CIVIL_AVIATION/aircraft/BWB-Q100/releases/v1.0/models/README.md
git commit -m "docs(bwb-q100): add models/README.md (aero model + propulsion sim stubs)"
git push
````
