import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import requests
from bs4 import BeautifulSoup
import json
import sqlite3


# Define a function to capture video from your camera and process each frame
def scan_barcodes():
    cap = cv2.VideoCapture(0)  # 0 means the default camera on your device
    font = cv2.FONT_HERSHEY_PLAIN
    barcode_data = None  # Create a variable to store the decoded barcode data
    while barcode_data is None:  # Keep scanning until a barcode is successfully decoded
        _, frame = cap.read()  # Read each frame from the camera
        decoded_objects = pyzbar.decode(frame)  # Decode any barcodes in the frame
        for obj in decoded_objects:
            # Draw a rectangle around the barcode and display its data
            cv2.rectangle(frame, (obj.rect.left, obj.rect.top),
                          (obj.rect.left + obj.rect.width, obj.rect.top + obj.rect.height), (255, 0, 0), 2)
            cv2.putText(frame, str(obj.data.decode('utf-8')), (obj.rect.left, obj.rect.top), font, 2, (255, 255, 255),
                        2, cv2.LINE_AA)
            barcode_data = obj.data.decode('utf-8')  # Save the decoded data to the variable
        # Display the processed frame
        cv2.imshow("Barcode Scanner", frame)
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return barcode_data  # Return the decoded barcode data`


# Call the function to start scanning barcodes and save the result to a variable
# barcode_result = scan_barcodes()
# print(barcode_result)   # Print the decoded barcode data

# Website to use for searching barcode values
def get_price(barcode_result):
    url = "https://api.barcodespider.com/v1/lookup"
    querystring = {"upc": barcode_result}

    headers = {
        'token': "d970f9f75b5fb1d6c3a5",
        'Host': "api.barcodespider.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    price = response.text

    data_dict = json.loads(price)
    try: 
        # Extract the price from the dictionary
        price = data_dict['Stores'][0]['price']
        name = data_dict['item_attributes']['title']

        print(f"The name of item is {name}")
    
        return price, name
    except KeyError: 
        return None, None


# print(get_price(barcode_result))

# price, name = get_price(barcode_result)


def create_database():
    # Prompt the user for a database name
    dbname = 'barcode_data'

    # Create a connection to the database
    conn = sqlite3.connect(dbname + ".db")

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table with three columns
    cursor.execute('''CREATE TABLE products
                      (UPC TEXT PRIMARY KEY,
                       Name TEXT,
                       Price REAL
                       Category TEXT)''')

    # Commit the table creation
    conn.commit()

    # Close the connection
    conn.close()

    print(f"Database {dbname}.db created with table 'products' containing columns 'UPC', 'Name', 'Price' and 'Category'.")


# create_database()


def update_database(name, barcode, price, category):
    conn = sqlite3.connect("barcode_data.db")

    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute("INSERT INTO barcode_data (UPC, Name, Price, Category) VALUES (?, ?, ?, ?)", 
                   (barcode, name, price, category))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
    return

# update_database(sql_name,name, barcode_result, price)


if __name__ == "__main__": 
    pass

