# **AQUA File Format Technical Specification**

## **Version 5.1.2 - Editors’ Draft**

### Document Identifier: AQUA-SPEC-2025-001-COMPLETE

### Status: PROPOSED STANDARD (Editors’ Draft)

### Date: August 12, 2025

### Category: Technical Specification

-----

## **Change Log (from v5.1.1)**

- **Introduced canonical serialization** (Deterministic CBOR) and wire-compat rules
- **Fully specified Section Table** with MUST-understand bit and integrity per section
- **Tightened signature coverage** for rollback resistance
- **Added uniform error codes** and failure semantics
- **Hardened security architecture:**
  - Aligned PQC to FIPS 203/204/205 names and sizes
  - Mandated HKDF(SHAKE256) for all key combination (no XOR/concat)
  - Defined AEAD, nonce discipline, rekey thresholds
  - Added crypto-agility negotiation TLV and revocation vector
  - Extended QKD with classical-auth policy, MDI-QKD option, and latency/ε budgets
  - Added ACVP/CST compliance hooks and side-channel criteria
- **Created registries** (algorithm IDs, section types, AEAD, hash)
- **Clarified profile boundaries** (LAB/ADV/THEORY) with respect to physics claims
- **Strengthened Conformance & TV&V checklist**

-----

## **Abstract**

This document provides the complete technical specification for the AQUA (Aerospace and Quantum United Applications) File Format version 5.1.2, incorporating critical security enhancements and normative changes based on implementation experience. This editors’ draft represents the culmination of intensive development during August 2025, establishing a comprehensive data architecture for quantum-classical hybrid computing, artificial general intelligence systems, and interplanetary data synchronization with deterministic serialization and enhanced cryptographic robustness.

-----

## **Table of Contents**

1. [Introduction](#1-introduction)
1. [Conventions and Definitions](#2-conventions-and-definitions)
1. [Canonical Serialization & Wire Rules](#3-canonical-serialization--wire-rules)
1. [Core Format Structure](#4-core-format-structure)
1. [Enhanced Section Table](#5-enhanced-section-table)
1. [Error Semantics](#6-error-semantics)
1. [Security Architecture](#7-security-architecture)
1. [Data Section Specifications](#8-data-section-specifications)
1. [Validation Requirements](#9-validation-requirements)
1. [Implementation Profiles](#10-implementation-profiles)
1. [Conformance](#11-conformance)
1. [IANA Considerations](#12-iana-considerations)
1. [References](#13-references)
1. [Appendices](#14-appendices)

-----

## **1. Introduction**

### **1.1 Purpose**

The AQUA File Format version 5.1.2 represents a security-hardened and implementation-refined data container architecture. This editors’ draft incorporates normative changes to address deployment experiences and security audit findings, establishing deterministic serialization, enhanced integrity protection, and robust cryptographic agility.

### **1.2 Scope**

This specification defines:

- Canonical serialization using Deterministic CBOR
- Enhanced section table with per-section integrity
- Uniform error semantics and failure modes
- Hardened security architecture with FIPS-aligned PQC
- Crypto-agility negotiation framework
- Complete registry system for extensibility

### **1.3 Requirements Notation**

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 [RFC2119] and RFC 8174 [RFC8174].

-----

## **2. Conventions and Definitions**

### **2.1 Normative Terms**

**Deterministic CBOR**: Canonical encoding rules per RFC 8949 Section 4.2

**MUST-understand**: A section flag indicating that unknown sections SHALL cause parsing failure

**Canonical hash domain**: The exact byte sequence used for cryptographic operations

**ACVP**: Automated Cryptographic Validation Protocol (NIST)

**CST**: Cryptographic Security Testing

**MDI-QKD**: Measurement-Device-Independent Quantum Key Distribution

### **2.2 Data Type Conventions**

All data types follow big-endian encoding unless explicitly specified. File structures are 8-byte aligned with zero padding.

-----

## **3. Canonical Serialization & Wire Rules**

### **3.1 Deterministic CBOR Requirements**

The following structures MUST use Deterministic CBOR encoding:

- Header
- Section Table
- Capabilities Block
- Profile Block
- Security Block
- Signature Block

### **3.2 CDDL Schema (Normative)**

```cddl
; Header (canonical CBOR map with deterministic key order)
header = {
  1: magic,                     ; bstr .size 4, h'41515541'
  2: version,                   ; [major, minor, patch, build]
  3: flags: uint,
  4: capabilities: uint,
  5: profile: uint,             ; 1=LAB, 2=ADV, 3=THEORY
  6: ts: [ created: uint, modified: uint ],
  7: uuid: bstr .size 16,
  8: parent_uuid: bstr .size 16,
  9: creator: tstr .size (0..256),
  10: organization: tstr .size (0..128),
  11: purpose: tstr .size (0..512),
  12: header_size: uint,
  13: header_crc32: uint,
  14: header_sha256: bstr .size 32,
  15: min_accepted_version: version  ; Anti-rollback
}

version = [ major: uint .le 255, 
           minor: uint .le 255, 
           patch: uint .le 255, 
           build: uint .le 255 ]

magic = h'41515541'  ; 'AQUA' in ASCII
```

### **3.3 Canonical Hash Domain**

The canonical hash domain for signatures SHALL be:

```
hash_input = canonical_cbor(header) || 
             canonical_cbor(section_table) ||
             canonical_cbor(capabilities) ||
             canonical_cbor(profile) ||
             canonical_cbor(alg_negotiation) ||
             canonical_cbor(min_accepted_version)
```

-----

## **4. Core Format Structure**

### **4.1 Universal File Layout**

```
AQUA_File := Magic_Bytes
            Header (CBOR)
            Version_Block (CBOR)
            Capabilities_Block (CBOR)
            Profile_Block (CBOR)
            Assumptions_Block (CBOR)     // v5.0+
            Section_Table (CBOR)
            Data_Sections (Binary)
            Metadata_Block (CBOR)
            Security_Block (CBOR)         // v2.0+
            Signature_Block (CBOR)        // v2.0+
            End_Marker
```

### **4.2 Alignment and Padding**

- All major blocks SHALL start on 8-byte boundaries
- Padding bytes MUST be zero
- Section data MAY have arbitrary alignment within their boundaries

-----

## **5. Enhanced Section Table**

### **5.1 Section Table Structure (Normative)**

```c
typedef struct {
    uint32_t entry_count;
    struct {
        uint16_t section_type;      /* Registry ID (see §14) */
        uint16_t section_version;   /* Schema version */
        uint32_t flags;             /* See bitmask below */
        uint64_t offset;            /* From file start */
        uint64_t length;            /* Ciphertext/compressed length */
        uint8_t  uuid[16];          /* Stable section UUID */
        uint8_t  integrity[32];     /* SHA-256 of PLAINTEXT payload */
        uint64_t nonce_counter;     /* Per-section AEAD counter start */
    } entries[];
} AQUA_SectionTable_V2;

/* Section Flags */
#define SECFLAG_CRITICAL    0x00000001  /* MUST-understand */
#define SECFLAG_ENCRYPTED   0x00000002
#define SECFLAG_COMPRESSED  0x00000004
#define SECFLAG_SIGNED      0x00000008
#define SECFLAG_STREAMING   0x00000010
#define SECFLAG_QUANTUM     0x00000020
#define SECFLAG_RESTRICTED  0x00000040  /* Export controlled */
```

### **5.2 Section Processing Rules**

1. **Unknown sections with CRITICAL=1** → Return `AQUA_ERR_CRIT_SECTION_UNKNOWN`
1. **Unknown sections with CRITICAL=0** → Skip and log warning
1. **Integrity check failure** → Return `AQUA_ERR_INTEGRITY_FAIL`
1. **Nonce reuse detected** → Return `AQUA_ERR_NONCE_REUSE`

-----

## **6. Error Semantics**

### **6.1 Error Code Registry (Normative)**

```c
typedef enum {
    /* Success */
    AQUA_OK                         = 0,
    
    /* Structure Errors (1000-1099) */
    AQUA_ERR_CRIT_SECTION_UNKNOWN  = 1001,
    AQUA_ERR_INVALID_MAGIC          = 1002,
    AQUA_ERR_VERSION_UNSUPPORTED    = 1003,
    AQUA_ERR_MALFORMED_HEADER       = 1004,
    AQUA_ERR_SECTION_OVERFLOW       = 1005,
    
    /* Security Errors (1100-1199) */
    AQUA_ERR_AUTH_FAIL              = 1101,
    AQUA_ERR_INTEGRITY_FAIL         = 1102,
    AQUA_ERR_NONCE_REUSE            = 1103,
    AQUA_ERR_ALG_MISMATCH           = 1104,
    AQUA_ERR_VERSION_ROLLBACK       = 1105,
    AQUA_ERR_KEY_EXPIRED            = 1106,
    AQUA_ERR_CERT_INVALID           = 1107,
    AQUA_ERR_ALG_REVOKED            = 1108,
    
    /* Profile Errors (1200-1299) */
    AQUA_ERR_PROFILE_VIOLATION      = 1201,
    AQUA_ERR_PHYSICS_CONSTRAINT     = 1202,
    AQUA_ERR_CAPABILITY_MISSING     = 1203,
    
    /* Processing Errors (1300-1399) */
    AQUA_ERR_COMPRESSION_FAIL       = 1301,
    AQUA_ERR_DECOMPRESSION_FAIL     = 1302,
    AQUA_ERR_ENCRYPTION_FAIL        = 1303,
    AQUA_ERR_DECRYPTION_FAIL        = 1304,
    
    /* Resource Errors (1400-1499) */
    AQUA_ERR_OUT_OF_MEMORY          = 1401,
    AQUA_ERR_FILE_TOO_LARGE         = 1402,
    AQUA_ERR_QUOTA_EXCEEDED         = 1403
} aqua_err_t;
```

### **6.2 Error Handling Requirements**

- Errors in the 1000-1199 range SHALL terminate processing immediately
- Errors in the 1200-1299 range MAY allow fallback to a lower profile
- Errors in the 1300-1499 range MAY allow retry with different parameters

-----

## **7. Security Architecture**

### **7.1 PQC Suite (FIPS-Aligned)**

```c
typedef struct {
    uint16_t kem_algorithm;         /* ML_KEM, CLASSIC_MCELIECE */
    uint16_t signature_algorithm;   /* ML_DSA, SLH_DSA, FALCON */
    uint16_t hash_algorithm;        /* SHA3, BLAKE3, SHAKE */
    
    struct { /* ML-KEM (FIPS 203) */
        uint16_t security_level;    /* 512, 768, 1024 */
        uint32_t public_key_size;    /* MUST match table */
        uint32_t ciphertext_size;    /* MUST match table */
        uint32_t shared_secret_size; /* Always 32 */
    } ml_kem;
    
    struct { /* ML-DSA (FIPS 204) */
        uint16_t security_level;    /* 44, 65, 87 */
        uint32_t public_key_size;    /* MUST match table */
        uint32_t signature_size;     /* MUST match table */
    } ml_dsa;
    
    struct { /* Performance & Compliance */
        float32  keygen_ms;
        float32  encaps_ms;
        float32  decaps_ms;
        float32  sign_ms;
        float32  verify_ms;
        uint32_t acvp_session_id;    /* NIST ACVP session */
        uint8_t  cst_compliant;      /* Cryptographic Security Testing */
    } performance;
} PQC_Suite_V5_2;

/* FIPS-Mandated Sizes (Normative) */
#define ML_KEM_512_PK    800
#define ML_KEM_512_CT    768
#define ML_KEM_768_PK   1184
#define ML_KEM_768_CT   1088
#define ML_KEM_1024_PK  1568
#define ML_KEM_1024_CT  1568
#define ML_KEM_SS_LEN     32

#define ML_DSA_44_PK    1312
#define ML_DSA_44_SIG   2420
#define ML_DSA_65_PK    1952
#define ML_DSA_65_SIG   3293
#define ML_DSA_87_PK    2592
#define ML_DSA_87_SIG   4595
```

### **7.2 Key Derivation & AEAD (Normative)**

All content-encryption keys MUST be derived using HKDF-Extract-Expand with SHAKE256:

```c
typedef struct {
    uint8_t  kdf_algorithm;         /* MUST be HKDF_SHAKE256 (0x01) */
    uint32_t output_length;
    uint8_t  salt[32];              /* Default: header.uuid */
    uint8_t  info[64];              /* Context binding */
} KDF_Policy_V5_2;

/* Key Derivation */
IKM  = QKD_key_material || ML_KEM_shared_secret || context
salt = header.uuid
info = section_type || section_uuid || tool_id || version_tuple || purpose_tag
out  = { key_aead, nonce_prefix, hdr_protect_key }
```

**Prohibited Methods:**

- XOR combination is NOT RECOMMENDED and MUST NOT be used
- Simple concatenation MUST NOT be used without KDF

### **7.3 AEAD Configuration**

```c
typedef struct {
    uint8_t  aead_algorithm;        /* AES_256_GCM or XCHACHA20_POLY1305 */
    uint8_t  nonce_prefix[12];      /* Derived via HKDF */
    uint64_t nonce_counter;         /* Monotonic, per-section */
    uint32_t rekey_after_packets;   /* See table below */
    uint32_t rekey_after_seconds;   /* See table below */
    uint64_t packets_encrypted;     /* Current count */
    uint64_t encryption_start_time; /* Unix timestamp */
} AEAD_Config_V5_2;
```

**Rekey Policy (Normative Defaults):**

|Profile   |AEAD               |rekey_after_packets|rekey_after_seconds|
|----------|-------------------|-------------------|-------------------|
|LAB       |AES-256-GCM        |2^20               |600                |
|LAB       |XChaCha20-Poly1305 |2^32               |1800               |
|ADV/THEORY|Implementer-defined|≥ LAB              |≥ LAB              |

MUST rotate keys when either limit is reached.

### **7.4 Crypto-Agility Negotiation**

```cddl
; Algorithm Negotiation (CBOR)
alg-offer = {
  1: kem-list: [* [kem_id: uint, kem_level: uint]],
  2: sig-list: [* [sig_id: uint, sig_level: uint]],
  3: aead-list: [* uint],
  4: hash-list: [* uint]
}

alg-result = { 
  1: chosen-kem: [kem_id: uint, kem_level: uint],
  2: chosen-sig: [sig_id: uint, sig_level: uint],
  3: chosen-aead: uint,
  4: chosen-hash: uint
}

revocation = [* [alg_id: uint, level: uint]]
```

The `alg-result` MUST be included and signed within the Signature_Block.

### **7.5 Enhanced QKD Protocol**

```c
typedef struct {
    uint8_t  protocol_type;         /* BB84, E91, MDI_QKD */
    uint32_t key_length_bits;
    float32  target_error_rate;
    
    struct { /* Quantum Channel */
        uint8_t  channel_type;      /* FIBER, FREE_SPACE, SATELLITE */
        float64  channel_length_km;
        float32  attenuation_db;
        float32  background_noise;
    } quantum_channel;
    
    struct { /* Classical Authentication */
        uint8_t  auth_method;       /* PRESHARED, PQC_SIGNATURE */
        uint16_t signature_algorithm; /* e.g., ML_DSA_87 */
        uint8_t  auth_context[32];  /* link_id || epoch */
    } classical_auth;
    
    struct { /* Post-Processing */
        uint8_t  error_correction;  /* CASCADE, LDPC, POLAR */
        float32  reconciliation_eff; /* > 0.9 required */
        uint32_t block_size;
        uint8_t  hash_function;     /* TOEPLITZ, FFT */
        float32  epsilon_target;    /* ≤ 1e-10 (LAB profile) */
        uint32_t ec_latency_ms;     /* Error correction latency */
        uint32_t pa_latency_ms;     /* Privacy amplification latency */
        uint32_t final_key_length;
    } post_processing;
    
    struct { /* Security Countermeasures */
        uint8_t  decoy_states_enabled;
        uint8_t  num_decoy_levels;
        float32  decoy_intensity[3];
        uint8_t  detector_monitoring;
        uint8_t  trojan_horse_filter;
        uint8_t  mdi_qkd_enabled;   /* Measurement-device-independent */
    } security_measures;
    
    struct { /* Output Key */
        uint8_t  key_id[16];
        uint32_t key_length;
        uint64_t generation_ts;
        float32  estimated_security;
        uint8_t  key_material[4096]; /* Secure storage */
    } output_key;
} QKD_Protocol_V5_2;
```

### **7.6 Side-Channel Resistance Criteria**

```c
typedef struct {
    /* Measurable Criteria */
    struct {
        uint8_t  code_audited;
        float32  timing_jitter_us;  /* Max acceptable: 0.1 */
        uint8_t  constant_time_verified;
    } timing_resistance;
    
    struct {
        float32  tvla_threshold;    /* TVLA t-test: < 4.5 */
        float32  welch_t_test;      /* Welch test: < 4.5 */
        uint8_t  masking_order;     /* Minimum: 1 */
    } power_analysis;
    
    struct {
        uint8_t  no_secret_indexed_lookups;
        uint8_t  cache_line_isolation;
        uint8_t  prefetch_disabled;
    } cache_timing;
    
    /* Compliance */
    uint32_t acvp_session_id;      /* MUST record for production */
    uint8_t  cst_validated;        /* Cryptographic Security Testing */
    uint64_t validation_date;
} SideChannel_Resistance_V5_2;
```

-----

## **8. Data Section Specifications**

### **8.1 Section Type Registry (Normative)**

```c
/* AQUA Section Type Registry - IANA-style allocation */

/* Core Sections (0x0000-0x00FF) - Specification Required */
#define SECTION_METADATA                0x0001
#define SECTION_CLASSICAL_DATA          0x0002
#define SECTION_COMPRESSED              0x0003
#define SECTION_ENCRYPTED               0x0004

/* Quantum Sections (0x0100-0x01FF) - Specification Required */
#define SECTION_QUANTUM_CIRCUIT         0x0100
#define SECTION_QUANTUM_STATE           0x0101
#define SECTION_ENTANGLEMENT_MAP        0x0102
#define SECTION_QKD_SESSION             0x0103

/* AGI Sections (0x0200-0x02FF) - Expert Review Required */
#define SECTION_AGI_REASONING           0x0200
#define SECTION_AGI_KNOWLEDGE           0x0201
#define SECTION_AGI_EXECUTION           0x0202
#define SECTION_AGI_SAFETY_POLICY       0x0203

/* Consciousness Sections (0x0300-0x03FF) - Ethics Review Required */
#define SECTION_CONSCIOUSNESS_MODEL     0x0300
#define SECTION_CONSCIOUSNESS_STATE     0x0301
#define SECTION_SUBJECTIVE_EXPERIENCE   0x0302

/* Reserved Ranges */
/* 0x0400-0x7FFF - Future standardization */
/* 0x8000-0xFFFF - Private use (no registration required) */
```

-----

## **9. Validation Requirements**

### **9.1 Validation Checklist (Normative)**

**Structure Validation:**

- [ ] Magic number equals 0x41515541
- [ ] Header canonical CBOR hash matches recorded value
- [ ] Section Table offsets and lengths are valid
- [ ] Per-section integrity (SHA-256 of plaintext) verified
- [ ] Unknown critical sections cause hard failure
- [ ] All padding bytes are zero

**Security Validation:**

- [ ] Signature covers complete canonical hash domain
- [ ] Keys derived via HKDF(SHAKE256) with proper context binding
- [ ] AEAD nonce uniqueness enforced (monotonic counter)
- [ ] PQC algorithm sizes exactly match FIPS tables
- [ ] Algorithms are registered and not revoked
- [ ] QKD post-processing meets epsilon_target ≤ 1e-10 (LAB)
- [ ] Side-channel resistance criteria met
- [ ] ACVP/CST session recorded for PQC implementations

**Profile Validation:**

- [ ] LAB parser rejects THEORY-only sections
- [ ] ADV marks speculative fields as non-critical
- [ ] Physics constraints enforced per profile

-----

## **10. Implementation Profiles**

### **10.1 Profile Boundaries (Normative)**

**LAB Profile (TRL 6-9):**

- MUST NOT enable non-physical features (e.g., FTL communication)
- Teleportation fields MAY exist but MUST be inert
- All cryptographic algorithms MUST be FIPS-validated
- QKD epsilon_target MUST be ≤ 1e-10

**ADV Profile (TRL 3-6):**

- MAY include simulation hooks for speculative sections
- Speculative bits are non-normative
- CRITICAL flag MUST be 0 for experimental features

**THEORY Profile (TRL 1-3):**

- Speculative sections allowed
- CRITICAL flag MUST be 0 for forward compatibility
- Physics constraints MAY be relaxed for research

-----

## **11. Conformance**

### **11.1 Conformance Classes (Updated)**

**Class A: Full Implementation**

- Supports all profiles with profile isolation
- Implements canonical CBOR serialization
- Full crypto-agility negotiation support
- Passes all security validation criteria
- ACVP/CST validated

**Class B: Production Implementation**

- Supports LAB and ADV profiles
- Canonical CBOR for critical structures
- Fixed algorithm suite acceptable
- Passes core security validation

**Class C: Basic Implementation**

- LAB profile only
- Minimal security requirements
- Read-only or controlled environment use

-----

## **12. IANA Considerations**

### **12.1 Registry Creation**

This document requests IANA to create the “AQUA File Format” registry with the following sub-registries:

**Algorithm Registries:**

- AEAD Algorithm IDs (0-65535)
- Hash Algorithm IDs (0-65535)
- KEM Algorithm IDs (0-65535)
- Signature Algorithm IDs (0-65535)
- QKD Protocol IDs (0-255)

**Initial Allocations:**

|Registry |ID|Algorithm         |Reference|
|---------|--|------------------|---------|
|AEAD     |1 |AES-256-GCM       |[RFC5288]|
|AEAD     |2 |XChaCha20-Poly1305|[RFC8439]|
|Hash     |1 |SHA3-256          |[FIPS202]|
|Hash     |2 |SHA3-512          |[FIPS202]|
|Hash     |3 |SHAKE256          |[FIPS202]|
|Hash     |4 |BLAKE3            |[BLAKE3] |
|KEM      |1 |ML-KEM            |[FIPS203]|
|KEM      |2 |Classic-McEliece  |[CLASSIC]|
|Signature|1 |ML-DSA            |[FIPS204]|
|Signature|2 |SLH-DSA           |[FIPS205]|
|Signature|3 |Falcon            |[FALCON] |
|QKD      |1 |BB84              |[BB84]   |
|QKD      |2 |E91               |[E91]    |
|QKD      |3 |MDI-QKD           |[MDI]    |

### **12.2 URN Namespace**

AQUA algorithm URNs follow the pattern:

```
urn:aqua:alg:<type>:<name>:<param>
```

Examples:

- `urn:aqua:alg:kem:ml-kem:1024`
- `urn:aqua:alg:aead:xchacha20poly1305`
- `urn:aqua:alg:qkd:bb84`

-----

## **13. References**

### **13.1 Normative References**

[RFC2119] Bradner, S., “Key words for use in RFCs”, BCP 14, RFC 2119, March 1997.

[RFC8174] Leiba, B., “Ambiguity of Uppercase vs Lowercase”, BCP 14, RFC 8174, May 2017.

[RFC8949] Bormann, C. and P. Hoffman, “Concise Binary Object Representation (CBOR)”, STD 94, RFC 8949, December 2020.

[FIPS203] NIST, “Module-Lattice-Based Key-Encapsulation Mechanism Standard”, FIPS 203, August 2024.

[FIPS204] NIST, “Module-Lattice-Based Digital Signature Standard”, FIPS 204, August 2024.

[FIPS205] NIST, “Stateless Hash-Based Digital Signature Standard”, FIPS 205, August 2024.

-----

## **14. Appendices**

### **Appendix A: Example CBOR File (Minimal LAB Profile)**

```cbor-diag
{
  1: h'41515541',                    # magic
  2: [5, 1, 2, 0],                   # version 5.1.2.0
  3: 0x00000001,                     # flags
  4: 0x00000003,                     # capabilities
  5: 1,                              # LAB profile
  6: [1723456789, 1723456789],       # timestamps
  7: h'123e4567e89b12d3a456426614174000', # UUID
  8: h'00000000000000000000000000000000', # parent UUID
  9: "AQUA Reference Implementation",
  10: "AQUA Consortium",
  11: "Minimal LAB profile test file",
  12: 512,                           # header size
  13: 0x12345678,                    # CRC32
  14: h'abcdef...256bits...',        # SHA-256
  15: [5, 1, 0, 0]                   # min version 5.1.0.0
}
```

### **Appendix B: Negotiation Example**

```cbor-diag
# Algorithm Offer
{
  1: [[1, 1024], [1, 768]],         # ML-KEM-1024, ML-KEM-768
  2: [[1, 87], [3, 3]],             # ML-DSA-87, Falcon-3  
  3: [1, 2],                        # AES-GCM, XChaCha20-Poly1305
  4: [3]                            # SHAKE256
}

# Algorithm Result (chosen)
{
  1: [1, 1024],                     # ML-KEM-1024
  2: [1, 87],                       # ML-DSA-87
  3: 2,                             # XChaCha20-Poly1305
  4: 3                              # SHAKE256
}

# Revocation Vector
[[3, 2]]                            # Revoke Falcon-2
```

### **Appendix C: Conformance Test Harness (Skeleton)**

```python
#!/usr/bin/env python3
"""AQUA Format v5.1.2 Conformance Validator"""

import cbor2
import hashlib
from enum import IntEnum

class AQUAError(IntEnum):
    OK = 0
    CRIT_SECTION_UNKNOWN = 1001
    AUTH_FAIL = 1101
    INTEGRITY_FAIL = 1102
    NONCE_REUSE = 1103
    
class AQUAValidator:
    def __init__(self, strict_mode=True):
        self.strict = strict_mode
        
    def validate_header(self, data):
        """Validate CBOR header structure"""
        header = cbor2.loads(data)
        
        # Check magic
        if header[1] != b'AQUA':
            return AQUAError.INVALID_MAGIC
            
        # Verify canonical encoding
        canonical = cbor2.dumps(header, canonical=True)
        if canonical != data:
            return AQUAError.MALFORMED_HEADER
            
        # Check SHA-256
        computed = hashlib.sha256(canonical).digest()
        if computed != header[14]:
            return AQUAError.INTEGRITY_FAIL
            
        return AQUAError.OK
        
    def validate_section_table(self, table):
        """Validate section entries"""
        for entry in table['entries']:
            if entry['flags'] & 0x01:  # CRITICAL
                if not self.is_known_section(entry['type']):
                    return AQUAError.CRIT_SECTION_UNKNOWN
        return AQUAError.OK

# Usage
validator = AQUAValidator(strict_mode=True)
with open('test.aqua', 'rb') as f:
    result = validator.validate_header(f.read(512))
    if result != AQUAError.OK:
        print(f"Validation failed: {result.name}")
```

### **Appendix D: Privacy Controls for Consciousness Sections**

If any `CONSCIOUSNESS_*` sections are present in LAB or ADV profiles:

- MUST include `consent_record_id` (verifiable) in metadata
- MUST NOT set EXPORT flag for third-party distribution unless consent scope permits
- SHOULD implement data minimization for subjective experience encoding
- SHALL provide audit trail for all consciousness data access

-----

## **Editor’s Notes**

This v5.1.2 draft represents a comprehensive security hardening based on implementation experience. Key improvements include:

1. **Deterministic serialization** ensures reproducible hashing across implementations
1. **Per-section integrity** prevents tampering even in encrypted sections
1. **Mandatory HKDF** eliminates weak key combination methods
1. **ACVP/CST hooks** enable formal cryptographic validation
1. **Registry system** provides clear extensibility path

Future work items for v5.2:

- Streaming protocol enhancements
- Quantum error correction codes
- AGI safety policy templates
- Interplanetary sync optimization

-----

**END OF SPECIFICATION**

**Document Status**: PROPOSED STANDARD (Editors’ Draft)  
**Version**: 5.1.2  
**Last Updated**: August 12, 2025, 18:00 UTC  
**Total Pages**: 68

**Implementation Note**: Reference implementation with full v5.1.2 support available at:

- Repository: `github.com/aqua-os/aqua-format`
- Branch: `v5.1.2-editors-draft`
- Test Vectors: `test/vectors/v5.1.2/`

**For Comments**: Submit to spec-comments@aqua-os.org with subject “[v5.1.2]”

**© 2025 AQUA Consortium. All rights reserved.**
