/**
 * AMPEL360 Platform Core
 * UTCS-MI Code: [411] Platform Core
 * 
 * Core infrastructure for the AMPEL360 comprehensive platform
 */

#include <iostream>
#include <memory>
#include <vector>
#include <unordered_map>
#include "platform-core.h"

namespace AQUA {
namespace AMPEL360 {

class PlatformCore {
private:
    bool initialized;
    std::unordered_map<std::string, std::shared_ptr<Service>> services;
    std::unique_ptr<ServiceMesh> service_mesh;
    std::unique_ptr<APIGateway> api_gateway;
    std::unique_ptr<ConfigurationManager> config_manager;
    
public:
    /**
     * Initialize AMPEL360 platform
     */
    PlatformCore() : initialized(false) {
        std::cout << "AMPEL360 Platform Core v1.0 - UTCS-MI Code [411]" << std::endl;
    }
    
    /**
     * Start platform initialization
     */
    int initialize() {
        if (initialized) {
            return 0;
        }
        
        std::cout << "Initializing AMPEL360 Platform..." << std::endl;
        
        try {
            // Initialize configuration manager first
            config_manager = std::make_unique<ConfigurationManager>();
            if (config_manager->load_configuration() != 0) {
                throw std::runtime_error("Configuration loading failed");
            }
            
            // Initialize service mesh
            service_mesh = std::make_unique<ServiceMesh>();
            if (service_mesh->initialize() != 0) {
                throw std::runtime_error("Service mesh initialization failed");
            }
            
            // Initialize API gateway
            api_gateway = std::make_unique<APIGateway>();
            if (api_gateway->initialize() != 0) {
                throw std::runtime_error("API gateway initialization failed");
            }
            
            // Register core services
            register_core_services();
            
            initialized = true;
            std::cout << "AMPEL360 Platform initialization complete" << std::endl;
            return 0;
            
        } catch (const std::exception& e) {
            std::cerr << "AMPEL360 Platform initialization failed: " << e.what() << std::endl;
            return -1;
        }
    }
    
    /**
     * Register a service with the platform
     */
    void register_service(const std::string& name, 
                         std::shared_ptr<Service> service) {
        services[name] = service;
        service_mesh->register_service(name, service);
        
        std::cout << "Registered service: " << name << std::endl;
    }
    
    /**
     * Get a service by name
     */
    std::shared_ptr<Service> get_service(const std::string& name) {
        auto it = services.find(name);
        return (it != services.end()) ? it->second : nullptr;
    }
    
    /**
     * Start all platform services
     */
    int start_services() {
        std::cout << "Starting AMPEL360 platform services..." << std::endl;
        
        int started = 0;
        for (auto& [name, service] : services) {
            try {
                if (service->start() == 0) {
                    started++;
                    std::cout << "Started service: " << name << std::endl;
                } else {
                    std::cerr << "Failed to start service: " << name << std::endl;
                }
            } catch (const std::exception& e) {
                std::cerr << "Exception starting service " << name << ": " << e.what() << std::endl;
            }
        }
        
        std::cout << "Started " << started << "/" << services.size() << " services" << std::endl;
        return (started == services.size()) ? 0 : -1;
    }
    
    /**
     * Stop all platform services
     */
    void stop_services() {
        std::cout << "Stopping AMPEL360 platform services..." << std::endl;
        
        // Stop services in reverse order
        for (auto it = services.rbegin(); it != services.rend(); ++it) {
            try {
                it->second->stop();
                std::cout << "Stopped service: " << it->first << std::endl;
            } catch (const std::exception& e) {
                std::cerr << "Exception stopping service " << it->first << ": " << e.what() << std::endl;
            }
        }
    }
    
    /**
     * Get platform health status
     */
    PlatformHealth get_health_status() {
        PlatformHealth health;
        health.overall_status = HealthStatus::HEALTHY;
        health.service_count = services.size();
        health.healthy_services = 0;
        health.degraded_services = 0;
        health.failed_services = 0;
        
        for (const auto& [name, service] : services) {
            ServiceHealth service_health = service->get_health();
            health.service_health[name] = service_health;
            
            switch (service_health.status) {
                case HealthStatus::HEALTHY:
                    health.healthy_services++;
                    break;
                case HealthStatus::DEGRADED:
                    health.degraded_services++;
                    if (health.overall_status == HealthStatus::HEALTHY) {
                        health.overall_status = HealthStatus::DEGRADED;
                    }
                    break;
                case HealthStatus::FAILED:
                    health.failed_services++;
                    health.overall_status = HealthStatus::FAILED;
                    break;
            }
        }
        
        return health;
    }
    
    /**
     * Get platform metrics
     */
    PlatformMetrics get_metrics() {
        PlatformMetrics metrics;
        metrics.uptime_seconds = get_uptime();
        metrics.total_requests = api_gateway->get_total_requests();
        metrics.active_connections = service_mesh->get_active_connections();
        metrics.memory_usage_mb = get_memory_usage();
        metrics.cpu_usage_percent = get_cpu_usage();
        
        return metrics;
    }
    
    /**
     * Shutdown platform
     */
    void shutdown() {
        if (!initialized) {
            return;
        }
        
        std::cout << "AMPEL360 Platform shutdown initiated" << std::endl;
        
        stop_services();
        
        if (api_gateway) api_gateway.reset();
        if (service_mesh) service_mesh.reset();
        if (config_manager) config_manager.reset();
        
        services.clear();
        initialized = false;
        
        std::cout << "AMPEL360 Platform shutdown complete" << std::endl;
    }
    
private:
    void register_core_services() {
        // Register authentication service
        auto auth_service = std::make_shared<AuthenticationService>();
        register_service("authentication", auth_service);
        
        // Register authorization service
        auto authz_service = std::make_shared<AuthorizationService>();
        register_service("authorization", authz_service);
        
        // Register monitoring service
        auto monitoring_service = std::make_shared<MonitoringService>();
        register_service("monitoring", monitoring_service);
        
        // Register discovery service
        auto discovery_service = std::make_shared<DiscoveryService>();
        register_service("discovery", discovery_service);
        
        // Register configuration service
        auto config_service = std::make_shared<ConfigurationService>();
        register_service("configuration", config_service);
    }
};

// Global platform instance
static std::unique_ptr<PlatformCore> g_platform_core = nullptr;

/**
 * Initialize AMPEL360 platform
 */
extern "C" int ampel360_platform_init(void) {
    try {
        g_platform_core = std::make_unique<PlatformCore>();
        return g_platform_core->initialize();
    } catch (const std::exception& e) {
        std::cerr << "AMPEL360 platform initialization failed: " << e.what() << std::endl;
        return -1;
    }
}

/**
 * Get global platform instance
 */
extern "C" PlatformCore* get_ampel360_platform(void) {
    return g_platform_core.get();
}

/**
 * Shutdown AMPEL360 platform
 */
extern "C" void ampel360_platform_shutdown(void) {
    if (g_platform_core) {
        g_platform_core->shutdown();
        g_platform_core.reset();
    }
}

} // namespace AMPEL360
} // namespace AQUA