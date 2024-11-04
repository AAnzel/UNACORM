# Contributing to The Unified DNA Encodings Platform

Thank you for your interest in contributing to our DNA data storage evaluation tool! We welcome contributions that enhance the functionality and expand the range of encoding methods. Below are the guidelines on how to contribute your own DNA encoding.

## Contribution Guidelines

### 1. Fork the Repository
- Start by forking the repository on GitHub. This creates a personal copy of the project where you can make changes.

### 2. Create a New Branch
- Create a new branch for your feature or fix. Use a descriptive name for your branch:
  ```bash
  git checkout -b feature/my-new-encoding
  ```

### 3. Implement Your Encoding
- Your encoding should be implemented in Python or as a Python wrapper. Please add your encoding files in a separate directory under the following root directory of the project:
[Source/Encodings/](Source/Encodings/)
  
- The structure of your code should include two main functions:
  
  **Encode Function**
  - **Function Name:** `encode(file_path, bool_array)`
  - **Parameters:**
    - `file_path`: Path to the file or a NumPy boolean array representing binary data.
    - `bool_array`: A NumPy boolean array (optional if using file_path, but preferred).
  - **Returns:** A list of DNA strings representing the encoded sequence, where each character is from the alphabet {A, C, G, T}.

  **Decode Function**
  - **Function Name:** `decode(file_path, list_of_dna_strings)`
  - **Parameters:**
    - `file_path`: Path to the file or a list of DNA strings.
    - `list_of_dna_strings`: A list of DNA strings (optional if using file_path, but preferred).
  - **Returns:** A NumPy boolean array reconstructing the original binary data.

### 4. Use OS-Agnostic File Management
- When implementing file handling, please use OS-agnostic file management functions (e.g., `os.path` for paths and `open()` for file operations) to ensure compatibility across different operating systems.

### 5. Testing Your Code
- Ensure that you write tests for your encoding and decoding functions. This helps maintain code quality and ensures that your contributions work as expected.

### 6. Commit Your Changes
- Once you are satisfied with your changes, commit them with a clear message:
  ```bash
  git add .
  git commit -m "Added: Added new encoding method named ->method name here<-"
  ```

### 7. Push Your Changes
- Push your changes to your forked repository:
  ```bash
  git push origin feature/my-new-encoding
  ```

### 8. Create a Pull Request
- Navigate to the original repository and create a pull request from your branch. Provide a clear description of what you have implemented and why it should be merged.

## Additional Notes
- Please ensure that your code adheres to the project's coding standards.
- Review existing encodings in the repository for reference.
- Engage with other contributors in discussions regarding your pull request.

We appreciate your contributions and look forward to seeing your innovative encoding methods!