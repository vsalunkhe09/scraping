import pickle
def save_product_details(product, filename):
    with open(filename,"w", encoding="utf-8") as f:
        f.write("Product Details : \n")
        f.write("Name : " + product.name + "\n")
        f.write("Price : " + product.price + "\n")
        f.write("Product-id : " + product.productid + "\n")
        f.write("Baseprice : " + product.baseprice + "\n")
        f.write("Discount : " + product.discount + "\n")
        f.write("Main image : " + product.image + "\n")
        f.write("Alt images : " + str(product.altimages) + "\n")
        f.write("Info : " + product.info + "\n")
        f.write("Selected Variant " + product.selectedvariant + "\n")
        f.writelines("Available Colors : " + str(product.colorvariats) + "\n")
        f.write("Available sizes : " + str(product.sizevariants) + "\n")
        f.write("Paymentoffers : " + product.paymentoffers + "\n")
        f.write("\n***********************************\n")
        f.close()

def save_seller_details(seller, filename):
    with open(filename,"a", encoding="utf-8") as f:
        f.write("Seller Details : \n")
        f.write("seller Name : " + seller.name + "\n")
        f.write("Seller Price : " + seller.price + "\n")
        f.write("------------\n")
        f.close()

def read_product_details(filename):
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
        print(obj.name)
