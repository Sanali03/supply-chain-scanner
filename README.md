# Supply Chain Security Scanning Tool

A desktop-based cybersecurity tool designed to identify and manage software supply chain risks by analyzing third-party dependencies, detecting known vulnerabilities, classifying security risks, and enforcing security policies.

## 📌 Project Overview

Modern software applications rely heavily on third-party and open-source dependencies. Vulnerable or outdated dependencies can introduce significant security risks into software projects.

This project provides an integrated approach to software supply chain security by combining:

- Software Bill of Materials (SBOM) generation
- Dependency analysis
- Vulnerability detection
- Risk classification
- Policy-based security evaluation
- Security visualization and reporting

The system aims to provide better visibility into software dependencies and support proactive security decision-making within the Software Development Life Cycle (SDLC).

## 🎯 Objectives

- Identify direct and transitive software dependencies.
- Generate an SBOM for analyzed projects.
- Detect known vulnerabilities in dependencies.
- Classify dependencies according to security risk.
- Prioritize vulnerabilities for remediation.
- Evaluate project security using predefined policies.
- Provide visual insights into dependency and vulnerability risks.
- Support secure decision-making before software deployment.

## ⚙️ Key Features

### 1. SBOM Generation
Uses **Syft** to generate a Software Bill of Materials containing information such as:

- Package name
- Package version
- Package ecosystem
- Direct and transitive dependencies

### 2. Vulnerability Detection
Uses the **OSV API** to identify known vulnerabilities associated with project dependencies.

The system retrieves:

- CVE/OSV identifiers
- Severity levels
- Vulnerability descriptions
- CVSS scores

### 3. Risk Classification

Dependencies and vulnerabilities are categorized into:

- Critical
- High
- Medium
- Low

The system also calculates an overall project risk level.

### 4. Policy Enforcement

Security policies are applied based on vulnerability severity.

Projects can be classified as:

- ✅ Approved
- ⚠️ Pending
- 🚫 Blocked

High-risk dependencies are flagged to support security decisions before deployment.

### 5. Dashboard & Visualization

The application provides visual representations of:

- Risk distribution
- Vulnerability summaries
- Dependency risk ratios
- Vulnerability trends
- Scan results

### 6. Scan History

The system maintains previous scan results, allowing projects to be rescanned and historical results to be tracked.

<img width="940" height="495" alt="image" src="https://github.com/user-attachments/assets/68a9b45e-7d57-4c87-aa53-d3351ccd374e" />


<img width="940" height="495" alt="image" src="https://github.com/user-attachments/assets/5eed3df0-b8fa-4e5c-944f-05db2d422f55" />


<img width="940" height="495" alt="image" src="https://github.com/user-attachments/assets/a94c3c25-cc20-4dcf-aec7-7d207ae65269" />


<img width="940" height="495" alt="image" src="https://github.com/user-attachments/assets/976aaa19-b9cc-4ae0-80ef-bae623d28a9d" />


<img width="940" height="495" alt="image" src="https://github.com/user-attachments/assets/6be3213e-b124-4ffe-b349-e0dd9b89abb1" />
