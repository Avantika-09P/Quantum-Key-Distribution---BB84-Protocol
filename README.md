# 🔐 Quantum Key Distribution (QKD) – BB84 Protocol Simulator

An interactive web-based simulation of the **BB84 Quantum Key Distribution Protocol**, demonstrating how two communicating parties can establish a secure shared secret key using the fundamental principles of quantum mechanics.

The project explores quantum communication, polarization/basis encoding, key reconciliation, and the detection of potential eavesdropping through quantum measurement.

<p align="center">

  **🚀 Live Application:** [BB84 Protocol Simulator](https://quantum-key-distribution---bb84-protocol-yvdjxbmjdrsbcshbqs6ts.streamlit.app/)

</p>

---

## 📌 Overview

The **BB84 protocol**, introduced by Charles Bennett and Gilles Brassard in 1984, is one of the first and most widely studied Quantum Key Distribution (QKD) protocols.

Unlike classical key exchange methods, BB84 utilizes quantum properties to establish a shared secret key. Its security relies on the fact that measuring an unknown quantum state can disturb it, making unauthorized interception potentially detectable.

This project provides an interactive way to understand the working of BB84 and how quantum mechanics contributes to secure communication.

## ✨ Key Concepts

- **Quantum State Preparation:** Encoding classical bits into quantum states using different bases.
- **Basis Selection:** Using two measurement bases – Rectilinear (+) and Diagonal (×).
- **Quantum Measurement:** Understanding how measurement outcomes depend on the selected basis.
- **Basis Reconciliation:** Comparing measurement bases over a public classical channel.
- **Key Sifting:** Retaining only the bits for which the sender and receiver selected matching bases.
- **Eavesdropping Detection:** Understanding how an interceptor's measurements can introduce errors into the shared key.
- **Quantum Bit Error Rate (QBER):** Measuring the error rate to assess potential interference in the quantum channel.

## ⚛️ How BB84 Works

The protocol involves three participants:

| Participant | Role |
|---|---|
| Alice | Generates and transmits quantum bits |
| Bob | Measures the received quantum states |
| Eve | Potential eavesdropper attempting to intercept communication |

### Step-by-Step Workflow

**1. Bit Generation**

Alice generates a random sequence of classical bits (0s and 1s).

**2. Basis Selection**

Alice randomly selects one of two encoding bases:

| Basis | Bit 0 | Bit 1 |
|---|---|---|
| Rectilinear (+) | 0° | 90° |
| Diagonal (×) | 45° | 135° |

**3. Quantum Transmission**

Alice encodes her bits into quantum states and transmits them to Bob.

**4. Measurement**

Bob independently chooses random measurement bases to measure the received quantum states.

**5. Basis Reconciliation**

Alice and Bob publicly compare their basis choices without revealing their actual bit values.

**6. Key Sifting**

They retain only the bits where their selected bases match, forming the sifted key.

**7. Eavesdropping Detection**

A sample of the sifted key can be compared to estimate the Quantum Bit Error Rate (QBER). An unexpectedly high error rate may indicate eavesdropping or channel noise.

## 📊 Understanding QBER

Quantum Bit Error Rate (QBER) measures the proportion of mismatched bits between Alice's and Bob's sifted keys.

\[
QBER = \frac{\text{Number of Error Bits}}{\text{Total Compared Bits}}\times 100
\]

In an ideal BB84 simulation:

- Without eavesdropping or channel noise, QBER is ideally 0%.
- Under an ideal intercept-resend attack with Eve choosing random bases, the expected QBER is 25% on the sifted key.
- In practical quantum communication, noise and device imperfections can also contribute to errors.

## 🛠️ Technology Stack

- **Python** – Core programming language
- **Streamlit** – Interactive web application framework
- **Quantum Computing Concepts** – Quantum states, measurement, and basis encoding
- **BB84 Protocol** – Quantum key distribution and eavesdropping detection

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

Open the local URL provided by Streamlit in your browser.

*Note: Update the entry-point filename and dependencies according to the actual repository structure.*

## 🎯 Learning Objectives

- Understand the fundamental principles of Quantum Key Distribution.
- Explore quantum encoding and measurement using different bases.
- Understand why matching bases are necessary for successful key generation.
- Learn how quantum measurement can reveal potential eavesdropping.
- Explore the role of QBER in evaluating quantum communication security.

## 🔮 Future Scope

- Implementation of additional QKD protocols such as E91, COW, and DPS.
- Integration of quantum circuit simulation using Qiskit.
- Visualization of quantum states and measurement outcomes.
- AI/ML-based detection and classification of quantum communication attacks.
- Comparative analysis of classical and quantum machine learning approaches for QKD security.

## 📚 References

1. Bennett, C. H., & Brassard, G. (1984). *Quantum Cryptography: Public Key Distribution and Coin Tossing.*
2. [IBM Quantum Learning](https://learning.quantum.ibm.com/)
3. [Qiskit Documentation](https://docs.quantum.ibm.com/)

---

<p align="center">

  **Exploring the intersection of Quantum Computing, Cryptography, and Secure Communication.**

  ⭐ If you find this project interesting, consider giving the repository a star!

</p>
