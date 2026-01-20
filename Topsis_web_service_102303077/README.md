# TOPSIS Web Service (Part-III)

## Project Overview

This project is a **web-based implementation of the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)** method.  
It allows users to upload a CSV file, provide weights and impacts for criteria, and compute rankings for multiple alternatives using the TOPSIS algorithm.

The application is developed using **Flask** and provides a simple web interface for interaction.

---

## Objectives

- Develop a web service for TOPSIS
- Accept user input through a web interface
- Validate weights and impacts
- Generate TOPSIS scores and ranks
- Display results on the screen
- Provide an option to send results via email
- Deploy the application as a web service

---

## Technologies Used

- **Programming Language:** Python  
- **Web Framework:** Flask  
- **Frontend:** HTML, CSS  
- **Decision-Making Method:** TOPSIS (MCDM)  
- **Email Service:** Flask-Mail (SMTP)  
- **Deployment Platform:** Render  

---

## Input Specifications

- Input file must be in **CSV format**
- First column contains **alternative names**
- Remaining columns contain **numeric criteria values**
- Number of weights must equal number of criteria
- Number of impacts must equal number of criteria
- Impacts must be either `+` or `-`
- Weights and impacts must be comma-separated

---

## Sample Input CSV

## Sample Input CSV

```csv
Fund Name,P1,P2,P3,P4
M1,0.67,0.45,6.5,42.6
M2,0.60,0.36,3.6,53.3
M3,0.82,0.67,3.8,63.1
M4,0.60,0.36,3.5,69.2
M5,0.76,0.58,4.8,43.0
```
---
##Output Description
The output includes:
-Original input data
-TOPSIS Score for each alternative
-Rank based on TOPSIS score(Higher score indicates better rank)
---
##The result is:
-Displayed on the web page
-Optionally sent to a user-provided email ID
---
##Application Workflow
-User uploads a CSV file
-User enters weights and impacts
-Inputs are validated
-TOPSIS algorithm is applied
-Result is generated and displayed
-User may choose to send result via email


