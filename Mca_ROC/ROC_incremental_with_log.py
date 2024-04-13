import os
import re
import sys
import time
import json
import requests
import traceback
import pandas as pd
import mysql.connector
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from config import mca_config
from urllib.parse import quote
from sqlalchemy import create_engine

db_host = '127.0.0.1'
db_user = 'root'
db_password = 'root'
db_name = 'dpiit_final'
table_name = 'mca_orders'

conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

conn1 = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

cursor = conn.cursor()

log_cursor = conn1.cursor()

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

current_date = datetime.now().strftime("%Y-%m-%d")

def current_date_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

log_list = [None] * 8

no_data_avaliable = 0

no_data_scraped = 0


# Create a Chrome webdriver instance


base_url = "https://www.mca.gov.in/bin/dms/searchDocList?page=1&perPage={}&sortField=Date&sortOrder=D&searchField=Title&searchKeyword=&startDate=&endDate=&filter=&dialog=%7B%22folder%22%3A%22441%22%2C%22language%22%3A%22English%22%2C%22totalColumns%22%3A3%2C%22columns%22%3A%5B%22Title%22%2C%22ROC%22%2C%22Date%22%5D%7D"


def get_data_count(cursor):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE type_of_order = 'ROC'")
    total_rows = cursor.fetchone()[0]
    return total_rows
    
data_in_database = get_data_count(cursor)
print("Total data in database",data_in_database)

def insert_log_into_table(log_cursor, log_list):
    query = """
        INSERT INTO mca_log (source_name, script_status, data_available, data_scraped, total_record_count, failure_reason, comments, source_status)
        VALUES (%(source_name)s, %(script_status)s, %(data_available)s, %(data_scraped)s, %(total_record_count)s, %(failure_reason)s, %(comments)s, %(source_status)s)
    """
    values = {
        'source_name': log_list[0] if log_list[0] else None,
        'script_status': log_list[1] if log_list[1] else None,
        'data_available': log_list[2] if log_list[2] else None,
        'data_scraped': log_list[3] if log_list[3] else None,
        'total_record_count': log_list[4] if log_list[4] else None,
        'failure_reason': log_list[5] if log_list[5] else None,
        'comments': log_list[6] if log_list[6] else None,
        'source_status': mca_config.source_status
    }

    log_cursor.execute(query, values)
    
def insert_into_database(excel_file_path):
    
    global log_list, data_in_database
    try:
        
        df = pd.read_excel(excel_file_path, sheet_name='Sheet1',engine='openpyxl')

        table_name = "mca_orders"
        
        df = df.where(pd.notnull(df), None)

        connection= mysql.connector.connect(
        host = '127.0.0.1',
        user = 'root',
        password = 'root',
        database = 'dpiit_final'
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

        print(f"Data has been successfully inserted into the '{table_name}' table in the database.")


        log_list[0] = "mca_roc"
        log_list[1] = " Success"
        log_list[2] = no_data_avaliable
        log_list[3] = get_data_count(log_cursor) - data_in_database  
        log_list[4] = get_data_count(log_cursor)
        insert_log_into_table(log_cursor, log_list)
        conn1.commit()
        log_list = [None] * 8

    except Exception as e:  
        traceback.print_exc()
        log_list[0] = "mca_roc"
        log_list[1] = " Failure"
        log_list[4] = get_data_count(log_cursor)
        log_list[5] = "script error"
        insert_log_into_table(log_cursor, log_list)
        print(log_list)
        conn1.commit()
        log_list = [None] * 8
        sys.exit("script error")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

# def download_pdf_files(excel_file_path, download_folder="downloaded_documents\ROC"):
    
    
#     global log_list
    
#     try:
#         # Create the download folder if it doesn't exist
#         if not os.path.exists(download_folder):
#             os.makedirs(download_folder)

#         # Read the Excel file to get the links
#         df = pd.read_excel(excel_file_path)
#         links = df['link_to_order']

#         # Custom headers
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }

#         # Loop through each row in the DataFrame
#         for index, link in enumerate(links, start=1):
#             try:
#                 # Make a request to download the document with User-Agent header
#                 response = requests.get(link, headers=headers)

#                 if response.status_code == 200:
#                     content_disposition = response.headers.get('content-disposition')

#                     if content_disposition:
#                         match = re.search(r'filename="(.+)"', content_disposition)
#                         if match:
#                             original_filename = match.group(1)
#                         else:
#                             original_filename = f"document_{index}.pdf"
#                     else:
#                         original_filename = f"document_{index}.pdf"

#                     # Ensure the file extension is PDF
#                     if not original_filename.lower().endswith('.pdf'):
#                         original_filename += '.pdf'
#                     day, month, year = map(int, df.at[index - 1, 'date_of_order'].split('-'))
#                     month_name = datetime(year, month, day).strftime('%B')
#                     year_folder = str(year)
#                     month_year_folder = os.path.join(year_folder, month_name)
#                     file_folder = os.path.join(download_folder, month_year_folder)
#                     if not os.path.exists(file_folder):
#                         os.makedirs(file_folder)
 
#                     # Save the document in the new folder with the original filenam
#                     # Save the document in the new folder with the original filename
#                     file_name = os.path.join(file_folder, original_filename)
#                     with open(file_name, 'wb') as file:
#                         file.write(response.content)

#                     # Update DataFrame with file name and path
#                     pdf_file_name = os.path.splitext(original_filename)[0]  # Extract file name without extension
#                     df.at[index-1, 'pdf_file_name'] = pdf_file_name  # Indexing in DataFrame is 0-based
#                     df.at[index-1, 'pdf_file_path'] = file_name

#                     # Print status
#                     print(f"Document {index}/{len(links)} downloaded successfully: {file_name}")
#                 else:
#                     print(f"Failed to download file {index}/{len(links)} from link: {link}")
#             except Exception as e:
#                 print(f"An error occurred while downloading file {index}/{len(links)}: {str(e)}")
#                 traceback.print_exc()
#                 log_list[0] = "mca_roc"
#                 log_list[1] = " Failure"
#                 log_list[4] = get_data_count(log_cursor)
#                 log_list[5] = "script error"
#                 insert_log_into_table(log_cursor, log_list)
#                 print(log_list)
#                 conn1.commit()
#                 log_list = [None] * 8
#                 sys.exit("script error")

#         # Save the updated DataFrame back to the Excel file
#         df.to_excel(excel_file_path, index=False)
#         insert_into_database(excel_file_path)
#         print("Excel file updated with pdf_file_name and pdf_file_path columns.")
#     except Exception as e:
#         traceback.print_exc()
#         log_list[0] = "mca_roc"
#         log_list[1] = " Failure"
#         log_list[4] = get_data_count(log_cursor)
#         log_list[5] = "script error"
#         insert_log_into_table(log_cursor, log_list)
#         print(log_list)
#         conn1.commit()
#         log_list = [None] * 8
#         sys.exit("script error")  
def download_pdf_files(excel_file_path, download_folder="downloaded_documents\ROC"):
    global log_list
    
    try:
        # Create the download folder if it doesn't exist
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Read the Excel file to get the links
        df = pd.read_excel(excel_file_path)
        links = df['link_to_order']

        # Custom headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Loop through each row in the DataFrame
        for index, link in enumerate(links, start=1):
            try:
                # Make a request to download the document with User-Agent header
                response = requests.get(link, headers=headers)

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
                    day, month, year = map(int, df.at[index - 1, 'date_of_order'].split('-'))
                    month_name = datetime(year, month, day).strftime('%B')
                    year_folder = str(year)
                    month_year_folder = os.path.join(year_folder, month_name)
                    file_folder = os.path.join(download_folder, month_year_folder)
                    if not os.path.exists(file_folder):
                        os.makedirs(file_folder)

                    # Check for existing files and create a unique filename if necessary
                    base_filename, extension = os.path.splitext(original_filename)
                    unique_filename = original_filename
                    counter = 1
                    while os.path.exists(os.path.join(file_folder, unique_filename)):
                        unique_filename = f"{base_filename}({counter}){extension}"
                        counter += 1

                    # Save the document in the new folder with the unique filename
                    file_name = os.path.join(file_folder, unique_filename)
                    with open(file_name, 'wb') as file:
                        file.write(response.content)

                    # Update DataFrame with file name and path
                    pdf_file_name = os.path.splitext(unique_filename)[0]  # Extract file name without extension
                    df.at[index-1, 'pdf_file_name'] = pdf_file_name  # Indexing in DataFrame is 0-based
                    df.at[index-1, 'pdf_file_path'] = file_name

                    # Print status
                    print(f"Document {index}/{len(links)} downloaded successfully: {file_name}")
                else:
                    print(f"Failed to download file {index}/{len(links)} from link: {link}")
            except Exception as e:
                print(f"An error occurred while downloading file {index}/{len(links)}: {str(e)}")
                traceback.print_exc()
                log_list[0] = "mca_roc"
                log_list[1] = " Failure"
                log_list[4] = get_data_count(log_cursor)
                log_list[5] = "script error"
                insert_log_into_table(log_cursor, log_list)
                print(log_list)
                conn1.commit()
                log_list = [None] * 8
                sys.exit("script error")

        # Save the updated DataFrame back to the Excel file
        df.to_excel(excel_file_path, index=False)
        insert_into_database(excel_file_path)
        print("Excel file updated with pdf_file_name and pdf_file_path columns.")
    except Exception as e:
        traceback.print_exc()
        log_list[0] = "mca_roc"
        log_list[1] = " Failure"
        log_list[4] = get_data_count(log_cursor)
        log_list[5] = "script error"
        insert_log_into_table(log_cursor, log_list)
        print(log_list)
        conn1.commit()
        log_list = [None] * 8
        sys.exit("script error") 

def add_new_data_to_database( excel_file_path, db_table_name):
    
    
    global log_list
    
    try:
        database_uri = f'mysql://{db_user}:{db_password}@{db_host}/{db_name}'
        engine = create_engine(database_uri)

        columns_to_select = ['title_of_order','type_of_order', 'ROC_RD_LOCATION', 'date_of_order','link_to_order']
        select_query = f"SELECT {', '.join(columns_to_select)} FROM {db_table_name};"
        database_table_df = pd.read_sql(select_query, con=engine)

        excel_data_df = pd.read_excel(excel_file_path)

        merged_df = pd.merge(excel_data_df, database_table_df, how='left', indicator=True)
        missing_rows = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

        if not missing_rows.empty:
            print("Rows from Excel Data not in Database Table")
            print(missing_rows)

            # Save missing rows to a new Excel sheet with the current date as the filename
            current_date = datetime.now().strftime("%Y-%m-%d")
            new_excel_file_path = rf"C:\Users\magudapathy.7409\Desktop\MCA\NEW_ROC\incremental_excel_sheets\Missing_Data_{current_date}.xlsx"
            missing_rows.to_excel(new_excel_file_path, index=False)
            print(f"Missing rows saved to {new_excel_file_path}")
            excel_data = pd.read_excel(new_excel_file_path)
            df = pd.DataFrame(excel_data)
            download_pdf_files(new_excel_file_path)
            
            # Insert missing rows into the database
            # missing_rows.to_sql(db_table_name, con=engine, if_exists='append', index=False)
            # print(df,"Missing rows inserted into new excel file")

    except Exception as e:
        traceback.print_exc()
        log_list[0] = "mca_roc"
        log_list[1] = " Failure"
        log_list[4] = get_data_count(log_cursor)
        log_list[5] = "script error"
        insert_log_into_table(log_cursor, log_list)
        print(log_list)
        conn1.commit()
        log_list = [None] * 8
        sys.exit("script error")

def extract_json_excel():
    global log_list
    
    try:
        # Specify the path to your JSON file in ".txt" format
        json_file_path = r"C:\Users\magudapathy.7409\Desktop\MCA\NEW_ROC\webpage.txt"

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
        excel_file_path = r"C:\Users\magudapathy.7409\Desktop\MCA\NEW_ROC\output.xlsx"
        table_name = "mca_orders"

        # Download PDF files
        add_new_data_to_database(excel_file_path,table_name) # to compare the database table and incremental excel sheet
    except Exception as e :
        traceback.print_exc()
        log_list[0] = "mca_roc"
        log_list[1] = " Failure"
        log_list[4] = get_data_count(log_cursor)
        log_list[5] = "script error"
        insert_log_into_table(log_cursor, log_list)
        print(log_list)
        conn1.commit()
        log_list = [None] * 8
        sys.exit("script error")

def compare_db_and_excel_to_find_incremental():
    
    global log_list, no_data_avaliable
    
    
    try:
    
        chrome_options = webdriver.ChromeOptions()
        
        browser = webdriver.Chrome(options=chrome_options)
        
        browser.get(base_url.format(10))  # Default perPage value is set to 5
        time.sleep(5)

        # Get the page source
        page_source = browser.page_source

        # Close the browser
        browser.quit()

        # Extract JSON data from HTML using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        json_data = soup.find('pre').text
    
    except Exception as e :
        traceback.print_exc()
        log_list[0] = "mca_roc"
        log_list[1] = " Failure"
        log_list[4] = get_data_count(log_cursor)
        log_list[5] = "404 error"
        insert_log_into_table(log_cursor, log_list)
        print(log_list)
        conn1.commit()
        log_list = [None] * 8
        sys.exit("script error")
    

    # Save the extracted JSON data to a text file
    with open("webpage.txt", "w", encoding="utf-8") as file:
        file.write(json_data)

    # Read the JSON data from the file
    with open("webpage.txt", "r", encoding="utf-8") as file:
        json_data = file.read()

    # Parse the JSON data
    data = json.loads(json_data)

    # Extract and print the count associated with 'totalResults' key
    total_results_count = data.get('totalResults', 0)
    print(f'The totalResults count is: {total_results_count}')

    # Get the total count of rows in the table
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE type_of_order = 'ROC'")
    total_rows = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    print(f'The total number of rows in {table_name} table is: {total_rows}')
    result_dict = {'total_rows': total_rows}

    # Check if the total number of rows in the table is less than totalResults count
    if total_rows < total_results_count:
        
        no_data_avaliable = total_results_count - total_rows
        print("Updating URL with totalResults count...")
        
        # Update the URL with the totalResults count
        updated_url = base_url.format(total_results_count)
        try:
            # Use the updated URL to fetch JSON data
            browser = webdriver.Chrome(options=chrome_options)
            browser.get(updated_url)
            time.sleep(5)
            
            # Get the page source
            updated_page_source = browser.page_source
            
            # Close the browser
            browser.quit()
        except Exception as e :
            traceback.print_exc()
            log_list[0] = "mca_roc"
            log_list[1] = " Failure"
            log_list[4] = get_data_count(log_cursor)
            log_list[5] = "404 error"
            insert_log_into_table(log_cursor, log_list)
            print(log_list)
            conn1.commit()
            log_list = [None] * 8
            sys.exit("script error")
            
        # Extract JSON data from the updated HTML
        updated_soup = BeautifulSoup(updated_page_source, 'html.parser')
        updated_json_data = updated_soup.find('pre').text
        
        # Save the updated JSON data to a text file
        with open("webpage.txt", "w", encoding="utf-8") as file:
            file.write(updated_json_data)
        
        print("Updated JSON data saved to webpage.txt")

        extract_json_excel()
        
    else:
        print("no new data found")
        log_list[0] = "mca_roc"
        log_list[1] = " Success"
        log_list[4] = get_data_count(log_cursor)
        log_list[6] = "no new data found"
        insert_log_into_table(log_cursor, log_list)
        print(log_list)
        conn1.commit()
        log_list = [None] * 8
        sys.exit("there is no new data")
        
        
        
if mca_config.source_status == "Active":
    compare_db_and_excel_to_find_incremental()
elif mca_config.source_status == "Hibernate":
    log_list[0] = "mca_roc"
    log_list[1] = " not run"
    log_list[4] = get_data_count(log_cursor)
    insert_log_into_table(log_cursor, log_list)
    conn1.commit()
    log_list = [None] * 8
    sys.exit("there is no new data")
elif mca_config.source_status == "Inactive":
    log_list[0] = "mca_roc"
    log_list[1] = " not run"
    log_list[4] = get_data_count(log_cursor)
    insert_log_into_table(log_cursor, log_list)
    conn1.commit()
    log_list = [None] * 8
    sys.exit("there is no new data")
