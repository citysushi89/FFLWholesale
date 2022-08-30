import csv
import json

# Combine CSVs
from functions import combine_user_csvs
wholesalers_to_combine = ['MGE Wholesale', 'Chattanooga Shooting', 'Second Amendment Wholesale', 'Orion Wholesale', 'Zanders', ]
# combine_user_csvs(wholesalers_to_combine)

path_to_csv = r'C:\Users\Owen\Documents\Personal Info\Independent Courses\Python Learning\fflwholesalerproductpps\Data\Users\1\wholesaler_data25Aug22.csv'
path_to_json = 'data.json'

def csv_to_json(path_to_csv, path_to_json):
    jsonArray = []

    # Read CSV
    with open(path_to_csv, encoding='utf-8') as csvf:
        # load csv file data using dict reader
        csvReader = csv.DictReader(csvf)

        # Convert each row into a python dict
        for row in csvReader:
            jsonArray.append(row)
    
    # Convert python jsonArray to JSON String and write to file
    with open(path_to_json, 'w', encoding='utf-8') as jsonf:
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

csv_to_json(path_to_csv, path_to_json)