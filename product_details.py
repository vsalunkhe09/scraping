class ProductDetails:
    name = ''
    price = 0.0
    productid = ''
    baseprice = 0.0
    discount = 0.0
    image = ''
    altimages = []
    deliveryInfo = ''
    selectedvariant = ''
    colorvariats = []
    sizevariants = []
    info = ''
    paymentoffers = ''

    def __init__(self, name, price, productid, baseprice, discount, image, altimages, deliveryInfo, selectedvariant, colorvariants, sizevariants, info, paymentoffers):
        self.name = name
        self.price = price
        self.productid = productid
        self.baseprice = baseprice
        self.discount = discount
        self.image = image
        self.altimages = altimages
        self.deliveryInfo = deliveryInfo
        self.selectedvariant = selectedvariant
        self.colorvariats = colorvariants
        self.sizevariants = sizevariants
        self.info = info
        self.paymentoffers = paymentoffers

    def printProductDetails(self):
        print(self.name)
        print(self.price)
        print(self.productid)
        print(self.baseprice)
        print(self.discount)
        print(self.deliveryInfo)
        print(self.selectedvariant)
        print(self.colorvariats)
        print(self.sizevariants)
        #print(self.info)
        #print(self.paymentoffers)

class SellerDetails:
    name = ''
    price = 0.0

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def printSellerDetails(self):
        print(self.name)
        print(self.price)
