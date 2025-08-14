/**
 * Task Scheduler
 * UTCS-MI Code: [051] Task Scheduler
 * 
 * Quantum-aware scheduler for classical and quantum processes
 */

#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "scheduler.h"

#define MAX_PRIORITY_LEVELS 140
#define QUANTUM_TIME_SLICE_MS 100
#define CLASSICAL_TIME_SLICE_MS 10

typedef struct task_node {
    uint32_t pid;
    uint32_t priority;
    uint64_t runtime_remaining;
    uint64_t quantum_time_remaining;
    bool is_quantum_task;
    struct task_node *next;
} task_node_t;

typedef struct {
    task_node_t *head;
    task_node_t *tail;
    uint32_t count;
} task_queue_t;

// Scheduler data structures
static task_queue_t ready_queues[MAX_PRIORITY_LEVELS];
static task_queue_t quantum_ready_queue;
static task_node_t *current_task = NULL;
static uint64_t scheduler_ticks = 0;
static bool scheduler_running = false;

/**
 * Initialize task scheduler
 */
int scheduler_init(void) {
    printk("Task Scheduler initializing...\n");
    
    // Initialize all priority queues
    for (int i = 0; i < MAX_PRIORITY_LEVELS; i++) {
        ready_queues[i].head = NULL;
        ready_queues[i].tail = NULL;
        ready_queues[i].count = 0;
    }
    
    // Initialize quantum ready queue
    quantum_ready_queue.head = NULL;
    quantum_ready_queue.tail = NULL;
    quantum_ready_queue.count = 0;
    
    current_task = NULL;
    scheduler_ticks = 0;
    scheduler_running = false;
    
    printk("Task Scheduler initialized\n");
    return 0;
}

/**
 * Add task to ready queue
 */
void scheduler_add_task(uint32_t pid, uint32_t priority, bool is_quantum) {
    task_node_t *task = allocate_task_node();
    if (!task) {
        printk("ERROR: Failed to allocate task node for PID %d\n", pid);
        return;
    }
    
    task->pid = pid;
    task->priority = priority;
    task->runtime_remaining = is_quantum ? QUANTUM_TIME_SLICE_MS : CLASSICAL_TIME_SLICE_MS;
    task->quantum_time_remaining = is_quantum ? QUANTUM_TIME_SLICE_MS : 0;
    task->is_quantum_task = is_quantum;
    task->next = NULL;
    
    if (is_quantum) {
        // Add to quantum ready queue
        if (quantum_ready_queue.tail) {
            quantum_ready_queue.tail->next = task;
        } else {
            quantum_ready_queue.head = task;
        }
        quantum_ready_queue.tail = task;
        quantum_ready_queue.count++;
    } else {
        // Add to appropriate priority queue
        uint32_t queue_index = (priority < MAX_PRIORITY_LEVELS) ? priority : MAX_PRIORITY_LEVELS - 1;
        
        if (ready_queues[queue_index].tail) {
            ready_queues[queue_index].tail->next = task;
        } else {
            ready_queues[queue_index].head = task;
        }
        ready_queues[queue_index].tail = task;
        ready_queues[queue_index].count++;
    }
    
    printk("Task added to scheduler: PID=%d, priority=%d, quantum=%s\n", 
           pid, priority, is_quantum ? "yes" : "no");
}

/**
 * Remove task from scheduler
 */
void scheduler_remove_task(uint32_t pid) {
    // Remove from all queues
    for (int i = 0; i < MAX_PRIORITY_LEVELS; i++) {
        remove_task_from_queue(&ready_queues[i], pid);
    }
    
    remove_task_from_queue(&quantum_ready_queue, pid);
    
    // If it's the current task, trigger reschedule
    if (current_task && current_task->pid == pid) {
        current_task = NULL;
        schedule();
    }
}

/**
 * Main scheduler function - select next task to run
 */
task_node_t* scheduler_select_next_task(void) {
    task_node_t *selected_task = NULL;
    
    // Priority 1: Check quantum tasks if quantum hardware is available
    if (is_quantum_hardware_available() && quantum_ready_queue.count > 0) {
        selected_task = dequeue_task(&quantum_ready_queue);
        if (selected_task) {
            printk("Scheduled quantum task: PID=%d\n", selected_task->pid);
            return selected_task;
        }
    }
    
    // Priority 2: Check classical tasks by priority
    for (int i = 0; i < MAX_PRIORITY_LEVELS; i++) {
        if (ready_queues[i].count > 0) {
            selected_task = dequeue_task(&ready_queues[i]);
            if (selected_task) {
                printk("Scheduled classical task: PID=%d, priority=%d\n", 
                       selected_task->pid, selected_task->priority);
                return selected_task;
            }
        }
    }
    
    // No tasks available
    return NULL;
}

/**
 * Schedule next task
 */
void schedule(void) {
    if (!scheduler_running) {
        return;
    }
    
    // Save current task state if there is one
    if (current_task) {
        save_task_context(current_task->pid);
    }
    
    // Select next task
    task_node_t *next_task = scheduler_select_next_task();
    
    if (next_task) {
        current_task = next_task;
        
        // Switch context to new task
        switch_to_task(next_task->pid);
        
        // Set up timer for preemption
        if (next_task->is_quantum_task) {
            set_timer_interrupt(next_task->quantum_time_remaining);
        } else {
            set_timer_interrupt(next_task->runtime_remaining);
        }
        
    } else {
        // No tasks to run, idle
        current_task = NULL;
        enter_idle_mode();
    }
}

/**
 * Handle timer interrupt (preemption)
 */
void scheduler_timer_interrupt(void) {
    if (!current_task) {
        return;
    }
    
    // Update task runtime
    if (current_task->is_quantum_task) {
        current_task->quantum_time_remaining -= QUANTUM_TIME_SLICE_MS;
        if (current_task->quantum_time_remaining <= 0) {
            // Quantum time slice expired, re-queue task
            scheduler_add_task(current_task->pid, current_task->priority, true);
            current_task = NULL;
        }
    } else {
        current_task->runtime_remaining -= CLASSICAL_TIME_SLICE_MS;
        if (current_task->runtime_remaining <= 0) {
            // Time slice expired, re-queue task
            scheduler_add_task(current_task->pid, current_task->priority, false);
            current_task = NULL;
        }
    }
    
    // Trigger reschedule
    schedule();
}

/**
 * Scheduler tick - called periodically
 */
void scheduler_tick(void) {
    scheduler_ticks++;
    
    // Update task priorities (aging to prevent starvation)
    if (scheduler_ticks % 100 == 0) {
        age_task_priorities();
    }
    
    // Check for quantum resource availability changes
    if (scheduler_ticks % 50 == 0) {
        update_quantum_task_priorities();
    }
}

/**
 * Start scheduler
 */
void scheduler_start(void) {
    printk("Starting task scheduler\n");
    scheduler_running = true;
    
    // Create idle task
    uint32_t idle_pid = create_idle_task();
    scheduler_add_task(idle_pid, MAX_PRIORITY_LEVELS - 1, false);
    
    // Start scheduling
    schedule();
}

/**
 * Stop scheduler
 */
void scheduler_stop(void) {
    printk("Stopping task scheduler\n");
    scheduler_running = false;
    current_task = NULL;
}

/**
 * Get scheduler statistics
 */
void get_scheduler_stats(scheduler_stats_t *stats) {
    stats->total_ticks = scheduler_ticks;
    stats->current_task_pid = current_task ? current_task->pid : 0;
    stats->total_ready_tasks = 0;
    stats->quantum_ready_tasks = quantum_ready_queue.count;
    
    for (int i = 0; i < MAX_PRIORITY_LEVELS; i++) {
        stats->total_ready_tasks += ready_queues[i].count;
    }
    
    stats->scheduler_running = scheduler_running;
}

/**
 * Shutdown scheduler
 */
void scheduler_shutdown(void) {
    scheduler_stop();
    
    // Free all task nodes
    for (int i = 0; i < MAX_PRIORITY_LEVELS; i++) {
        free_task_queue(&ready_queues[i]);
    }
    
    free_task_queue(&quantum_ready_queue);
    
    printk("Task Scheduler shutdown complete\n");
}