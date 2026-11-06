
import pandas as pd
import mysql.connector
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from flask import Flask, render_template_string


# ==========================================
# 1. CONNECT TO MYSQL DATABASE
# ==========================================

mysql_password = os.environ.get("MYSQL_PASSWORD")

if not mysql_password:
    raise ValueError("MYSQL_PASSWORD environment variable is not set.")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=mysql_password,
    database="FinancialRiskDB"
)

# Read transaction data from MySQL
data = pd.read_sql(
    "SELECT * FROM Transactions",
    connection
)

connection.close()


# ==========================================
# 2. FINANCIAL RISK ANALYSIS
# ==========================================

total_transactions = len(data)

total_amount = data["TransactionAmount"].sum()

average_amount = data["TransactionAmount"].mean()

highest_amount = data["TransactionAmount"].max()

lowest_amount = data["TransactionAmount"].min()

fraud_count = (data["IsFraud"] == 1).sum()

genuine_count = (data["IsFraud"] == 0).sum()

fraud_percentage = (
    (fraud_count / total_transactions) * 100
    if total_transactions > 0 else 0
)

genuine_percentage = (
    (genuine_count / total_transactions) * 100
    if total_transactions > 0 else 0
)


print("===== FINANCIAL RISK ANALYSIS =====")

print("Total Transactions:", total_transactions)
print("Total Transaction Amount:", total_amount)
print("Average Transaction Amount:", average_amount)
print("Highest Transaction Amount:", highest_amount)
print("Lowest Transaction Amount:", lowest_amount)

print("\n===== FRAUD ANALYSIS =====")

print("Fraud Transactions:", fraud_count)
print("Genuine Transactions:", genuine_count)

print("\n===== FRAUD RISK SUMMARY =====")

print("Fraud Percentage:", round(fraud_percentage, 2), "%")
print("Genuine Percentage:", round(genuine_percentage, 2), "%")


# ==========================================
# 3. RULE-BASED FRAUD DETECTION
# ==========================================

def detect_fraud(row):

    reasons = []

    # Rule 1: High transaction amount
    if row["TransactionAmount"] > 20000:
        reasons.append("High Transaction Amount")

    # Rule 2: Unusual transaction time
    if 0 <= row["TransactionHour"] <= 5:
        reasons.append("Unusual Transaction Time")

    # Rule 3: Sudden increase in transaction amount
    if row["TransactionAmount"] > 3 * row["PreviousTransactionAmount"]:
        reasons.append("Sudden Amount Increase")

    # Rule 4: Flag selected locations for review
    if row["Location"] in ["Mumbai", "Delhi"]:
        reasons.append("Location Flag")

    if len(reasons) > 0:
        return "Suspicious", ", ".join(reasons)

    else:
        return "Normal", "No Rules Triggered"


# Apply fraud detection rules
data[["RiskStatus", "RiskReason"]] = data.apply(
    lambda row: pd.Series(detect_fraud(row)),
    axis=1
)


print("\n===== RULE-BASED FRAUD DETECTION =====")

print(data[[
    "TransactionID",
    "TransactionAmount",
    "Location",
    "RiskStatus",
    "RiskReason"
]])


# ==========================================
# 4. FINANCIAL RISK SCORE CALCULATION
# ==========================================

def calculate_risk_score(row):

    score = 0

    # Rule 1: High transaction amount
    if row["TransactionAmount"] > 20000:
        score += 30

    # Rule 2: Unusual transaction time
    if 0 <= row["TransactionHour"] <= 5:
        score += 25

    # Rule 3: Sudden amount increase
    if row["TransactionAmount"] > 3 * row["PreviousTransactionAmount"]:
        score += 25

    # Rule 4: Location flag
    if row["Location"] in ["Mumbai", "Delhi"]:
        score += 20

    return score


# Calculate risk score
data["RiskScore"] = data.apply(
    calculate_risk_score,
    axis=1
)


# Classify risk level
def classify_risk(score):

    if score <= 30:
        return "Low Risk"

    elif score <= 60:
        return "Medium Risk"

    else:
        return "High Risk"


data["RiskLevel"] = data["RiskScore"].apply(classify_risk)


print("\n===== FINANCIAL RISK SCORE ANALYSIS =====")

print(data[[
    "TransactionID",
    "TransactionAmount",
    "RiskScore",
    "RiskLevel"
]])


# ==========================================
# 5. GENERATE FINANCIAL RISK CHARTS
# ==========================================

os.makedirs("static", exist_ok=True)

# Chart 1: Suspicious vs Normal Transactions
fraud_counts = data["RiskStatus"].value_counts()

plt.figure(figsize=(6, 4))

if len(fraud_counts) > 0:
    plt.pie(
        fraud_counts,
        labels=fraud_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

plt.title("Suspicious vs Normal Transactions")

plt.savefig(
    "static/fraud_chart.png",
    bbox_inches="tight"
)

plt.close()


# Chart 2: Risk Level Distribution
risk_order = ["Low Risk", "Medium Risk", "High Risk"]

risk_counts = (
    data["RiskLevel"]
    .value_counts()
    .reindex(risk_order, fill_value=0)
)

plt.figure(figsize=(6, 4))

plt.bar(
    risk_counts.index,
    risk_counts.values
)

plt.title("Risk Level Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Number of Transactions")

plt.savefig(
    "static/risk_chart.png",
    bbox_inches="tight"
)

plt.close()

print("\nCharts generated successfully!")


# ==========================================
# 6. SAVE FINAL ANALYSIS RESULTS
# ==========================================

data.to_csv(
    "risk_analysis_results.csv",
    index=False
)

print("\nRisk analysis results saved successfully!")
print("File Name: risk_analysis_results.csv")


# ==========================================
# 7. FLASK DASHBOARD
# ==========================================

app = Flask(__name__)


@app.route("/")
def dashboard():

    total = len(data)

    fraud = (data["RiskStatus"] == "Suspicious").sum()

    genuine = total - fraud

    average = data["TransactionAmount"].mean() if total > 0 else 0

    # ======================================
    # 8. CUSTOMER-WISE FINANCIAL RISK ANALYSIS
    # ======================================

    customer_summary = data.groupby("CustomerID").agg(

        TotalTransactions=("TransactionID", "count"),

        TotalAmount=("TransactionAmount", "sum"),

        SuspiciousTransactions=(
            "RiskStatus",
            lambda x: (x == "Suspicious").sum()
        )

    ).reset_index()


    # Classify customer risk
    def customer_risk(row):

        if row["SuspiciousTransactions"] >= 2:
            return "High Risk"

        elif row["SuspiciousTransactions"] == 1:
            return "Medium Risk"

        else:
            return "Low Risk"


    customer_summary["CustomerRisk"] = customer_summary.apply(
        customer_risk,
        axis=1
    )


    # ======================================
    # 9. CREATE HTML TABLES
    # ======================================

    table = data[[
        "TransactionID",
        "CustomerID",
        "TransactionAmount",
        "RiskStatus",
        "RiskScore",
        "RiskLevel"
    ]].to_html(
        index=False,
        classes="table",
        border=0
    )


    customer_table = customer_summary.to_html(
        index=False,
        classes="table",
        border=0
    )


    # ======================================
    # 10. DASHBOARD HTML DESIGN
    # ======================================

    html = """
    <!DOCTYPE html>
    <html>

    <head>

        <title>Financial Risk Analysis Dashboard</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- Font Awesome Icons -->
        <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

        <style>

            * {
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                padding: 30px;
                margin: 0;
                color: #1e293b;
            }

            .header {
                background: #172554;
                color: white;
                padding: 25px;
                text-align: center;
                border-radius: 12px;
                margin-bottom: 30px;
            }

            .header h1 {
                margin: 0;
                font-size: 30px;
            }

            .header p {
                color: #cbd5e1;
                margin-bottom: 0;
            }

            h2 {
                color: #172554;
                margin-top: 35px;
                margin-bottom: 20px;
            }

            .section-icon {
                margin-right: 10px;
                color: #2563eb;
            }

            .cards {
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }

            .card {
                background: white;
                padding: 22px;
                width: 220px;
                text-align: center;
                border-radius: 12px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.08);
                border-bottom: 4px solid #2563eb;
                transition: transform 0.2s;
            }

            .card:hover {
                transform: translateY(-5px);
            }

            .card i {
                font-size: 36px;
                margin-bottom: 10px;
            }

            .card:nth-child(1) {
                border-bottom-color: #2563eb;
            }

            .card:nth-child(1) i {
                color: #2563eb;
            }

            .card:nth-child(2) {
                border-bottom-color: #dc2626;
            }

            .card:nth-child(2) i {
                color: #dc2626;
            }

            .card:nth-child(3) {
                border-bottom-color: #16a34a;
            }

            .card:nth-child(3) i {
                color: #16a34a;
            }

            .card:nth-child(4) {
                border-bottom-color: #9333ea;
            }

            .card:nth-child(4) i {
                color: #9333ea;
            }

            .card h3 {
                font-size: 15px;
                color: #475569;
            }

            .card h2 {
                margin: 10px 0;
                font-size: 25px;
                color: #172554;
            }

            .chart-container {
                display: flex;
                justify-content: center;
                gap: 30px;
                flex-wrap: wrap;
            }

            .chart-box {
                background: white;
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 3px 10px rgba(0,0,0,0.08);
                max-width: 100%;
            }

            .chart-box img {
                max-width: 100%;
                height: auto;
            }

            .table-container {
                overflow-x: auto;
                background: white;
                border-radius: 10px;
                padding: 10px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.06);
            }

            table {
                width: 100%;
                background: white;
                border-collapse: collapse;
                margin-top: 10px;
            }

            th, td {
                padding: 12px;
                border: 1px solid #e2e8f0;
                text-align: center;
            }

            th {
                background: #172554;
                color: white;
            }

            tr:nth-child(even) {
                background: #f8fafc;
            }

            tr:hover {
                background: #e0f2fe;
            }

            .footer {
                text-align: center;
                margin-top: 35px;
                color: #64748b;
                font-size: 13px;
            }

            @media (max-width: 600px) {

                body {
                    padding: 15px;
                }

                .header h1 {
                    font-size: 23px;
                }

                .card {
                    width: 100%;
                }

            }

        </style>

    </head>


    <body>

        <!-- DASHBOARD HEADER -->

        <div class="header">

            <h1>
                <i class="fa-solid fa-shield-halved"></i>
                Financial Risk Analysis Dashboard
            </h1>

            <p>Rule-Based Fraud Detection and Risk Monitoring System</p>

        </div>


        <!-- SUMMARY CARDS -->

        <div class="cards">

            <div class="card">

                <i class="fa-solid fa-money-bill-transfer"></i>

                <h3>Total Transactions</h3>

                <h2>{{ total }}</h2>

            </div>


            <div class="card">

                <i class="fa-solid fa-triangle-exclamation"></i>

                <h3>Suspicious Transactions</h3>

                <h2>{{ fraud }}</h2>

            </div>


            <div class="card">

                <i class="fa-solid fa-shield-check"></i>

                <h3>Genuine Transactions</h3>

                <h2>{{ genuine }}</h2>

            </div>


            <div class="card">

                <i class="fa-solid fa-indian-rupee-sign"></i>

                <h3>Average Amount</h3>

                <h2>₹{{ average }}</h2>

            </div>

        </div>


        <!-- FINANCIAL RISK CHARTS -->

        <h2>
            <i class="fa-solid fa-chart-pie section-icon"></i>
            Financial Risk Charts
        </h2>

        <div class="chart-container">

            <div class="chart-box">

                <h3>
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    Fraud Analysis
                </h3>

                <img src="/static/fraud_chart.png" width="350">

            </div>


            <div class="chart-box">

                <h3>
                    <i class="fa-solid fa-chart-column"></i>
                    Risk Level Analysis
                </h3>

                <img src="/static/risk_chart.png" width="350">

            </div>

        </div>


        <!-- CUSTOMER-WISE ANALYSIS -->

        <h2>
            <i class="fa-solid fa-users section-icon"></i>
            Customer-wise Financial Risk Analysis
        </h2>

        <div class="table-container">

            {{ customer_table | safe }}

        </div>


        <!-- TRANSACTION DETAILS -->

        <h2>
            <i class="fa-solid fa-list-check section-icon"></i>
            Transaction Risk Details
        </h2>

        <div class="table-container">

            {{ table | safe }}

        </div>


        <!-- FOOTER -->

        <div class="footer">

            <p>
                Financial Risk Analysis and Rule-Based Fraud Detection System
            </p>

            <p>
                Developed using Python, Flask, Pandas and MySQL
            </p>

        </div>


    </body>

    </html>
    """


    return render_template_string(

        html,

        total=total,

        fraud=fraud,

        genuine=genuine,

        average=f"{average:,.2f}",

        table=table,

        customer_table=customer_table

    )


# ==========================================
# 11. RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)
