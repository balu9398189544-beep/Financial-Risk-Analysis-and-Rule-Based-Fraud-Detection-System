
import csv
import mysql.connector
import os
from getpass import getpass

# Get the folder containing this Python file
folder_path = os.path.dirname(os.path.abspath(__file__))

# Get the CSV file path
csv_path = os.path.join(folder_path, "transactions.csv")

# Check CSV file
if not os.path.exists(csv_path):
    print("ERROR: transactions.csv not found!")
    exit()

print("CSV FILE LOCATION:", csv_path)
print("CSV FILE SIZE:", os.path.getsize(csv_path), "bytes")

connection = None
cursor = None

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password=getpass("Enter MySQL password: "),
        database="FinancialRiskDB"
    )

    cursor = connection.cursor()

    # Read CSV file and skip blank lines
    with open(csv_path, "r", newline="", encoding="utf-8-sig") as file:

        reader = csv.DictReader(
            line for line in file if line.strip()
        )

        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or has no header row.")

        # Remove spaces from column names
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        print("ACTUAL CSV HEADERS:", repr(reader.fieldnames))
        print("NUMBER OF COLUMNS:", len(reader.fieldnames))

        # Required CSV columns
        required_columns = [
            "TransactionID",
            "CustomerID",
            "TransactionAmount",
            "TransactionType",
            "Location",
            "TransactionHour",
            "PreviousTransactionAmount",
            "IsFraud"
        ]

        if reader.fieldnames != required_columns:
            raise ValueError("CSV column names do not match the required columns.")

        # SQL INSERT query
        query = """
        INSERT INTO Transactions (
            TransactionID,
            CustomerID,
            TransactionAmount,
            TransactionType,
            Location,
            TransactionHour,
            PreviousTransactionAmount,
            IsFraud
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        records = []

        # Read transaction records
        for row in reader:
            records.append((
                int(row["TransactionID"]),
                row["CustomerID"],
                float(row["TransactionAmount"]),
                row["TransactionType"],
                row["Location"],
                int(row["TransactionHour"]),
                float(row["PreviousTransactionAmount"]),
                int(row["IsFraud"])
            ))

    if not records:
        raise ValueError("No transaction records found in CSV.")

    # Insert records into MySQL
    cursor.executemany(query, records)
    connection.commit()

    print(len(records), "transactions imported successfully!")

except Exception as error:
    if connection is not None and connection.is_connected():
        connection.rollback()

    print("ERROR:", error)

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
