# AQUA OS Makefile
# Build system for Mixed Operating System

# Version and metadata
VERSION = 20.0
CODENAME = Unified-Quantum-Aerospace
BUILD_DATE = $(shell date +%Y-%m-%d)
GIT_COMMIT = $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")

# Compiler and tools
CC = gcc
CXX = g++
PYTHON = python3
CARGO = cargo
GO = go

# Directories
SRC_DIR = .
BUILD_DIR = build
DIST_DIR = dist
KERNEL_DIR = kernel
FRAMEWORK_DIR = framework
PLATFORM_DIR = platforms
TOOLS_DIR = tools
TEST_DIR = tests

# Kernel build configuration
KERNEL_CFLAGS = -std=c11 -Wall -Wextra -O2 -fno-stack-protector -nostdlib -ffreestanding
KERNEL_INCLUDES = -I$(KERNEL_DIR)/include -I/usr/src/linux-headers-$(shell uname -r)/include
KERNEL_SOURCES = $(wildcard $(KERNEL_DIR)/*/*.c)
KERNEL_OBJECTS = $(KERNEL_SOURCES:%.c=$(BUILD_DIR)/%.o)

# Framework build configuration  
FRAMEWORK_CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -fPIC
FRAMEWORK_INCLUDES = -I$(FRAMEWORK_DIR)/include
FRAMEWORK_SOURCES = $(wildcard $(FRAMEWORK_DIR)/*/*.cpp)
FRAMEWORK_OBJECTS = $(FRAMEWORK_SOURCES:%.cpp=$(BUILD_DIR)/%.o)

# Platform build configuration
PLATFORM_CXXFLAGS = -std=c++17 -Wall -Wextra -O2 -fPIC
PLATFORM_INCLUDES = -I$(PLATFORM_DIR)/include -I$(FRAMEWORK_DIR)/include
PLATFORM_SOURCES = $(wildcard $(PLATFORM_DIR)/*/*.cpp)
PLATFORM_OBJECTS = $(PLATFORM_SOURCES:%.cpp=$(BUILD_DIR)/%.o)

# Python dependencies
PYTHON_REQUIREMENTS = requirements.txt

# Default target
.PHONY: all
all: info kernel frameworks platforms tools

# Build information
.PHONY: info
info:
	@echo "======================================"
	@echo "  AQUA OS v$(VERSION) Build System"
	@echo "  Codename: $(CODENAME)"
	@echo "  Build Date: $(BUILD_DATE)"
	@echo "  Git Commit: $(GIT_COMMIT)"
	@echo "======================================"

# Create build directories
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(BUILD_DIR)/$(KERNEL_DIR)
	@mkdir -p $(BUILD_DIR)/$(FRAMEWORK_DIR)
	@mkdir -p $(BUILD_DIR)/$(PLATFORM_DIR)

# Kernel build targets
.PHONY: kernel
kernel: $(BUILD_DIR) $(KERNEL_OBJECTS)
	@echo "Building MOS kernel..."
	$(CC) $(KERNEL_CFLAGS) $(KERNEL_OBJECTS) -o $(BUILD_DIR)/mos-kernel
	@echo "Kernel build complete"

$(BUILD_DIR)/$(KERNEL_DIR)/%.o: $(KERNEL_DIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(KERNEL_CFLAGS) $(KERNEL_INCLUDES) -c $< -o $@

# Framework build targets
.PHONY: frameworks
frameworks: $(BUILD_DIR) python-deps
	@echo "Building AQUA frameworks..."
	@echo "  - Building CQEA framework..."
	$(CXX) $(FRAMEWORK_CXXFLAGS) $(FRAMEWORK_INCLUDES) -c $(FRAMEWORK_DIR)/cqea/cqea-core.cpp -o $(BUILD_DIR)/cqea-core.o
	@echo "  - Building Python frameworks..."
	$(PYTHON) -m py_compile $(FRAMEWORK_DIR)/amores/regulatory-engine.py
	$(PYTHON) -m py_compile $(FRAMEWORK_DIR)/wee/wee-core.py
	$(PYTHON) -m py_compile $(FRAMEWORK_DIR)/demos/demos-core.py
	@echo "Frameworks build complete"

# Platform build targets
.PHONY: platforms
platforms: $(BUILD_DIR) frameworks
	@echo "Building AQUA platforms..."
	@echo "  - Building AMPEL360 platform..."
	$(CXX) $(PLATFORM_CXXFLAGS) $(PLATFORM_INCLUDES) -c $(PLATFORM_DIR)/ampel360/platform-core.cpp -o $(BUILD_DIR)/ampel360-core.o
	@echo "Platforms build complete"

# Python dependencies
.PHONY: python-deps
python-deps:
	@echo "Installing Python dependencies..."
	@if [ -f $(PYTHON_REQUIREMENTS) ]; then \
		$(PYTHON) -m pip install -r $(PYTHON_REQUIREMENTS); \
	else \
		$(PYTHON) -m pip install numpy scipy pyyaml; \
	fi

# Tools build
.PHONY: tools
tools: $(BUILD_DIR)
	@echo "Building AQUA tools..."
	@chmod +x $(TOOLS_DIR)/deployment/*.sh
	@chmod +x $(TOOLS_DIR)/maintenance/*.sh
	@chmod +x $(TOOLS_DIR)/operations/*.sh
	@echo "Tools build complete"

# Testing targets
.PHONY: test
test: test-kernel test-frameworks test-platforms test-integration

.PHONY: test-kernel
test-kernel:
	@echo "Running kernel tests..."
	@if [ -d $(TEST_DIR)/kernel ]; then \
		cd $(TEST_DIR)/kernel && $(PYTHON) -m pytest -v; \
	fi

.PHONY: test-frameworks
test-frameworks:
	@echo "Running framework tests..."
	@if [ -d $(TEST_DIR)/framework ]; then \
		cd $(TEST_DIR)/framework && $(PYTHON) -m pytest -v; \
	fi

.PHONY: test-platforms
test-platforms:
	@echo "Running platform tests..."
	@if [ -d $(TEST_DIR)/platforms ]; then \
		cd $(TEST_DIR)/platforms && $(PYTHON) -m pytest -v; \
	fi

.PHONY: test-integration
test-integration:
	@echo "Running integration tests..."
	@if [ -d $(TEST_DIR)/integration ]; then \
		cd $(TEST_DIR)/integration && $(PYTHON) -m pytest -v; \
	fi

# Static analysis
.PHONY: lint
lint:
	@echo "Running static analysis..."
	@echo "  - C/C++ static analysis..."
	@if command -v cppcheck >/dev/null 2>&1; then \
		cppcheck --enable=all --std=c11 $(KERNEL_DIR)/; \
		cppcheck --enable=all --std=c++17 $(FRAMEWORK_DIR)/ $(PLATFORM_DIR)/; \
	fi
	@echo "  - Python static analysis..."
	@if command -v pylint >/dev/null 2>&1; then \
		find . -name "*.py" -exec pylint {} + || true; \
	fi

# Security scanning
.PHONY: security-scan
security-scan:
	@echo "Running security scans..."
	@if command -v bandit >/dev/null 2>&1; then \
		bandit -r $(FRAMEWORK_DIR)/ $(PLATFORM_DIR)/ || true; \
	fi

# Documentation generation
.PHONY: docs
docs:
	@echo "Generating documentation..."
	@mkdir -p $(BUILD_DIR)/docs
	@find . -name "*.md" -exec cp {} $(BUILD_DIR)/docs/ \;
	@echo "Documentation generated in $(BUILD_DIR)/docs/"

# Installation targets
.PHONY: install
install: all
	@echo "Installing AQUA OS..."
	@mkdir -p /opt/aqua
	@mkdir -p /etc/aqua
	@mkdir -p /var/lib/aqua
	@mkdir -p /var/log/aqua
	@cp -r config/* /etc/aqua/
	@cp -r $(BUILD_DIR)/* /opt/aqua/
	@echo "AQUA OS installed"

.PHONY: install-dev
install-dev: all
	@echo "Installing AQUA OS (development mode)..."
	@mkdir -p $$HOME/.aqua
	@cp -r config/* $$HOME/.aqua/
	@echo "AQUA OS development installation complete"

# Boot image creation
.PHONY: boot-image
boot-image: kernel
	@echo "Creating boot image..."
	@mkdir -p $(BUILD_DIR)/boot
	@cp boot/aqua-bootloader.efi $(BUILD_DIR)/boot/
	@cp $(BUILD_DIR)/mos-kernel $(BUILD_DIR)/boot/mos-kernel.img
	@cp boot/initramfs.img $(BUILD_DIR)/boot/
	@cp -r boot/config $(BUILD_DIR)/boot/
	@echo "Boot image created in $(BUILD_DIR)/boot/"

# ISO creation for deployment
.PHONY: iso
iso: boot-image
	@echo "Creating AQUA OS ISO..."
	@mkdir -p $(DIST_DIR)
	@if command -v genisoimage >/dev/null 2>&1; then \
		genisoimage -R -J -c boot/boot.cat -b boot/aqua-bootloader.efi \
		-o $(DIST_DIR)/aqua-os-$(VERSION).iso $(BUILD_DIR)/; \
	else \
		echo "genisoimage not found, ISO creation skipped"; \
	fi

# Container build
.PHONY: container
container:
	@echo "Building AQUA OS container..."
	@if command -v docker >/dev/null 2>&1; then \
		docker build -t aqua-os:$(VERSION) -t aqua-os:latest .; \
	else \
		echo "Docker not found, container build skipped"; \
	fi

# Deployment
.PHONY: deploy
deploy: iso container
	@echo "Deploying AQUA OS..."
	@$(TOOLS_DIR)/deployment/global-deployment.sh

# Cleanup targets
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR)
	@rm -rf $(DIST_DIR)
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

.PHONY: clean-all
clean-all: clean
	@echo "Cleaning all generated files..."
	@rm -rf /var/lib/aqua/build
	@rm -rf /var/cache/aqua

# Development helpers
.PHONY: format
format:
	@echo "Formatting code..."
	@if command -v clang-format >/dev/null 2>&1; then \
		find $(KERNEL_DIR) $(FRAMEWORK_DIR) $(PLATFORM_DIR) -name "*.c" -o -name "*.cpp" -o -name "*.h" | xargs clang-format -i; \
	fi
	@if command -v black >/dev/null 2>&1; then \
		black $(FRAMEWORK_DIR)/ $(PLATFORM_DIR)/ --line-length 100; \
	fi

.PHONY: check
check: lint security-scan
	@echo "Code quality checks complete"

# Development environment setup
.PHONY: setup-dev
setup-dev:
	@echo "Setting up development environment..."
	@sudo apt-get update
	@sudo apt-get install -y build-essential linux-headers-$(shell uname -r)
	@sudo apt-get install -y python3-dev python3-pip
	@sudo apt-get install -y cppcheck clang-format
	@$(PYTHON) -m pip install --user pytest pylint black bandit
	@echo "Development environment setup complete"

# Status and information
.PHONY: status
status:
	@echo "AQUA OS Build Status:"
	@echo "  Version: $(VERSION)"
	@echo "  Build Date: $(BUILD_DATE)"
	@echo "  Git Commit: $(GIT_COMMIT)"
	@echo "  Kernel Sources: $(words $(KERNEL_SOURCES)) files"
	@echo "  Framework Sources: $(words $(FRAMEWORK_SOURCES)) files"
	@echo "  Platform Sources: $(words $(PLATFORM_SOURCES)) files"

.PHONY: help
help:
	@echo "AQUA OS Build System Help"
	@echo "========================="
	@echo ""
	@echo "Main targets:"
	@echo "  all          - Build all components"
	@echo "  kernel       - Build MOS kernel"
	@echo "  frameworks   - Build CQEA, WEE, AMOReS, DeMOS"
	@echo "  platforms    - Build AMPEL360, DiQIaaS, CaaS, GAIA"
	@echo "  tools        - Build development and deployment tools"
	@echo ""
	@echo "Testing:"
	@echo "  test         - Run all tests"
	@echo "  lint         - Static code analysis"
	@echo "  security-scan - Security vulnerability scanning"
	@echo ""
	@echo "Deployment:"
	@echo "  boot-image   - Create bootable image"
	@echo "  iso          - Create installation ISO"
	@echo "  container    - Build Docker container"
	@echo "  deploy       - Full deployment"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean        - Clean build artifacts"
	@echo "  format       - Format source code"
	@echo "  setup-dev    - Setup development environment"
	@echo ""
	@echo "Information:"
	@echo "  status       - Show build status"
	@echo "  help         - Show this help"

# Include additional makefiles for specific components
-include $(KERNEL_DIR)/Makefile.kernel
-include $(FRAMEWORK_DIR)/Makefile.frameworks
-include $(PLATFORM_DIR)/Makefile.platforms