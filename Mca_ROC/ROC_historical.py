import pandas as pd
import json
from urllib.parse import quote
import requests
import os
import re
from sqlalchemy import create_engine
from datetime import datetime
import mysql.connector


def extract_json_excel():
    # Specify the path to your JSON file in ".txt" format
    json_file_path = r"C:\Users\stagadmin\Mca_ROC\webpage.txt"

    # Read JSON data from the file
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    # Extract the "documentDetails" value and convert it to a list
    document_details_str = json_data.get("documentDetails", "[]")
    document_details_list = json.loads(document_details_str)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(document_details_list).fillna('')

    # Select only the desired columns
    selected_columns = ['column1', 'column2', 'docDate', 'docID']
    df = df[selected_columns]

    # Rename the columns
    df = df.rename(columns={
        'column1': 'title_of_order',
        'column2': 'ROC_RD_LOCATION',
        'docDate': 'date_of_order',
        'docID': 'Encoded_Id'
    })

    # Add a new column named "Type" with the value "ROC"
    df['type_of_order'] = 'ROC'
    df['updated_date'] = None

    # Rearrange the columns to place "Type" after "File_name"
    df = df[['title_of_order', 'type_of_order', 'ROC_RD_LOCATION', 'date_of_order', 'Encoded_Id','updated_date']]

    # Create the 'link' column
    df['link_to_order'] = df['Encoded_Id'].apply(lambda x: f"https://www.mca.gov.in/bin/dms/getdocument?mds={quote(x)}&type=open")

    # Specify the Excel file name
    excel_file_name = "output.xlsx"

    # Write the DataFrame to an Excel file
    df.to_excel(excel_file_name, index=False)

    print(f"Data has been successfully written to {excel_file_name}")

    # Create a new folder for saving files
    output_folder = 'downloaded_documents\ROC'
    os.makedirs(output_folder, exist_ok=True)

    # User-Agent header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        download_url = row['link_to_order']
        
        # Make a request to download the document with User-Agent header
        response = requests.get(download_url, headers=headers)
        
        if response.status_code == 200:
            content_disposition = response.headers.get('content-disposition')
            
            if content_disposition:
                match = re.search(r'filename="(.+)"', content_disposition)
                if match:
                    original_filename = match.group(1)
                else:
                    original_filename = f"document_{index}.pdf"
            else:
                original_filename = f"document_{index}.pdf"

            # Ensure the file extension is PDF
            if not original_filename.lower().endswith('.pdf'):
                original_filename += '.pdf'

            # Get the month and year from the 'date_of_order' column
            day, month, year = map(int, row['date_of_order'].split('-'))
            month_name = datetime(year, month, day).strftime('%B')
            year_folder = str(year)
            month_year_folder = os.path.join(year_folder, month_name)

            # Save the document in the new folder with a unique filename
            base_filename, extension = os.path.splitext(original_filename)
            unique_filename = original_filename
            counter = 1
            while os.path.exists(os.path.join(output_folder, month_year_folder, unique_filename)):
                unique_filename = f"{base_filename}({counter}){extension}"
                counter += 1

            file_folder = os.path.join(output_folder, month_year_folder)
            os.makedirs(file_folder, exist_ok=True)
            file_name = os.path.join(file_folder, unique_filename)
            with open(file_name, 'wb') as file:
                file.write(response.content)
            
            # Split the unique file name and add it to the 'pdf_file_name' column
            pdf_file_name = os.path.splitext(unique_filename)[0]  # Extract file name without extension
            df.at[index, 'pdf_file_name'] = pdf_file_name
            
            # Update the 'file_path' column with the exact download path
            df.at[index, 'pdf_file_path'] = file_name
            
            print(f"Document {index + 1}/{len(df)} downloaded: {file_name}")
        else:
            print(f"Failed to download document {index + 1}. Status code: {response.status_code}")

    # Update the Excel file with the 'pdf_file_name' column
    df.to_excel(excel_file_name, index=False)

    print("Download complete. All files are saved in the 'downloaded_documents' folder")




def insert_excel_data_to_mysql():

    try:
        excel_file_name = r"C:\Users\stagadmin\Mca_ROC\Historical_main.xlsx"

    # Read the Excel file into a DataFrame
        df = pd.read_excel(excel_file_name, sheet_name='Sheet1',engine='openpyxl')

        table_name = "mca_orders"
        
        df = df.where(pd.notnull(df), None)


    # Database connection parameters
        connection= mysql.connector.connect(
        host = 'localhost',
        user = 'root1',
        password = 'Mysql1234$',
        database = 'mca'
        )
        cursor=connection.cursor()
      
        for index, row in df.iterrows():
            insert_query = f"""
                INSERT INTO {table_name} (title_of_order, type_of_order, ROC_RD_LOCATION, date_of_order, link_to_order, pdf_file_path,pdf_file_name)
                VALUES (%s, %s, %s, %s, %s, %s,%s)
            """
           
            values = (row['title_of_order'], row['type_of_order'], row['ROC_RD_LOCATION'], row['date_of_order'], row['link_to_order'], row['pdf_file_path'],row['pdf_file_name'])

         
            cursor.execute(insert_query, values)
        connection.commit()
        cursor.close()
    except Exception as e:
        print(e)
# extract_json_excel()
insert_excel_data_to_mysql()