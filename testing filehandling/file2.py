

import pandas as pd
import json

# Create the nested dictionary
nested_data = {
    'dict1': {
        'message': 'This is an example JSON file.',
        'description': 'It contains some sample data.',
        'tags': ['json', 'example', 'python'],
        'test': 'testing'
    },
    'dict2': {
        'message': 'Another JSON file.',
        'description': 'Some sample data.',
        'tags': ['python']
    }
}

# Create a list of dictionaries from the nested dictionary
data = [
    {
        'dict1': json.dumps(nested_data['dict1']),
        'dict2': json.dumps(nested_data['dict2'])
    }
]

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)

# Print the DataFrames with each row on a new line
print(df.to_string(index=False, header=True))

# Write the DataFrame to an Excel file
df.to_excel('output10.xlsx', index=False)




# import pandas as pd

# # Nested dictionary
# nested_data = {
#     "persons": [
#         {"name": "Alice", "age": 25, "city": "New York"},
#         {"name": "Bob", "age": 32, "city": "London"},
#         {"name": "Charlie", "age": 28, "city": "Paris"}
#     ]
# }

# # Flatten the nested dictionary
# data = nested_data["persons"]
# print("data====", data)

# # Create a DataFrame from the list of dictionaries
# df = pd.DataFrame(data)

# print("df====", df)

# # Write the DataFrame to an Excel file
# df.to_excel("output2.xlsx", index=False)












