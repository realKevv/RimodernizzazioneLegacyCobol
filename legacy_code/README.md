# COBOL Program Execution Guide

## Overview
This project contains COBOL programs that interact with product and database files to process inventory and purchasing routines. The provided COBOL files include:
- `BUYROUTINE.COB`
- `SMRKTAFINAL.COB`

Supporting data files:
- `DATABASE.txt`
- `products.txt`

## Prerequisites
To execute the COBOL programs, you need the following software:

### Windows
1. **GnuCOBOL** - Open-source COBOL compiler
   - Download: [https://gnucobol.sourceforge.io/](https://gnucobol.sourceforge.io/)
   - Install using:
     ```sh
     choco install gnucobol
     ```
     *(Requires Chocolatey package manager)*

2. **GCC (GNU Compiler Collection)** - Needed for GnuCOBOL
   - Install using MinGW:
     ```sh
     choco install mingw
     ```
   - Verify installation:
     ```sh
     cobc -V
     ```

### Linux/macOS
1. Install **GnuCOBOL** via package manager:
   ```sh
   sudo apt install gnucobol  # Debian-based
   sudo dnf install gnucobol  # Fedora-based
   brew install gnucobol       # macOS (Homebrew)
   ```
2. Verify installation:
   ```sh
   cobc -V
   ```

## Compilation and Execution
Follow these steps to compile and run the COBOL programs:

1. **Compile the COBOL program**
   ```sh
   cobc -x BUYROUTINE.COB -o buyroutine
   cobc -x SMRKTAFINAL.COB -o smrktafinal
   ```

2. **Run the program**
   ```sh
   ./buyroutine
   ./smrktafinal
   ```

3. Ensure `DATABASE.txt` and `products.txt` are in the same directory as the compiled executables.

## File Descriptions
- **BUYROUTINE.COB**: Processes purchases and updates inventory.
- **SMRKTAFINAL.COB**: Handles sales market analysis.
- **DATABASE.txt**: Contains product details and prices.
- **products.txt**: Stores inventory product information.

## Troubleshooting
- If `cobc` is not found, check if GnuCOBOL is installed and added to PATH.
- Ensure the data files (`DATABASE.txt` and `products.txt`) exist in the execution directory.
- Use `cobc -free -x filename.COB -o output` if the COBOL program uses free format.

## License
This project is open-source and free to use for educational purposes.

