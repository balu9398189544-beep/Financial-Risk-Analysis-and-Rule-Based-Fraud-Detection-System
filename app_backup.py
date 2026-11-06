
import pandas as pd
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# Read transaction dataset
data = pd.read_csv("transactions.csv")

# Total number of transactions
total_transactions = len(data)

# Total transaction amount
total_amount = data["TransactionAmount"].sum()

# Average transaction amount
average_amount = data["TransactionAmount"].mean()

# Highest transaction amount
highest_amount = data["TransactionAmount"].max()

# Lowest transaction amount
lowest_amount = data["TransactionAmount"].min()

# Count fraudulent transactions
fraud_count = (data["IsFraud"] == 1).sum()

# Count genuine transactions
genuine_count = (data["IsFraud"] == 0).sum()

# Display results
print("===== FINANCIAL RISK ANALYSIS =====")

print("Total Transactions:", total_transactions)
print("Total Transaction Amount:", total_amount)
print("Average Transaction Amount:", average_amount)
print("Highest Transaction Amount:", highest_amount)
print("Lowest Transaction Amount:", lowest_amount)

print("\n===== FRAUD ANALYSIS =====")

print("Fraud Transactions:", fraud_count)
print("Genuine Transactions:", genuine_count)
# Calculate fraud percentage
fraud_percentage = (fraud_count / total_transactions) * 100

# Calculate genuine transaction percentage
genuine_percentage = (genuine_count / total_transactions) * 100

print("\n===== FRAUD RISK SUMMARY =====")

print("Fraud Percentage:", round(fraud_percentage, 2), "%")
print("Genuine Percentage:", round(genuine_percentage, 2), "%")

# RULE-BASED FRAUD DETECTION

def detect_fraud(row):

    reasons = []

    # Rule 1: High transaction amount
    if row["TransactionAmount"] > 20000:
        reasons.append("High Transaction Amount")

    # Rule 2: Unusual transaction time
    if row["TransactionHour"] >= 0 and row["TransactionHour"] <= 5:
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
    lambda row: pd.Series(detect_fraud(row)), axis=1
)

print("\n===== RULE-BASED FRAUD DETECTION =====")

print(data[[
    "TransactionID",
    "TransactionAmount",
    "Location",
    "RiskStatus",
    "RiskReason"
]])

# FINANCIAL RISK SCORE CALCULATION

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
data["RiskScore"] = data.apply(calculate_risk_score, axis=1)


# Classify risk level
def classify_risk(score):

    if score <= 30:
        return "Low Risk"

    elif score <= 60:
        return "Medium Risk"

    else:
        return "High Risk"


data["RiskLevel"] = data["RiskScore"].apply(classify_risk)


# Display risk analysis
print("\n===== FINANCIAL RISK SCORE ANALYSIS =====")

print(data[[
    "TransactionID",
    "TransactionAmount",
    "RiskScore",
    "RiskLevel"
]])
# GENERATE FINANCIAL RISK CHARTS

# Create static folder
os.makedirs("static", exist_ok=True)

# Chart 1: Suspicious vs Normal Transactions
fraud_counts = data["RiskStatus"].value_counts()

plt.figure(figsize=(6, 4))
plt.pie(
    fraud_counts,
    labels=fraud_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Suspicious vs Normal Transactions")
plt.savefig("static/fraud_chart.png", bbox_inches="tight")
plt.close()

# Chart 2: Risk Level Distribution
risk_counts = data["RiskLevel"].value_counts()

plt.figure(figsize=(6, 4))
plt.bar(risk_counts.index, risk_counts.values)
plt.title("Risk Level Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Number of Transactions")
plt.savefig("static/risk_chart.png", bbox_inches="tight")
plt.close()

print("Charts generated successfully!")
# SAVE FINAL ANALYSIS RESULTS

data.to_csv("risk_analysis_results.csv", index=False)

print("\nRisk analysis results saved successfully!")
print("File Name: risk_analysis_results.csv")

from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def dashboard():

    total = len(data)
    fraud = (data["RiskStatus"] == "Suspicious").sum()
    genuine = total - fraud
    average = data["TransactionAmount"].mean()

    table = data[[
        "TransactionID",
        "CustomerID",
        "TransactionAmount",
        "RiskStatus",
        "RiskScore",
        "RiskLevel"
    ]].to_html(index=False, classes="table", border=0)

    html = """
    <html>
    <head>
        <title>Financial Risk Dashboard</title>
        <style>
            body {
                font-family: Arial;
                background: #f2f4f8;
                padding: 30px;
            }
            h1 {
                color: #172554;
                text-align: center;
            }
            .cards {
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .card {
                background: white;
                padding: 20px;
                width: 180px;
                text-align: center;
                border-radius: 10px;
            }
            table {
                width: 100%;
                background: white;
                border-collapse: collapse;
                margin-top: 25px;
            }
            th, td {
                padding: 12px;
                border: 1px solid #ddd;
                text-align: center;
            }
            th {
                background: #172554;
                color: white;
            }
        </style>
    </head>

    <body>

        <h1>Financial Risk Analysis Dashboard</h1>

        <div class="cards">
            <div class="card">
                <h3>Total Transactions</h3>
                <h2>{{ total }}</h2>
            </div>

            <div class="card">
                <h3>Suspicious Transactions</h3>
                <h2>{{ fraud }}</h2>
            </div>

            <div class="card">
                <h3>Genuine Transactions</h3>
                <h2>{{ genuine }}</h2>
            </div>

            <div class="card">
                <h3>Average Amount</h3>
                <h2>₹{{ average }}</h2>
            </div>
        </div>
<h2>Financial Risk Charts</h2>

<div style="display:flex; justify-content:center; gap:30px; flex-wrap:wrap;">

    <div style="background:white; padding:15px; border-radius:10px;">
        <h3>Fraud Analysis</h3>
        <img src="/static/fraud_chart.png" width="350">
    </div>

    <div style="background:white; padding:15px; border-radius:10px;">
        <h3>Risk Level Analysis</h3>
        <img src="/static/risk_chart.png" width="350">
    </div>

</div>
        <h2>Transaction Risk Details</h2>

        {{ table | safe }}

    </body>
    </html>
    """

    return render_template_string(
        html,
        total=total,
        fraud=fraud,
        genuine=genuine,
        average=round(average, 2),
        table=table
    )


if __name__ == "__main__":
    app.run(debug=True)
