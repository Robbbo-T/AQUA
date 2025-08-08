# AMPEL360 BWB-Q100 — Release v1.0

**Vector:** LH₂ **fuel-cell electric** (PEM baseline)
**FCS @ EIS:** **Classical DAL-A primary**, **FbQW quantum augmentation only** (no safety credit)
**This folder:** Authoritative **v1.0** documentation set for the BWB-Q100 program.

## Contents (docs/)

* **PDC** — [`AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md`](docs/AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md)
  Program definition: mission, scope, posture, decisions, milestones.
* **SRS** — [`AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md`](docs/AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md)
  System requirements (L0/L1) with acceptance criteria.
* **SAD** — [`AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md`](docs/AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md)
  Architecture: energy chain (LH₂→PEM→HVDC→inverters→props), avionics/FCS, thermal, ICDs.
* **CCP** — [`AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md`](docs/AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md)
  Certification & safety planning (ARP4754A/ARP4761/DO-178C/DO-254/DO-160/DO-326A).
* **VVP** — [`AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md`](docs/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md)
  Verification & validation strategy, benches, HIL/SIL, evidence plan.
* **RTM** — [`AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md`](docs/AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md)
  Trace matrix linking PDC→SRS→SAD→VVP (bi-directional).
* **KPI** — [`AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md`](docs/AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md)
  Initial KPI set (safety, efficiency, dispatch, crypto budget, twin correlation).

## How to use (reading order)

1. **PDC** → program baseline and posture.
2. **SRS** → confirm L0/L1 requirements.
3. **SAD** → review architecture & ICDs against SRS.
4. **KPI** → align targets and measurement.
5. **VVP** → map verification to requirements.
6. **RTM** → check end-to-end traceability.
7. **CCP** → align certification & safety activities.

## Integrity & evidence

* Artefact hashes are anchored in the QAUDIT ledger:
  `AQUA/evidence/AQUART-EVID-CHAIN-DATA-LEDGER-qaudit_main-v1.0.jsonl`
* If a release ZIP is provided (optional): `AMPEL360_BWB-Q100_DocSet_v1.0.zip`
  verify with `sha256sum` and compare to the ledger entry.

## Certification posture (v1.0)

* **Primary control:** Classical FCS up to DAL-A; quantum channel is **augmentation only** at EIS.
* **Security:** PQC profiles (`nist_l3` default; `nist_l5` for roots of trust); crypto overhead on protected control paths **≤ 5%** loop period.
* **Hydrogen safety:** Ground/air scenarios tracked in CCP; verification cards in VVP.

## Notes

* “Latest” pointer for this program: `releases/latest.pointer` → `v1.0`.
* Adjacent folders *(if present in this release)*: `plans/`, `models/`, `tests/`, `evidence/`, `s1000d/`.

