# # Open the file in write mode
with open("example.txt", "w") as file:
    file.write("This is an example file.\n")
    file.write("It contains some text.\n")
    file.write("We'll use it to demonstrate file handling in Python.\n")
    
with open("task.txt", "w") as task:
    task.write("This is an example file.\n")
    # file.write("It contains some text.\n")
    # file.write("We'll use it to demonstrate file handling in Python.\n")
    
    
import pandas as pd

data = [{
    "message": "This is an example JSON file.",
    "description": "It contains some sample data.",
    "tags": ["json", "example", "python"],
    "test" : "testing"
}, 
{
    "message": "Another JSON file.",
    "description": "Some sample data.",
    "tags": ["python"]
}]


# Display the full DataFrame
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
# Write the DataFrame to an Excel file

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(data)
# print("df====\n", df)

# Print the DataFrames with each row on a new line
print(df.to_string(index=False, header=True))

print('\n') 

# Rename the "message" column to "firstdata"
df.rename(columns={"message": "firstdata"}, inplace=True)
# print("df rename column====\n", df)


print('\n')  # Empty line for separation
print(df.to_string(index=False, header=True))



df.to_excel("secondxlssss.xlsx", index=False)

print("Excel file  has been created.")







# import pandas as pd

data = {
    "message": "This is an example JSON file.",
    "description": "It contains some sample data.",
    "tags": "json",
    "test" : "testing"
}



# Display the full DataFrame
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', None)
# Write the DataFrame to an Excel file

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame([data])
# print("df====\n", df)

# Print the DataFrames with each row on a new line
print(df.to_string(index=False, header=True))

print('\n') 

# Rename the "message" column to "firstdata"
df.rename(columns={"message": "firstdata"}, inplace=True)
# print("df rename column====\n", df)


print('\n')  # Empty line for separation
print(df.to_string(index=False, header=True))



df.to_excel("xlss.xlsx", index=False)

print("Excel file  has been created.")



div_details    = [{'IEC Number': '0301014175', 'IEC Issuance Date': '19/06/2001', 'IEC Status': 'Cancelled', 'DEL Status': 'N', 'IEC Cancelled Date': '', 'IEC Suspended Date': '', 'File Number': '030413182678AM17', 'File Date': '10/08/2016', 'DGFT RA Office': 'RA MUMBAI', 'Nature of concern/Firm': 'Private Limited', 'Category of Exporters': 'Service Provider', 'Firm Name': 'ACCENTURE SERVICES PVT. LTD.', 'Address': 'PLANT 3 GODREJ & BOYCE COMPLEX ,\xa0\n\t\t\t\t\tLBS MARG VIKHROLI WEST Contact No: 919820934702 ,\xa0\n\t\t\t\t\tMUMBAI , \xa0MUMBAI ,\xa0\n\t\t\t\t\tMAHARASHTRA,\xa0\t400079'}]
details    = {'IEC Number': '0301014175', 'IEC Issuance Date': '19/06/2001', 'IEC Status': 'Cancelled', 'DEL Status': 'N', 'IEC Cancelled Date': '', 'IEC Suspended Date': '', 'File Number': '030413182678AM17', 'File Date': '10/08/2016', 'DGFT RA Office': 'RA MUMBAI', 'Nature of concern/Firm': 'Private Limited', 'Category of Exporters': 'Service Provider', 'Firm Name': 'ACCENTURE SERVICES PVT. LTD.', 'Address': 'PLANT 3 GODREJ & BOYCE COMPLEX ,\xa0\n\t\t\t\t\tLBS MARG VIKHROLI WEST Contact No: 919820934702 ,\xa0\n\t\t\t\t\tMUMBAI , \xa0MUMBAI ,\xa0\n\t\t\t\t\tMAHARASHTRA,\xa0\t400079'}


new_row = {
    
   
    'IEC Issuance Date': div_details[0].get('IEC Issuance Date', 'NULL'),
    'IEC Status': div_details[0].get('IEC Status', 'NULL'),
    'DEL Status': div_details[0].get('DEL Status', 'NULL'), 
    'IEC Cancelled Date': div_details[0].get('IEC Cancelled Date', 'NULL'),
    'IEC Suspended Date': details.get('IEC Suspended Date',''),
   
}

print("new_row====", new_row)

df = pd.DataFrame([new_row])
# print("df====\n", df)

# Print the DataFrames with each row on a new line
print(df.to_string(index=False, header=True))
