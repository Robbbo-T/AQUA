/*
 * MOS Task Scheduler
 * UTCS-MI Code: [051] Task Scheduler
 * 
 * Hybrid quantum-classical task scheduler for AQUA OS
 */

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#define MAX_PRIORITY_LEVELS 256
#define DEFAULT_TIME_SLICE_MS 10
#define QUANTUM_COHERENCE_THRESHOLD_MS 1

// Scheduling algorithms
typedef enum {
    SCHED_ROUND_ROBIN = 0,
    SCHED_PRIORITY_PREEMPTIVE,
    SCHED_QUANTUM_AWARE,
    SCHED_HYBRID_ADAPTIVE
} scheduling_algorithm_t;

// Task types for scheduling
typedef enum {
    TASK_TYPE_CLASSICAL = 0,
    TASK_TYPE_QUANTUM,
    TASK_TYPE_HYBRID,
    TASK_TYPE_REAL_TIME
} task_type_t;

// Scheduling priority classes
typedef enum {
    PRIORITY_CLASS_IDLE = 0,      // 0-63: Idle/background tasks
    PRIORITY_CLASS_NORMAL,        // 64-127: Normal user tasks
    PRIORITY_CLASS_HIGH,          // 128-191: High priority tasks
    PRIORITY_CLASS_REAL_TIME,     // 192-255: Real-time critical tasks
    PRIORITY_CLASS_QUANTUM_BOOST  // Special boost for quantum coherence
} priority_class_t;

// Runqueue structure
typedef struct runqueue {
    struct process_control_block* head;
    struct process_control_block* tail;
    uint32_t count;
    uint64_t total_wait_time;
} runqueue_t;

// Scheduler statistics
typedef struct scheduler_stats {
    uint64_t context_switches;
    uint64_t quantum_preservations;
    uint64_t coherence_violations;
    uint64_t real_time_misses;
    uint64_t idle_time;
    uint64_t quantum_time;
    uint64_t classical_time;
} scheduler_stats_t;

// Scheduler state
typedef struct scheduler_state {
    runqueue_t priority_queues[MAX_PRIORITY_LEVELS];
    runqueue_t quantum_coherent_queue;    // Special queue for quantum coherent tasks
    runqueue_t real_time_queue;           // Real-time tasks queue
    
    struct process_control_block* current_task;
    scheduling_algorithm_t algorithm;
    uint32_t time_slice_ms;
    uint64_t last_schedule_time;
    bool quantum_scheduling_enabled;
    bool preemption_enabled;
    
    scheduler_stats_t stats;
} scheduler_state_t;

// Global scheduler state
static scheduler_state_t g_scheduler = {0};

// Function prototypes
int scheduler_init(void);
void scheduler_tick(void);
int schedule_task(struct process_control_block* task);
int unschedule_task(struct process_control_block* task);
struct process_control_block* select_next_task(void);
void update_task_priority(struct process_control_block* task);
void handle_quantum_coherence(void);
void preempt_current_task(void);

// Priority calculation functions
uint8_t calculate_dynamic_priority(struct process_control_block* task);
bool should_boost_quantum_priority(struct process_control_block* task);
void apply_quantum_priority_boost(struct process_control_block* task);
void decay_priority_boost(struct process_control_block* task);

/*
 * Initialize the scheduler
 */
int scheduler_init(void)
{
    printk("Initializing Task Scheduler...\n");
    
    // Initialize runqueues
    for (int i = 0; i < MAX_PRIORITY_LEVELS; i++) {
        g_scheduler.priority_queues[i].head = NULL;
        g_scheduler.priority_queues[i].tail = NULL;
        g_scheduler.priority_queues[i].count = 0;
        g_scheduler.priority_queues[i].total_wait_time = 0;
    }
    
    // Initialize special queues
    g_scheduler.quantum_coherent_queue.head = NULL;
    g_scheduler.quantum_coherent_queue.tail = NULL;
    g_scheduler.quantum_coherent_queue.count = 0;
    
    g_scheduler.real_time_queue.head = NULL;
    g_scheduler.real_time_queue.tail = NULL;
    g_scheduler.real_time_queue.count = 0;
    
    // Set scheduler configuration
    g_scheduler.current_task = NULL;
    g_scheduler.algorithm = SCHED_HYBRID_ADAPTIVE;
    g_scheduler.time_slice_ms = DEFAULT_TIME_SLICE_MS;
    g_scheduler.quantum_scheduling_enabled = true;
    g_scheduler.preemption_enabled = true;
    g_scheduler.last_schedule_time = get_system_time();
    
    // Initialize statistics
    memset(&g_scheduler.stats, 0, sizeof(scheduler_stats_t));
    
    printk("Task Scheduler initialized\n");
    printk("Algorithm: Hybrid Adaptive\n");
    printk("Time slice: %u ms\n", g_scheduler.time_slice_ms);
    printk("Quantum scheduling: %s\n", 
           g_scheduler.quantum_scheduling_enabled ? "ENABLED" : "DISABLED");
    
    return 0;
}

/*
 * Main scheduler tick - called by timer interrupt
 */
void scheduler_tick(void)
{
    uint64_t current_time = get_system_time();
    
    // Handle quantum coherence monitoring
    if (g_scheduler.quantum_scheduling_enabled) {
        handle_quantum_coherence();
    }
    
    // Check if current task's time slice expired
    if (g_scheduler.current_task) {
        uint64_t elapsed = current_time - g_scheduler.last_schedule_time;
        uint64_t time_slice_ns = g_scheduler.time_slice_ms * 1000000ULL;
        
        if (elapsed >= time_slice_ns) {
            preempt_current_task();
        }
    }
    
    // Select and switch to next task
    struct process_control_block* next_task = select_next_task();
    if (next_task && next_task != g_scheduler.current_task) {
        // Perform context switch
        struct process_control_block* prev_task = g_scheduler.current_task;
        
        if (switch_context(prev_task, next_task) == 0) {
            g_scheduler.current_task = next_task;
            g_scheduler.last_schedule_time = current_time;
            g_scheduler.stats.context_switches++;
            
            // Update task states
            if (prev_task) {
                prev_task->state = PROCESS_READY;
                schedule_task(prev_task); // Add back to runqueue
            }
            next_task->state = PROCESS_RUNNING;
        }
    }
}

/*
 * Add a task to the appropriate runqueue
 */
int schedule_task(struct process_control_block* task)
{
    if (!task) {
        return -1;
    }
    
    runqueue_t* target_queue = NULL;
    
    // Determine target queue based on task characteristics
    if (task->type == PROCESS_TYPE_QUANTUM && task->quantum_coherent) {
        // Quantum coherent tasks get special priority
        target_queue = &g_scheduler.quantum_coherent_queue;
        printk("Scheduling quantum coherent task PID %u\n", task->pid);
    } else if (task->priority >= 192) {
        // Real-time tasks
        target_queue = &g_scheduler.real_time_queue;
    } else {
        // Regular priority-based scheduling
        target_queue = &g_scheduler.priority_queues[task->priority];
    }
    
    // Add to end of queue (FIFO within priority)
    task->next = NULL;
    if (target_queue->tail) {
        target_queue->tail->next = task;
    } else {
        target_queue->head = task;
    }
    target_queue->tail = task;
    target_queue->count++;
    
    return 0;
}

/*
 * Remove a task from runqueues
 */
int unschedule_task(struct process_control_block* task)
{
    if (!task) {
        return -1;
    }
    
    // Search through all queues to find and remove the task
    runqueue_t* queues[] = {
        &g_scheduler.quantum_coherent_queue,
        &g_scheduler.real_time_queue
    };
    
    // Check special queues first
    for (int i = 0; i < 2; i++) {
        runqueue_t* queue = queues[i];
        struct process_control_block* current = queue->head;
        struct process_control_block* prev = NULL;
        
        while (current) {
            if (current->pid == task->pid) {
                // Remove from queue
                if (prev) {
                    prev->next = current->next;
                } else {
                    queue->head = current->next;
                }
                
                if (current == queue->tail) {
                    queue->tail = prev;
                }
                
                queue->count--;
                current->next = NULL;
                return 0;
            }
            prev = current;
            current = current->next;
        }
    }
    
    // Check priority queues
    for (int i = 0; i < MAX_PRIORITY_LEVELS; i++) {
        runqueue_t* queue = &g_scheduler.priority_queues[i];
        struct process_control_block* current = queue->head;
        struct process_control_block* prev = NULL;
        
        while (current) {
            if (current->pid == task->pid) {
                // Remove from queue
                if (prev) {
                    prev->next = current->next;
                } else {
                    queue->head = current->next;
                }
                
                if (current == queue->tail) {
                    queue->tail = prev;
                }
                
                queue->count--;
                current->next = NULL;
                return 0;
            }
            prev = current;
            current = current->next;
        }
    }
    
    return -1; // Task not found in any queue
}

/*
 * Select the next task to run
 */
struct process_control_block* select_next_task(void)
{
    struct process_control_block* selected = NULL;
    
    // Priority order:
    // 1. Quantum coherent tasks (highest priority)
    // 2. Real-time tasks
    // 3. Regular priority queues (highest to lowest)
    
    // Check quantum coherent queue first
    if (g_scheduler.quantum_coherent_queue.count > 0) {
        selected = g_scheduler.quantum_coherent_queue.head;
        
        // Remove from queue
        g_scheduler.quantum_coherent_queue.head = selected->next;
        if (!selected->next) {
            g_scheduler.quantum_coherent_queue.tail = NULL;
        }
        g_scheduler.quantum_coherent_queue.count--;
        
        g_scheduler.stats.quantum_time += get_system_time();
        return selected;
    }
    
    // Check real-time queue
    if (g_scheduler.real_time_queue.count > 0) {
        selected = g_scheduler.real_time_queue.head;
        
        // Remove from queue
        g_scheduler.real_time_queue.head = selected->next;
        if (!selected->next) {
            g_scheduler.real_time_queue.tail = NULL;
        }
        g_scheduler.real_time_queue.count--;
        
        return selected;
    }
    
    // Check priority queues from highest to lowest
    for (int i = MAX_PRIORITY_LEVELS - 1; i >= 0; i--) {
        runqueue_t* queue = &g_scheduler.priority_queues[i];
        if (queue->count > 0) {
            selected = queue->head;
            
            // Remove from queue
            queue->head = selected->next;
            if (!selected->next) {
                queue->tail = NULL;
            }
            queue->count--;
            
            // Update dynamic priority
            update_task_priority(selected);
            
            g_scheduler.stats.classical_time += get_system_time();
            return selected;
        }
    }
    
    // No runnable tasks - return idle task or current task
    g_scheduler.stats.idle_time += get_system_time();
    return NULL;
}

/*
 * Update task priority based on various factors
 */
void update_task_priority(struct process_control_block* task)
{
    if (!task) {
        return;
    }
    
    // Calculate dynamic priority
    uint8_t new_priority = calculate_dynamic_priority(task);
    
    // Check if quantum priority boost should be applied
    if (should_boost_quantum_priority(task)) {
        apply_quantum_priority_boost(task);
    } else {
        // Decay any existing priority boost
        decay_priority_boost(task);
    }
    
    task->priority = new_priority;
}

/*
 * Handle quantum coherence monitoring and scheduling
 */
void handle_quantum_coherence(void)
{
    uint64_t current_time = get_system_time();
    
    // Check current task's quantum coherence
    if (g_scheduler.current_task && 
        (g_scheduler.current_task->type == PROCESS_TYPE_QUANTUM ||
         g_scheduler.current_task->type == PROCESS_TYPE_HYBRID) &&
        g_scheduler.current_task->quantum_coherent) {
        
        // Update coherence time
        uint64_t elapsed = current_time - g_scheduler.last_schedule_time;
        if (elapsed < g_scheduler.current_task->coherence_time_remaining) {
            g_scheduler.current_task->coherence_time_remaining -= elapsed;
        } else {
            // Coherence time expired
            g_scheduler.current_task->coherence_time_remaining = 0;
            g_scheduler.current_task->quantum_coherent = false;
            g_scheduler.stats.coherence_violations++;
            
            printk("WARNING: Quantum coherence lost for process PID %u\n",
                   g_scheduler.current_task->pid);
        }
    }
    
    // Scan all quantum tasks and update coherence status
    for (int i = 0; i < MAX_PRIORITY_LEVELS; i++) {
        struct process_control_block* task = g_scheduler.priority_queues[i].head;
        while (task) {
            if ((task->type == PROCESS_TYPE_QUANTUM || task->type == PROCESS_TYPE_HYBRID) 
                && task->quantum_coherent && task->coherence_time_remaining > 0) {
                
                // Check if coherence is about to expire
                if (task->coherence_time_remaining < QUANTUM_COHERENCE_THRESHOLD_MS * 1000000ULL) {
                    // Move to quantum coherent queue for immediate scheduling
                    unschedule_task(task);
                    task->next = NULL;
                    
                    if (g_scheduler.quantum_coherent_queue.tail) {
                        g_scheduler.quantum_coherent_queue.tail->next = task;
                    } else {
                        g_scheduler.quantum_coherent_queue.head = task;
                    }
                    g_scheduler.quantum_coherent_queue.tail = task;
                    g_scheduler.quantum_coherent_queue.count++;
                    
                    break; // Queue structure changed, restart scan
                }
            }
            task = task->next;
        }
    }
}

/*
 * Preempt the current task
 */
void preempt_current_task(void)
{
    if (!g_scheduler.current_task || !g_scheduler.preemption_enabled) {
        return;
    }
    
    // Special handling for quantum coherent tasks
    if ((g_scheduler.current_task->type == PROCESS_TYPE_QUANTUM ||
         g_scheduler.current_task->type == PROCESS_TYPE_HYBRID) &&
        g_scheduler.current_task->quantum_coherent) {
        
        // Try to preserve quantum coherence
        if (preserve_quantum_coherence(g_scheduler.current_task) == 0) {
            g_scheduler.stats.quantum_preservations++;
        } else {
            g_scheduler.current_task->quantum_coherent = false;
            g_scheduler.stats.coherence_violations++;
        }
    }
    
    printk("Preempting task PID %u\n", g_scheduler.current_task->pid);
}

// Priority calculation functions
uint8_t calculate_dynamic_priority(struct process_control_block* task)
{
    // Base priority adjusted by CPU usage and wait time
    uint8_t base_priority = task->priority;
    
    // Implement aging to prevent starvation
    uint64_t wait_time = get_system_time() - task->last_scheduled;
    if (wait_time > 100000000ULL) { // 100ms
        base_priority = (base_priority < 255) ? base_priority + 1 : 255;
    }
    
    return base_priority;
}

bool should_boost_quantum_priority(struct process_control_block* task)
{
    return (task->type == PROCESS_TYPE_QUANTUM || task->type == PROCESS_TYPE_HYBRID) &&
           task->quantum_coherent &&
           task->coherence_time_remaining < 10000000ULL; // 10ms threshold
}

void apply_quantum_priority_boost(struct process_control_block* task)
{
    // Boost priority to real-time level
    if (task->priority < 192) {
        task->priority = 192;
    }
}

void decay_priority_boost(struct process_control_block* task)
{
    // Gradually decay priority boost
    if (task->priority > 128) {
        task->priority = (task->priority > 128) ? task->priority - 1 : 128;
    }
}

// Utility functions (placeholders)
uint64_t get_system_time(void)
{
    // Placeholder: would return system time in nanoseconds
    static uint64_t fake_time = 0;
    return fake_time += 1000000; // Simulate 1ms increments
}

void memset(void* ptr, int value, size_t size)
{
    unsigned char* p = (unsigned char*)ptr;
    for (size_t i = 0; i < size; i++) {
        p[i] = (unsigned char)value;
    }
}