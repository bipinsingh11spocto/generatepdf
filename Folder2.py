import json
import mysql.connector
from datetime import datetime
import sys

import re
import os 
import pdfkit

def remove_last_page(input_pdf):
    """
    Remove the last page from a PDF file using pikepdf.
    
    Args:
        input_pdf (str): Path to the input PDF file.
    
    Returns:
        str: Path to the modified PDF file.
    """
    try:
        # Open the PDF
        pdf = pikepdf.Pdf.open(input_pdf)
        
        # If the PDF has only one page, we can't remove the last page
        if len(pdf.pages) <= 1:
            print(f"PDF {input_pdf} has only one page. Skipping page removal.")
            return input_pdf
        
        # Create a new PDF with all pages except the last one
        new_pdf = pikepdf.Pdf.new()
        
        # Copy all pages except the last one
        for page in pdf.pages[:-1]:
            new_pdf.pages.append(page)
        
        # Save the modified PDF
        new_pdf.save(input_pdf)
        
        print(f"Successfully removed last page from {input_pdf}")
        return input_pdf
    
    except Exception as e:
        print(f"Error removing last page from PDF: {e}")
        return None

def get_db_config(config_file):
    """
    Reads database configuration from a JSON file.
    """
    with open(config_file, 'r') as file:
        return json.load(file)
    
def modify_placeholders(html_content, placeholders):
    for placeholder_name, new_value in placeholders.items():
        if not isinstance(new_value, str):
            new_value = str(new_value)  
        # Pattern to find placeholders of the form @PLACEHOLDER@
        # pattern = fr"@{placeholder_name}@"
        # pattern = fr"@\s*{re.escape(placeholder_name)}\s*@"
        pattern = fr"@[^@<]*?{re.escape(placeholder_name)}[^@>]*?@"
        # pattern = fr"{{placeholder_name}}"


        
        print(pattern)
        # Replace the placeholder with the new value
        html_content = re.sub(pattern, new_value, html_content)
    return html_content

def html_to_pdf(input_html, output_pdf=None):
    """
    Convert an HTML file to PDF.
    
    Args:
        input_html (str): Path to the input HTML file.
        output_pdf (str, optional): Path for the output PDF file. 
                                    If not provided, uses the input filename with .pdf extension.
    
    Returns:
        str: Path to the generated PDF file.
    """
    # If no output path is specified, create one based on input filename
    if output_pdf is None:
        base_name = os.path.splitext(input_html)[0]
        output_pdf = f"{base_name}.pdf"
    
    input_html_path = os.path.abspath(input_html)

    # Configuration options (optional)
    config = {
        'page-size': 'Letter',
        'page-height': '150',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'load-error-handling': 'ignore',
        'load-media-error-handling': 'ignore',
        'enable-local-file-access': True,  # Allow access to local files
        'minimum-font-size': '12' 

        # You can add more configuration options here
    }

#     config = {
#     'page-size': 'A4',  # Use the correct page size
#     'margin-top': '1in',
#     'margin-right': '1in',
#     'margin-bottom': '0in',
#     'margin-left': '1in',
#     'encoding': "UTF-8",
#     'dpi': 300,  # Higher DPI for better resolution
#     'custom-header': [('Accept-Encoding', 'gzip')],  # Improves style rendering
#     'enable-local-file-access': True,
#     'minimum-font-size': '10',  # Minimum font size
#     'print-media-type': True,  # Use print styles instead of screen styles
#     'zoom': 1.2  # Adjust scaling factor if styles are distorted
# }
    
    try:
        # Convert HTML to PDF
        pdfkit.from_file(input_html_path, output_pdf, options=config)
        print(f"Successfully converted {input_html} to {output_pdf}")
        return output_pdf
    except Exception as e:
        print(f"Error converting HTML to PDF: {e}")
        return None
    
def load_mapping(mapping_file):
    """
    Load db_to_placeholder_mapping from a JSON file.
    """
    with open(mapping_file, 'r') as file:
        return json.load(file)

def fetch_records(folder_name,mapping_file,batch_no):



    """
    Connects to the MySQL database and fetches all records from the `xyz` table.
    """

    db_to_placeholder_mapping = load_mapping(mapping_file)
    # db_to_placeholder_mapping = {
    #     "id": "Date of Notice",
    #     "owner_id": "Customer_Name",
    #     "position": "Customer_Email",
    #     "phone": "Loan_Account_No. / Credit_Card_Account_No.",
    #     "address1": "CRN",
    #     "customerid": "Loan_Accout_No. / Credit_Card_No.",
    #     "is_paid": "O/s Status Date (TOS / OD)",
    #     "sp_amount": "Current_EMI_O/s",
    #     "sp_product": "POS",
    #     "spoctoid": "Overdue_Amt",
    #     "minimum_amount_due": "CM_Name",
    #     "original_amount": "CM_MOB_No",
    #     "cm_email": "CM_Email",
    #     "kcc_mad_amount": "KCC_MAD_Amount",
    #     "tos": "TOS",
    #     "loan_amount": "Loan_Amount",
    #     "co_borrower_1": "Co-Borrower_Name_1",
    #     "co_borrower_2": "Co-Borrower_Name_2",
    #     "co_borrower_3": "Co-Borrower_Name_3",
    #     "co_borrower_4": "Co-Borrower_Name_4",
    #     "guarantor_1": "Guarantor_1",
    #     "guarantor_2": "Guarantor_2",
    #     "guarantor_3": "Guarantor_Name_3",
    #     "guarantor_4": "Guarantor_4.",
    #     "loan_agreement_date": "Loan_Agmt_Date",
    #     "first_installment": "1st installment",
    #     "last_installment": "Last Installment"
    # }


# bk1 dln 


    # db_to_placeholder_mapping = {
    #     "due_date": "Date of Notice",
    #     "firstname": "Customer_Name",
    #     "email": "Customer_Email",

    #     "sp_account_number": "Loan_Account_No. / Credit_Card_Account_No.",

    #     "zipcode": "CRN",
    #     "recommendation1": "Loan_Account_No. / Credit_Card_No.",

    #     "sp_date": "O/s Status Date (TOS / OD)",

    #     # "amount_due": "Current_EMI_O/s",
        
    #     "sp_principal_outstanding": "POS",

    #     "total_overdue": "Overdue_Amt",

    #     "flex_1": "CM_Name",
    #     "flex_2": "CM_MOB_No",
    #     "flex_3": "CM_Email",

    #     "min_partial_amount": "KCC_MAD_Amount",
    #     "total_payable_amount": "TOS",
    #     "amount_due": "Loan_Amount",
    #     "flex_4": "Co-Borrower_Name_1",
    #     "lastname": "Co-Borrower_Name_2",
    #     "flex_5": "Co-Borrower_Name_3",
    #     "co_borrower_4": "Co-Borrower_Name_4",
    #     "flex_6": "Guarantor_1",
    #     "flex_7": "Guarantor_2",
    #     "guarantor_3": "Guarantor_Name_3",
    #     "guarantor_4": "Guarantor_4.",
    #     "last_followup_date": "Loan_Agmt_Date",
    #     "minimum_amount_due": "1st installment",
    #     "payment_amount": "Last Installment",
    #     "address1":"Customer_Address_1",
    #     "state":"Customer_Address_2",
    #     "sp_product":"Product",
    #     "flex_8":"Co-Borrower_Name_1_Address_1",
    #     "country":"Co-Borrower_Name_2_Address_1",
    #     "city":"Co-Borrower_Name_3_Address_1",
    #     "recommendation2":"Guarantor_1_Address_1",
    #     "repeated_final_status":"Guarantor_2_Address_1",
    #     "bill_cycle":"Tenur"





    # }

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
        # cursor.execute("SELECT id,owner_id ,position,phone,address1,customerid,is_paid,sp_amount,sp_product,spoctoid,minimum_amount_due,original_amount   FROM sp_leads  WHERE company IS NOT NULL limit 1")
        batch_no = int(batch_no)
        cursor.execute("SELECT * FROM sp_leads where batch_no = %s AND sp_account_number IN ('0009406188000947477','0009406300001860787')  ",(batch_no,))


#         cursor.execute("""
#     SELECT id ,due_date, firstname, email, sp_account_number, customerid, 
#        recommendation1, payment_date, minimum_amount_due, 
#        sp_principal_outstanding, total_overdue, flex_1, flex_2, flex_3
# FROM sp_leads
# ORDER BY
#     (CASE WHEN due_date IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN firstname IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN email IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN sp_account_number IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN customerid IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN recommendation1 IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN payment_date IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN minimum_amount_due IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN sp_principal_outstanding IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN total_overdue IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN flex_1 IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN flex_2 IS NOT NULL THEN 1 ELSE 0 END +
#      CASE WHEN flex_3 IS NOT NULL THEN 1 ELSE 0 END) DESC
#     LIMIT 1
# """)
#         cursor.execute("""
#     SELECT id ,due_date, firstname, email, sp_account_number, customerid, 
#        recommendation1, payment_date, minimum_amount_due, 
#        sp_principal_outstanding, total_overdue, flex_1, flex_2, flex_3
# FROM sp_leads
# WHERE batch_no=9180
#     LIMIT 1
# """)
        

        

        column_names = [desc[0] for desc in cursor.description]

        records = cursor.fetchall()
        print(records)

        # Print all records
        # for record in records:
        #     a,b,c,d,e,f,g,h=record
        #     print(f"a: {a}, b: {b}, c: {c}")

        #     # print(record)

        # html_file_path = "Fol3/Fol3.html"

        html_file_path = f"{folder_name}/{folder_name}.html"

        
        

        with open(html_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()        


        for record in records:
            record_dict = dict(zip(column_names, record))

            placeholders = {placeholder: "xxx" for placeholder in db_to_placeholder_mapping.values()}

            # print(placeholders)

            # Populate placeholders using the mapping
            # for db_column, placeholder in db_to_placeholder_mapping.items():
            #     if db_column in record_dict:
            #         value = record_dict[db_column]
            #         # Convert datetime objects to strings
            #         if isinstance(value, datetime):
            #             if db_column in ["due_date", "sp_date"]:
            #                 value = value.date().strftime("%d/%m/%Y")  # Convert to DD/MM/YYYY
            #                 print(f"Formatted '{db_column}' to DD/MM/YYYY: {value}")
            #             else:
            #                 value = value.strftime("%Y-%m-%d")  # Default format
            #                 print(f"Converted {db_column} datetime to string: {value}")
            #         elif value is None:
            #             value = ""  # Handle None values by replacing with an empty string
            #         placeholders[placeholder] = value

            for db_column, placeholder in db_to_placeholder_mapping.items():
                if db_column in record_dict:
                    value = record_dict[db_column]
                    # Convert datetime objects to strings
                    if db_column in ["sp_date"]:
                        print("working")
                        print("sp_date : " , value)
                        print(type(value))
                        value=value.strftime("%d/%m/%Y")
                    # if db_column in ["amount_due"]:
                    #     value = int(value)
                    # if db_column in ["dpd"]:
                    #     value = int(value)
                    # if db_column in ["min_partial_amount"]:
                    #     value = int(value)
                    # placeholders[placeholder] = value
                    if db_column in ["amount_due", "dpd", "min_partial_amount"]:
                        if value is not None:
                            value = int(value)
                        else:
                            value = 0  # or continue
                    if value is not None:
                        placeholders[placeholder] = value
                    
                    
                    
                    


            # print(json.dumps(placeholders, indent=4))
            modified_html_content = modify_placeholders(html_content, placeholders)


            # with open("modified_file.html", "w", encoding="utf-8") as file:
            #     file.write(modified_html_content)

            file_name = f"{folder_name}/modified_file_{record_dict['id']}.html"
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(modified_html_content)
            print("All placeholders updated successfully!")

            input_html = f'{folder_name}/modified_file_{record_dict['id']}.html'

            pdf_path = html_to_pdf(input_html)
            if pdf_path:
                # remove_last_page(pdf_path)
                print(f"PDF saved at: {pdf_path}")
            




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
    if len(sys.argv) < 4:
        print("Usage: python script.py <folder_name> <mapping_file>")
        sys.exit(1)
    batch_no=sys.argv[1]
    mapping_file = sys.argv[2]
    folder_name = sys.argv[3]
    fetch_records(folder_name,mapping_file,batch_no)
