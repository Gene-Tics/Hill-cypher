```markdown
# 🎉 Hill Cipher Encryption/Decryption System 🎉

**Authors**: Bryan Ross Vocales & Eugene Albert Navarro  
**Date**: Created on 09/21/24, Last Modified on 09/25/24  
**Version**: 1.0 

---

## 🔍 Purpose
This program implements the **Hill cipher algorithm** to encrypt and decrypt plaintext messages using a matrix-based key.

---

## 🖥️ System Requirements:
- **Hardware**:  
  - 💻 CPU: Minimum 1 GHz processor  
  - 🖥️ RAM: Minimum 512MB  
  - 💾 Storage: Minimum 50MB for Python and libraries  
- **Software**: Any OS supporting Python 3.x (Windows, Linux, macOS)  
- **Python Version**: Python 3.x  
- **Required Libraries**: NumPy (for matrix operations)

---

## 🛠️ Functional Description:

### Input:
- **Plaintext**: A string of alphabetic characters (A-Z). Non-alphabetic characters are removed.
- **Key Matrix**: A square matrix (e.g., 2x2 or 3x3) used for encryption and decryption.

### Processing:
- Convert the plaintext to numerical values (A=0, B=1, …, Z=25).
- Pad the plaintext if needed to match the key matrix size.
- For encryption, perform matrix multiplication between the key matrix and the plaintext column vector, followed by modulo 26.
- For decryption, compute the inverse of the key matrix and perform similar multiplication and modulo operations.

### Output:
- 🔐 **Encrypted Text**: A string of encrypted characters based on the Hill cipher.
- 🔓 **Decrypted Text**: The original plaintext, restored from the encrypted message.

---

## 🔒 Security Considerations:

### Vulnerability Assessment:
- Susceptible to frequency analysis attacks if used with short messages.
- The key matrix must be invertible for successful decryption.

### Mitigation Strategies:
- Use longer plaintexts to mitigate frequency analysis.
- Ensure the matrix key is carefully selected to be invertible under mod 26.

---

## ✅ Testing:
- Encrypt and decrypt test cases to verify correct functionality.
- Test with different key matrices to ensure invertibility and correctness.

---

## 🚀 Usage Instructions:

### Installation:
1. Install Python 3.x from [python.org](https://www.python.org/downloads/).
2. Install the NumPy library using the following command:  
   ```bash
   pip install numpy
   ```

### Configuration:
- Modify the key matrix in the code to change the encryption key.

### Execution:
- Run the program by executing:
  ```bash
  python hill_cipher.py
  ```
- Follow prompts to input plaintext and observe encrypted and decrypted results.

---

## ⚙️ Error Handling:

### Error Codes:
- **Invalid Matrix**: If the key matrix is not invertible, decryption will fail.
- **Invalid Characters**: Non-alphabetic characters are automatically ignored during input.

### Recovery Procedures:
- Ensure the key matrix is invertible and adjust the input plaintext to contain only alphabetic characters.

---

## 📝 Maintenance Log:

| Date       | Changes                               | Author                          |
|------------|---------------------------------------|---------------------------------|
| 2024-09-24 | Initial creation of the program.      | Bryan Ross Vocales & Eugene Albert Navarro |
| 2024-10-02 | Additional features or bug fixes.     | Bryan Ross Vocales & Eugene Albert Navarro |

---

## 📚 Additional Documentation Tools:
- **Docstrings**: Each function has a docstring describing its purpose, parameters, and return values.
- **Version Control**: Use Git for version control. Example commands:  
  ```bash
  git init
  git add hill_cipher.py
  git commit -m "Initial Hill Cipher implementation"
  ```

---

