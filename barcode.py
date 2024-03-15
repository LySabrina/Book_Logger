import numpy as np
import cv2 as cv
import requests
import json


BASE_ISBN_URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:" #Base URL to find book by ISBN
BASE_COST ="https://www.googleapis.com/books/v1/volumes?q=intitle:"   #Base url to findd book by title


def readISBN(img):
    read = cv.imread(img)
    gray = cv.cvtColor(read, cv.COLOR_BGR2GRAY)
    barcode = cv.barcode.BarcodeDetector()
    isbn = barcode.detectAndDecode(gray)[0]
    if isbn:
        return isbn
    else:
        return None

def getBookInfo(isbn):
    request = requests.get(BASE_ISBN_URL + isbn)
    
    response = json.loads(request.text)
    volume =response['items'][0]['volumeInfo']
    title =response['items'][0]['volumeInfo']['title']
    thumbnail = volume['imageLinks']['smallThumbnail']
    price = findPrice(title)
    data = {
        "thumbnail" : thumbnail,
        "title" : title,
        "price" : price
    }
    return data

def findTitleByISBN(isbn):
    request = requests.get(BASE_ISBN_URL + isbn)
    print(request)
    response = json.loads(request.text)
    title = response['items'][0]['volumeInfo']['title']
    return title

def findPrice(title):
    print(BASE_COST + title)
    request = requests.get(BASE_COST + title)
    
    response = json.loads(request.text)
    
    for item in range(2):
        book_title = response['items'][item]['volumeInfo']['title']
        if(book_title == title):
            saleInfo = response['items'][item]['saleInfo']
            if("retailPrice" in saleInfo):
                return saleInfo['retailPrice']['amount']
    
    # if(book_title == title):
    #     # retail_price = response['items'][0]['volumeInfo']['saleInfo']['retailPrice']['amount']
    #     retail_price = response['items'][0]['volumeInfo']
    #     # print(retail_price)
    # #     if(retail_price):
    # #         return retail_price
    # # else:
    # #     return None
    

def findBook(img):
    isbn = readISBN(img)
    if(isbn is None):
        return None
    else:
        return getBookInfo(isbn)
    
