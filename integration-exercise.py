import csv
import requests
import pandas as pd
from datetime import datetime
import json
import argparse
s3_bucket = "cityhive-stores"
region = "us-west-2"
object_key = "/_utils/inventory_export_sample_exercise.csv"
# Add the code that will make a GET request to Amazon's S3 with the details above
# and download the file in a local location.

# make the path to the local file
local_file_path = "inventory_export_sample_exercise.csv"
# make the path to the output processed file
output_file_path = "processed_inventory.csv"
# make the web path to the bucket location using the provided details 
s3_url = fr'https://{s3_bucket}.s3.{region}.amazonaws.com{object_key}'
def getmargin(p,c):
    try:
        #remove leading/trailing spaces on trings
        price = str(p).strip()
        cost = str(c).strip()
        # if they are not null then
        if price and cost:
            #convert to float
            cost = float(cost)
            price = float(price)
            # if divide by zero assuming to increase price by 0.09
            if cost != 0:
                margin =  ((price-cost)/cost)
            else: 
                margin = 0
            if margin >= 0.3:
                price_increase = round(price + (price * 0.07 ),2)
                lo_hi_margin = 'high_margin'
            else:
                price_increase = round(price + (price * 0.09 ),2)
                lo_hi_margin = 'low_margin'
        else:
            price_increase = round(0,2)
        return price_increase,lo_hi_margin
    #if there is an error return the price
    except ValueError:
        return p
        
def process_line(idx,line,dupe):
  if len(line) > 10:
    try:
        date = datetime.strptime(line[40].strip(),"%Y-%m-%d %H:%M:%S.%f").year
    except:
        date = None
    if date == 2020:
        # if upc is not a number or is not a number with a length > 5 then follow # 4
        # values made for #4
        tags = []
        if line[0].isdigit() and len(line[0]) > 5:
            upc = line[0]
            id = None
            if line[0] in dupe:
                tags.append('duplicate_sku')
        else:
            upc = None
            id = f'biz_id_{idx}'
        # create properties JSON for #8 
        properties = {
            'department':line[13].strip(), #assuming column 13
            'vendor':line[12].strip(), #assuming column 12
            'description':line[143].strip() #assuming column 143 , 142 has alot of nulls
                    }
        
        newprice,lo_hi_margin = getmargin(line[4],line[3])
        tags.append(lo_hi_margin)
        return {
            'upc': upc,
            'price':newprice , # previously line[4] with price increase.
            'quantity': line[5],
            'department': line[13], # line[13] is DeptId
            'internal_id':id, #id none if criteria met else biz_id_{idx}
            'name' : f'{line[1]} {line[36]}',#assuming that ItemName and ItemName_Extra are the two columns
            'properties' : json.dumps(properties), # add JSON of properties for #8
            'tags' : tags #assuming list of 2 tags, duplicate and high/low margin

              }
def check_duplicate(reader):
    seen,dupe = set(),set()
    #check for dupes
    for line in reader:
        if line:
            item_num = line[0].strip()
            if item_num in seen:
                dupe.add(item_num)
            else:
                seen.add(item_num)    
    return dupe
def generate_csv():
    try:
        response = requests.get(s3_url, stream=True)
        response.raise_for_status()
        
        # download and save the file. 
        with open(local_file_path,"wb") as file:
            file.write(response.content)
        with open(local_file_path,"r") as in_file:
            reader = csv.reader(in_file, delimiter='|')
            duplicates = check_duplicate(reader)
        with open(local_file_path,"r") as in_file, open(output_file_path, "w", newline='') as out_file:
            reader = csv.reader(in_file, delimiter='|')
            writer = csv.DictWriter(out_file, fieldnames=["upc", "price", "quantity", "internal_id", "department", "name", "properties", "tags"])
            writer.writeheader()  # Write header to the output file
            for idx,line in enumerate(reader):
                l = process_line(idx,line,duplicates)
                if l: 
                    #print(l)
                    writer.writerow(l) # write the row to a csv
    except requests.exceptions.RequestException as e:
       print(f"Error downloading :{e}")
# A function to search for column index's 
def find_column(string):
    df = pd.read_csv(local_file_path,delimiter='|')
    i = 0
    for x in df.columns:
        if string in x:
            print(f'{x} on index {i}')
        i+=1
# Run the function
def upload():
    API_URL = "http://127.0.0.1:3000/inventory_uploads.json"
    df = pd.read_csv("processed_inventory.csv")

    # Convert DataFrame to a proper JSON array
    inventory_data = json.loads(df.to_json(orient="records"))

    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, json=inventory_data, headers=headers)

    if response.status_code == 201:
        print("Data uploaded successfully.")
    else:
        print(f"Failed to upload data. Status code: {response.status_code}, Response: {response.text}")

def list_uploads():
    API_URL = "http://127.0.0.1:3000/inventory_uploads.json"
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        print("Inventory Uploads:")
        print(json.dumps(data, indent=4)) 
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description="Process inventory data.")
    parser.add_argument("action", choices=["generate_csv", "upload", "list_uploads"],
                        help="Action to perform: 'generate_csv', 'upload', or 'list_uploads'")
    
    args = parser.parse_args()
    
    if args.action == "generate_csv":
        generate_csv()
    elif args.action == "upload":
        upload()
    elif args.action == "list_uploads":
        list_uploads()
if __name__ == "__main__":
    # generate_csv()
    # upload()
    # list_uploads()
    main()
    #find_column('Desc') # function to locate columns
    print("Finished!")