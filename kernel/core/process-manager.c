/**
 * Process Manager
 * UTCS-MI Code: [030] Process Manager
 * 
 * Manages process lifecycle, scheduling, and quantum-classical hybrid processes
 */

#include <stdint.h>
#include <stdbool.h>
#include "process-manager.h"

#define MAX_PROCESSES 1024
#define QUANTUM_PROCESS_FLAG 0x8000

typedef enum {
    PROCESS_STATE_NEW,
    PROCESS_STATE_READY,
    PROCESS_STATE_RUNNING,
    PROCESS_STATE_WAITING,
    PROCESS_STATE_QUANTUM_BLOCKED,
    PROCESS_STATE_TERMINATED
} process_state_t;

typedef struct process_control_block {
    uint32_t pid;
    uint32_t parent_pid;
    process_state_t state;
    uint32_t flags;
    
    // Memory management
    uint64_t virtual_address_space;
    uint64_t memory_size;
    
    // Quantum resources
    uint32_t allocated_qubits;
    uint32_t quantum_circuit_id;
    
    // Scheduling
    uint32_t priority;
    uint64_t cpu_time_used;
    uint64_t quantum_time_used;
    
    // Process tree
    struct process_control_block *parent;
    struct process_control_block *children;
    struct process_control_block *siblings;
    struct process_control_block *next;
} pcb_t;

static pcb_t process_table[MAX_PROCESSES];
static pcb_t *free_process_list = NULL;
static pcb_t *ready_queue = NULL;
static pcb_t *quantum_queue = NULL;
static uint32_t next_pid = 1;

/**
 * Initialize process manager
 */
int process_manager_init(void) {
    // Initialize process table
    for (int i = 0; i < MAX_PROCESSES; i++) {
        process_table[i].pid = 0;
        process_table[i].state = PROCESS_STATE_NEW;
        process_table[i].next = (i < MAX_PROCESSES - 1) ? &process_table[i + 1] : NULL;
    }
    
    free_process_list = &process_table[0];
    ready_queue = NULL;
    quantum_queue = NULL;
    
    printk("Process Manager initialized - max processes: %d\n", MAX_PROCESSES);
    return 0;
}

/**
 * Create a new process
 */
uint32_t create_process(const char *name, void *entry_point, uint32_t flags) {
    if (free_process_list == NULL) {
        printk("ERROR: No free process slots available\n");
        return 0;
    }
    
    pcb_t *pcb = free_process_list;
    free_process_list = free_process_list->next;
    
    // Initialize process control block
    pcb->pid = next_pid++;
    pcb->parent_pid = get_current_pid();
    pcb->state = PROCESS_STATE_READY;
    pcb->flags = flags;
    pcb->priority = 100;  // Default priority
    pcb->cpu_time_used = 0;
    pcb->quantum_time_used = 0;
    pcb->allocated_qubits = 0;
    pcb->quantum_circuit_id = 0;
    
    // Allocate virtual address space
    pcb->virtual_address_space = allocate_virtual_address_space();
    pcb->memory_size = 0;
    
    // Add to ready queue
    add_to_ready_queue(pcb);
    
    printk("Process created: PID=%d, name=%s, flags=0x%x\n", pcb->pid, name, flags);
    return pcb->pid;
}

/**
 * Create a quantum-enabled process
 */
uint32_t create_quantum_process(const char *name, void *entry_point, uint32_t qubit_count) {
    uint32_t flags = QUANTUM_PROCESS_FLAG;
    uint32_t pid = create_process(name, entry_point, flags);
    
    if (pid > 0) {
        pcb_t *pcb = get_process_by_pid(pid);
        if (pcb && allocate_quantum_resources(pcb, qubit_count) == 0) {
            pcb->allocated_qubits = qubit_count;
            add_to_quantum_queue(pcb);
            printk("Quantum process created: PID=%d, qubits=%d\n", pid, qubit_count);
        } else {
            printk("WARNING: Failed to allocate quantum resources for PID=%d\n", pid);
        }
    }
    
    return pid;
}

/**
 * Process scheduler integration
 */
void process_manager_tick(void) {
    // Update process statistics
    pcb_t *current = get_current_process();
    if (current) {
        current->cpu_time_used++;
        
        if (current->flags & QUANTUM_PROCESS_FLAG) {
            current->quantum_time_used++;
        }
    }
    
    // Handle quantum process timeouts
    process_quantum_timeouts();
}

/**
 * Terminate a process
 */
int terminate_process(uint32_t pid) {
    pcb_t *pcb = get_process_by_pid(pid);
    if (!pcb) {
        return -1;
    }
    
    // Free quantum resources if allocated
    if (pcb->flags & QUANTUM_PROCESS_FLAG) {
        free_quantum_resources(pcb);
    }
    
    // Free virtual address space
    free_virtual_address_space(pcb->virtual_address_space);
    
    // Remove from queues
    remove_from_ready_queue(pcb);
    remove_from_quantum_queue(pcb);
    
    // Mark as terminated and return to free list
    pcb->state = PROCESS_STATE_TERMINATED;
    pcb->next = free_process_list;
    free_process_list = pcb;
    
    printk("Process terminated: PID=%d\n", pid);
    return 0;
}

/**
 * Get process statistics
 */
void get_process_stats(process_stats_t *stats) {
    stats->total_processes = 0;
    stats->quantum_processes = 0;
    stats->running_processes = 0;
    
    for (int i = 0; i < MAX_PROCESSES; i++) {
        if (process_table[i].pid > 0) {
            stats->total_processes++;
            
            if (process_table[i].flags & QUANTUM_PROCESS_FLAG) {
                stats->quantum_processes++;
            }
            
            if (process_table[i].state == PROCESS_STATE_RUNNING) {
                stats->running_processes++;
            }
        }
    }
}

/**
 * Shutdown process manager
 */
void process_manager_shutdown(void) {
    // Terminate all processes gracefully
    for (int i = 0; i < MAX_PROCESSES; i++) {
        if (process_table[i].pid > 0 && process_table[i].state != PROCESS_STATE_TERMINATED) {
            terminate_process(process_table[i].pid);
        }
    }
    
    printk("Process Manager shutdown complete\n");
}