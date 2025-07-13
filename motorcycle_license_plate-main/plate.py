import requests
from pprint import pprint
import os
import time
import re

regions = ['in']  # Change to your country
recognized_plates = set()

def recognize_plate(image_path):
    with open(image_path, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=fp),
            headers={'Authorization': 'Token}
        )
    
    # Check if the response is successful
    
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            plate_number = data['results'][0]['plate']
            return plate_number.upper()  # Convert to uppercase
        else:
            print(f"No plate detected in {image_path}.")
            return None

def process_number_plate_folder():
    for filename in os.listdir('number_plates'):
        if filename.lower().endswith(('.jpg')):
            image_path = os.path.join('number_plates', filename)
            print(f"Processing {image_path}...")
            plate_number = recognize_plate(image_path)
            if plate_number:
                recognized_plates.add(plate_number)
            time.sleep(1) 

# Print all recognized license plates
