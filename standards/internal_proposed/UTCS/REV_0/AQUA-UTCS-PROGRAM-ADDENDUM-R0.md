# UTCS Specification Addendum
## Program-Specific Application Domain Substitution
### Implementation Flexibility Guidelines

**Document ID:** AQUA-UTCS-PROGRAM-ADDENDUM-R0  
**Classification:** Implementation Guidance  
**Effective Date:** 2025-01-20  
**Purpose:** Enable Organization-Specific Program Identification  

---

## 1. PROGRAM SUBSTITUTION PRINCIPLE

### 1.1 Core Concept
The Application Domain field ([APP]) in the UTCS identifier can be substituted with **actual program identifiers** for established or announced programs, providing immediate program context and improving traceability.

### 1.2 Format Flexibility
```
Generic Format:
UTCS:[TYPE]-[LIFECYCLE]-[ATA]-[CATEGORY]-[SEQUENCE]-[STATE]-[APP]

Program-Specific Format:
UTCS:[TYPE]-[LIFECYCLE]-[ATA]-[CATEGORY]-[SEQUENCE]-[STATE]-[PROGRAM]
```

---

## 2. IMPLEMENTATION EXAMPLES

### 2.1 Commercial Aircraft Programs
```yaml
Generic:
  UTCS:REQ-DSN-27-FBQW-001-SPR-AIR  # Generic airborne

Boeing Implementation:
  UTCS:REQ-DSN-27-FBQW-001-SPR-B737MAX   # Boeing 737 MAX
  UTCS:REQ-DSN-27-FBQW-001-SPR-B777X     # Boeing 777X
  UTCS:REQ-DSN-27-FBQW-001-SPR-B787      # Boeing 787

Airbus Implementation:
  UTCS:REQ-DSN-27-FBQW-001-SPR-A320NEO   # Airbus A320neo
  UTCS:REQ-DSN-27-FBQW-001-SPR-A350      # Airbus A350
  UTCS:REQ-DSN-27-FBQW-001-SPR-A380      # Airbus A380

AQUA Programs:
  UTCS:REQ-DSN-27-FBQW-001-SPR-BWBQ100   # BWB-Q100 aircraft
  UTCS:REQ-DSN-27-FBQW-001-SPR-HE180     # Hybrid-Electric 180
  UTCS:REQ-DSN-27-FBQW-001-SPR-EVTOL360  # 360CITY eVTOL
```

### 2.2 Space Programs
```yaml
Generic:
  UTCS:REQ-OPS-98-QCOMM-001-COL-SPC  # Generic spaceborne

NASA Implementation:
  UTCS:REQ-OPS-98-QCOMM-001-COL-ARTEMIS  # Artemis Program
  UTCS:REQ-OPS-98-QCOMM-001-COL-ORION    # Orion Spacecraft
  UTCS:REQ-OPS-98-QCOMM-001-COL-SLS      # Space Launch System

SpaceX Implementation:
  UTCS:REQ-OPS-98-QCOMM-001-COL-STARSHIP # Starship
  UTCS:REQ-OPS-98-QCOMM-001-COL-F9       # Falcon 9
  UTCS:REQ-OPS-98-QCOMM-001-COL-STARLINK # Starlink

AQUA Space Programs:
  UTCS:REQ-OPS-98-QCOMM-001-COL-GAIA     # GAIA constellation
  UTCS:REQ-OPS-98-QCOMM-001-COL-QSAT     # Quantum satellite
```

### 2.3 Defense Programs
```yaml
Generic:
  UTCS:REQ-CDV-27-FBW-001-ENT-DEF  # Generic defense

Specific Programs:
  UTCS:REQ-CDV-27-FBW-001-ENT-F35        # F-35 Lightning II
  UTCS:REQ-CDV-27-FBW-001-ENT-F22        # F-22 Raptor
  UTCS:REQ-CDV-27-FBW-001-ENT-TYPHOON    # Eurofighter Typhoon
  UTCS:REQ-CDV-27-FBW-001-ENT-RAFALE     # Dassault Rafale
  UTCS:REQ-CDV-27-FBW-001-ENT-FCAS       # Future Combat Air System
  UTCS:REQ-CDV-27-FBW-001-ENT-TEMPEST    # BAE Tempest
```

### 2.4 Ground Systems
```yaml
Generic:
  UTCS:REQ-OPS-45-CMC-001-COL-GND  # Generic ground

Airport-Specific:
  UTCS:REQ-OPS-45-CMC-001-COL-KLAX      # Los Angeles International
  UTCS:REQ-OPS-45-CMC-001-COL-EGLL      # London Heathrow
  UTCS:REQ-OPS-45-CMC-001-COL-OMDB      # Dubai International

Facility-Specific:
  UTCS:REQ-OPS-45-CMC-001-COL-MRO1      # MRO Facility 1
  UTCS:REQ-OPS-45-CMC-001-COL-TESTLAB   # Test Laboratory
  UTCS:REQ-OPS-45-CMC-001-COL-SIMCTR    # Simulation Center
```

### 2.5 Cross-Domain Programs
```yaml
Generic:
  UTCS:REQ-DSN-98-QCRYPT-001-SPR-CRS  # Generic cross-domain

Multi-Program Application:
  UTCS:REQ-DSN-98-QCRYPT-001-SPR-COMMON  # Common to all programs
  UTCS:REQ-DSN-98-QCRYPT-001-SPR-NATO    # NATO standard
  UTCS:REQ-DSN-98-QCRYPT-001-SPR-ACARE   # ACARE initiative
  UTCS:REQ-DSN-98-QCRYPT-001-SPR-SESAR   # SESAR program
  UTCS:REQ-DSN-98-QCRYPT-001-SPR-NEXTGEN # NextGen ATM
```

---

## 3. PROGRAM IDENTIFIER RULES

### 3.1 Format Requirements
```yaml
Length: 3-10 characters
Characters: A-Z, 0-9 only (no special characters)
Case: UPPERCASE only
Structure: 
  - Can include numbers (B737, A320, F35)
  - Can be acronyms (BWB, GAIA, FCAS)
  - Can be codes (KLAX, EGLL)
  - Must be unique within organization
```

### 3.2 Registration Guidelines
```yaml
Internal Programs:
  - Register in organization's UTCS registry
  - No external approval needed
  - Must be unique within organization

Industry Programs:
  - Should align with industry conventions
  - Consider IATA/ICAO codes for airports
  - Use established program names

Joint Programs:
  - Agree on identifier with partners
  - Document in collaboration agreements
  - Maintain consistency across organizations
```

### 3.3 Reserved Identifiers
```yaml
Always Reserved:
  AIR: Generic airborne (fallback)
  SPC: Generic spaceborne (fallback)
  GND: Generic ground (fallback)
  DEF: Generic defense (fallback)
  CRS: Cross-domain (fallback)
  TEST: Test articles only
  PROTO: Prototypes only
  SIM: Simulation only
```

---

## 4. PRACTICAL EXAMPLES

### 4.1 Boeing 787 Dreamliner Implementation
```yaml
# Flight Control System for 787
Requirement:  UTCS:REQ-DSN-27-FBQW-001-SPR-B787
Code:         UTCS:ART-CDV-27-FBQW-001-ENT-B787
Test:         UTCS:TST-SIT-27-FBQW-001-ENT-B787
Evidence:     UTCS:EVD-VAL-27-FBQW-001-COL-B787
Document:     UTCS:DOC-OPS-27-FBQW-001-COL-B787

# Same system adapted for 777X
Requirement:  UTCS:REQ-DSN-27-FBQW-002-SPR-B777X
```

### 4.2 Multi-Program Component
```yaml
# PQC system used across multiple aircraft
Base Development:     UTCS:ART-CDV-98-QCRYPT-001-SPR-COMMON
Boeing Integration:   UTCS:ART-INT-98-QCRYPT-001-ENT-B737MAX
Airbus Integration:   UTCS:ART-INT-98-QCRYPT-001-ENT-A320NEO
Defense Integration:  UTCS:ART-INT-98-QCRYPT-001-ENT-F35
```

### 4.3 Program Evolution
```yaml
# Technology transfer from military to commercial
Original:     UTCS:ART-OPS-27-FBW-001-COL-F22
Adapted:      UTCS:ART-MOD-27-FBW-001-SPR-B787
Certified:    UTCS:ART-OPS-27-FBW-001-COL-B787
```

---

## 5. MIGRATION STRATEGIES

### 5.1 New Programs
- Start with program identifier from day one
- No generic identifiers needed
- Direct program traceability

### 5.2 Existing Programs
```yaml
Phase 1: Dual Identification
  Old: UTCS:REQ-OPS-27-FBW-001-COL-AIR
  New: UTCS:REQ-OPS-27-FBW-001-COL-A350

Phase 2: Program Primary
  Primary: UTCS:REQ-OPS-27-FBW-001-COL-A350
  Reference: (formerly AIR)

Phase 3: Program Only
  Final: UTCS:REQ-OPS-27-FBW-001-COL-A350
```

### 5.3 Cross-Program Components
```yaml
Development Phase:
  UTCS:ART-CDV-98-QCRYPT-001-SPR-COMMON

Integration Phase:
  UTCS:ART-INT-98-QCRYPT-001-ENT-[PROGRAM]

Operations Phase:
  UTCS:ART-OPS-98-QCRYPT-001-COL-[PROGRAM]
```

---

## 6. BENEFITS OF PROGRAM SUBSTITUTION

### 6.1 Immediate Context
```yaml
Generic:       UTCS:REQ-OPS-32-BRAKE-001-COL-AIR
               # Which aircraft? What program?

Program-Specific: UTCS:REQ-OPS-32-BRAKE-001-COL-B787
                  # Clearly Boeing 787 brake requirement
```

### 6.2 Better Traceability
- Direct link to program documentation
- Clear configuration management
- Simplified program reporting
- Enhanced search capabilities

### 6.3 Multi-Program Management
```yaml
Query: "Show all B787 requirements"
Result: UTCS:*-*-*-*-*-*-B787

Query: "Compare F35 and F22 flight controls"
Result: UTCS:*-*-27-*-*-*-F35 vs UTCS:*-*-27-*-*-*-F22
```

### 6.4 Supply Chain Clarity
```yaml
Supplier Quote Request:
  "Need brake actuators for UTCS:*-*-32-ACTR-*-*-A320NEO"
  # Supplier knows exactly: A320neo brake actuators
```

---

## 7. IMPLEMENTATION EXAMPLES BY ORGANIZATION

### 7.1 Airbus Implementation
```yaml
Programs:
  A220, A319, A320, A321, A320NEO, A321NEO
  A330, A330NEO, A340, A350, A380
  A400M, H125, H135, H145, H160, H175, H225

Example Set:
  UTCS:REQ-DSN-27-FBW-001-SPR-A350
  UTCS:ART-CDV-27-FBW-001-ENT-A350
  UTCS:TST-VAL-27-FBW-001-COL-A350
```

### 7.2 Boeing Implementation
```yaml
Programs:
  B737, B737MAX, B747, B757, B767, B777, B777X, B787
  KC46, P8, E7, T7, MQ25, AH64, CH47, V22

Example Set:
  UTCS:REQ-DSN-73-FADEC-001-SPR-B737MAX
  UTCS:ART-MFG-73-FADEC-001-ENT-B737MAX
  UTCS:DOC-OPS-73-FADEC-001-COL-B737MAX
```

### 7.3 AQUA Initiative Programs
```yaml
Programs:
  BWBQ100, HE180, TD20, EVTOL360
  GAIA, QSAT, QNET
  AMPEL360, DIQIAAS, ROBOT

Example Set:
  UTCS:REQ-CNC-27-FBQW-001-SPR-BWBQ100
  UTCS:ART-CDV-27-FBQW-001-ENT-BWBQ100
  UTCS:TST-VAL-27-FBQW-001-COL-BWBQ100
```

---

## 8. REGISTRY CONSIDERATIONS

### 8.1 Program Registration
```sql
CREATE TABLE program_registry (
  program_code VARCHAR(10) PRIMARY KEY,
  program_name VARCHAR(100),
  organization VARCHAR(100),
  type ENUM('AIRCRAFT','SPACECRAFT','SYSTEM','INFRASTRUCTURE'),
  status ENUM('CONCEPT','DEVELOPMENT','PRODUCTION','RETIRED'),
  start_date DATE,
  end_date DATE,
  parent_program VARCHAR(10),
  UNIQUE KEY (program_code, organization)
);
```

### 8.2 Cross-Reference Table
```sql
CREATE TABLE program_mapping (
  generic_domain VARCHAR(3),  -- AIR, SPC, GND, DEF, CRS
  program_code VARCHAR(10),
  valid_from DATE,
  valid_to DATE,
  PRIMARY KEY (generic_domain, program_code)
);
```

---

## 9. APPROVAL

**Addendum Status:** APPROVED FOR IMMEDIATE ADOPTION

**Flexibility Statement:**
Organizations are authorized to implement program-specific identifiers in place of generic application domains while maintaining all other UTCS structural requirements.

**Effective:** Immediately upon local program registration

---

**"Making UTCS speak your program's language"**

© 2025 AQUA Initiative - Flexibility Through Structure
