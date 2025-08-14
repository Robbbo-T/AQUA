/**
 * Security Manager
 * UTCS-MI Code: [047] Security Manager
 * 
 * Advanced security system with post-quantum cryptography
 */

#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "security-manager.h"
#include "post-quantum-crypto.h"

// Security levels
typedef enum {
    SECURITY_LEVEL_MINIMAL = 1,
    SECURITY_LEVEL_STANDARD = 2,
    SECURITY_LEVEL_HIGH = 3,
    SECURITY_LEVEL_MAXIMUM = 4,
    SECURITY_LEVEL_QUANTUM_SAFE = 5
} security_level_t;

// Security context
typedef struct {
    uint32_t process_id;
    security_level_t level;
    uint32_t permissions;
    uint8_t pqc_key_id[32];
    bool quantum_access_allowed;
} security_context_t;

static security_level_t system_security_level = SECURITY_LEVEL_QUANTUM_SAFE;
static security_context_t security_contexts[MAX_PROCESSES];
static bool pqc_initialized = false;

/**
 * Initialize security manager
 */
int security_manager_init(void) {
    printk("Security Manager initializing...\n");
    
    // Initialize post-quantum cryptography
    if (pqc_init() != 0) {
        printk("FATAL: Post-quantum cryptography initialization failed\n");
        return -1;
    }
    pqc_initialized = true;
    
    // Initialize security contexts
    memset(security_contexts, 0, sizeof(security_contexts));
    
    // Set system security level based on configuration
    system_security_level = SECURITY_LEVEL_QUANTUM_SAFE;
    
    // Initialize access control matrices
    if (init_access_control() != 0) {
        printk("FATAL: Access control initialization failed\n");
        return -1;
    }
    
    // Initialize audit logging
    if (init_audit_logging() != 0) {
        printk("WARNING: Audit logging initialization failed\n");
        // Non-fatal, continue
    }
    
    printk("Security Manager initialized - Level: %d, PQC: %s\n", 
           system_security_level, pqc_initialized ? "enabled" : "disabled");
    
    return 0;
}

/**
 * Create security context for a process
 */
int create_security_context(uint32_t pid, security_level_t level, uint32_t permissions) {
    if (pid >= MAX_PROCESSES) {
        return -1;
    }
    
    security_context_t *ctx = &security_contexts[pid];
    ctx->process_id = pid;
    ctx->level = level;
    ctx->permissions = permissions;
    ctx->quantum_access_allowed = (level >= SECURITY_LEVEL_HIGH);
    
    // Generate post-quantum keys for this process
    if (pqc_initialized) {
        if (pqc_generate_keypair(ctx->pqc_key_id, 32) != 0) {
            printk("WARNING: Failed to generate PQC keys for PID %d\n", pid);
        }
    }
    
    audit_log("SECURITY_CONTEXT_CREATED", pid, level);
    
    printk("Security context created for PID %d, level %d\n", pid, level);
    return 0;
}

/**
 * Check access permission
 */
bool check_access_permission(uint32_t pid, uint32_t resource_id, uint32_t operation) {
    if (pid >= MAX_PROCESSES) {
        return false;
    }
    
    security_context_t *ctx = &security_contexts[pid];
    
    // Check basic permissions
    if ((ctx->permissions & operation) == 0) {
        audit_log("ACCESS_DENIED_PERMISSION", pid, resource_id);
        return false;
    }
    
    // Check security level requirements
    uint32_t required_level = get_resource_security_level(resource_id);
    if (ctx->level < required_level) {
        audit_log("ACCESS_DENIED_SECURITY_LEVEL", pid, resource_id);
        return false;
    }
    
    // Special check for quantum resources
    if (is_quantum_resource(resource_id) && !ctx->quantum_access_allowed) {
        audit_log("ACCESS_DENIED_QUANTUM", pid, resource_id);
        return false;
    }
    
    audit_log("ACCESS_GRANTED", pid, resource_id);
    return true;
}

/**
 * Encrypt data using post-quantum cryptography
 */
int encrypt_data_pqc(const uint8_t *plaintext, uint32_t plaintext_len,
                     uint8_t *ciphertext, uint32_t *ciphertext_len,
                     const uint8_t *key_id) {
    if (!pqc_initialized) {
        return -1;
    }
    
    return pqc_encrypt(plaintext, plaintext_len, ciphertext, ciphertext_len, key_id);
}

/**
 * Decrypt data using post-quantum cryptography
 */
int decrypt_data_pqc(const uint8_t *ciphertext, uint32_t ciphertext_len,
                     uint8_t *plaintext, uint32_t *plaintext_len,
                     const uint8_t *key_id) {
    if (!pqc_initialized) {
        return -1;
    }
    
    return pqc_decrypt(ciphertext, ciphertext_len, plaintext, plaintext_len, key_id);
}

/**
 * Validate digital signature
 */
bool validate_digital_signature(const uint8_t *data, uint32_t data_len,
                                const uint8_t *signature, uint32_t signature_len,
                                const uint8_t *public_key) {
    if (!pqc_initialized) {
        return false;
    }
    
    return pqc_verify_signature(data, data_len, signature, signature_len, public_key);
}

/**
 * Generate secure random data
 */
int generate_secure_random(uint8_t *buffer, uint32_t length) {
    // Use quantum entropy source if available
    if (is_quantum_entropy_available()) {
        return quantum_random_bytes(buffer, length);
    } else {
        return hardware_random_bytes(buffer, length);
    }
}

/**
 * Security threat assessment
 */
security_threat_level_t assess_threat_level(uint32_t pid) {
    security_context_t *ctx = &security_contexts[pid];
    
    // Analyze process behavior
    uint32_t suspicious_activities = count_suspicious_activities(pid);
    uint32_t failed_access_attempts = count_failed_access_attempts(pid);
    
    if (suspicious_activities > 10 || failed_access_attempts > 5) {
        audit_log("HIGH_THREAT_DETECTED", pid, suspicious_activities);
        return THREAT_LEVEL_HIGH;
    } else if (suspicious_activities > 5 || failed_access_attempts > 2) {
        return THREAT_LEVEL_MEDIUM;
    } else {
        return THREAT_LEVEL_LOW;
    }
}

/**
 * Get security status
 */
void get_security_status(security_status_t *status) {
    status->system_security_level = system_security_level;
    status->pqc_enabled = pqc_initialized;
    status->quantum_access_enabled = is_quantum_hardware_available();
    status->active_contexts = 0;
    status->threat_level = THREAT_LEVEL_LOW;
    
    // Count active security contexts
    for (int i = 0; i < MAX_PROCESSES; i++) {
        if (security_contexts[i].process_id > 0) {
            status->active_contexts++;
            
            // Check for elevated threat levels
            security_threat_level_t threat = assess_threat_level(i);
            if (threat > status->threat_level) {
                status->threat_level = threat;
            }
        }
    }
}

/**
 * Shutdown security manager
 */
void security_manager_shutdown(void) {
    // Clear all security contexts
    memset(security_contexts, 0, sizeof(security_contexts));
    
    // Shutdown post-quantum cryptography
    if (pqc_initialized) {
        pqc_shutdown();
        pqc_initialized = false;
    }
    
    // Shutdown audit logging
    shutdown_audit_logging();
    
    printk("Security Manager shutdown complete\n");
}