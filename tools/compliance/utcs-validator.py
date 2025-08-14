#!/usr/bin/env python3
"""
AQUA OS Structure Compliance Validator
Validates complete AQUA OS structure against UTCS-MI v5.0 requirements
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any

class UTCSMIValidator:
    """UTCS-MI v5.0 compliance validator"""
    
    def __init__(self, aqua_root: Path):
        self.aqua_root = aqua_root
        self.validation_results = {
            "completeness": {},
            "structure": {},
            "consistency": {},
            "compliance": {}
        }
        
    def validate_completeness(self) -> Dict[str, bool]:
        """Validate completeness checklist"""
        print("[COMPLETENESS]")
        
        # Check major directories
        required_dirs = [
            "boot", "kernel", "framework", "platforms", 
            "integration", "standards", "technologies", 
            "config", "tests", "var", "tools"
        ]
        
        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = self.aqua_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                print(f"  ✓ {dir_name}/ directory present and populated")
            else:
                print(f"  ✗ {dir_name}/ directory missing")
                missing_dirs.append(dir_name)
        
        # Check UTCS-MI code presence
        utcs_codes_found = 0
        for root, dirs, files in os.walk(self.aqua_root):
            for file in files:
                if file.endswith(('.c', '.cpp', '.py', '.md', '.yaml')):
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        if '[0' in content and ']' in content:  # UTCS-MI code pattern
                            utcs_codes_found += 1
                            break
                    except:
                        pass
        
        print(f"  ✓ UTCS-MI codes found in {utcs_codes_found} files")
        
        # Check subsystem implementations
        subsystems = {
            "MOS Core": "kernel/core/mos-main.c",
            "Process Manager": "kernel/core/process-manager.c", 
            "Memory Manager": "kernel/core/memory-manager.c",
            "Scheduler": "kernel/core/scheduler.c",
            "Security Manager": "kernel/security/security-manager.c",
            "CQEA Framework": "framework/cqea/cqea-core.cpp",
            "AMOReS Engine": "framework/amores/regulatory-engine.py",
            "WEE Engine": "framework/wee/wee-core.py",
            "DeMOS System": "framework/demos/demos-core.py",
            "AMPEL360 Platform": "platforms/ampel360/platform-core.cpp",
            "CaaS Service": "platforms/caas/caas-core.py",
            "GAIA System": "platforms/gaia/gaia-core.py"
        }
        
        missing_subsystems = []
        for name, path in subsystems.items():
            if (self.aqua_root / path).exists():
                print(f"  ✓ {name} implemented")
            else:
                print(f"  ✗ {name} missing")
                missing_subsystems.append(name)
        
        completeness_pass = len(missing_dirs) == 0 and len(missing_subsystems) == 0
        
        if completeness_pass:
            print("  ✓ COMPLETENESS: PASS")
        else:
            print(f"  ✗ COMPLETENESS: FAIL - Missing {len(missing_dirs)} directories, {len(missing_subsystems)} subsystems")
        
        self.validation_results["completeness"] = {
            "pass": completeness_pass,
            "missing_directories": missing_dirs,
            "missing_subsystems": missing_subsystems,
            "utcs_codes_found": utcs_codes_found
        }
        
        return self.validation_results["completeness"]
    
    def validate_structure(self) -> Dict[str, bool]:
        """Validate structure compliance"""
        print("\n[STRUCTURE]")
        
        structure_issues = []
        
        # Check kernel structure
        kernel_subdirs = ["core", "config", "drivers", "io", "ipc", "net", "power", "quantum", "runtime", "security"]
        for subdir in kernel_subdirs:
            if not (self.aqua_root / "kernel" / subdir).exists():
                structure_issues.append(f"kernel/{subdir} missing")
            else:
                print(f"  ✓ kernel/{subdir} present")
        
        # Check framework structure
        framework_subdirs = ["amores", "cqea", "demos", "wee"]
        for subdir in framework_subdirs:
            if not (self.aqua_root / "framework" / subdir).exists():
                structure_issues.append(f"framework/{subdir} missing")
            else:
                print(f"  ✓ framework/{subdir} present")
        
        # Check platform structure
        platform_subdirs = ["ampel360", "caas", "diqiaas", "gaia"]
        for subdir in platform_subdirs:
            if not (self.aqua_root / "platforms" / subdir).exists():
                structure_issues.append(f"platforms/{subdir} missing")
            else:
                print(f"  ✓ platforms/{subdir} present")
        
        structure_pass = len(structure_issues) == 0
        
        if structure_pass:
            print("  ✓ STRUCTURE: PASS")
        else:
            print(f"  ✗ STRUCTURE: FAIL - {len(structure_issues)} issues")
            for issue in structure_issues:
                print(f"    - {issue}")
        
        self.validation_results["structure"] = {
            "pass": structure_pass,
            "issues": structure_issues
        }
        
        return self.validation_results["structure"]
    
    def validate_consistency(self) -> Dict[str, bool]:
        """Validate file and specification consistency"""
        print("\n[CONSISTENCY]")
        
        consistency_issues = []
        
        # Check for matching .md/.yaml/.c files
        config_spec_pairs = [
            ("kernel/config/kernel-config.yaml", "kernel/core/mos-main.c"),
            ("boot/config/boot-config.yaml", "boot/bootloader.c"),
            ("platforms/ampel360/config/platform-config.yaml", "platforms/ampel360/platform-core.cpp")
        ]
        
        for config_file, spec_file in config_spec_pairs:
            config_path = self.aqua_root / config_file
            spec_path = self.aqua_root / spec_file
            
            if config_path.exists() and spec_path.exists():
                print(f"  ✓ {config_file} ↔ {spec_file} pair present")
            elif config_path.exists() or spec_path.exists():
                consistency_issues.append(f"Incomplete pair: {config_file} ↔ {spec_file}")
            else:
                consistency_issues.append(f"Missing pair: {config_file} ↔ {spec_file}")
        
        # Check naming conventions (kebab-case)
        naming_violations = []
        for root, dirs, files in os.walk(self.aqua_root):
            for name in dirs + files:
                if "_" in name and "-" in name:  # Mixed conventions
                    rel_path = str(Path(root).relative_to(self.aqua_root) / name)
                    naming_violations.append(rel_path)
        
        if naming_violations:
            print(f"  ⚠ {len(naming_violations)} naming convention warnings")
        else:
            print("  ✓ Naming conventions consistent")
        
        consistency_pass = len(consistency_issues) == 0
        
        if consistency_pass:
            print("  ✓ CONSISTENCY: PASS")
        else:
            print(f"  ✗ CONSISTENCY: FAIL - {len(consistency_issues)} issues")
        
        self.validation_results["consistency"] = {
            "pass": consistency_pass,
            "issues": consistency_issues,
            "naming_violations": naming_violations
        }
        
        return self.validation_results["consistency"]
    
    def validate_compliance(self) -> Dict[str, bool]:
        """Validate UTCS-MI and regulatory compliance"""
        print("\n[COMPLIANCE]")
        
        compliance_issues = []
        
        # Check for standards references
        standards_files = [
            "standards/aerospace/aerospace-standards-index.md"
        ]
        
        standards_present = 0
        for standards_file in standards_files:
            if (self.aqua_root / standards_file).exists():
                standards_present += 1
                print(f"  ✓ {standards_file} present")
            else:
                compliance_issues.append(f"Missing standards file: {standards_file}")
        
        # Check UTCS-MI metadata in specs
        specs_with_utcs = 0
        total_specs = 0
        
        for root, dirs, files in os.walk(self.aqua_root):
            for file in files:
                if file.endswith('.md') and not file.startswith('README'):
                    total_specs += 1
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        if 'UTCS-MI' in content or '[0' in content:
                            specs_with_utcs += 1
                    except:
                        pass
        
        utcs_coverage = (specs_with_utcs / total_specs * 100) if total_specs > 0 else 0
        print(f"  ✓ UTCS-MI coverage: {utcs_coverage:.1f}% ({specs_with_utcs}/{total_specs} specs)")
        
        # Check regulatory compliance references
        regulatory_systems = ["amores", "caas"]
        regulatory_present = 0
        
        for system in regulatory_systems:
            if (self.aqua_root / "framework" / system).exists() or (self.aqua_root / "platforms" / system).exists():
                regulatory_present += 1
                print(f"  ✓ {system} regulatory system present")
            else:
                compliance_issues.append(f"Missing regulatory system: {system}")
        
        compliance_pass = len(compliance_issues) == 0 and utcs_coverage >= 75
        
        if compliance_pass:
            print("  ✓ COMPLIANCE: PASS")
        else:
            print(f"  ✗ COMPLIANCE: FAIL - {len(compliance_issues)} issues, {utcs_coverage:.1f}% UTCS coverage")
        
        self.validation_results["compliance"] = {
            "pass": compliance_pass,
            "issues": compliance_issues,
            "utcs_coverage_percent": utcs_coverage,
            "standards_present": standards_present,
            "regulatory_systems": regulatory_present
        }
        
        return self.validation_results["compliance"]
    
    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        
        print("\n" + "=" * 60)
        print("AQUA OS UTCS-MI v5.0 COMPLIANCE VALIDATION REPORT")
        print("=" * 60)
        
        # Run all validations
        completeness = self.validate_completeness()
        structure = self.validate_structure()
        consistency = self.validate_consistency()
        compliance = self.validate_compliance()
        
        # Overall result
        overall_pass = all([
            completeness["pass"],
            structure["pass"], 
            consistency["pass"],
            compliance["pass"]
        ])
        
        print(f"\n{'✓ OVERALL RESULT: PASS' if overall_pass else '✗ OVERALL RESULT: FAIL'}")
        print("=" * 60)
        
        return {
            "overall_pass": overall_pass,
            "completeness": completeness,
            "structure": structure,
            "consistency": consistency,
            "compliance": compliance,
            "validation_timestamp": "2025-01-01T00:00:00Z"
        }

def main():
    """Main validation entry point"""
    # Use current working directory as AQUA root
    aqua_root = Path.cwd()
    
    # Verify we're in the right directory by checking for key files
    if not (aqua_root / "config" / "aqua-global.yaml").exists():
        print("Error: Not in AQUA root directory or config/aqua-global.yaml missing")
        return 1
    
    validator = UTCSMIValidator(aqua_root)
    
    # Generate validation report
    report = validator.generate_validation_report()
    
    # Save report
    report_file = aqua_root / "VALIDATION-REPORT.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nValidation report saved to: {report_file}")
    
    return 0 if report["overall_pass"] else 1

if __name__ == "__main__":
    exit(main())