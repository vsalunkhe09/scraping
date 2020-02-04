import csv
import pickle
import os.path

def save_product_details(product,seller,  filename):
    isExists = os.path.isfile(filename)
    with open(filename,"a", encoding="utf-8") as f:
        headers = ["Name","Price", "Baseprice", "Discount", "Image" , "Alt Images", "Selected Variant", "Seller name" , "Seller Price"]
        writer = csv.DictWriter(f, dialect='excel', fieldnames=headers)
        if not isExists:
            writer.writeheader()
        writer.writerow({"Name": str(product.name), "Price": str(product.price), "Baseprice" : str(product.baseprice), "Discount":str(product.discount), "Image":str(product.image) , "Alt Images" : str(product.altimages), "Selected Variant" : str(product.selectedvariant), "Seller name":str(seller.name) , "Seller Price": str(seller.price)})

def save_seller_details(seller, filename):
    with open(filename,"a", encoding="utf-8") as f:
        headers = ["Seller Name","Seller Price"]
        writer = csv.DictWriter(f,dialect='excel', fieldnames=headers)
        writer.writerows({"Seller Name": seller.name, "Seller Price": seller.price})
        f.close()

def read_product_details(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
        print(obj.name)
