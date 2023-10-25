import csv
import re

# Read the original text file and create a new CSV file
with open("GroceryStoreDataset-master/dataset/classes_modified.csv", "r") as infile, open("postprocessed_grocery_data.csv", "w", newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile, delimiter=';')  # Change delimiter to ';'
    
    # Write the header to the new CSV file
    writer.writerow(['name', 'family', 'title', 'description'])

    # Process each line from the original text file
    for row in reader:
        name, name_id, family, family_id, img_path, info_path = row
        if info_path[:15] == 'Product Informa': continue
        
        # Read the information file
        with open('GroceryStoreDataset-master/dataset' + info_path, 'r') as infofile:
            # Read the first line and split to get the title
            title_line = infofile.readline().strip()
            title = title_line.split(":")[1].strip() if ":" in title_line else "Not_Found"

            # Read the rest of the file as description
            information = infofile.read().strip().replace('\n', '')
            information = information.replace(';', ',')
            information = re.sub(r'http\S+|www\S+', '', information)
            information = re.sub(r'(?i)Url:', '', information).strip()

        # Write to the new CSV file
        writer.writerow([name, family, title, information])  # Using 'Not_Found' for country as it wasn't clear where it's sourced from
