# Assignment-01: TOPSIS Implementation

## Student Details

* **Name:** Tanya Mediratta
* **Roll Number:** 102303077
* **Course Assignment:** Assignment-01
* **Method Used:** TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)

---

## Repository Overview

This repository contains **all three parts of Assignment-01**, implemented step by step:

1. **TOPSIS as a PyPI Package**
2. **TOPSIS as a Python Command-Line Program**
3. **TOPSIS as a Web Service**

Each part builds upon the previous one.

---

## Repository Structure
```
Assignment01/
│
├── topsis/                           
│   # Part-I: PyPI package (Topsis-Tanya-102303077)
│
├── Topsis-Tanya-102303077/           
│   # Part-II: Python command-line implementation
│
├── Topsis_web_service_102303077/     
│   # Part-III: Flask-based web service
│
└── README.md                         
```

---

## Part-I: TOPSIS PyPI Package

In this part, the TOPSIS algorithm is implemented as a **Python package** and published on **PyPI**.

### Package Details

* **Package Name:** `Topsis-Tanya-102303077`
* **Version:** 1.0.3
* **PyPI Link:** [https://pypi.org/project/Topsis-Tanya-102303077/1.0.3/](https://pypi.org/project/Topsis-Tanya-102303077/1.0.3/)

### Features

* Installable using `pip`
* Executable via command line
* User manual provided
* Tested after installation

### Installation
```bash
pip install Topsis-Tanya-102303077
```

---

## Part-II: Python Command-Line Implementation

This part contains a **standalone Python program** that implements the TOPSIS algorithm using command-line arguments.

### Usage
```bash
python <program.py> <InputDataFile> <Weights> <Impacts> <OutputResultFileName>
```

### Example
```bash
python topsis.py data.csv "1,1,1,2" "+,+,-,+" output-result.csv
```

---

### Input Validation Rules

The program checks for:

* Correct number of parameters
* Handling of **File Not Found** exception
* Input file must contain **three or more columns**
* Columns from 2nd to last must contain **numeric values only**
* Number of weights = number of impacts = number of criteria
* Impacts must be either `+` or `-`
* Weights and impacts must be **comma-separated**

Appropriate error messages are shown for invalid inputs.

---

### Input / Output Format

**Input CSV Format**

* First column → Alternative names
* Remaining columns → Numeric criteria values

**Output CSV**

* Original input data
* TOPSIS score for each alternative
* Rank (higher score = better rank)

---

## Part-III: TOPSIS Web Service

In this part, a **Flask-based web service** is developed for TOPSIS computation.

### Web Service Features

* Upload CSV input file
* Enter weights and impacts
* Validate all inputs
* Generate TOPSIS result
* Display result on the web page
* Option to send result via email

### Validation Rules

* Number of weights must equal number of impacts
* Impacts must be either `+` or `-`
* Weights and impacts must be comma-separated
* Email ID must be in valid format

---

### Deployed Web Service

* **Live URL:** [https://topsis-web-service-102303077.onrender.com](https://topsis-web-service-102303077.onrender.com)
* **Backend:** Flask
* **Frontend:** HTML, CSS
* **Email Service:** SMTP (Flask-Mail)
* **Deployment Platform:** Render

---

## Technologies Used

* **Programming Language:** Python
* **Decision-Making Method:** TOPSIS
* **Web Framework:** Flask
* **Frontend:** HTML, CSS
* **Email Service:** SMTP
* **Deployment:** Render
* **Package Hosting:** PyPI

---

## Conclusion

This repository successfully completes all requirements of **Assignment-01**:

* TOPSIS implemented as a PyPI package
* TOPSIS implemented as a command-line program
* TOPSIS deployed as a web service

Each part demonstrates a progressive enhancement of functionality and usability.

---
