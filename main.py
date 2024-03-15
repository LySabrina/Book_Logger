# import numpy as np
# import cv2 as cv
import gspread
from google.oauth2.service_account import Credentials
import barcode
import config
import sys
import os

args = sys.argv

def updateSheetWithBook(book):
    worksheet1 = config.getWorksheet()
    if(worksheet1 is not None and book is not None):
        rows_filled = len(worksheet1.get_all_values())
        worksheet1.update_cell(rows_filled+1, 1, f'=IMAGE("{book.get("thumbnail")}")')
        worksheet1.update_cell(rows_filled+1, 2, book["title"])
        worksheet1.update_cell(rows_filled+1, 3, book["price"])

def readBooks(folder_path):
    book_list = []
    try:
        files = os.listdir(folder_path)
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(folder_path, file)
                bookInfo = barcode.findBook(file_path)
                print("Appending - " + file_path)
                book_list.append(bookInfo)
            else:
                print("FILE DID NOT END WITH EITHER: .png, .jpg, .jpeg")
        return book_list
    
    except FileNotFoundError:
        sys.exit("FOLDER PATH CANNOT BE FOUND")
        
    

if len(args) != 2:
    sys.exit("Must have at least the folder path of your book images to be scanned")

book_list = readBooks(args[1])

for book in book_list:
    updateSheetWithBook(book)







# img = cv.imread("./game4.jpg")
# # print(img.shape)
# # shape is x, y, channel for images
# # channel = BGR = 0 = blue, 1 = green, 2 = red
# barcode = cv.barcode.BarcodeDetector()
# isbn = barcode.detectAndDecode(img)[0]
# print(isbn)