from urllib.request import urlopen
import requests
from urllib.error import HTTPError
from urllib.error import URLError
from html.parser import HTMLParser
from product_details import ProductDetails as product
from product_details import SellerDetails as seller
import re
import read_write
from bs4 import BeautifulSoup as bs

url = 'https://www.amazon.in/Nokia-105-2019-Single-Black/dp/B07YYNX5X6/ref=sr_1_4?crid=7RHHJSPWTJUZ&keywords=nokia%2Bmobile%2Bphone&qid=1580718816&s=electronics&sprefix=nokia%2Bm%2Celectronics%2C325&sr=1-4&th=1'
#url = 'https://www.amazon.in/Nokia-105-2019-Single-Black/dp/B07YYNLCD2/ref=sr_1_4?crid=7RHHJSPWTJUZ&keywords=nokia%2Bmobile%2Bphone&qid=1580718816&s=electronics&sprefix=nokia%2Bm%2Celectronics%2C325&sr=1-4&th=1'
#url='https://www.amazon.in/Nokia-105-2019-Single-Black/dp/B07YYMYXVD/ref=sr_1_4?crid=7RHHJSPWTJUZ&keywords=nokia%2Bmobile%2Bphone&qid=1580718816&s=electronics&sprefix=nokia%2Bm%2Celectronics%2C325&sr=1-4&th=1'
resp = ''
headers = {"Authority":"www.amazon.in", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
resp = requests.get(url, headers=headers)
if resp.status_code == 200:
    print('Crawler running...!!')
    productpage = bs(resp.content, "lxml")
    name = productpage.h1.get_text()
    product.name = name.strip()

    product.price = productpage.find('span', {'id': 'priceblock_ourprice'}).text.strip()

    product.baseprice = productpage.find('span', {'class': 'priceBlockStrikePriceString a-text-strike'}).text.strip()

    discount = productpage.find('tr', {'id': 'regularprice_savings'}).text.replace("\n", "")
    product.discount = discount.replace("You Save: ", "").strip()

    imagediv = productpage.find('div', {'id':'imgTagWrapperId'})
    mainimage = imagediv.img['data-old-hires'].title()
    product.image = mainimage.lower()
    otherimage = imagediv.img['data-a-dynamic-image'].title()
    image = otherimage.lower()
    altimages = re.findall("\"(.*?)\":", str(image))
    product.altimages = altimages
    if product.image == '':
        product.image = altimages[0]

    #nextpage.a['href'].title())
    #images = productpage.find("img", {'id':'landingImage'})
    #print(images)

    colordiv = productpage.find(id = 'variation_color_name')
    selectedcolor = ''
    if colordiv != None:
        selectedcolor = colordiv.find('span', {'class' : 'selection'}).get_text()
        selectedcolor = selectedcolor.strip()

    selectedsize = productpage.find('span', {'class': 'selection'}).text.strip()
    selectedsize = selectedsize.replace("\n", "").replace(" ", "")
    if selectedcolor != None:
        product.selectedvariant = selectedcolor
    else:
        product.selectedvariant = selectedsize

    variantsdiv = productpage.find('form', {'id': 'twister'})

    colors = variantsdiv.find_all('img', {'class' : 'imgSwatch'})
    for color in colors:
        color = color.get('alt')
        product.colorvariats.append(color)

    sizes = variantsdiv.find_all('span', {'class' : 'a-size-base'})
    for size in sizes:
        size = size.text
        product.sizevariants.append(size)

    info = productpage.find('div', {'id': 'feature-bullets'}).text.strip()
    extrainfo = productpage.find('div', {'id': 'productDescription'}).text.strip()

    maininfo = info + extrainfo
    product.info = maininfo.replace("\n", "")

    product.paymentoffers = productpage.find('ul', {'class': 'a-unordered-list a-vertical a-spacing-small'}).text.strip()
    product.paymentoffers = product.paymentoffers.replace("Here's how", "")
    product.paymentoffers = product.paymentoffers.replace("\n" , "")
    product.paymentoffers = product.paymentoffers.replace("\t" , "")

    product.info = product.info.replace("\t", "")

    pid = re.search("\"currentAsin\"\\s*:\\s*\"(.*)\"", str(productpage))
    product.productid = pid[1]

    #print(soup.prettify())
    #product.printProductDetails(product)

    #write product details to file  =====>>>
    #read_write.save_product_details(product, 'Output.csv')


    #getting Next pages seller
    def getsellernextpage(nextpageno,index):
        nexturl = 'https://www.amazon.in/gp/offer-listing/' + pid[1] + '/ref=olp_page_' + str(nextpageno) + '?ie=UTF8&f_new=true&startIndex=' + str(index)
        #print("nextpage : " + nexturl)
        return nexturl

    #parse-----Seller Details--------

    def parseSellerDetails(sellerurl):
        try:
            #print("page 1 : " + sellerurl)
            req = requests.get(sellerurl, headers=headers)
            sellerpage = req
        except HTTPError as e:
            print('Error while parsing seller: ')
            print(e)
        except URLError as e:
            print('Error while parsing seller: ')
            print(e)
        else:
            sellerObj = bs(sellerpage.content, 'lxml')
            sellerdivs = sellerObj.find_all('div', {'class' : 'a-row a-spacing-mini olpOffer'})

            #if len(pages) > 3:
                #nextpage = len(pages)-2
                #nextpageno = pages[nextpage].find('a').text
                #nexturl = getsellernextpage(nextpageno)
                #parseSellerDetails(nexturl)
                #print(re.findall("[0-9]+", str(pages[nextpage])))

            #print(nextpagediv)
            #nextpage = nextpagediv.find_all('li')
            #print(nextpage.a['href'].title())
            #print(nextpage)
            for sel in sellerdivs:
                #print(sel)
                spandiv = sel.div.select('span')
                seller.price = spandiv[0].text.strip()
                seller.name = sel.find('h3', {'class':'a-spacing-none olpSellerName'}).text.strip()
                #seller.printSellerDetails(seller)
                read_write.save_product_details(product, seller, 'Output.csv')
                #read_write.save_seller_details(seller, "output.csv")
                #break
    #pages = re.search("New\\\\s*\\((\\\\d+)\\)\\\\s*from", productpage)
    #print(pages)

    a = re.search("New\\s*\((\\d+)\)\\s*from", str(productpage))
    availablesellers = 0
    if a:
        availablesellers = a[1]
    else:
        availablesellers = 1
    totalpages = int(availablesellers)/10
    startindex = 0
    for pageno in range (1,int(totalpages + 2)):
        #print(pageno)
        nexturl = getsellernextpage(pageno, startindex)
        startindex += 10
        parseSellerDetails(nexturl)


    print("Crawler stopped plz check Output.csv file")

    #sellerDiv = productpage.find('div', {'id': 'olp-upd-new-freeshipping'})
    #seller = sellerDiv.find('a', href=True)
    #sellerurl = 'https://www.amazon.in' + seller['href']
    #sellerurl = 'https://www.amazon.in/gp/offer-listing/B005FYNT3G/ref=dp_olp_new_mbc?ie=UTF8&condition=new'
    #parseSellerDetails(sellerurl)

     #C:\Users\Vaibhav\PycharmProjects\amazon_scraping\product_details.txt
    #read_write.read_product_details('prod')
else:
    print("Status code : "+  str(resp.status_code))
