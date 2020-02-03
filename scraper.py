from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from html.parser import HTMLParser
from product_details import ProductDetails as product
from product_details import SellerDetails as seller
import re
import read_write
from bs4 import BeautifulSoup as bs

#url = 'https://www.amazon.in/gp/product/B07X1KT6LW/ref=s9_acss_bw_ln_x_1_11_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-leftnav&pf_rd_r=MN7PBK9JRKNQXQ86KFSN&pf_rd_t=101&pf_rd_p=2385127f-71dd-4475-be35-f9f1e6f2410b&pf_rd_i=1389401031'
url = 'https://www.amazon.in/SanDisk-Cruzer-Blade-Flash-Drive/dp/B005FYNT3G/ref=olp_product_details?_encoding=UTF8&me=  '
#url='https://www.amazon.in/Nokia-105-2019-Single-Black/dp/B07YYNX5X6/ref=sr_1_4?crid=7RHHJSPWTJUZ&keywords=nokia+mobile+phone&qid=1580718816&s=electronics&sprefix=nokia+m%2Celectronics%2C325&sr=1-4'
resp = ''
try:
    resp = urlopen(url,timeout=5)
except HTTPError as e:
    print(e)
except URLError as e:
    print(e)
else:
    print('Crawler running...!!')
    productpage = bs(resp.read(), 'lxml')
    name = productpage.h1.get_text()
    product.name = name.strip()

    product.price = productpage.find('span', {'id': 'priceblock_ourprice'}).text.strip()

    product.baseprice = productpage.find('span', {'class': 'priceBlockStrikePriceString a-text-strike'}).text.strip()

    discount = productpage.find('tr', {'id': 'regularprice_savings'}).text.replace("\n", "")
    product.discount = discount.replace("You Save: ", "").strip()

    imagediv = productpage.find('div', {'id':'imgTagWrapperId'})
    mainimage = imagediv.img['src'].title()
    product.image = mainimage.lower()
    otherimage = imagediv.img['data-a-dynamic-image'].title()
    image = otherimage.lower()
    altimages = re.findall("\"(.*?)\":", str(image))
    product.altimages = altimages

    #nextpage.a['href'].title())
    #images = productpage.find("img", {'id':'landingImage'})
    #print(images)

    colordiv = productpage.find(id = 'variation_color_name')
    selectedcolor = ''
    if colordiv != None:
        selectedcolor = colordiv.find('span', {'class' : 'selection'}).get_text()
        selectedcolor = selectedcolor.strip()

    selectedsize = 'size:' + productpage.find('span', {'class': 'selection'}).text.strip()
    selectedsize = selectedsize.replace("\n", "").replace(" ", "")
    if not selectedcolor:
        product.selectedvariant = selectedcolor + " : " + selectedsize
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
    product.info = maininfo.replace("\t", "")

    product.paymentoffers = productpage.find('ul', {'class': 'a-unordered-list a-vertical a-spacing-small'}).text.strip()

    pid = re.search("\"currentAsin\"\\s*:\\s*\"(.*)\"", str(productpage))
    product.productid = pid[1]

    #print(soup.prettify())
    #product.printProductDetails(product)

    #write product details to file  =====>>>
    read_write.save_product_details(product, 'Output.txt')


    #getting Next pages seller
    def getsellernextpage(nextpageno,index):
        nexturl = 'https://www.amazon.in/gp/offer-listing/' + pid[1] + '/ref=olp_page_' + str(nextpageno) + '?ie=UTF8&f_new=true&startIndex=' + str(index)
        #print("nextpage : " + nexturl)
        return nexturl

    #parse-----Seller Details--------

    def parseSellerDetails(sellerurl):
        try:
            #print("page 1 : " + sellerurl)
            sellerpage = urlopen(sellerurl)
        except HTTPError as e:
            print('Error while parsing seller: ')
            print(e)
        except URLError as e:
            print('Error while parsing seller: ')
            print(e)
        else:
            sellerObj = bs(sellerpage.read(), 'lxml')
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
                read_write.save_seller_details(seller, "output.txt")
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


    print("Crawler stopped plz check Output.txt file")

    #sellerDiv = productpage.find('div', {'id': 'olp-upd-new-freeshipping'})
    #seller = sellerDiv.find('a', href=True)
    #sellerurl = 'https://www.amazon.in' + seller['href']
    #sellerurl = 'https://www.amazon.in/gp/offer-listing/B005FYNT3G/ref=dp_olp_new_mbc?ie=UTF8&condition=new'
    #parseSellerDetails(sellerurl)

     #C:\Users\Vaibhav\PycharmProjects\amazon_scraping\product_details.txt
    #read_write.read_product_details('prod')
