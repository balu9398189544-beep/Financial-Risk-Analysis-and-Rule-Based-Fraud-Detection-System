# Financial Risk Analysis and Fraud Detection System
**College Project | Python, Flask and MySQL**

## Abstract

The Financial Risk Analysis and Fraud Detection System is a Python-based application designed to analyze financial transactions and identify potentially suspicious activities. It calculates transaction statistics, detects unusual transaction patterns using predefined rules, assigns financial risk scores, and classifies transactions into different risk levels. The system also generates financial risk charts and provides a web-based dashboard to display transaction summaries, customer-wise risk information, and suspicious transaction details.

## Problem Statement and Objectives

Financial transactions may involve unusual patterns such as unusually high amounts, transactions during unusual hours, sudden increases in transaction values, and transactions from selected locations. Identifying these activities manually can be difficult and time-consuming.

This project uses rule-based fraud detection and risk scoring to identify transactions that require further review and provide a clear summary of financial transaction risks.

**Objectives:**

- Analyze financial transaction records.
- Calculate total, average, highest, and lowest transaction amounts.
- Identify fraudulent and genuine transactions using the available dataset labels.
- Detect suspicious transactions using predefined rules.
- Calculate financial risk scores for individual transactions.
- Classify transactions into Low Risk, Medium Risk, and High Risk.
- Generate fraud analysis and risk distribution charts.
- Display transaction information through a Flask web dashboard.
- Perform customer-wise financial risk analysis.
- Export the final analysis results into a CSV file.

## Scope and Limitations

The project uses a sample transaction dataset containing transaction IDs, customer IDs, transaction amounts, transaction types, locations, transaction hours, previous transaction amounts, and fraud labels.

The system uses predefined rule-based conditions rather than machine learning. The results are intended for educational and demonstration purposes. A suspicious transaction is only a signal for further investigation and does not necessarily confirm fraud. The system is not connected to a real banking or payment service.

## Features

- Transaction data analysis using Pandas.
- Total transaction amount and average transaction amount calculation.
- Identification of highest and lowest transaction amounts.
- Fraudulent and genuine transaction counting.
- Rule-based suspicious transaction detection.
- Detection of high transaction amounts above ₹20,000.
- Detection of transactions occurring between 12 AM and 5 AM.
- Identification of sudden transaction increases greater than three times the previous transaction amount.
- Location-based flagging for Mumbai and Delhi.
- Financial risk score calculation.
- Risk classification into Low, Medium, and High categories.
- Fraud analysis pie chart.
- Risk level distribution bar chart.
- Responsive Flask dashboard.
- Customer-wise financial risk summary.
- Transaction risk details displayed in tabular format.
- Export of analysis results to `risk_analysis_results.csv`.

## Technology Stack

- **Python:** Main programming language.
- **Pandas:** Transaction data processing and analysis.
- **MySQL:** Database for storing transaction records.
- **MySQL Connector:** Connecting Python with the MySQL database.
- **Matplotlib:** Creating financial risk charts.
- **Flask:** Developing the web-based dashboard.
- **HTML and CSS:** Dashboard structure and styling.
- **CSV:** Storing transaction data and exporting analysis results.

## Project Architecture

The project contains three main Python files.

- `app.py` connects to the MySQL database, retrieves transaction records, performs financial risk analysis, detects suspicious transactions, calculates risk scores, generates charts, exports results, and runs the Flask dashboard.
- `app_backup.py` performs similar analysis directly using the `transactions.csv` dataset instead of retrieving records from MySQL. It also generates charts, exports results, and runs a Flask dashboard.
- `import_data.py` reads transaction records from `transactions.csv`, validates the column names, connects to MySQL, and imports the records into the `Transactions` table.

The project also includes:

- `transactions.csv` – Input dataset containing financial transaction records.
- `risk_analysis_results.csv` – Output dataset containing transaction details, risk status, reasons, risk scores, and risk levels.
- `static/` – Folder used to store generated financial risk charts.

## Dataset Description

The input dataset contains the following columns:

| Column | Description |
|---|---|
| TransactionID | Unique transaction identification number |
| CustomerID | Customer identification number |
| TransactionAmount | Amount involved in the transaction |
| TransactionType | Type of transaction, such as UPI, ATM, ONLINE, or TRANSFER |
| Location | Location where the transaction occurred |
| TransactionHour | Hour at which the transaction occurred |
| PreviousTransactionAmount | Amount of the customer's previous transaction |
| IsFraud | Indicates whether the transaction is labelled fraudulent or genuine |

The `IsFraud` column uses 1 for fraudulent transactions and 0 for genuine transactions.

## Fraud Detection Rules

The system uses four predefined rules to identify suspicious transactions.

**Rule 1: High Transaction Amount**

Transactions greater than ₹20,000 are flagged as suspicious.

**Rule 2: Unusual Transaction Time**

Transactions occurring between 12 AM and 5 AM are flagged for review.

**Rule 3: Sudden Increase in Transaction Amount**

A transaction is flagged when its amount is greater than three times the previous transaction amount.

**Rule 4: Location-Based Flagging**

Transactions from Mumbai and Delhi are flagged for review.

If one or more rules are triggered, the transaction is classified as Suspicious. Otherwise, it is classified as Normal.

## Financial Risk Score Calculation

The system assigns risk points based on the rules triggered by each transaction.

| Risk Condition | Score |
|---|---:|
| High transaction amount | 30 |
| Unusual transaction time | 25 |
| Sudden increase in amount | 25 |
| Location flag | 20 |
| **Maximum Score** | **100** |

The final risk score is calculated by adding the points for all triggered conditions.

**Risk Classification:**

- 0–30: Low Risk
- 31–60: Medium Risk
- 61–100: High Risk

## Dashboard and Visualization

The Flask dashboard provides a visual representation of the financial risk analysis.

It includes:

- Total number of transactions.
- Number of suspicious transactions.
- Number of genuine transactions.
- Average transaction amount.
- Fraud analysis pie chart.
- Risk level distribution bar chart.
- Customer-wise financial risk analysis table.
- Transaction risk details table.

The dashboard helps users understand the transaction patterns and identify records that require further attention.

## Setup and Installation

### Requirements

Install Python and the required libraries:

```bash
pip install pandas matplotlib flask mysql-connector-python
```

### MySQL Configuration

1. Install and start MySQL.
2. Create a database named `FinancialRiskDB`.
3. Create a table named `Transactions` with the required columns matching the input dataset.
4. Configure the MySQL username and password.

The application expects the database to be available on localhost and uses the MySQL user `root`.

### Import Transaction Data

Run the following command to import the CSV records into MySQL:

```bash
python import_data.py
```

Enter your MySQL password when prompted.

The script validates the CSV headers and imports the transaction records into the `Transactions` table.

### Run the Main Application

Set the MySQL password as an environment variable.

**Windows PowerShell:**

```powershell
$env:MYSQL_PASSWORD="your_mysql_password"
python app.py
```

**macOS / Linux:**

```bash
export MYSQL_PASSWORD="your_mysql_password"
python app.py
```

Open the following address in your browser:

`http://127.0.0.1:5000`

### Run the Backup Application

Alternatively, the backup application can be executed directly using the CSV dataset:

```bash
python app_backup.py
```

It reads `transactions.csv` from the current working directory and runs the Flask dashboard without requiring the MySQL database connection.

## Output Files

The project automatically generates the following outputs:

- `static/fraud_chart.png` – Pie chart showing suspicious and normal transaction distribution.
- `static/risk_chart.png` – Bar chart showing the distribution of financial risk levels.
- `risk_analysis_results.csv` – Final transaction analysis results, including risk status, reasons, scores, and classifications.

The output CSV is generated when either analysis application runs.

## Known Limitations and Future Enhancements

- The system uses predefined rules and does not use machine learning algorithms.
- Location-based flags may identify genuine transactions for additional review.
- Suspicious transactions are not automatically confirmed as fraudulent.
- The system uses sample transaction data for demonstration.
- MySQL must be configured and running to use the main application.
- The backup application requires the CSV file to be available in its working directory.
- The dashboard runs in local development mode.

**Suggested Future Enhancements:**

- Integrate machine learning models for improved fraud detection.
- Add real-time transaction monitoring.
- Introduce customer authentication and administrator access.
- Add more advanced fraud detection rules.
- Include transaction history and trend analysis.
- Improve dashboard filtering and reporting features.
- Integrate email or SMS alerts for suspicious transactions.

## Conclusion

The Financial Risk Analysis and Fraud Detection System demonstrates how Python, Pandas, MySQL, Matplotlib, and Flask can be used together to analyze financial transactions and identify potentially suspicious activities. It provides transaction statistics, rule-based fraud detection, risk scoring, graphical reports, and an interactive dashboard. This project provides a basic understanding of financial risk monitoring and how automated analysis can support the identification of unusual transaction patterns.
