# Copilot Validation Instructions – AQUA Repo

## Purpose
Ensure **completeness, structure, consistency, and compliance** of this repository according to the AQUA UTCS-MI v5.0 standard and aerospace/quantum regulatory context.

---

## 1. Completeness Checklist
- [ ] All major top-level directories (`boot/`, `kernel/`, `framework/`, `platforms/`, `domains/`, `data/`, `docs/`, `infrastructure/`, `integration/`, `standards/`, `technologies/`, `tools/`, `config/`, `tests/`, `var/`) are present and populated.
- [ ] All files have UTCS-MI IDs in their metadata or filenames where applicable.
- [ ] Each subsystem (e.g. MOS, CQEA, WEE, AMOReS, DeMOS) has:
  - Source code
  - Specification (`*.md`)
  - Configuration (`*.yaml`)
  - Diagram (`*.svg` / `.json` if dashboard)
- [ ] Required artefacts for certification (`caas/`), validation (`validation/`), and safety (`safety/`) are present.

---

## 2. Structure Checklist
- [ ] Directory hierarchy matches **UTCS-MI v5.0** and domain mapping (codes 001-920).
- [ ] Each platform under `platforms/` contains:
  - `core` or equivalent engine
  - API definitions
  - Configurations
  - Specifications & diagrams
- [ ] `domains/` has per-domain applications with `architecture/`, `certification/`, `operations/`, `maintenance/`, `training/`, `testing/`, `validation/` subfolders.
- [ ] `data/` subdivided into `ai-ml/`, `schemas/`, `storage/`, `workflows/` with DDLs, diagrams, and policies.

---

## 3. Consistency Checklist
- [ ] Filenames and folder names use kebab-case and match their UTCS-MI code mapping.
- [ ] Config files (`.yaml`) match corresponding specs (`.md`) and code modules.
- [ ] Diagrams are up-to-date with related specs (last modified date ≤ spec’s last update).
- [ ] No duplicate artefacts across `docs/` and implementation folders unless symlinked or explicitly referenced.

---

## 4. Compliance Checklist
- [ ] Aerospace standards in `/standards/aerospace/` are referenced in related code/specs.
- [ ] Security standards (ISO 27001, DO-326A, NIST PQC) linked to `security/` modules.
- [ ] Quality standards (AS9100, ISO 9001) linked to `quality/` documentation.
- [ ] UTCS-MI v5.0 metadata fields present in all specs.
- [ ] Regulatory compliance docs (`compliance/`) map to certification artefacts in `platforms/` and `domains/`.

---

## 5. Report Format
When Copilot runs a check, output:

```text
[COMPLETENESS]
- PASS/FAIL with missing artefacts list

[STRUCTURE]
- PASS/FAIL with mismatches or misplaced files

[CONSISTENCY]
- PASS/FAIL with file/spec mismatches

[COMPLIANCE]
- PASS/FAIL with missing regulatory links or UTCS-MI fields
