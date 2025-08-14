#!/usr/bin/env python3
"""
AQUA OS Main System Initialization
Orchestrates the complete AQUA OS startup sequence
"""

import asyncio
import logging
import sys
import signal
from pathlib import Path

# Import all major subsystems
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "framework" / "amores"))
sys.path.append(str(Path(__file__).parent / "framework" / "wee"))
sys.path.append(str(Path(__file__).parent / "framework" / "demos"))
sys.path.append(str(Path(__file__).parent / "platforms" / "caas"))
sys.path.append(str(Path(__file__).parent / "platforms" / "gaia"))
sys.path.append(str(Path(__file__).parent / "integration" / "global"))
sys.path.append(str(Path(__file__).parent / "technologies" / "quantum"))

class AQUAOSInitializer:
    """Main AQUA OS initialization orchestrator"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.initialized_systems = []
        self.shutdown_requested = False
        
    def _setup_logging(self):
        """Setup logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('/var/log/aqua-system.log', mode='a')
            ]
        )
        return logging.getLogger("AQUA.System")
    
    async def initialize_all_systems(self):
        """Initialize all AQUA OS systems in correct order"""
        
        self.logger.info("=" * 60)
        self.logger.info("AQUA OS System Initialization Starting")
        self.logger.info("=" * 60)
        
        try:
            # Phase 1: Core Framework Systems
            await self._initialize_framework_systems()
            
            # Phase 2: Platform Systems  
            await self._initialize_platform_systems()
            
            # Phase 3: Integration Systems
            await self._initialize_integration_systems()
            
            # Phase 4: Technology Systems
            await self._initialize_technology_systems()
            
            self.logger.info("=" * 60)
            self.logger.info("✓ AQUA OS System Initialization Complete")
            self.logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"System initialization failed: {e}")
            await self._emergency_shutdown()
            return False
    
    async def _initialize_framework_systems(self):
        """Initialize framework systems"""
        self.logger.info("Phase 1: Initializing Framework Systems")
        
        try:
            # Initialize AMOReS Regulatory Engine
            from regulatory_engine import initialize_regulatory_engine
            regulatory = initialize_regulatory_engine()
            self.initialized_systems.append(("amores", regulatory))
            self.logger.info("✓ AMOReS Regulatory Engine [188] initialized")
            
            # Initialize WEE Wisdom Engine
            from wee_core import initialize_wee_engine
            wee = initialize_wee_engine()
            self.initialized_systems.append(("wee", wee))
            self.logger.info("✓ WEE Wisdom Engine [171] initialized")
            
            # Initialize DeMOS Metrics System
            from demos_core import initialize_demos_system
            demos = initialize_demos_system()
            self.initialized_systems.append(("demos", demos))
            self.logger.info("✓ DeMOS Metrics System [198] initialized")
            
        except ImportError as e:
            self.logger.warning(f"Framework system import failed: {e}")
        except Exception as e:
            self.logger.error(f"Framework initialization failed: {e}")
            raise
    
    async def _initialize_platform_systems(self):
        """Initialize platform systems"""
        self.logger.info("Phase 2: Initializing Platform Systems")
        
        try:
            # Initialize CaaS Certification Service
            from caas_core import initialize_caas_system
            caas = initialize_caas_system()
            self.initialized_systems.append(("caas", caas))
            self.logger.info("✓ CaaS Certification Service [511] initialized")
            
            # Initialize GAIA Aerospace Architecture
            from gaia_core import initialize_gaia_system
            gaia = initialize_gaia_system()
            self.initialized_systems.append(("gaia", gaia))
            self.logger.info("✓ GAIA Aerospace Architecture [533] initialized")
            
        except ImportError as e:
            self.logger.warning(f"Platform system import failed: {e}")
        except Exception as e:
            self.logger.error(f"Platform initialization failed: {e}")
            raise
    
    async def _initialize_integration_systems(self):
        """Initialize integration systems"""
        self.logger.info("Phase 3: Initializing Integration Systems")
        
        try:
            # Initialize Global Integration System
            from global_integration import initialize_global_integration
            integration = initialize_global_integration()
            self.initialized_systems.append(("integration", integration))
            self.logger.info("✓ Global Integration System [900] initialized")
            
            # Start integration processes
            await integration.start_health_monitoring()
            self.logger.info("✓ Integration health monitoring started")
            
        except ImportError as e:
            self.logger.warning(f"Integration system import failed: {e}")
        except Exception as e:
            self.logger.error(f"Integration initialization failed: {e}")
            raise
    
    async def _initialize_technology_systems(self):
        """Initialize technology systems"""
        self.logger.info("Phase 4: Initializing Technology Systems")
        
        try:
            # Initialize Quantum Technology Core
            from quantum_core import initialize_quantum_technology
            quantum_tech = initialize_quantum_technology()
            await quantum_tech.initialize()
            self.initialized_systems.append(("quantum_tech", quantum_tech))
            self.logger.info("✓ Quantum Technology Core [351] initialized")
            
        except ImportError as e:
            self.logger.warning(f"Technology system import failed: {e}")
        except Exception as e:
            self.logger.error(f"Technology initialization failed: {e}")
            raise
    
    async def run_system_health_check(self):
        """Run comprehensive system health check"""
        self.logger.info("Running system health check...")
        
        health_status = {
            "overall_healthy": True,
            "systems": {}
        }
        
        for system_name, system_instance in self.initialized_systems:
            try:
                if hasattr(system_instance, 'get_health_status'):
                    system_health = system_instance.get_health_status()
                    health_status["systems"][system_name] = system_health
                    
                    if not system_health.get("healthy", True):
                        health_status["overall_healthy"] = False
                        self.logger.warning(f"System {system_name} reports unhealthy status")
                else:
                    health_status["systems"][system_name] = {"healthy": True, "note": "No health check available"}
                    
            except Exception as e:
                health_status["systems"][system_name] = {"healthy": False, "error": str(e)}
                health_status["overall_healthy"] = False
                self.logger.error(f"Health check failed for {system_name}: {e}")
        
        if health_status["overall_healthy"]:
            self.logger.info("✓ System health check passed")
        else:
            self.logger.warning("⚠ System health check detected issues")
        
        return health_status
    
    async def main_loop(self):
        """Main system operation loop"""
        self.logger.info("Starting AQUA OS main operation loop")
        
        try:
            while not self.shutdown_requested:
                # Run periodic health checks
                await self.run_system_health_check()
                
                # Sleep for 60 seconds between checks
                await asyncio.sleep(60)
                
        except asyncio.CancelledError:
            self.logger.info("Main loop cancelled")
        except Exception as e:
            self.logger.error(f"Main loop error: {e}")
    
    async def shutdown_all_systems(self):
        """Graceful shutdown of all systems"""
        self.logger.info("AQUA OS System Shutdown Initiated")
        
        self.shutdown_requested = True
        
        # Shutdown systems in reverse order
        for system_name, system_instance in reversed(self.initialized_systems):
            try:
                if hasattr(system_instance, 'shutdown'):
                    system_instance.shutdown()
                    self.logger.info(f"✓ {system_name} shutdown complete")
                else:
                    self.logger.info(f"✓ {system_name} (no shutdown method)")
                    
            except Exception as e:
                self.logger.error(f"Error shutting down {system_name}: {e}")
        
        self.logger.info("AQUA OS System Shutdown Complete")
    
    async def _emergency_shutdown(self):
        """Emergency shutdown procedure"""
        self.logger.critical("EMERGENCY SHUTDOWN INITIATED")
        await self.shutdown_all_systems()

async def main():
    """Main entry point"""
    
    # Setup signal handlers for graceful shutdown
    initializer = AQUAOSInitializer()
    
    def signal_handler(signum, frame):
        asyncio.create_task(initializer.shutdown_all_systems())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize all systems
    success = await initializer.initialize_all_systems()
    
    if success:
        # Run main operation loop
        await initializer.main_loop()
    else:
        sys.exit(1)

if __name__ == "__main__":
    # Ensure var/log directory exists
    Path("/var/log").mkdir(parents=True, exist_ok=True)
    
    # Run main async function
    asyncio.run(main())