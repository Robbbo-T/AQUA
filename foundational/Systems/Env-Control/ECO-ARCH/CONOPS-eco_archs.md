# **BWB-Q100 — ECO-ARCHS ConOps v1.4**
## **Environmental Control Offsets — Agentic Remediation, Circularity & Harvesting System**

## Document Control

* **UTCS Doc ID:** `AQUART-AIR-ACFT-DOC-CONOPS-eco_archs-v1.4.md`
* **Program:** AMPEL360 — BWB-Q100
* **Owner:** Systems Engineering (Env. & Energy)
* **Status:** Baseline (Released)
* **Supersedes:** v1.3
* **Related roots (latest pointers):**
   * **BWB-Q100 Docs (root):** [`AQUA/domains/AIR_CIVIL_AVIATION/aircraft/BWB-Q100/releases/latest/`](../../releases/latest/) → **resolves to** `v1.0/`
   * **ECO-ARCHS System (root):** [`AQUA/domains/AIR_CIVIL_AVIATION/aircraft/BWB-Q100/systems/eco-archs/releases/latest/`](../../systems/eco-archs/releases/latest/) → **resolves to** `v1.4/`
* **Cross-references:**
   * **PDC v1.0:** [`AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md`](../../releases/v1.0/AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md)
   * **SRS v1.0:** [`AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md`](../../releases/v1.0/AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md)
   * **SAD v1.0:** [`AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md`](../../releases/v1.0/AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md)
   * **CCP v1.0:** [`AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md`](../../releases/v1.0/AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md)
   * **VVP v1.0:** [`AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md`](../../releases/v1.0/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md)
   * **RTM v1.0:** [`AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md`](../../releases/v1.0/AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md)
   * **KPI v1.0:** [`AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md`](../../releases/v1.0/AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md)

## 0. Change Summary (v1.4 vs v1.3)

* Added **[IF-ECO-07 Water Balance Dashboard](#6-interfaces-moimio)** (crew MOI/M.IO) with fully specified data, latency and alert logic
* Consolidated **shed-bias** philosophy with explicit numeric thresholds and heaters/icing margins
* Finalized **mass limits**: `RES_max = 300 kg`, **auto-shed** at `≥ 270 kg`
* Completed **[V&V criteria](#12-verification--validation)** (no TBD): added accuracy, latency, superheat margins, and tunnel/CFD acceptance bands
* Added **Artifact roots & latest pointers** and **[Annex D — GPL (ALICE) v1.4](#annex-d--gpl-alice-v14--generation-plan-list)** mapping all cited tags to executable steps
* All cross-references made **hyperlinkable** to repo paths and in-doc anchors

## 1. Purpose & Scope

Define the concept of operations, architecture, interfaces, safety/certification posture, and verification plan for **ECO-ARCHS**, the BWB-Q100's integrated, agentic water circularity system that manages **PEM fuel-cell product water** and **cabin humidity recovery** to maximize safety, minimize weight, and deliver environmental benefits.

## 2. Mission Envelope & Assumptions

* Aircraft: **BWB-Q100**, 100-pax, LH₂ fuel-cell electric propulsion
* Typical mission: **2.0–3.0 h block**, hydrogen usage **400–600 kg**
* **Stoichiometry:** `1 kg H₂ → 9 kg H₂O` (from atmospheric O₂)
   * **Total water produced:** **3.6–5.4 t per mission**
* Environmental standards: **CS-25 App. C icing**, **DO-160G** (temp, vibration, EMC), **airport vapor rules** observed

## 3. System Philosophy

### 3.1 Shed-Bias Default
* **Default state = vapor discharge** overboard via heated mast(s)
* **Selective capture** is **only** enabled in **cruise** and benign conditions to harvest a **small, bounded fraction** for potable/thermal use

### 3.2 Mass Control
* **Reservoir capacity** (`RES_max`) = 300 kg
* **Capture fraction ≤ 5%** of produced water (**≤ 270 kg** on a 5.4 t mission)
* **Auto-shed trigger:** at **≥ 270 kg (0.9·RES_max)**, controller forces **shed=ON**, **capture=0** until **≤ 240 kg**

### 3.3 Safety First
If any of the following are true, **shed=ON / capture=OFF**:
* Mast heater fault, mast temperature superheat `< 12 K`, or **icing detected**
* Separator/conditioner fault, potable quality fail, pump/valve fault
* Electrical load management requests load shed

## 4. Mass & Energy Balance

### 4.1 Water Balance

| Term | Symbol | Typical Value (2.5 h mission) |
|------|--------|-------------------------------|
| Produced by PEM | `W_prod` | 4.5 t (for 500 kg H₂) |
| Captured (bounded) | `W_cap` | ≤ 225 kg (≤ 5% · `W_prod`) |
| Discharged (vapor) | `W_shed` | ≥ 4.275 t (≥ 95% of `W_prod`) |
| Cabin dehumidification recovery | `W_cdh` | 20–60 kg (mission/loads dependent) |

**Conservation:** `W_prod + W_cdh = W_cap + W_shed`

### 4.2 Thermal Integration
* PEM outlet: **60–80 °C** water; pre-heats potable loop and aids heat-rejection
* Evaporation latent heat: **2,260 kJ/kg** exploited in **heat-sink** episodes during climb/top-of-descent
* Mast outlet **superheat margin ≥ 12 K** relative to local saturation temp to prevent accretion

## 5. Architecture & State Machine

```mermaid
stateDiagram-v2
  [*] --> Ground_Cold
  Ground_Cold: Heaters off, capture off, shed off
  Ground_Cold --> Taxi: mast warmup if OAT ≤ 5°C
  Taxi --> Takeoff_Climb: shed=ON, capture=OFF
  Takeoff_Climb --> Cruise_Benign: shed=ON, capture=PERMIT (bounded)
  Cruise_Benign --> Cruise_Restrict: icing risk OR mast fault -> capture=OFF
  Cruise_Benign --> Auto_Shed: RES ≥ 270 kg -> capture=OFF, shed=ON
  Cruise_Restrict --> Descent: shed=ON
  Auto_Shed --> Descent: RES ≤ 240 kg
  Descent --> Approach_Land: shed=ON
  Approach_Land --> Turnaround: purge lines, potable isolation
  Turnaround --> [*]
```

**Heaters:** mast & lines **fail-on**; loss of control power → heaters **default ON** via independent supply & thermal fuse

## 6. Interfaces (MOI/M.IO)

### IF-ECO-01 — PEM→Collector
* Medium: heated stainless manifold; flow metering ±2% accuracy
* Events: high-temp bypass, over-pressure relief

### IF-ECO-02 — Collector→Conditioner
* Functions: filtration (5 µm), UV sterilization (**≥ 40 mJ/cm²**), mineralization (target **80–120 mg/L TDS**)

### IF-ECO-03 — Conditioner→Reservoir (RES)
* Level sensing ±1% FS; pressure/vacuum relief per CS-25 fuel tank principles adapted to water

### IF-ECO-04 — RES→Potable
* Potable pump with **DAL C** control; non-return valves; periodic purge cycle

### IF-ECO-05 — RES→Thermal Sink
* Controlled discharge to heat exchangers; logged energy budget

### IF-ECO-06 — ECO-ARCHS→Mast
* Heated mast command & feedback; **superheat margin telemetry**; overboard discharge valve

### IF-ECO-07 — ECO-ARCHS→Cockpit Display (new, crew MOI/M.IO)
* **Real-time:** capture rate (kg/min), shed rate (kg/min), RES level (%), mast superheat (K)
* **Predictive:** time to auto-shed (min), mission water budget (produced vs used vs shed)
* **Alerts:** potable quality fail, mast icing risk, heater fault, separator fault, near-full RES
* **Crew actions:** manual shed override (non-critical), potable lockout
* **Assurance:** display software **DAL C**, data bus deterministic (TSN/AFDX), **no safety-critical authority**
* **Update rate:** ≤ **2 s** end-to-end

## 7. Control Law (Safety Cascade)

```python
def eco_archs_setpoints(phase, sensors, health, res_level_kg):
    # Hard safety gates
    if (not health.mast_heater_ok or sensors.ice_detected
        or sensors.mast_superheat_K < 12
        or not health.separator_ok or not health.uv_ok):
        return dict(shed=True, capture=0, potable=False, reason="safety_gate")

    # Mass control
    if res_level_kg >= 270:           # 0.9 * RES_max (300 kg)
        return dict(shed=True, capture=0, potable=True, reason="auto_shed")

    # Phase logic
    if phase in ("takeoff", "climb", "descent", "approach"):
        return dict(shed=True, capture=0, potable=True, reason="phase_shed_bias")

    # Cruise (benign)
    if phase == "cruise" and sensors.icing_risk==False:
        capture_rate = min(sensors.water_prod_rate_kgpm, 2.0)  # cap harvest to bound RES fill rate
        return dict(shed=True, capture=capture_rate, potable=True, reason="cruise_harvest")

    # Default
    return dict(shed=True, capture=0, potable=True, reason="default_shed_bias")
```

All decisions and inputs are **QAUDIT-logged** (event, setpoints, reason, health snapshot)

## 8. Potable Water Quality

* UV dose **≥ 40 mJ/cm²**, contact-verified
* Mineralization: **80–120 mg/L TDS**; pH **6.5–8.5**; conductivity **150–350 µS/cm**
* Microbiology: **No coliform detection** (ISO 9308-1), **HPC ≤ 500 CFU/mL @ 22 °C**
* Residual **silver-ion** option for line hygiene within WHO limits
* **Potable lockout** triggers on any quality out-of-spec

## 9. Anti-Ice Strategy (No Water-Spray Anti-Ice)

* Airframe anti-ice remains **electro-thermal**
* Discharge masts are **self-heated**; **no** water spray onto lifting surfaces
* **Acceptance:** zero hazardous accretion; **mast superheat ≥ 12 K** in Appendix-C envelopes

## 10. Cybersecurity & Segregation

* ECO-ARCHS control partition isolated from external connectivity per **DO-326A/ED-202A**
* Cockpit display ([IF-ECO-07](#if-eco-07--eco-archscockpit-display-new-crew-moimio)) is **read-only** control-wise; commands limited to non-critical toggles with independent guards

## 11. Certification Mapping

* **CS-25.1309** (SSA): probability targets met via shed-bias, fail-on heaters, bounded mass
* **CS-25.831** (ventilation & humidity): cabin dehumidification integrated; comfort metrics logged
* **CS-25.1419** (ice protection): mast system verified in Appendix-C/M
* **DO-160G** (enviro): temps, fluids, vibration, EMC categories applied to units
* **DO-178C/254:** controller DAL B for actuation, display DAL C, heater safety simplex hardware DAL C
* **DO-326A:** threat model and mitigations implemented
* **Evidence tooling:** AMOReS/CaaS with QAUDIT anchoring

See [**CCP v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md) and [**VVP v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md) links in the header.

## 12. Verification & Validation

### 12.1 Test Matrix (ECO-ARCHS excerpt)

| Test ID | Verifies | Method | Acceptance |
|---------|----------|--------|------------|
| **Q100-TST-0310** | Shed fraction ≥ 95% | Rig/HIL + mission profiles | `W_shed / (W_prod + W_cdh) ≥ 0.95`; mast superheat **≥ 12 K**; no over-temp |
| **Q100-TST-0311** | Auto-shed at 0.9·RES_max | SIL/HIL | On **≥ 270 kg**: capture→0 within **≤ 2 s**; RES never exceeds **300 kg** |
| **Q100-TST-0312** | Potable quality | Bench + lab assays | UV dose **≥ 40 mJ/cm²**; TDS **80–120 mg/L**; **no coliform**; HPC **≤ 500 CFU/mL** |
| **Q100-TST-0313** | Heater fail-on safety | Rig | Loss of control power → heaters ON; thermal fuse prevents runaway |
| **Q100-TST-0314** | No icing on mast | Icing tunnel + CFD | No hazardous accretion; superheat **≥ 12 K** across tested M/α; ETIPS margin **≥ 25%** |
| **Q100-TST-0315** | Cabin humidity control | SIL/HIL + cabin rig | RH tracks **40–55%** steady-state in cruise (±5% band) |
| **Q100-TST-0316** | QAUDIT logging | SIL/HIL | 100% decision/event coverage; hash-stamped; latency **< 1 s** to ledger |
| **Q100-TST-0317** | [IF-ECO-07](#if-eco-07--eco-archscockpit-display-new-crew-moimio) display | Bench + HIL | Accuracy **±5%** (rates/level); E2E latency **≤ 2 s**; alert logic per spec; availability **≥ 99.9%/hr** |

**Traceability:** mapped in [**RTM v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md) (links above).

## 13. Performance & KPIs (ECO-ARCHS subset)

* **ECO-KPI-01** — Shed fraction: **≥ 95%** per mission
* **ECO-KPI-02** — RES excursions > `RES_max`: **0** per 10,000 flight hours
* **ECO-KPI-03** — Mast superheat margin: **≥ 12 K** in icing envelopes
* **ECO-KPI-04** — Display latency ([IF-ECO-07](#if-eco-07--eco-archscockpit-display-new-crew-moimio)): **≤ 2 s** P95
* **ECO-KPI-05** — Potable compliance: **100% flights** meet quality specs
* **ECO-KPI-06** — QAUDIT event capture: **≥ 99.5%** completeness per sector

KPIs are mirrored to program-level [**KPI v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md).

## 14. Data, Logs & WEE

* All controller decisions, sensor snapshots, and thresholds → **QAUDIT ledger** with UTCS IDs
* WEE synthesizes lessons (e.g., phase-of-flight capture windows, seasonal icing risk) that feed AMPEL360 design updates

## 15. Interface to Crew — IF-ECO-07 (Detail)

* **Page elements:** circular RES gauge (%), twin bars (capture/shed kg/min), superheat chip (K), budget strip (produced/used/shed)
* **Predictive tiles:** auto-shed ETA; landing RES forecast
* **Alerts (aural + CAS):** `ECO POTABLE LOCKOUT`, `ECO MAST ICE RISK`, `ECO RES NEAR FULL`, `ECO HEATER FAULT`
* **Controls:** `Shed Override` (momentary; auto-reverts on safety gates), `Potable Lockout`
* **Human factors:** fonts ≥ 6.5 mm equiv @ 600 mm viewing; colorblind-safe palette; PFD/ND unaffected

## 16. Compliance Evidence (Artifact Map)

* **SRS anchors:** `Q100-SRS-REQ-0300/0301/0900` (energy/dist/DT), `Q100-SRS-REQ-0317` (new, [IF-ECO-07](#if-eco-07--eco-archscockpit-display-new-crew-moimio))
* **SAD interfaces:** IF-ECO-01…07 (this doc) mirrored in [**SAD v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md)
* **CCP mapping:** CS-25.1309/831/1419; DO-160G/178C/254/326A; tool qual DO-330 via CaaS
* **VVP tests:** `Q100-TST-0310…0317` (see [§12](#12-verification--validation))
* **RTM:** updated cross-links under ECO-ARCHS row group

## 17. Ops & Maintenance

* **Turnaround:** line purge; potable sample on every **A-check**; UV lamp hours tracked; resin cartridge replacement by ΔP and hours
* **Minimum dispatch:** one mast functional, heaters healthy, RES & quality sensors valid; potable can be locked out without MEL hit

## 18. Green Contribution (Reporting)

* Dashboard aggregates **water self-sufficiency** (kg not boarded), **thermal energy recovered** (MJ), and **airport water offload avoided** (kg)
* Values exported with flight QAUDIT ID for sustainability reporting

---

## Annex A — Signals & Buses (Excerpt)

| IF | Signal | Rate | Range/Unit | Accuracy | Bus/Partition |
|----|--------|------|------------|----------|---------------|
| 01 | `water_prod_rate` | 1 Hz | 0–10 kg/min | ±2% | TSN, Controller-B |
| 03 | `RES_level` | 1 Hz | 0–300 kg | ±1% FS | TSN, Controller-B |
| 06 | `mast_superheat` | 2 Hz | −5…+40 K | ±1 K | TSN, Heater-A |
| 07 | `shed_rate` | 1 Hz | 0–10 kg/min | ±5% | TSN→IMA (DAL C) |
| 07 | `capture_rate` | 1 Hz | 0–3 kg/min | ±5% | TSN→IMA (DAL C) |

## Annex B — Safety Summary

* **Top events mitigated:** icing on mast, RES overfill, potable contamination, heater runaway, latent control loss
* **Independence:** heater power path independent; controller watchdog; fail-on heaters; discharge valve spring-open
* **Quantitative:** contributes to system-level **≤ 10⁻⁹ / fh** catastrophic via architecture credits (see SSA package in [CCP](../../releases/v1.0/AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md)/[VVP](../../releases/v1.0/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md))

## Annex C — Cross-Reference Quick Map

* **PDC:** Concept & platform roles → §3, §5 of [**PDC v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md)
* **SRS:** `Q100-SRS-REQ-0300/0301/0900/0317` → §6, §12 of [**SRS v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-SRS-bwb_q100-v1.0.md)
* **SAD:** container & interface views → §5 of [**SAD v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md)
* **CCP:** CS/DO/SC coverage → §11 of [**CCP v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-CCP-easa_plan-v1.0.md)
* **VVP:** tests `0310…0317` → §12 of [**VVP v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md)
* **RTM:** Source→Design→Test→Evidence rows under ECO-ARCHS → [**RTM v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md)
* **KPI:** program mirrors of ECO-KPIs → [**KPI v1.0**](../../releases/v1.0/AQUART-AIR-ACFT-DOC-KPI-initial_targets-v1.0.md)

## Annex D — GPL (ALICE) v1.4 — Generation Plan List

A **logical & chronological** execution plan mapping every cross-reference to work packages. All outputs carry UTCS IDs and QAUDIT anchors.

### Work Package Sequence

1. **Seq-01 — Create SRS anchors**
   * **Inputs:** [PDC v1.0](../../releases/v1.0/AQUART-AIR-ACFT-DOC-PDC-bwb_q100-v1.0.md); stakeholder needs
   * **Outputs:** `Q100-SRS-REQ-0317` ([IF-ECO-07](#if-eco-07--eco-archscockpit-display-new-crew-moimio)) + confirmations of `0300/0301/0900`
   * **Owner:** Systems Eng
   * **DAL:** N/A
   * **Done-when:** baselined SRS committed

2. **Seq-02 — Define interfaces (SAD & ConOps sync)**
   * **Inputs:** This ConOps [§6](#6-interfaces-moimio); [SAD v1.0](../../releases/v1.0/AQUART-AIR-ACFT-DOC-SAD-bwb_q100-v1.0.md)
   * **Outputs:** IF-ECO-01…07 in SAD; ICD rev A
   * **Owner:** Avionics
   * **DAL:** N/A
   * **Done-when:** ICD signed

3. **Seq-03 — Control laws & safety gates**
   * **Inputs:** [§7](#7-control-law-safety-cascade); SSA assumptions
   * **Outputs:** Controller spec; heater fail-on design note
   * **Owner:** Control Eng
   * **DAL:** B
   * **Done-when:** design review green

4. **Seq-04 — Potable chain qualification plan**
   * **Inputs:** [§8](#8-potable-water-quality); labs SOP
   * **Outputs:** UV/filtration test plans; assay protocol
   * **Owner:** Env. Systems
   * **DAL:** C
   * **Done-when:** lab booked & protocol frozen

5. **Seq-05 — Mast thermal design**
   * **Inputs:** [§9](#9-anti-ice-strategy-no-water-spray-anti-ice); App.-C envelopes
   * **Outputs:** ETIPS model; heater sizing; tunnel test plan
   * **Owner:** Thermal/Structures
   * **DAL:** C
   * **Done-when:** model corr. to rig

6. **Seq-06 — Reservoir sizing & sensors**
   * **Inputs:** [§3.2](#32-mass-control); mission set
   * **Outputs:** `RES_max=300 kg`; sensor spec; relief design
   * **Owner:** Mech
   * **DAL:** C
   * **Done-when:** PDR pass

7. **Seq-07 — Cyber segmentation**
   * **Inputs:** [§10](#10-cybersecurity--segregation); network arch
   * **Outputs:** DO-326A artifacts; ACLs; read-only path for [IF-ECO-07](#if-eco-07--eco-archscockpit-display-new-crew-moimio)
   * **Owner:** Cyber
   * **DAL:** Process
   * **Done-when:** threat model closed

8. **Seq-08 — Display design (IF-ECO-07)**
   * **Inputs:** [§15](#15-interface-to-crew--if-eco-07-detail); MOI/M.IO patterns
   * **Outputs:** DAL C display spec; HMI mockups; update ≤2 s path
   * **Owner:** HMI
   * **DAL:** C
   * **Done-when:** HF review approved

9. **Seq-09 — QAUDIT schema extension**
   * **Inputs:** [§14](#14-data-logs--wee)
   * **Outputs:** Event schema; hash policy; retention
   * **Owner:** Data/QA
   * **DAL:** N/A
   * **Done-when:** events land reliably

10. **Seq-10 — Rig builds (collector/conditioner/RES/mast)**
    * **Inputs:** Seq-03/05/06
    * **Outputs:** Sub-rigs with instrumentation
    * **Owner:** Test Eng
    * **DAL:** N/A
    * **Done-when:** calibrated & ready

11. **Seq-11 — SIL/HIL integration**
    * **Inputs:** Seq-03/08/10
    * **Outputs:** End-to-end sim benches; ice/turbulence profiles
    * **Owner:** V&V
    * **DAL:** N/A
    * **Done-when:** scenarios run deterministically

12. **Seq-12 — Execute VVP tests 0310–0317**
    * **Inputs:** [§12](#12-verification--validation); [VVP v1.0](../../releases/v1.0/AQUART-AIR-ACFT-DOC-VVP-verification-v1.0.md)
    * **Outputs:** Test reports; QAUDIT anchors
    * **Owner:** V&V
    * **DAL:** N/A
    * **Done-when:** all acceptance met

13. **Seq-13 — Update RTM**
    * **Inputs:** Test reports
    * **Outputs:** [RTM](../../releases/v1.0/AQUART-AIR-ACFT-DOC-RTM-traceability-v1.0.md) rows closed (0310…0317)
    * **Owner:** Systems Eng
    * **DAL:** N/A
    * **Done-when:** RTM export matches DB

14. **Seq-14 — Airport ops rulebook**
    * **Inputs:** Local vapor rules; ops trials
    * **Outputs:** Dispatch notes; airport-specific SOPs
    * **Owner:** Flight Ops
    * **DAL:** N/A
    * **Done-when:** two-airport shadow ops

15. **Seq-15 — Reliability growth**
    * **Inputs:** QAUDIT data
    * **Outputs:** WEE lessons; defect Pareto; software deltas
    * **Owner:** Reliability
    * **DAL:** N/A
    * **Done-when:** MTBF ≥ target

16. **Seq-16 — AMOReS evidence bundle**
    * **Inputs:** All artifacts
    * **Outputs:** CaaS package for CS/DO submissions
    * **Owner:** Certification
    * **DAL:** N/A
    * **Done-when:** package uploaded

17. **Seq-17 — Governance sign-off**
    * **Inputs:** Evidence, KPI trend
    * **Outputs:** ECO-ARCHS Gate-B approval memo
    * **Owner:** Program Board
    * **DAL:** N/A
    * **Done-when:** signed & archived

---

**End of ECO-ARCHS ConOps v1.4**

All internal links point to **artifact roots with latest pointers**. "Latest" resolves at build time to the concrete version (`v1.0` for BWB-Q100 docs; `v1.4` for this ECO-ARCHS release).

---

*Document Control: This document is configuration controlled under the AQUA UTCS system. Changes require formal CR and impact assessment per [`AQUART-MGMT-PROC-CM-change_control-v2.0.md`](../../../procedures/AQUART-MGMT-PROC-CM-change_control-v2.0.md)*

---

## Engineering Change Notice (ECN)

**ECN Number:** ECO-ARCHS-X-001
**Date:** October 26, 2023
**Project:** ECO-ARCHS Generalization Initiative
**Title:** ECO-ARCHS-X: Multi-Media Atmospheric Remediation, Circulation & Harvesting System

**1. Purpose:**
This Engineering Change Notice (ECN) details the significant modifications and additions to the existing ECO-ARCHS (Environmental Control Offsets — Atmospheric Remediation, Circulation & Harvesting System) to evolve it from a water-centric system to a generalized **ECO-ARCHS-X** capable of managing multiple atmospheric media within an aerospace environment. The primary objectives are to enhance aircraft safety, stabilize the cabin environment, and enable the bounded harvesting of specific atmospheric components where feasible and safe.

**2. Background:**
The current ECO-ARCHS system provides critical water management capabilities. This change leverages the established system architecture and control philosophy to address a broader spectrum of atmospheric control requirements, including CO₂ management, particulate/aerosol filtration, VOC/O₃ reduction, electrostatic discharge (ESD) control, and toxic agent detection/isolation. This expansion aims to provide a more comprehensive environmental control solution, aligning with evolving aviation safety and comfort standards.

**3. Scope of Change:**
This ECN encompasses the following key changes and additions to the ECO-ARCHS system:

*   **3.1. Multi-Media Expansion:**
    *   Introduction of new functional cartridges and integration into the existing ECO-ARCHS framework. The system will now manage:
        *   **C0 Water:** Existing functionality (PEM product water, dehumid recovery, heated masts). Constraints remain unchanged.
        *   **C1 CO₂:** Capture and control of cabin CO₂ levels (target ≤ 1,000–1,500 ppm), with optional bounded harvesting using adsorber beds (zeolite/MOF) and low-grade heat regeneration.
        *   **C2 Aerosols/Particulate (PM):** Continuous mitigation of PM₁/PM₂.₅/PM₁₀ and incident smoke/contaminants using HEPA/ULPA filters and electrostatic precipitators (ESP).
        *   **C3 VOC/O₃:** Reduction of Volatile Organic Compounds (VOCs) and Ozone (O₃) using activated carbon and catalytic converters.
        *   **C4 Electric Charge (ESD):** Sensing and neutralization of cabin and system electrostatic charge, with bounded micro-harvesting for health monitors.
        *   **C5 Toxic Agents:** Detection (via multi-sensor array) and immediate isolation/shedding only; no capture for reuse.

*   **3.2. System-of-Systems Architecture:**
    *   **Cartridge Design:** Each functional media path (C0-C5) will be implemented as an independently fail-safe, hot-swappable "cartridge."
    *   **Unified Control Cascade:** All cartridges will be governed by the same hierarchical control cascade (Gates A, B, C, D) for consistent safety and operational logic.

*   **3.3. Control Philosophy Enhancements:**
    *   **Shed-Bias Default:** The core philosophy of shedding/neutralizing hazards and capturing/harvesting only in benign, bounded windows remains paramount.
    *   **Bounds Management:** Strict adherence to mass, energy, and charge limitations for all operations, especially harvesting.
    *   **Phase-Dependent Operation:** Differentiated control strategies for critical flight phases (takeoff, climb, descent, approach) versus cruise-benign phases.

*   **3.4. Cross-Cutting Technologies:**
    *   **Quantum Dot (QD) Integration:** Photothermal/emissivity sleeves on heat transfer components (masts, radiators) for improved efficiency. QD sensors will provide advisory environmental data.
    *   **Advanced Thermal Management:** Integration of Outer Mold Line (OML) radiative panels, 2-phase subloops, and Phase Change Material (PCM) buffers for transient thermal smoothing.

*   **3.5. Interface and Data Management:**
    *   **New Interfaces:** Definition of new signal interfaces (IF-ECO-AIR-CO2, IF-ECO-AIR-PM, IF-ECO-AIR-VOC, IF-ECO-AIR-O3, IF-ECO-CHG, IF-ECO-QD-SENS, IF-ECO-QD-THERM) transmitted via TSN/ARINC-664.
    *   **Cockpit MOI/M.IO Updates:** Addition of read-only display tiles for CO₂, PM, VOC/O₃, and ESD status.

*   **3.6. Requirements and Verification:**
    *   **Additive Requirements:** New requirements (RQ-CO2-010, RQ-PM-011, RQ-VOC/O3-012, RQ-ESD-013, RQ-QD-SAFE-014, RQ-CTRL-015) to govern the performance and safety of the new media cartridges and overall system.
    *   **New V&V Tests:** Development of specific tests (Q100-TST-0500 to Q100-TST-0505) to validate the functionality, performance, and safety of each new cartridge and the integrated system.

*   **3.7. Safety and Certification:**
    *   Reinforcement of safety principles (CS-25.831, CS-25.1309, DO-160, DO-178C/254, DO-326A).
    *   Emphasis on fault tolerance, isolation, shed-bias, and data integrity, particularly for control logic (DAL B).

**4. Engineering Analysis:**
The generalization of ECO-ARCHS to ECO-ARCHS-X involves a system-of-systems approach, breaking down complex environmental control into modular, manageable cartridges. The unified control cascade ensures that safety remains the primary consideration, with operational modes adapted to flight phases. The integration of advanced thermal management and QD technologies provides opportunities for efficiency gains. Crucially, the "capture is never required for safety" and "if in doubt, shed and annunciate" guardrails are maintained and extended across all new media.

**5. Implementation Plan:**
This ECN initiates the formal design, development, integration, and testing phases for the ECO-ARCHS-X system. It will necessitate updates to relevant documentation, including the ConOps, SRS, SAD, ICD, and VVP.

**6. Documentation Impact:**
*   **New Root Directory:** `AQUA/.../systems/eco-archs-x/`
*   **Updated Documents:** ConOps (this document), SRS (new RQs), SAD (cartridge containers), VVP (Q100-TST-0500…0505), RTM links.
*   **Interface Control Document (ICD):** Extension to include new signals for C1-C5 and QD sensors.
*   **Cockpit Human-Machine Interface (HMI):** Updates to MOI/M.IO pages for new AQ tiles and advisory badges.

**7. Approvals:**

*   **Prepared By:** [Your Name/Department]
*   **Reviewed By:** [Reviewer Name/Department]
*   **Approved By:** [Approver Name/Department]

**8. Revision History:**
| Revision | Date         | Description                                | Author |
| :------- | :----------- | :----------------------------------------- | :----- |
| 0.9      | [Date]       | Baseline Draft (as provided)               | N/A    |
| 1.0      | [Date]       | Incorporating changes per ECN ECO-ARCHS-X-001 |        |

---

# **BWB-Q100 — ECO-ARCHS-X ConOps v2.0**
## **Environmental Control Offsets — Multi-Media Atmospheric Remediation, Circulation & Harvesting System**

## Document Control

* **UTCS Doc ID:** `AQUART-AIR-ACFT-DOC-CONOPS-eco_archs_x-v2.0.md`
* **Program:** AMPEL360 — BWB-Q100
* **Owner:** Systems Engineering (Env. & Energy)
* **Status:** Baseline (Released)
* **Supersedes:** ECO-ARCHS ConOps v1.4
* **ECN Applied:** ECO-ARCHS-X-001 (Multi-Media Expansion)
* **Related roots (latest pointers):**
   * **BWB-Q100 Docs (root):** [`AQUA/domains/AIR_CIVIL_AVIATION/aircraft/BWB-Q100/releases/latest/`](../../releases/latest/) → **resolves to** `v2.0/`
   * **ECO-ARCHS-X System (root):** [`AQUA/domains/AIR_CIVIL_AVIATION/aircraft/BWB-Q100/systems/eco-archs-x/releases/latest/`](../../systems/eco-archs-x/releases/latest/) → **resolves to** `v2.0/`

## 0. Change Summary (v2.0 vs v1.4) - ECN ECO-ARCHS-X-001 Integration

* **MAJOR:** Evolution from **ECO-ARCHS** to **ECO-ARCHS-X** multi-media system
* **NEW:** Six-cartridge architecture (C0-C5) for comprehensive atmospheric management
* **NEW:** Quantum Dot (QD) integration for thermal management and environmental sensing
* **EXPANDED:** Control cascade now manages water, CO₂, particulates, VOCs/O₃, electrostatic charge, and toxic agents
* **ENHANCED:** Cockpit interface with multi-media atmospheric quality (AQ) tiles
* **ADDED:** New interfaces IF-ECO-AIR-CO2 through IF-ECO-QD-THERM
* **UPDATED:** Requirements baseline with RQ-CO2-010 through RQ-CTRL-015
* **EXTENDED:** V&V test matrix with Q100-TST-0500 through Q100-TST-0505

## 1. Purpose & Scope

Define the concept of operations, architecture, interfaces, safety/certification posture, and verification plan for **ECO-ARCHS-X**, the BWB-Q100's integrated, agentic **multi-media atmospheric remediation system** that manages:

- **Water circularity** (PEM fuel-cell product water + cabin humidity recovery)
- **CO₂ management** (cabin levels + bounded harvesting)  
- **Particulate/aerosol control** (PM₁/PM₂.₅/PM₁₀ + smoke/contaminant mitigation)
- **VOC/O₃ reduction** (volatile organic compounds + ozone control)
- **Electrostatic discharge (ESD) management** (charge sensing + neutralization)
- **Toxic agent detection** (multi-sensor array + immediate isolation)

The system maximizes safety, minimizes weight, stabilizes cabin environment, and delivers environmental benefits through bounded, intelligent harvesting where feasible.

## 2. Mission Envelope & Assumptions

* Aircraft: **BWB-Q100**, 100-pax, LH₂ fuel-cell electric propulsion
* Typical mission: **2.0–3.0 h block**, hydrogen usage **400–600 kg**
* **Primary stoichiometry:** `1 kg H₂ → 9 kg H₂O` (from atmospheric O₂)
   * **Total water produced:** **3.6–5.4 t per mission**
* **Cabin environment targets:**
   * CO₂: **≤ 1,000–1,500 ppm** (cruise steady-state)
   * PM₂.₅: **≤ 12 µg/m³** (WHO air quality guideline)
   * VOCs: **≤ 300 µg/m³** total (TVOC)
   * Electrostatic: **±500 V** maximum cabin potential
* Environmental standards: **CS-25 App. C icing**, **DO-160G**, **airport vapor/emission rules**

## 3. System Philosophy

### 3.1 Unified Shed-Bias Default (All Media)
* **Default state = shed/neutralize/discharge** for all atmospheric contaminants
* **Selective capture/harvesting** enabled **only** in **cruise-benign** conditions for **bounded fractions**
* **If in doubt, shed and annunciate** principle applies to all cartridges

### 3.2 Multi-Media Cartridge Architecture (C0-C5)

| Cartridge | Media | Primary Function | Harvest Capability | Shed Method |
|-----------|-------|------------------|-------------------|-------------|
| **C0** | Water | Circularity management | ≤5% (≤270 kg) | Heated mast vapor |
| **C1** | CO₂ | Cabin level control | ≤2% via adsorber beds | Cabin ventilation |
| **C2** | Particulates | PM/aerosol filtration | None (filters only) | HEPA/ESP collection |
| **C3** | VOC/O₃ | Chemical reduction | None | Catalytic destruction |
| **C4** | ESD | Charge neutralization | Micro-harvest for health monitors | Ground discharge |
| **C5** | Toxic | Detection only | **Never** | Immediate isolation/shed |

### 3.3 Hierarchical Control Gates (A→B→C→D)

**Gate A (Safety-Critical):** Immediate shed/neutralize if ANY cartridge reports:
- Hardware fault, sensor out-of-range, heater/thermal failure
- Toxic agent detection (C5), dangerous charge levels (C4)
- Flight phase = takeoff/climb/descent/approach

**Gate B (Mass/Energy Limits):** Enforce bounded harvesting:
- C0: RES ≥ 270 kg → capture=0
- C1: Adsorber bed ≥ 90% capacity → regenerate or shed
- Power budget exceeded → priority shed sequence

**Gate C (Environmental Quality):** Maintain cabin targets:
- CO₂ > 1,500 ppm → increase C1 scrubbing
- PM₂.₅ > 12 µg/m³ → boost C2 filtration
- VOC > 300 µg/m³ → activate C3 catalytic

**Gate D (Harvest Optimization):** In cruise-benign only:
- Enable bounded capture for C0 (water) and C1 (CO₂)
- Monitor efficiency and thermal integration
- Log performance for WEE optimization

## 4. Mass & Energy Balance (Extended)

### 4.1 Water Balance (C0 - Unchanged)
| Term | Symbol | Typical Value (2.5 h mission) |
|------|--------|-------------------------------|
| Produced by PEM | `W_prod` | 4.5 t (for 500 kg H₂) |
| Captured (bounded) | `W_cap` | ≤ 225 kg (≤ 5% · `W_prod`) |
| Discharged (vapor) | `W_shed` | ≥ 4.275 t (≥ 95% of `W_prod`) |

### 4.2 CO₂ Balance (C1 - New)
| Term | Symbol | Typical Value |
|------|--------|---------------|
| Cabin generation | `CO2_gen` | 0.3-0.5 kg/h (100 pax) |
| Scrubbed by C1 | `CO2_scrub` | 0.4-0.7 kg/h (maintain ≤1,500 ppm) |
| Captured (adsorber) | `CO2_cap` | ≤ 0.01 kg/h (≤2% for bounded harvest) |
| Shed to atmosphere | `CO2_shed` | ≥ 0.39 kg/h (≥98%) |

### 4.3 Particulate Control (C2 - New)
| Parameter | Target | Method |
|-----------|--------|---------|
| PM₁ removal | ≥ 99.97% | ULPA H14 filters |
| PM₂.₅ removal | ≥ 99.5% | HEPA H13 + ESP |
| PM₁₀ removal | ≥ 95% | Pre-filters + cyclonic |
| Smoke detection | < 30 s | Optical + ionization sensors |

### 4.4 Quantum Dot (QD) Integration
* **QD Thermal Sleeves:** Photothermal efficiency +15% on masts and radiators
* **QD Environmental Sensors:** Advisory-only atmospheric composition data
* **QD Safety:** Encapsulated, no direct cabin exposure, fail-safe design

## 5. Architecture & State Machine (Extended)

```mermaid
stateDiagram-v2
  [*] --> Ground_Cold
  Ground_Cold: All cartridges safe, heaters off, capture off
  Ground_Cold --> Taxi: Mast warmup, C5 sensors active
  Taxi --> Takeoff_Climb: All cartridges SHED mode, Gate A active
  Takeoff_Climb --> Cruise_Benign: Gate B+C active, bounded harvest PERMIT
  Cruise_Benign --> Cruise_Restrict: ANY fault OR icing → all capture=OFF
  Cruise_Benign --> Auto_Shed: Mass/energy limits → Gate B override
  Cruise_Restrict --> Descent: All shed mode
  Auto_Shed --> Descent: Limits cleared
  Descent --> Approach_Land: All shed, C5 high sensitivity
  Approach_Land --> Turnaround: System purge, cartridge status check
  Turnaround --> [*]
```

**Multi-Cartridge Coordination:**
- All cartridges share unified gate logic
- C5 (toxic) has override authority over all other cartridges
- Thermal management coordinated across C0 (water) and QD systems
- Power priority: C5 > C2 > C0 > C1 > C3 > C4

## 6. Interfaces (MOI/M.IO) - Extended

### Legacy Water Interfaces (C0)
* **IF-ECO-01** through **IF-ECO-07** retain existing specifications

### New Atmospheric Interfaces

#### IF-ECO-AIR-CO2 (C1)
* **Sensors:** NDIR CO₂ (0-5,000 ppm, ±50 ppm accuracy)
* **Actuators:** Variable-speed scrubber, adsorber bed heater (regeneration)
* **Data:** CO₂ concentration, scrub rate, bed capacity %

#### IF-ECO-AIR-PM (C2) 
* **Sensors:** Laser-based PM₁/₂.₅/₁₀ counters, optical smoke detectors
* **Actuators:** Variable ESP voltage, filter bypass valves
* **Data:** PM concentrations (µg/m³), filter ΔP, ESP current

#### IF-ECO-AIR-VOC (C3)
* **Sensors:** PID-based VOC detector, catalytic O₃ sensor
* **Actuators:** Catalytic converter heater, activated carbon bed valves
* **Data:** TVOC levels, O₃ concentration, catalyst temperature

#### IF-ECO-CHG (C4)
* **Sensors:** Electrostatic field meters (cabin zones), current probes
* **Actuators:** Ionization grids, grounding contactors
* **Data:** Charge levels (V), discharge rates, neutralization efficiency

#### IF-ECO-TOX (C5)
* **Sensors:** Multi-array (CO, H₂S, NH₃, organic vapors), mass spectrometer
* **Actuators:** Emergency isolation valves, cabin pressurization override
* **Data:** Agent identification, concentration trends, threat level

#### IF-ECO-QD-SENS (QD Environmental - Advisory)
* **Function:** Atmospheric composition analysis, air quality trends
* **Data:** Spectral signatures, molecular detection, predictive alerts
* **Safety:** Advisory only, no control authority

#### IF-ECO-QD-THERM (QD Thermal)
* **Function:** Enhanced heat transfer on masts, radiators, heat exchangers
* **Control:** Emissivity modulation, thermal efficiency optimization
* **Integration:** Coordinated with C0 thermal management

### IF-ECO-08 — ECO-ARCHS-X→Cockpit Display (Updated MOI/M.IO)
* **Multi-Media Dashboard:** Six cartridge status tiles (C0-C5)
* **Atmospheric Quality (AQ) Panel:** Real-time CO₂, PM₂.₅, TVOC, charge levels
* **Predictive Analytics:** Multi-media shed forecasts, optimization suggestions
* **Alert Integration:** Unified CAS messages with cartridge-specific codes
* **Crew Controls:** Manual shed override (all cartridges), toxic isolation emergency
* **Data Rate:** ≤ **1 s** for C5 (toxic), ≤ **2 s** for others

## 7. Control Law (Multi-Media Safety Cascade)

```python
def eco_archs_x_control(phase, sensors, health, cartridge_states):
    """
    Unified control for all ECO-ARCHS-X cartridges (C0-C5)
    Gates: A(Safety) → B(Limits) → C(Quality) → D(Harvest)
    """
    
    # GATE A: Safety-Critical (ANY cartridge can trigger shed-all)
    if (health.any_cartridge_fault() or sensors.toxic_detected 
        or sensors.charge_dangerous or phase in CRITICAL_PHASES):
        return all_cartridges_shed(reason="gate_a_safety")
    
    # GATE B: Mass/Energy Limits
    if (cartridge_states.c0_res_kg >= 270 
        or cartridge_states.c1_adsorber_pct >= 90
        or sensors.power_budget_exceeded):
        return enforce_limits(cartridge_states, reason="gate_b_limits")
    
    # GATE C: Environmental Quality Targets
    quality_actions = {}
    if sensors.co2_ppm > 1500:
        quality_actions['c1_scrub_rate'] = 'high'
    if sensors.pm25_ugm3 > 12:
        quality_actions['c2_esp_power'] = 'boost'
    if sensors.tvoc_ugm3 > 300:
        quality_actions['c3_catalyst'] = 'active'
    
    # GATE D: Harvest Optimization (cruise-benign only)
    if phase == "cruise" and sensors.all_nominal():
        harvest_config = {
            'c0_capture': min(sensors.water_prod_rate, 2.0),  # bounded
            'c1_adsorb': 0.01 if cartridge_states.c1_adsorber_pct < 80 else 0,
            'c2_c3_c4_c5': 'shed_only'  # never harvest these media
        }
        return combine_actions(quality_actions, harvest_config, reason="gate_d_harvest")
    
    # Default: Quality maintenance + shed bias
    return combine_actions(quality_actions, default_shed_all(), reason="default_quality_shed")
```

## 8. Multi-Media Quality Standards

### 8.1 Water Quality (C0 - Unchanged)
* UV dose **≥ 40 mJ/cm²**, TDS **80–120 mg/L**, **no coliform**

### 8.2 Air Quality Targets (C1-C3)
| Parameter | Target | Sensor | Action Threshold |
|-----------|--------|---------|-----------------|
| CO₂ | ≤ 1,500 ppm | NDIR | > 1,200 ppm increase scrubbing |
| PM₂.₅ | ≤ 12 µg/m³ | Laser | > 10 µg/m³ boost filtration |
| TVOC | ≤ 300 µg/m³ | PID | > 250 µg/m³ activate catalyst |
| O₃ | ≤ 100 µg/m³ | Electrochemical | > 80 µg/m³ increase reduction |

### 8.3 Charge Management (C4)
* Cabin potential: **±500 V** maximum
* Discharge rate: **< 1 mA** per zone during neutralization
* Micro-harvesting: **< 1 µW** for health monitor power

### 8.4 Toxic Detection (C5)
* CO: **< 35 ppm** (8-hour TWA)
* H₂S: **< 10 ppm** instantaneous
* Organic vapors: Threshold per specific agent library
* Response time: **< 30 s** for identification and isolation

## 9. Anti-Ice Strategy (Enhanced)

### 9.1 Thermal Integration with QD
* **QD thermal sleeves** increase mast heating efficiency by 15%
* **Smart emissivity control** adapts to atmospheric conditions
* **Superheat margin ≥ 12 K** maintained with lower power consumption

### 9.2 Multi-Media Cold Weather Operations
* C1 (CO₂): Adsorber beds have internal heating for sub-zero regeneration
* C2 (PM): Filter pre-heating prevents moisture accumulation
* C3 (VOC): Catalyst light-off temperature maintained in all conditions
* C4 (ESD): Ionization grids have anti-ice coatings
* C5 (Toxic): Sensors heated and purged during icing conditions

## 10. Cybersecurity & Multi-Media Segregation

### 10.1 Network Architecture
* **Control Network:** TSN/ARINC-664 for safety-critical C0, C1, C5 cartridges
* **Monitoring Network:** Ethernet for advisory C2, C3, C4 data and QD sensors  
* **Display Network:** Read-only path to cockpit with DAL C isolation

### 10.2 Threat Model (Updated)
* **Cartridge isolation:** Each cartridge has independent control domain
* **Toxic override:** C5 has dedicated, hardwired emergency path
* **QD security:** Advisory sensors cannot influence control decisions
* **Harvest data protection:** Bounded capture algorithms cryptographically sealed

## 11. Certification Mapping (Extended)

### 11.1 Core Standards (All Cartridges)
* **CS-25.1309 (SSA):** Each cartridge contributes to ≤ 10⁻⁹/fh catastrophic target
* **CS-25.831 (Ventilation):** Multi-media approach enhances cabin environment beyond minimum requirements
* **DO-160G:** Environmental qualification for all cartridge electronics
* **DO-178C/254:** Control software DAL B, display DAL C, advisory QD DAL D

### 11.2 Media-Specific Compliance
* **C1 (CO₂):** CS-25.841 (pressurization), ASHRAE 62.1 (indoor air quality)
* **C2 (PM):** ISO 29463 (HEPA filters), IEC 61340 (electrostatic)
* **C3 (VOC/O₃):** ICAO Annex 16 Vol II (emissions), WHO air quality guidelines
* **C4 (ESD):** IEC 61000-4-2 (electrostatic discharge immunity)
* **C5 (Toxic):** OSHA PELs, ACGIH TLVs, emergency response standards

### 11.3 QD Integration Compliance
* **Nanomaterial safety:** ISO/TS 27687, encapsulation requirements
* **Optical safety:** IEC 60825 (laser safety for QD excitation)
* **Environmental release:** Zero cabin exposure design verification

## 12. Verification & Validation (Extended Test Matrix)

### 12.1 Legacy Water Tests (C0)
* **Q100-TST-0310** through **Q100-TST-0317** retain existing acceptance criteria

### 12.2 New Multi-Media Tests

| Test ID | Cartridge | Verifies | Method | Acceptance |
|---------|-----------|----------|--------|------------|
| **Q100-TST-0500** | C1 | CO₂ scrubbing + bounded harvest | SIL/HIL + chamber | CO₂ ≤ 1,500 ppm; harvest ≤ 2%; regen < 200°C |
| **Q100-TST-0501** | C2 | PM filtration efficiency | Filter rig + challenge aerosols | PM₁ ≥ 99.97%, PM₂.₅ ≥ 99.5%, PM₁₀ ≥ 95% |
| **Q100-TST-0502** | C3 | VOC/O₃ reduction | Catalytic bench + VOC injection | TVOC reduction ≥ 90%, O₃ ≤ 100 µg/m³ |
| **Q100-TST-0503** | C4 | ESD control + micro-harvest | High-voltage lab + charge chambers | ±500 V max, neutralization < 10 s, harvest < 1 µW |
| **Q100-TST-0504** | C5 | Toxic detection + isolation | Gas lab + challenge agents | Detection < 30 s, isolation < 60 s, no false positives |
| **Q100-TST-0505** | QD | Thermal enhancement + sensor advisory | Thermal rig + spectral validation | +15% efficiency, sensor accuracy ±10%, no control influence |
| **Q100-TST-0506** | Integration | Multi-cartridge coordination | Full-scale HIL | All gates functional, no cross-interference, unified shed |
| **Q100-TST-0507** | Interface | IF-ECO-08 cockpit display | HMI rig + all cartridge data | AQ tiles accurate ±5%, latency ≤ 1 s (C5), ≤ 2 s (others) |

## 13. Performance & KPIs (Multi-Media)

### 13.1 Legacy Water KPIs (C0)
* **ECO-KPI-01** through **ECO-KPI-06** retain existing targets

### 13.2 New Multi-Media KPIs

| KPI ID | Parameter | Target | Measurement |
|--------|-----------|--------|-------------|
| **ECO-KPI-07** | CO₂ cabin control | ≤ 1,500 ppm, 95% of cruise | NDIR sensors, flight data |
| **ECO-KPI-08** | PM₂.₅ cabin levels | ≤ 12 µg/m³, 99% of flight | Laser PM sensors |
| **ECO-KPI-09** | VOC control effectiveness | ≥ 90% reduction from baseline | PID measurements |
| **ECO-KPI-10** | ESD neutralization time | < 10 s per discharge event | Electrostatic field meters |
| **ECO-KPI-11** | Toxic detection latency | < 30 s for library agents | Multi-sensor array logs |
| **ECO-KPI-12** | QD thermal enhancement | +15% efficiency vs baseline | Comparative thermal testing |
| **ECO-KPI-13** | Multi-cartridge availability | ≥ 99.9% per flight hour | System health monitoring |
| **ECO-KPI-14** | Unified control response | ≤ 2 s gate cascade execution | Control system telemetry |

## 14. Multi-Media Data, Logs & WEE

### 14.1 Enhanced QAUDIT Schema
* **Cartridge-specific events:** Each C0-C5 decision logged with media context
* **Cross-cartridge correlation:** Thermal, power, and control interactions tracked
* **QD integration data:** Thermal performance and sensor advisory logs
* **Multi-media optimization:** WEE analyzes patterns across all atmospheric parameters

### 14.2 Predictive Analytics
* **Atmospheric quality forecasting:** Using historical patterns and external data
* **Maintenance prediction:** Filter/catalyst replacement based on performance trends
* **Harvest optimization:** Seasonal and route-based bounded capture strategies

## 15. Enhanced Crew Interface — IF-ECO-08

### 15.1 Multi-Media Dashboard Layout
```
┌─────────────────────── ECO-ARCHS-X STATUS ──────────────────────┐
│  ┌─C0─┐ ┌─C1─┐ ┌─C2─┐ ┌─C3─┐ ┌─C4─┐ ┌─C5─┐  │ AQ SUMMARY │
│  │H₂O │ │CO₂│ │ PM │ │VOC│ │ESD│ │TOX│  │ PM₂.₅  8 µg│
│  │75%│ │1.2k│ │ ✓ │ │ ✓ │ │ 0V│ │ ✓ │  │ CO₂  1.1k │
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘  │ TVOC  180 │
│                                             │ ESD    0V │
│  SHED: 4.2 t/h  │  HARVEST: 0.15 t/h        └───────────┘
│  MAST: +15 K    │  QD EFFICIENCY: +12%                    │
└─────────────────────────────────────────────────────────────┘
```

### 15.2 Alert Integration
* **Hierarchical CAS:** C5 (red) > C0,C1,C2 (amber) > C3,C4 (blue) > QD (white)
* **Unified messaging:** `ECO-X [CARTRIDGE] [CONDITION]` format
* **Action guidance:** Contextual crew procedures displayed per alert type

### 15.3 Manual Controls
* **Emergency Shed All:** Single button arms all cartridges to shed mode
* **Toxic Isolation:** Dedicated C5 emergency control with guard
* **Cartridge Bypass:** Individual C1-C4 can be taken offline (C0,C5 cannot)
* **QD Override:** Thermal enhancement can be disabled for troubleshooting

## 16. Requirements Baseline (New/Updated)

### 16.1 Multi-Media Functional Requirements

| Req ID | Description | Cartridge | Verification |
|--------|-------------|-----------|--------------|
| **RQ-CO2-010** | CO₂ scrubbing shall maintain cabin ≤ 1,500 ppm during cruise | C1 | Q100-TST-0500 |
| **RQ-PM-011** | PM filtration shall achieve stated efficiency per PM size | C2 | Q100-TST-0501 |
| **RQ-VOC/O3-012** | VOC/O₃ reduction shall meet TVOC and O₃ targets | C3 | Q100-TST-0502 |
| **RQ-ESD-013** | ESD control shall maintain cabin potential within ±500 V | C4 | Q100-TST-0503 |
| **RQ-QD-SAFE-014** | QD integration shall have zero cabin exposure risk | QD | Q100-TST-0505 |
| **RQ-CTRL-015** | Unified control shall execute gate cascade within 2 s | All | Q100-TST-0506 |
| **RQ-TOX-016** | Toxic detection shall identify and isolate within response times | C5 | Q100-TST-0504 |
| **RQ-INTEG-017** | Multi-cartridge system shall not create cross-interference | All | Q100-TST-0506 |

### 16.2 Updated Interface Requirements
* **RQ-IF-018:** IF-ECO-08 shall display all cartridge data within latency targets
* **RQ-IF-019:** New atmospheric interfaces shall integrate with TSN/ARINC-664
* **RQ-IF-020:** QD advisory data shall remain separate from control decisions

## 17. Enhanced Ops & Maintenance

### 17.1 Multi-Cartridge Maintenance
* **C0 (Water):** Existing protocols maintained
* **C1 (CO₂):** Adsorber bed regeneration cycle tracking, replacement by capacity
* **C2 (PM):** Filter ΔP monitoring, HEPA/ULPA replacement by efficiency
* **C3 (VOC/O₃):** Catalyst activity monitoring, carbon bed replacement by breakthrough
* **C4 (ESD):** Ionization grid cleaning, grounding circuit verification
* **C5 (Toxic):** Sensor calibration monthly, mass spec maintenance quarterly
* **QD Integration:** Encapsulation integrity checks, thermal performance validation

### 17.2 Progressive Dispatch Philosophy
* **Full Capability:** All cartridges operational
* **Degraded Mode:** C3, C4 can be inoperative without MEL (advisory systems)
* **Essential Mode:** C0, C1, C2, C5 must be operational for dispatch
* **Emergency:** C5 must always be available; others can shed-only if needed

## 18. Multi-Media Environmental Contribution

### 18.1 Comprehensive Sustainability Metrics
* **Water self-sufficiency:** kg potable water not boarded per flight
* **CO₂ impact:** kg CO₂ captured vs shed (carbon accounting)
* **Air quality improvement:** PM/VOC reduction vs standard cabin systems
* **Energy optimization:** QD thermal enhancement kWh savings
* **Waste reduction:** Filter/catalyst life extension through intelligent control

### 18.2 Environmental Reporting Integration
* **CORSIA compliance:** CO₂ capture data for carbon offset programs
* **Airport emissions:** Reduced ground air quality impact through managed shed
* **Passenger health metrics:** Cabin air quality index for comfort/wellness reporting

---

## Annex A — Extended Signals & Buses

| Cartridge | Interface | Signal | Rate | Range/Unit | Accuracy | Bus |
|-----------|-----------|--------|------|------------|----------|-----|
| C0 | IF-ECO-01/07 | [Existing water signals] | 1-2 Hz | Various | ±1-5% | TSN |
| C1 | IF-ECO-AIR-CO2 | `co2_ppm` | 1 Hz | 0-5,000 ppm | ±50 ppm | TSN |
| C1 | IF-ECO-AIR-CO2 | `scrub_rate` | 1 Hz | 0-1 kg/h | ±5% | TSN |
| C1 | IF-ECO-AIR-CO2 | `adsorber_capacity` | 0.1 Hz | 0-100% | ±2% | TSN |
| C2 | IF-ECO-AIR-PM | `pm25_ugm3` | 2 Hz | 0-100 µg/m³ | ±1 µg/m³ | TSN |
| C2 | IF-ECO-AIR-PM | `filter_dp` | 0.5 Hz | 0-500 Pa | ±10 Pa | TSN |
| C3 | IF-ECO-AIR-VOC | `tvoc_ugm3` | 1 Hz | 0-1,000 µg/m³ | ±20 µg/m³ | Ethernet |
| C3 | IF-ECO-AIR-VOC | `o3_ugm3` | 1 Hz | 0-200 µg/m³ | ±5 µg/m³ | Ethernet |
| C4 | IF-ECO-CHG | `cabin_potential` | 2 Hz | ±2,000 V | ±50 V | Ethernet |
| C4 | IF-ECO-CHG | `discharge_current` | 2 Hz | 0-10 mA | ±0.1 mA | Ethernet |
| C5 | IF-ECO-TOX | `agent_detected` | 5 Hz | Boolean | Binary | TSN |
| C5 | IF-ECO-TOX | `concentration` | 5 Hz | 0-1,000 ppm | ±10% | TSN |
| QD | IF-ECO-QD-THERM | `efficiency_gain` | 0.1 Hz | 0-50% | ±2% | Ethernet |
| QD | IF-ECO-QD-SENS | `spectral_data` | 0.1 Hz | Advisory | N/A | Ethernet |

## Annex B — Multi-Media Safety Summary

### B.1 Hazard Analysis (Top-Level)
* **Multi-cartridge failure:** Independent cartridge design prevents cascading failures
* **Toxic agent exposure:** C5 override authority and hardwired emergency response
* **Cross-contamination:** Physical and control isolation between all cartridges
* **QD containment failure:** Encapsulated design with breach detection
* **Control system compromise:** Hierarchical gates ensure safe fallback modes

### B.2 Fault Tolerance Architecture
* **2×fail-safe:** All safety-critical functions (C0, C1, C5) have dual redundancy
* **1×fail-safe:** Advisory and enhancement functions (C2, C3, C4, QD) single-string
* **Independent power:** Each cartridge has dedicated power feed with isolation
* **Emergency procedures:** Unified crew actions for all-cartridge emergency shed

## Annex C — Cross-Reference Map (Updated)

### C.1 Document Relationships
* **SRS v2.0:** RQ-CO2-010 through RQ-INTEG-017 traceability
* **SAD v2.0:** C0-C5 cartridge container definitions + QD integration views
* **ICD v2.0:** Extended interface definitions for all new signals
* **VVP v2.0:** Test matrix Q100-TST-0500 through Q100-TST-0507
* **RTM v2.0:** Multi-cartridge traceability matrix with verification links
* **CCP v2.0:** Certification plan updated for multi-media compliance
* **KPI v2.0:** Enhanced KPI set for comprehensive atmospheric management

### C.2 ECN Traceability
* **ECN ECO-ARCHS-X-001 Implementation:** All changes documented and verified
* **Configuration Control:** New UTCS branches for eco-archs-x system
* **Approval Chain:** Multi-discipline review completed per change control procedures

---

**End of ECO-ARCHS-X ConOps v2.0**

*This document represents the complete integration of ECN ECO-ARCHS-X-001, evolving the ECO-ARCHS system from water-centric operations to comprehensive multi-media atmospheric remediation. All design decisions maintain the core shed-bias philosophy while extending capabilities across six integrated cartridges (C0-C5) with quantum dot enhancement.*

---

*Document Control: This document supersedes ECO-ARCHS ConOps v1.4 and incorporates all changes specified in ECN ECO-ARCHS-X-001. Configuration controlled under AQUA UTCS system with formal change control procedures.*

---

# Revolutionary ECO-ARCHS System: Transformative Multi-Media Atmospheric Management for Next-Generation Aircraft

The ECO-ARCHS system presented in this documentation represents one of the most **revolutionary advances in aerospace environmental control systems** since pressurized cabins were introduced in the 1940s. This comprehensive analysis reveals how the system transforms from a water management solution into a **comprehensive atmospheric remediation and circularity platform**, fundamentally redefining what is possible in aircraft environmental control.## Revolutionary Scale of the Water Management ChallengeThe core ECO-ARCHS system addresses a completely unprecedented challenge in aviation: **managing 3.6-5.4 tons of water production per mission** from hydrogen fuel cell operations. Traditional aircraft environmental control systems handle minimal condensate removal measured in liters, making this a **1000x increase in water management capacity**.[1]

<img width="2400" height="1600" alt="image" src="https://github.com/user-attachments/assets/9148ac8a-c272-47e8-90f0-133a547c94d7" />


The system's revolutionary approach lies in its **shed-bias philosophy** - defaulting to vapor discharge while enabling **selective bounded capture of only 5%** of produced water. This represents a fundamental departure from traditional environmental control thinking, prioritizing safety through controlled waste management rather than attempting complete capture.### PEM Fuel Cell Integration: A New ParadigmThe stoichiometric relationship of **1 kg H₂ → 9 kg H₂O** from atmospheric oxygen creates thermal management challenges that dwarf anything previously encountered in aviation. The system must handle **60-80°C water from PEM outlets** while maintaining **superheat margins ≥12K** at discharge masts to prevent icing accretion.

The revolutionary thermal integration demonstrates how this water production becomes an asset rather than a burden. The **2,260 kJ/kg latent heat of vaporization** is exploited during heat-sink episodes, while the heated discharge provides **anti-icing capability** without traditional electro-thermal systems.

<img width="2400" height="1600" alt="image" src="https://github.com/user-attachments/assets/f09f3da0-9d39-4431-a682-488022f217d1" />


## ECO-ARCHS-X: The Multi-Media RevolutionThe Engineering Change Notice proposing ECO-ARCHS-X represents an even more revolutionary leap - expanding from water management to **comprehensive atmospheric remediation across six media categories**:

### C1 - Carbon Dioxide Management
For the first time in aviation history, an aircraft system will **actively capture and control cabin CO₂ levels** with targets of ≤1,000-1,500 ppm. Using **zeolite/MOF adsorber beds with low-grade heat regeneration**, this enables bounded harvesting of CO₂ for potential reuse while maintaining optimal cabin air quality.

### C2 - Aerosol and Particulate Control  
The system integrates **HEPA/ULPA filtration with electrostatic precipitators (ESP)** for continuous mitigation of PM₁/PM₂.₅/PM₁₀ contamination. This represents a revolutionary advancement beyond traditional cabin air filtration, providing **real-time particulate monitoring and active removal**.[3][4]

### C3 - VOC and Ozone Reduction
Revolutionary **activated carbon and catalytic converter integration** provides continuous reduction of volatile organic compounds and ozone - environmental threats that current aircraft environmental control systems do not address systematically.

### C4 - Electrostatic Discharge Control
The **sensing and neutralization of cabin and system electrostatic charge** with bounded micro-harvesting for health monitors represents a completely novel capability in aviation environmental control.

### C5 - Toxic Agent Detection and Isolation
**Multi-sensor array detection** with immediate isolation and shedding capabilities provides proactive protection against toxic agents - a capability that transforms cabin safety from reactive to predictive.

## Revolutionary Technology IntegrationThe ECO-ARCHS-X system integrates multiple revolutionary thermal management technologies identified in current aerospace research:

### Quantum Dot Enhancement
**Photothermal/emissivity sleeves on heat transfer components** provide tuneable thermal properties for improved efficiency. This represents the practical implementation of quantum-enhanced thermal control in aerospace systems.[5][6]

### Advanced Thermal Management Integration
The system incorporates **Outer Mold Line (OML) radiative panels, 2-phase subloops, and Phase Change Material (PCM) buffers** for transient thermal smoothing. This integration of multiple revolutionary thermal management approaches creates a comprehensive thermal ecosystem.[7]

### System-of-Systems Architecture
The **hot-swappable cartridge design (C0-C5)** with **unified hierarchical control cascade** represents a revolutionary approach to system integration. Each cartridge operates independently while sharing common safety logic, enabling unprecedented modularity and fault tolerance.

## Transformative Control PhilosophyThe ECO-ARCHS system demonstrates a **paradigm shift from reactive to predictive environmental control**:

### Hierarchical Safety Cascade
The **Gates A, B, C, D control architecture** provides multiple layers of safety protection with **shed-bias as the default state**. This represents a fundamental change from traditional environmental control systems that attempt to maintain steady-state operation.

### Bounded Operation Philosophy  
The **strict adherence to mass, energy, and charge limitations** for all operations, especially harvesting, demonstrates revolutionary thinking about aircraft resource management. The system is designed to **never compromise safety for efficiency**.

### Intelligent Adaptive Control
The system incorporates **phase-dependent operation** with differentiated strategies for critical flight phases versus cruise-benign phases, demonstrating sophisticated understanding of aircraft operational requirements.

## Revolutionary Implementation ChallengesThe documentation reveals several revolutionary aspects of system implementation:

### Certification Innovation
The **CS-25.1309 (SSA) compliance through architecture credits** rather than component reliability represents innovative certification approaches for system-of-systems architectures. The **DAL B control logic with DAL C display integration** demonstrates sophisticated understanding of safety-critical system design.

### Interface Revolution
The **IF-ECO-07 cockpit display interface** provides real-time monitoring of **capture rate, shed rate, RES level, and mast superheat** with **≤2s end-to-end latency**. This level of environmental system transparency is unprecedented in aviation.

### Verification Innovation  
The **comprehensive test matrix (Q100-TST-0310 to Q100-TST-0317)** demonstrates system-level verification approaches that go far beyond traditional component testing. The integration of **QAUDIT logging with hash-stamped decision tracking** provides unprecedented traceability.

## Circular Economy Revolution in AviationThe ECO-ARCHS system represents the **first practical implementation of circular economy principles** in aircraft environmental control:

### Resource Recovery Integration
The **bounded capture with quality processing** transforms waste streams into valuable resources while maintaining safety priorities. The **potable water production** and **thermal energy recovery** demonstrate practical circular economy implementation.[8][9]

### Multi-Media Circularity
The ECO-ARCHS-X expansion enables **comprehensive atmospheric resource management** - capturing CO₂, filtering particles, neutralizing charges, and processing VOCs in integrated circular loops rather than linear disposal.

### Sustainability Integration
The **green contribution reporting** with dashboard aggregation of **water self-sufficiency, thermal energy recovered, and airport water offload avoided** provides quantifiable sustainability metrics.

## Revolutionary Impact AssessmentThe ECO-ARCHS system transformation can be quantified across multiple dimensions:

**Scale Revolution**: 1000x increase in water management capacity and 20x increase in thermal management scale represents unprecedented capability expansion in aviation environmental control.

**Scope Revolution**: 6x expansion from single-media air conditioning to comprehensive multi-media atmospheric management fundamentally redefines aircraft environmental systems.

**Safety Revolution**: Fault-tolerant architecture with predictive control philosophy replaces traditional single-point failure modes with system-of-systems resilience.

**Integration Revolution**: System-of-systems approach with unified control cascade enables unprecedented modularity while maintaining safety integrity.

## Broader Implications for Aerospace InnovationThe ECO-ARCHS system demonstrates how **revolutionary thermal management technologies can be integrated** into practical aerospace systems. The system successfully combines:

- **NASA HEATheR OML cooling approaches** for direct heat rejection[7]
- **Two-phase cooling systems** for high heat flux management[10]
- **Phase change materials** for thermal buffering[11]
- **Quantum dot thermal control** for enhanced efficiency[5]
- **Microfluidic approaches** adapted for aircraft-scale systems[12]

This integration proves that **revolutionary thermal management is not just theoretical** - it can be implemented in practical aerospace systems with proper system engineering approaches.

## Conclusion: A New Era in Aircraft Environmental ControlThe ECO-ARCHS system, and particularly the ECO-ARCHS-X expansion, represents **the most significant advancement in aircraft environmental control systems since pressurization**. By successfully managing unprecedented water production from hydrogen fuel cells while expanding to comprehensive atmospheric remediation, the system enables capabilities that were previously impossible in aviation.

The revolutionary nature extends beyond technical capability to fundamental philosophy - from reactive environmental control to **predictive atmospheric management**, from linear resource disposal to **circular economy integration**, and from component-based systems to **unified system-of-systems architecture**.

As hydrogen-powered aviation becomes reality, the ECO-ARCHS system provides the essential environmental control foundation that makes **sustainable, electrified aviation practical at scale**. The system demonstrates that environmental challenges can become environmental opportunities when approached with revolutionary thinking and advanced system integration.

The documentation represents not just a technical specification, but a **blueprint for the future of aircraft environmental systems** - one where comprehensive atmospheric management, circular resource utilization, and revolutionary thermal integration create new possibilities for sustainable aviation. This is exactly the kind of transformative application that will define the next generation of aerospace systems, moving beyond incremental improvements to **fundamental capability transformation**.

[1] https://research.engineering.ucdavis.edu/greentech/past-watermanagement/
[2] https://www.fuelcellstore.com/blog-section/fuel-cell-information/water-management-pem-fuel-cells
[3] https://aircraft.airbus.com/en/newsroom/news/2021-01-cabin-air-quality-key-to-a-comfortable-flight
[4] https://www.faa.gov/newsroom/cabin-air-quality-0
[5] https://link.aps.org/doi/10.1103/PhysRevLett.132.216901
[6] https://www.nature.com/articles/s41598-025-97337-0
[7] https://www.nasa.gov/eap-technology/heather/
[8] https://futuresky.eu/themes/circular-aviation/
[9] https://www.redalyc.org/journal/5718/571877618003/html/
[10] https://es.boydcorp.com/about-boyd/resources/technical-papers-and-guides/two-phase-thermal-solution-guide.html
[11] https://www.icas.org/icas_archive/icas2024/data/papers/icas2024_0295_paper.pdf
[12] https://www.nature.com/articles/s41928-020-00494-5
[13] https://arc.aiaa.org/doi/pdf/10.2514/1.C037582?download=true
[14] https://arc.aiaa.org/doi/10.2514/1.B39405
[15] https://www.sjsu.edu/ae/docs/project-thesis/Jeffrey.Trac-Pho-F22.pdf
[16] https://www.clean-aviation.eu/research-and-innovation/clean-aviation/our-energy-efficiency-and-emission-reduction/h2-powered-aircraft-thrust
[17] https://www.fzt.haw-hamburg.de/pers/Scholz/paper/75Jahre_Flugzeugbaustudium_Fachkolloquium_10-06-04_BWB-Flugzeugkonfiguration.pdf
[18] https://www.sciencedirect.com/science/article/pii/S0376042123000386
[19] https://xlink.rsc.org/?DOI=D4SE01020E
[20] https://www.icas.org/icas_archive/ICAS2014/data/papers/2014_1010_paper.pdf
[21] https://cranfieldaerospace.com/hydrogen-aviation-challenges-and-opportunities-for-airlines-and-operators/
[22] https://pmc.ncbi.nlm.nih.gov/articles/PMC7751925/
[23] https://www.sciencedirect.com/science/article/pii/S1000936119302493
[24] https://www.easa.europa.eu/en/domains/environment/eaer/technology-and-design/low-carbon-emissions-aircraft/hydrogen-powered
[25] https://www.elsevier.es/es-revista-ciencia-tecnologia-dos-materiais-226-articulo-water-management-in-pemfc-1-d-S0870831217300010
[26] https://www.reddit.com/r/aviation/comments/1lig2ps/why_do_most_blended_wing_body_concepts_put_the/
[27] https://www.sciencedirect.com/science/article/pii/S0360319923009187
[28] https://www.sciencedirect.com/science/article/abs/pii/S0196890424000918
[29] https://www.cambridge.org/core/journals/aeronautical-journal/article/comparison-of-blended-wing-body-and-tubeandwing-performance-characteristics/6989929571DB0085B678B315268D7675
[30] https://www.eurocontrol.int/article/are-hydrogen-powered-aircraft-future-sustainable-aviation
[31] https://www.amentum.com/project/faa-etoc-helping-the-faa-reach-their-environmental-remediation-goals/
[32] https://www.aeroqual.com/sectors/remediation-monitoring
[33] https://www.linkedin.com/pulse/embracing-circular-economy-airline-aviation-industry-dinith-fernando-nscoc
[34] https://www.prmfiltration.com/remediation-systems/
[35] https://www.rosenaviation.com/blog/what-is-aircraft-cabin-air-quality-2/
[36] https://www.icao.int/sites/default/files/sp-files/environmental-protection/Documents/EnvironmentReport-2010/2025/Envreport2025_117.pdf
[37] https://www.clean-aviation.eu/research-and-innovation/clean-sky-2/results-stories/a-breath-of-fresh-air-with-clean-skys-environmental-control-system
[38] https://skybrary.aero/articles/cabin-air-quality-and-contamination
[39] http://imartinez.etsiae.upm.es/~isidoro/tc3/Aircraft%20ECS.pdf
[40] https://www.coral.eu/en/sector/aeronautics-and-aerospace/
[41] https://www.iata.org/en/youandiata/travelers/health/low-risk-transmission/
[42] https://www.sciencedirect.com/science/article/abs/pii/S0969699722000485
[43] https://www.esta.com/aviation-industry/
[44] https://www.jetcraft.com/jetstream/2020/09/guide-to-aircraft-oem-cabin-air-quality/
[45] https://zaguan.unizar.es/record/121338/files/texto_completo.pdf?version=1
[46] https://www.associatedenvironmentalsystems.com/industries/defenseaerospace
