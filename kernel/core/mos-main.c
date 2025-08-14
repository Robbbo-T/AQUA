/**
 * MOS (Managed Operating System) Kernel Core
 * UTCS-MI Code: [026] MOS Kernel Core
 * 
 * Main kernel initialization and management system for AQUA OS
 */

#include <stdint.h>
#include <stdbool.h>
#include "mos-kernel.h"

// Kernel version and identification
#define MOS_VERSION_MAJOR 1
#define MOS_VERSION_MINOR 0
#define MOS_VERSION_PATCH 0
#define MOS_BUILD_ID "AQUA-MOS-2025"

// Kernel subsystem status
typedef struct {
    bool process_manager_ready;
    bool memory_manager_ready;
    bool scheduler_ready;
    bool io_manager_ready;
    bool network_stack_ready;
    bool quantum_gateway_ready;
    bool security_manager_ready;
} mos_subsystem_status_t;

static mos_subsystem_status_t subsystem_status = {0};

/**
 * Initialize MOS kernel core
 */
int mos_kernel_init(void) {
    printk("MOS Kernel Core v%d.%d.%d initializing...\n", 
           MOS_VERSION_MAJOR, MOS_VERSION_MINOR, MOS_VERSION_PATCH);
    
    // Initialize core subsystems in order
    if (process_manager_init() != 0) {
        printk("FATAL: Process manager initialization failed\n");
        return -1;
    }
    subsystem_status.process_manager_ready = true;
    
    if (memory_manager_init() != 0) {
        printk("FATAL: Memory manager initialization failed\n");
        return -1;
    }
    subsystem_status.memory_manager_ready = true;
    
    if (scheduler_init() != 0) {
        printk("FATAL: Scheduler initialization failed\n");
        return -1;
    }
    subsystem_status.scheduler_ready = true;
    
    if (io_manager_init() != 0) {
        printk("FATAL: I/O manager initialization failed\n");
        return -1;
    }
    subsystem_status.io_manager_ready = true;
    
    if (network_stack_init() != 0) {
        printk("WARNING: Network stack initialization failed\n");
        // Non-fatal, continue boot
    } else {
        subsystem_status.network_stack_ready = true;
    }
    
    if (quantum_gateway_init() != 0) {
        printk("WARNING: Quantum gateway initialization failed, falling back to classical mode\n");
        // Non-fatal, system can operate in classical mode
    } else {
        subsystem_status.quantum_gateway_ready = true;
        printk("Quantum capabilities enabled\n");
    }
    
    if (security_manager_init() != 0) {
        printk("FATAL: Security manager initialization failed\n");
        return -1;
    }
    subsystem_status.security_manager_ready = true;
    
    printk("MOS Kernel Core initialization complete\n");
    return 0;
}

/**
 * Get kernel subsystem status
 */
mos_subsystem_status_t* mos_get_subsystem_status(void) {
    return &subsystem_status;
}

/**
 * Kernel main loop
 */
void mos_kernel_main(void) {
    printk("Starting MOS kernel main loop\n");
    
    // Start scheduler
    scheduler_start();
    
    // Enable interrupts
    enable_interrupts();
    
    // Kernel idle loop
    while (1) {
        // Handle system maintenance tasks
        scheduler_tick();
        
        // Process quantum events if available
        if (subsystem_status.quantum_gateway_ready) {
            quantum_gateway_process_events();
        }
        
        // Yield to scheduler
        schedule();
    }
}

/**
 * Kernel shutdown sequence
 */
void mos_kernel_shutdown(void) {
    printk("MOS Kernel shutdown initiated\n");
    
    // Shutdown subsystems in reverse order
    security_manager_shutdown();
    quantum_gateway_shutdown();
    network_stack_shutdown();
    io_manager_shutdown();
    scheduler_shutdown();
    memory_manager_shutdown();
    process_manager_shutdown();
    
    printk("MOS Kernel shutdown complete\n");
}