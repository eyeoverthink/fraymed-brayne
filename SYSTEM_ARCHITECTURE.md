# Fraymus AGI System Architecture

Complete system architecture and interdependencies for the Fraymus AGI platform.

## Overview

The Fraymus AGI system is distributed across 15 specialized repositories, each handling specific aspects of the artificial general intelligence platform. This document explains how these components work together.

## Repository Map

### Core Infrastructure

**1. Fraymus-Core-System**
- Purpose: Core Java applications and foundational systems
- Dependencies: None (foundation layer)
- Provides: Base services, utilities, and core AGI infrastructure
- URL: https://github.com/eyeoverthink/Fraymus-Core-System

**2. Fraymus_Knowledge_Memory**
- Purpose: Knowledge storage, memory management, and persistence
- Dependencies: Fraymus-Core-System
- Provides: Memory blocks, knowledge chains, persistence layers
- URL: https://github.com/eyeoverthink/Fraymus_Knowledge_Memory

**3. Fraymus_Neural_AI**
- Purpose: Neural network implementations and AI models
- Dependencies: Fraymus-Core-System, Fraymus_Knowledge_Memory
- Provides: Neural architectures, AI processing, model integration
- URL: https://github.com/eyeoverthink/Fraymus_Neural_AI

### Specialized Systems

**4. Fraymus_Security**
- Purpose: Security protocols, encryption, and protection systems
- Dependencies: Fraymus-Core-System
- Provides: Cryptographic operations, security guards, protection layers
- URL: https://github.com/eyeoverthink/Fraymus_Security

**5. Fraymus_Living_Systems**
- Purpose: Living organisms, biological simulations, and digital life
- Dependencies: Fraymus-Core-System, Fraymus_Neural_AI
- Provides: Organism simulations, biological patterns, life systems
- URL: https://github.com/eyeoverthink/Fraymus_Living_Systems

**6. Fraymus_Genesis_AGI**
- Purpose: Genesis protocols and AGI bootstrap systems
- Dependencies: All core systems
- Provides: AGI initialization, genesis blocks, bootstrap protocols
- URL: https://github.com/eyeoverthink/Fraymus_Genesis_AGI

### Advanced Features

**7. Physics_Demos**
- Purpose: Physics engine demonstrations and simulations
- Dependencies: Fraymus-Core-System
- Provides: Physics simulations, demos, educational content
- URL: https://github.com/eyeoverthink/Physics_Demos

**8. Fraymus_Benchmarks_Applications**
- Purpose: Performance benchmarks and application testing
- Dependencies: All core systems
- Provides: Benchmarking tools, performance metrics, test applications
- URL: https://github.com/eyeoverthink/Fraymus_Benchmarks_Applications

### Integration & Communication

**9. Fraymus-OpenClaw**
- Purpose: Full OpenClaw implementation for agent communication
- Dependencies: Fraymus-Core-System
- Provides: Agent messaging, communication protocols, OpenClaw engine
- URL: https://github.com/eyeoverthink/Fraymus-OpenClaw

**10. Fraymus-Nano-Claw**
- Purpose: Lightweight claw implementation and AI core components
- Dependencies: Fraymus-Core-System
- Provides: Nano-claw agents, AI core utilities, lightweight communication
- URL: https://github.com/eyeoverthink/Fraymus-Nano-Claw

**11. Fraymus-Replit**
- Purpose: Replit integration and cloud deployment
- Dependencies: Fraymus-Core-System, Fraymus-OpenClaw
- Provides: Replit deployment, cloud integration, web interfaces
- URL: https://github.com/eyeoverthink/Fraymus-Replit-2

### Security Agent Systems

**12. Fraymus_Security_Agent**
- Purpose: Advanced security agent systems and experimental branches
- Dependencies: Fraymus-Core-System, Fraymus_Security
- Provides: Security agents, NEXUS systems, quantum oracle integration
- URL: https://github.com/eyeoverthink/Fraymus_Security_Agent

### User Interfaces & Media

**13. FraymusJAVA**
- Purpose: HTML demonstrations and web interfaces
- Dependencies: None (standalone web interfaces)
- Provides: Web demos, HTML interfaces, media assets
- URL: https://github.com/eyeoverthink/FraymusJAVA

**14. fraymed-brayne**
- Purpose: Python-based cognitive brain system
- Dependencies: None (Python-based, integrates via APIs)
- Provides: Python brain, cognitive processing, neural interfaces
- URL: https://github.com/eyeoverthink/fraymed-brayne

**15. Fraymus-MD-Files**
- Purpose: Documentation, context files, and system knowledge
- Dependencies: None (documentation layer)
- Provides: System documentation, guides, reference materials
- URL: https://github.com/eyeoverthink/Fraymus-MD-Files

## Dependency Graph

```
Fraymus-Core-System (Foundation)
├── Fraymus_Knowledge_Memory
├── Fraymus_Neural_AI
│   └── Fraymus_Living_Systems
├── Fraymus_Security
│   └── Fraymus_Security_Agent
├── Physics_Demos
├── Fraymus-OpenClaw
│   └── Fraymus-Replit
├── Fraymus-Nano-Claw
└── Fraymus_Genesis_AGI
    └── Fraymus_Benchmarks_Applications

FraymusJAVA (Standalone Web)
fraymed-brayne (Standalone Python)
Fraymus-MD-Files (Documentation)
```

## System Integration

### Java-Based Core
The core system is Java-based and requires:
- Java 17+ 
- Gradle for build management
- All core repositories cloned locally

### Python Integration
The Python brain (fraymed-brayne) integrates via:
- REST APIs
- Shared database connections
- File-based communication

### Web Interfaces
HTML demos (FraymusJAVA) connect via:
- WebSocket connections
- HTTP APIs
- Static file serving

## Full System Setup

### 1. Clone All Repositories
```bash
# Core Systems
git clone https://github.com/eyeoverthink/Fraymus-Core-System.git
git clone https://github.com/eyeoverthink/Fraymus_Knowledge_Memory.git
git clone https://github.com/eyeoverthink/Fraymus_Neural_AI.git
git clone https://github.com/eyeoverthink/Fraymus_Security.git
git clone https://github.com/eyeoverthink/Fraymus_Living_Systems.git
git clone https://github.com/eyeoverthink/Fraymus_Genesis_AGI.git

# Specialized
git clone https://github.com/eyeoverthink/Physics_Demos.git
git clone https://github.com/eyeoverthink/Fraymus_Benchmarks_Applications.git

# Integration
git clone https://github.com/eyeoverthink/Fraymus-OpenClaw.git
git clone https://github.com/eyeoverthink/Fraymus-Nano-Claw-.git
git clone https://github.com/eyeoverthink/Fraymus-Replit-2.git

# Security
git clone https://github.com/eyeoverthink/Fraymus_Security_Agent.git

# Interfaces
git clone https://github.com/eyeoverthink/FraymusJAVA.git
git clone https://github.com/eyeoverthink/fraymed-brayne.git
git clone https://github.com/eyeoverthink/Fraymus-MD-Files.git
```

### 2. Build Core System
```bash
cd Fraymus-Core-System
./gradlew build
```

### 3. Configure Dependencies
Each repository has its own configuration. Refer to individual READMEs for:
- Environment variables
- Database connections
- API keys
- Service endpoints

### 4. Start Services
Start in dependency order:
1. Fraymus-Core-System
2. Fraymus_Knowledge_Memory
3. Fraymus_Neural_AI
4. Other specialized systems

### 5. Launch Interfaces
- Open HTML demos from FraymusJAVA in browser
- Start Python brain from fraymed-brayne
- Access documentation from Fraymus-MD-Files

## Communication Between Systems

### Java-to-Java
- Direct method calls (same JVM)
- RMI (remote method invocation)
- Message queues

### Java-to-Python
- REST APIs
- gRPC
- Shared databases
- File-based communication

### Java-to-Web
- WebSocket
- HTTP/HTTPS
- Server-Sent Events

## Data Flow

```
User Input → Web Interface (FraymusJAVA)
         ↓
    API Gateway
         ↓
Core System (Fraymus-Core-System)
         ↓
┌────────┼────────┐
↓        ↓        ↓
Neural   Memory  Security
AI       Layer    Layer
↓        ↓        ↓
Processing & Storage
         ↓
Response → Web Interface
```

## Common Patterns

### Service Discovery
All Java services use a common service registry pattern defined in Fraymus-Core-System.

### Configuration
Shared configuration files are managed in Fraymus-Core-System and referenced by other systems.

### Logging
Centralized logging through the core system's logging framework.

### Error Handling
Standardized error handling across all Java-based repositories.

## Troubleshooting

### Dependency Issues
- Ensure all repositories are cloned
- Check build order (core first)
- Verify Gradle dependencies

### Communication Failures
- Check service ports
- Verify network connectivity
- Review firewall settings

### Performance Issues
- Consult Fraymus_Benchmarks_Applications
- Review system resources
- Check database performance

## Development Workflow

### Making Changes
1. Identify affected repositories
2. Update in dependency order
3. Run tests in each repository
4. Update integration tests
5. Commit with clear messages

### Testing
- Unit tests per repository
- Integration tests across repositories
- System-wide tests in Fraymus_Benchmarks_Applications

## Architecture Principles

1. **Modularity**: Each repository is independently deployable
2. **Loose Coupling**: Systems communicate via well-defined interfaces
3. **High Cohesion**: Related functionality grouped together
4. **Scalability**: Components can scale independently
5. **Maintainability**: Clear separation of concerns

## Future Expansion

New repositories should:
- Follow the dependency hierarchy
- Document their dependencies
- Include integration tests
- Update this architecture document

## Support

For detailed documentation, see:
- Fraymus-MD-Files: Complete system documentation
- Individual repository READMEs: Component-specific guides
- Fraymus_Benchmarks_Applications: Performance and testing

## License

See individual repositories for licensing information.
