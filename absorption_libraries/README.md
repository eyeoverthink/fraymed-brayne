# ABSORPTION LIBRARIES

This folder contains external libraries to be absorbed into Fraynix using the Transpilation Arsenal.

## Directory Structure

- `go/` - Go libraries for Go→Java transpilation
- `cpp/` - C++ libraries for C++→Java transpilation
- `python/` - Python libraries for Python→Java transpilation

## Target Libraries for Absorption

### Go Libraries (Priority 1)
- **Ollama** - LLM inference engine
  - Source: https://github.com/ollama/ollama
  - Command: `git clone https://github.com/ollama/ollama.git go/ollama`
  
- **Gemma4** - Google's Gemma 4 model (Go implementation)
  - Source: [TBD - find Go implementation]
  
- **Gemma3** - Google's Gemma 3 model (Go implementation)
  - Source: [TBD - find Go implementation]

### C++ Libraries (Priority 2)
- **TensorFlow** - Deep learning framework
  - Source: https://github.com/tensorflow/tensorflow
  - Command: `git clone https://github.com/tensorflow/tensorflow.git cpp/tensorflow`

### Python Libraries (Priority 3)
- **PyTorch** - Deep learning framework
- **NumPy** - Numerical computing
- **Pandas** - Data analysis

## Absorption Process

1. Download/clone libraries to appropriate folder
2. Use Fraynix transpile command:
   ```
   transpile ./absorption_libraries/go/ollama ./absorbed/ollama go2java
   transpile ./absorption_libraries/cpp/tensorflow ./absorbed/tensorflow cpp2java
   ```

## Quick Download Script

Run the PowerShell script `download_libraries.ps1` to automatically download all target libraries.

```powershell
.\download_libraries.ps1
```
