import json
import mysql.connector
from datetime import datetime

def get_db_config(config_file):
    """
    Reads database configuration from a JSON file.
    """
    with open(config_file, 'r') as file:
        return json.load(file)

def fetch_records():



    """
    Connects to the MySQL database and fetches all records from the `xyz` table.
    """


    db_to_placeholder_mapping = {
        "id": "Date of Notice",
        "owner_id": "Customer_Name",
        "position": "Customer_Email",
        "phone": "Loan_Account_No. / Credit_Card_Account_No.",
        "address1": "CRN",
        "customerid": "Loan_Accout_No. / Credit_Card_No.",
        "is_paid": "O/s Status Date (TOS / OD)",
        "sp_amount": "Current_EMI_O/s",
        "sp_product": "POS",
        "spoctoid": "Overdue_Amt",
        "minimum_amount_due": "CM_Name",
        "original_amount": "CM_MOB_No",
        "cm_email": "CM_Email",
        "kcc_mad_amount": "KCC_MAD_Amount",
        "tos": "TOS",
        "loan_amount": "Loan_Amount",
        "co_borrower_1": "Co-Borrower_Name_1",
        "co_borrower_2": "Co-Borrower_Name_2",
        "co_borrower_3": "Co-Borrower_Name_3",
        "co_borrower_4": "Co-Borrower_Name_4",
        "guarantor_1": "Guarantor_1",
        "guarantor_2": "Guarantor_2",
        "guarantor_3": "Guarantor_Name_3",
        "guarantor_4": "Guarantor_4.",
        "loan_agreement_date": "Loan_Agmt_Date",
        "first_installment": "1st installment",
        "last_installment": "Last Installment"
    }


    try:
        # Load the database configuration
        config = get_db_config('db_config.json')

        # Establish the database connection
        connection = mysql.connector.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'],
            database=config['database']
        )

        cursor = connection.cursor()
        # Execute the query
        cursor.execute("SELECT id,owner_id ,position,phone,address1,customerid,is_paid,sp_amount,sp_product,spoctoid,minimum_amount_due,original_amount   FROM sp_leads  WHERE company IS NOT NULL limit 1")
        column_names = [desc[0] for desc in cursor.description]

        records = cursor.fetchall()

        # Print all records
        # for record in records:
        #     a,b,c,d,e,f,g,h=record
        #     print(f"a: {a}, b: {b}, c: {c}")

        #     # print(record)

        for record in records:
            record_dict = dict(zip(column_names, record))

            placeholders = {placeholder: "xxx" for placeholder in db_to_placeholder_mapping.values()}

            # print(placeholders)

            # Populate placeholders using the mapping
            for db_column, placeholder in db_to_placeholder_mapping.items():
                if db_column in record_dict:
                    value = record_dict[db_column]
                    # Convert datetime objects to strings
                    if isinstance(value, datetime):
                        value = value.isoformat()
                        print("***",db_column)

                    placeholders[placeholder] = value


            print(json.dumps(placeholders, indent=4))
            


            # for column, value in record_dict.items():
                # print(f"{column}: {value}")
            print("-" * 40)  # Separator for better readability

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Ensure the connection is closed   
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    fetch_records()
