/**
 * CQEA (Classical Quantum-Extensible Apps) Core Framework
 * UTCS-MI Code: [126] CQEA Core Framework
 * 
 * Provides unified interface for classical and quantum application development
 */

#include <iostream>
#include <memory>
#include <vector>
#include <map>
#include <string>
#include "cqea-core.h"

namespace AQUA {
namespace CQEA {

class CQEACore {
private:
    bool quantum_mode_enabled;
    std::unique_ptr<QuantumInterface> quantum_interface;
    std::unique_ptr<ClassicalCore> classical_core;
    std::unique_ptr<HybridOrchestrator> orchestrator;
    
public:
    /**
     * Initialize CQEA framework
     */
    CQEACore() : quantum_mode_enabled(false) {
        std::cout << "CQEA Core Framework v1.0 - UTCS-MI Code [126]" << std::endl;
        
        // Initialize classical core first
        classical_core = std::make_unique<ClassicalCore>();
        
        // Try to initialize quantum interface
        try {
            quantum_interface = std::make_unique<QuantumInterface>();
            quantum_mode_enabled = quantum_interface->is_available();
            
            if (quantum_mode_enabled) {
                std::cout << "Quantum mode enabled" << std::endl;
                orchestrator = std::make_unique<HybridOrchestrator>(
                    classical_core.get(), quantum_interface.get());
            } else {
                std::cout << "Operating in classical-only mode" << std::endl;
            }
        } catch (const std::exception& e) {
            std::cout << "Quantum initialization failed: " << e.what() 
                      << " - Falling back to classical mode" << std::endl;
            quantum_mode_enabled = false;
        }
    }
    
    /**
     * Create a new CQEA application
     */
    std::shared_ptr<CQEAApplication> create_application(const std::string& name, 
                                                       ApplicationType type) {
        auto app = std::make_shared<CQEAApplication>(name, type);
        
        switch (type) {
            case ApplicationType::CLASSICAL:
                app->set_runtime(classical_core.get());
                break;
                
            case ApplicationType::QUANTUM:
                if (quantum_mode_enabled) {
                    app->set_runtime(quantum_interface.get());
                } else {
                    throw std::runtime_error("Quantum mode not available");
                }
                break;
                
            case ApplicationType::HYBRID:
                if (quantum_mode_enabled) {
                    app->set_runtime(orchestrator.get());
                } else {
                    // Fallback to classical-only
                    app->set_runtime(classical_core.get());
                    std::cout << "Warning: Hybrid app " << name 
                              << " running in classical-only mode" << std::endl;
                }
                break;
        }
        
        return app;
    }
    
    /**
     * Execute a quantum circuit
     */
    QuantumResult execute_quantum_circuit(const QuantumCircuit& circuit) {
        if (!quantum_mode_enabled) {
            throw std::runtime_error("Quantum execution not available");
        }
        
        return quantum_interface->execute_circuit(circuit);
    }
    
    /**
     * Execute classical computation
     */
    ClassicalResult execute_classical_computation(const ClassicalTask& task) {
        return classical_core->execute_task(task);
    }
    
    /**
     * Execute hybrid quantum-classical algorithm
     */
    HybridResult execute_hybrid_algorithm(const HybridAlgorithm& algorithm) {
        if (!quantum_mode_enabled) {
            // Fallback to classical approximation
            return classical_core->approximate_quantum_algorithm(algorithm);
        }
        
        return orchestrator->execute_hybrid(algorithm);
    }
    
    /**
     * Get system capabilities
     */
    SystemCapabilities get_capabilities() const {
        SystemCapabilities caps;
        caps.classical_enabled = true;
        caps.quantum_enabled = quantum_mode_enabled;
        caps.hybrid_enabled = quantum_mode_enabled;
        
        if (quantum_mode_enabled) {
            caps.available_qubits = quantum_interface->get_available_qubits();
            caps.quantum_volume = quantum_interface->get_quantum_volume();
            caps.gate_fidelity = quantum_interface->get_gate_fidelity();
        }
        
        caps.classical_cores = classical_core->get_core_count();
        caps.memory_gb = classical_core->get_memory_size_gb();
        
        return caps;
    }
    
    /**
     * Register extension
     */
    void register_extension(const std::string& name, 
                           std::shared_ptr<CQEAExtension> extension) {
        extensions[name] = extension;
        extension->initialize(this);
        std::cout << "Registered CQEA extension: " << name << std::endl;
    }
    
    /**
     * Get extension by name
     */
    std::shared_ptr<CQEAExtension> get_extension(const std::string& name) {
        auto it = extensions.find(name);
        return (it != extensions.end()) ? it->second : nullptr;
    }
    
    /**
     * Shutdown framework
     */
    void shutdown() {
        std::cout << "CQEA Core Framework shutdown initiated" << std::endl;
        
        // Shutdown extensions
        for (auto& [name, ext] : extensions) {
            ext->shutdown();
        }
        
        // Shutdown subsystems
        if (orchestrator) orchestrator.reset();
        if (quantum_interface) quantum_interface.reset();
        if (classical_core) classical_core.reset();
        
        std::cout << "CQEA Core Framework shutdown complete" << std::endl;
    }
    
private:
    std::map<std::string, std::shared_ptr<CQEAExtension>> extensions;
};

// Global CQEA framework instance
static std::unique_ptr<CQEACore> g_cqea_framework = nullptr;

/**
 * Initialize CQEA framework
 */
extern "C" int cqea_framework_init(void) {
    try {
        g_cqea_framework = std::make_unique<CQEACore>();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "CQEA framework initialization failed: " << e.what() << std::endl;
        return -1;
    }
}

/**
 * Get global CQEA framework instance
 */
extern "C" CQEACore* get_cqea_framework(void) {
    return g_cqea_framework.get();
}

/**
 * Shutdown CQEA framework
 */
extern "C" void cqea_framework_shutdown(void) {
    if (g_cqea_framework) {
        g_cqea_framework->shutdown();
        g_cqea_framework.reset();
    }
}

} // namespace CQEA
} // namespace AQUA