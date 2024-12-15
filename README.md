<div id="header" align="center">
  <h1>Safe & Sound - Password Manager</h1>

  [![Build Badge](https://img.shields.io/badge/Developed_by-DoktorSAS-brightgreen?style=for-the-badge&logo=x)](https://twitter.com/DoktorSAS)
  [![License](https://img.shields.io/badge/LICENSE-GPL--3.0-blue?style=for-the-badge&logo=appveyor)](LICENSE)
</div>

# Safe and Sound Password Manager

Welcome to the **Safe and Sound Password Manager** project! This project aims to develop a secure and user-friendly password management system using Python, specifically leveraging the [Eel](https://github.com/ChrisKnott/Eel) library for creating a desktop application with a web frontend.

## Overview

Safe and Sound Password Manager is designed to help users securely store, manage, and retrieve their passwords with ease. The key features include:

- **Password Encryption:** Protect your passwords using different methods:
  - **Passcode:** A numeric or alphanumeric code.
  - **Password:** A traditional password-based encryption.
  - **Image:** Use an image as part of your encryption key, adding an extra layer of complexity to your security.

- **User Interface:** Built with Eel, combining Python backend with HTML/CSS/JavaScript frontend for a smooth desktop application experience.

- **Cross-platform Compatibility:** Designed to run on Windows, macOS, and Linux.

## Installation

To get started with Safe and Sound Password Manager, follow these steps:

1. **Clone the Repository:**
   `git clone https://github.com/doktorsas/SafeAndSound.git`

2. **Install Dependencies:**
   - Ensure Python 3.x is installed on your system.
   - Install Eel and other required libraries

3. **Run the Application:**
   - TODO

## Usage

- **Add Passwords:** Store passwords with associated websites or applications.
- **Search and Retrieve:** Easily find and retrieve your passwords with a search function.
- **Encryption Method Selection:** Choose how you want to encrypt your data - via passcode, password, or image.

## Security Considerations

- **Encryption:** All passwords are encrypted using strong cryptographic algorithms. The choice of encryption key (passcode, password, or image) influences the security strength.
- **Image Encryption:** If using image encryption, ensure the image is complex enough to resist brute-force attacks, and keep in mind that image file integrity is crucial.
- **Local Storage:** Passwords are stored locally to prevent cloud vulnerabilities. Ensure your device is secure.

## Contributing

Contributions are welcome! Here's how you can participate:

- **Report Issues:** Found a bug or have a feature suggestion? Open an issue.
- **Improve Documentation:** Help us by improving this README or adding more detailed guides.
- **Code Contributions:** Submit pull requests for bug fixes, new features, or enhancements.

## License

This project is licensed under the [GNU License](LICENSE).
