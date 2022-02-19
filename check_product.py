from bs4 import BeautifulSoup
import requests

url_microwave = "https://www.amazon.com/dp/B07894S727/ref=ods_gw_eg_feb_d_atf_vicc_spr2?pf_rd_r=KY5A3DMPMD4XWP3ESJXE&pf_rd_p=ba8b312f-ff41-4e32-bef9-c1d351d0c3d1&pd_rd_r=9178b7b2-858d-454d-b2f2-bfb3ea015fa5&pd_rd_w=BFsYc&pd_rd_wg=OFCZF&ref_=pd_gw_unk"
url_bulbs = "https://www.amazon.com/Lights-Multi-Colored-Google-Assistant-Required/dp/B07DLSNNDS/ref=amzdv_cabsh_dp_1/134-8035992-7538446?pd_rd_w=I0jQ1&pf_rd_p=58745b8f-d858-46ce-8730-c8a1b64ac780&pf_rd_r=48HHFEPM3TZ5WDH4G345&pd_rd_r=aff35799-78c6-4b69-a0c6-10581de55b3e&pd_rd_wg=Q6Esk&pd_rd_i=B07DLSNNDS&th=1"
url_book = "https://www.amazon.com/gp/product/0132350882/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1.html"

HEADERS = ({'User-Agent':
           'Mozilla/5.0 (X11; Linux x86_64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/44.0.2403.157 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})

webpage = requests.get(url_microwave, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "lxml")

# Based on the div where id=dp, we will derive where to find our price
# Find type
try:
    item_type = soup.find("div", attrs={'id': 'dp'})
    item_type_value = item_type['class']
except AttributeError:
    item_type_value = "NA"

# Check if in stock
try:
    in_stock = soup.find("div", attrs={"id": 'availability'})
    in_stock = in_stock.find("span")
    in_stock_value = in_stock.string
except AttributeError:
    pass

# For microwave, (div id = dp, class = amazon_shm"), price is at span class="a-offscreen"
# Find pricing. Got the entire corePrice element, and then we can search for a discount
try:
    price = soup.find("div", attrs={"data-feature-name": "corePrice_desktop"})# attrs={"id": "corePrice_desktop"})
    price_value = price
except AttributeError:
    price_value = "NA"

# Is there a discount?
discount_price = price_value.find("span", attrs={"class": "apexPriceToPay"})
price_information = price_value.find_all("span", attrs={"class": "a-text-price"})

d_price = price_value.find("span", attrs={"class": "apexPriceToPay"}).find("span", {"class": "a-offscreen"}).string
savings = price_value.find("span", attrs={"class": "a-size-base", "data-a-color": "price"}).find("span", {"class": "a-offscreen"}).string
old_price = price_value.find("span", attrs={'class': "a-size-base", "data-a-color": "secondary"}).find("span", {"class": "a-offscreen"}).string
percent_saved = round( ((float(savings.strip("$")) / float(old_price.strip("$"))) * 100), 0)

# Find name as well
try:
    name = soup.find("span", attrs={"id": "productTitle"})
    name_value = name.string
except AttributeError:
    name_value = "NA"

price_message = "Looks like {} is available.\n" \
                "Current Price: {}\n" \
                "Previous Price: {}\n" \
                "Total savings of {} per unit ({})".format(name_value, d_price, old_price, savings, 'filler')

print(price_message)