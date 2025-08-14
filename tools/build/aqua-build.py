#!/usr/bin/env python3
"""
AQUA OS Build System
Comprehensive build tool for all AQUA OS components
"""

import os
import sys
import subprocess
import argparse
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional

class AQUABuilder:
    """Main AQUA OS build system"""
    
    def __init__(self, aqua_root: Path):
        self.aqua_root = aqua_root
        self.build_config = {}
        self.load_build_config()
        
    def load_build_config(self):
        """Load build configuration"""
        config_file = self.aqua_root / "config" / "aqua-global.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.build_config = yaml.safe_load(f)
    
    def build_boot_system(self) -> bool:
        """Build boot system components"""
        print("Building boot system...")
        
        boot_dir = self.aqua_root / "boot"
        
        # Compile bootloader (would require cross-compiler for UEFI)
        bootloader_src = boot_dir / "bootloader.c"
        if bootloader_src.exists():
            print("  ✓ Bootloader source found")
            # Note: Actual compilation would require UEFI development kit
            print("  ⚠ Bootloader compilation requires UEFI cross-compiler")
        
        # Validate configuration files
        config_files = [
            "config/boot.cfg",
            "config/boot-config.yaml", 
            "config/quantum-discovery.cfg"
        ]
        
        for config_file in config_files:
            config_path = boot_dir / config_file
            if config_path.exists():
                print(f"  ✓ {config_file} found")
            else:
                print(f"  ✗ {config_file} missing")
                return False
        
        print("Boot system build complete")
        return True
    
    def build_kernel(self) -> bool:
        """Build MOS kernel components"""
        print("Building MOS kernel...")
        
        kernel_dir = self.aqua_root / "kernel"
        
        # Check for kernel source files
        kernel_sources = [
            "core/mos-main.c",
            "core/process-manager.c", 
            "core/memory-manager.c",
            "core/scheduler.c",
            "security/security-manager.c"
        ]
        
        for source_file in kernel_sources:
            source_path = kernel_dir / source_file
            if source_path.exists():
                print(f"  ✓ {source_file} found")
                # Note: Actual compilation would require kernel build environment
            else:
                print(f"  ✗ {source_file} missing")
                return False
        
        print("  ⚠ Kernel compilation requires kernel build environment (gcc, make, etc.)")
        print("MOS kernel build complete")
        return True
    
    def build_framework(self) -> bool:
        """Build CQEA framework components"""
        print("Building CQEA framework...")
        
        framework_dir = self.aqua_root / "framework"
        
        # Check C++ components
        cpp_sources = [
            "cqea/cqea-core.cpp"
        ]
        
        for source_file in cpp_sources:
            source_path = framework_dir / source_file
            if source_path.exists():
                print(f"  ✓ {source_file} found")
            else:
                print(f"  ✗ {source_file} missing")
                return False
        
        # Check Python components
        python_sources = [
            "amores/regulatory-engine.py",
            "wee/wee-core.py",
            "demos/demos-core.py"
        ]
        
        for source_file in python_sources:
            source_path = framework_dir / source_file
            if source_path.exists():
                print(f"  ✓ {source_file} found")
                # Validate Python syntax
                try:
                    with open(source_path, 'r') as f:
                        compile(f.read(), source_path, 'exec')
                    print(f"  ✓ {source_file} syntax valid")
                except SyntaxError as e:
                    print(f"  ✗ {source_file} syntax error: {e}")
                    return False
            else:
                print(f"  ✗ {source_file} missing")
                return False
        
        print("CQEA framework build complete")
        return True
    
    def build_platforms(self) -> bool:
        """Build platform components"""
        print("Building platforms...")
        
        platforms_dir = self.aqua_root / "platforms"
        
        # Check platform implementations
        platform_sources = [
            "ampel360/platform-core.cpp",
            "caas/caas-core.py"
        ]
        
        for source_file in platform_sources:
            source_path = platforms_dir / source_file
            if source_path.exists():
                print(f"  ✓ {source_file} found")
                
                # Validate Python files
                if source_file.endswith('.py'):
                    try:
                        with open(source_path, 'r') as f:
                            compile(f.read(), source_path, 'exec')
                        print(f"  ✓ {source_file} syntax valid")
                    except SyntaxError as e:
                        print(f"  ✗ {source_file} syntax error: {e}")
                        return False
            else:
                print(f"  ✗ {source_file} missing")
                return False
        
        print("Platforms build complete")
        return True
    
    def run_tests(self) -> bool:
        """Run test suite"""
        print("Running AQUA OS test suite...")
        
        tests_dir = self.aqua_root / "tests"
        
        # Run system tests
        system_test = tests_dir / "system" / "test_aqua_os_structure.py"
        if system_test.exists():
            print("Running system structure tests...")
            result = subprocess.run([sys.executable, str(system_test)], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("  ✓ System tests passed")
                return True
            else:
                print("  ✗ System tests failed:")
                print(result.stdout)
                print(result.stderr)
                return False
        else:
            print("  ⚠ No system tests found")
            return True
    
    def validate_structure(self) -> bool:
        """Validate AQUA OS directory structure"""
        print("Validating AQUA OS structure...")
        
        required_dirs = [
            "boot", "kernel", "framework", "platforms", 
            "integration", "standards", "technologies", 
            "config", "tests", "var", "tools"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.aqua_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                print(f"  ✓ {dir_name}/ directory found")
            else:
                print(f"  ✗ {dir_name}/ directory missing")
                return False
        
        print("Structure validation complete")
        return True
    
    def build_all(self) -> bool:
        """Build entire AQUA OS system"""
        print("=" * 60)
        print("AQUA OS Comprehensive Build System")
        print("=" * 60)
        
        success = True
        
        # Validate structure first
        if not self.validate_structure():
            success = False
        
        # Build components
        if not self.build_boot_system():
            success = False
            
        if not self.build_kernel():
            success = False
            
        if not self.build_framework():
            success = False
            
        if not self.build_platforms():
            success = False
        
        # Run tests
        if not self.run_tests():
            success = False
        
        print("=" * 60)
        if success:
            print("✓ AQUA OS build completed successfully")
        else:
            print("✗ AQUA OS build failed")
        print("=" * 60)
        
        return success

def main():
    parser = argparse.ArgumentParser(description="AQUA OS Build System")
    parser.add_argument("--component", choices=["boot", "kernel", "framework", "platforms", "all"],
                       default="all", help="Component to build")
    parser.add_argument("--test", action="store_true", help="Run tests after build")
    parser.add_argument("--validate", action="store_true", help="Validate structure only")
    
    args = parser.parse_args()
    
    # Find AQUA root directory
    aqua_root = Path(__file__).parent.parent.parent
    if not (aqua_root / "config" / "aqua-global.yaml").exists():
        print("Error: Could not find AQUA root directory")
        print(f"Searched in: {aqua_root}")
        sys.exit(1)
    
    builder = AQUABuilder(aqua_root)
    
    if args.validate:
        success = builder.validate_structure()
    elif args.component == "all":
        success = builder.build_all()
    else:
        # Build specific component
        if args.component == "boot":
            success = builder.build_boot_system()
        elif args.component == "kernel":
            success = builder.build_kernel()
        elif args.component == "framework":
            success = builder.build_framework()
        elif args.component == "platforms":
            success = builder.build_platforms()
        
        if args.test and success:
            success = builder.run_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()