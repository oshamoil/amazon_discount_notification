from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
import env

HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


class ProductLookup:

    def __init__(self):
        self.webpage = None
        self.soup = None
        self.url_list = self.get_urls()
        self.text_client = self.create_text_client()

    def run(self):

        for url in self.url_list:
            self.webpage = self.get_response_from_url(url)
            self.soup = self.create_soup_from_webpage()
            payload = self.get_product_info(url)
            valid_payload = self.check_valid_payload(payload)
            if not valid_payload:
                print("Not a valid payload")
                continue
            message = self.create_message(payload)
            self.send_discount_message(message)
            self.reset_state()
            print(message)

    def get_urls(self):
        url_list = []
        with open("items.csv", "r") as file:
            for url in file:
                url_list.append(url)
        return url_list

    def create_message(self, payload):
        message = "Great News!\n" \
                  "{} is currently discounted!\n" \
                  "Original Price:\t {}\n" \
                  "NEW PRICE:\t\t {}\n" \
                  "Total Savings:\t {} ({}% off)\n" \
                  "Click here to purchase: {}".format(payload['title'],
                                                      payload['price_details']['old_price'],
                                                      payload['price_details']['discount_price'],
                                                      payload['price_details']['savings'],
                                                      payload['price_details']['percent_save'],
                                                      payload['url']
                                                      )
        return message

    def get_response_from_url(self, url):
        return requests.get(url, headers=HEADERS)

    def create_soup_from_webpage(self):
        return BeautifulSoup(self.webpage.content, "lxml")

    def get_product_info(self, url):
        product_info = {}
        product_info['url'] = url
        product_info['type'] = self.get_product_type()
        product_info['title'] = self.get_product_title()
        product_info['availability'] = self.get_product_availability()
        product_info['price_details'] = self.get_product_price_details()

        return product_info

    def get_product_type(self):
        try:
            product_type = self.soup.find("div", attrs={'id': 'dp'})
            product_type_value = product_type['class']
        except AttributeError:
            product_type_value = "NA"
        return product_type_value

    def get_product_title(self):
        try:
            title = self.soup.find("span", attrs={"id": "productTitle"})
            title_value = title.string.strip()
            title_value = "\"" + title_value + "\""
        except AttributeError:
            title_value = "NA"
        return title_value

    def get_product_availability(self):
        try:
            avilability = self.soup.find("div", attrs={"id": 'availability'})
            avilability = avilability.find("span")
            availability_value = avilability.text.strip()
        except AttributeError:
            availability_value = "NA"
        return availability_value

    def get_product_price_details(self):
        price_information = {}
        price_element = self.get_price_element()
        price_information['old_price'] = self.get_old_price(price_element)
        price_information['discount_price'] = self.get_discount_price(price_element)
        price_information['savings'] = self.get_savings(price_element)
        price_information['percent_save'] = self.get_percent_saved(price_information['savings'], price_information['old_price'])

        return price_information

    def get_price_element(self):
        try:
            price_element = self.soup.find("div", attrs={"id": "corePrice_desktop"})
        except AttributeError:
            price_element = "NA"
        return price_element

    def get_old_price(self, price_element):
        try:
            old_price = price_element.find("span", attrs={'class': "a-size-base", "data-a-color": "secondary"})\
                .find("span", {"class": "a-offscreen"}).string
        except AttributeError:
            old_price = "NA"
        return old_price

    def get_discount_price(self, price_element):
        try:
            discount_price = price_element.find("span", attrs={"class": "apexPriceToPay"})\
                .find("span", {"class": "a-offscreen"}).string
        except AttributeError:
            discount_price = "NA"
        return discount_price

    def get_savings(self, price_element):
        try:
            savings = price_element.find("span", attrs={"class": "a-size-base", "data-a-color": "price"})\
                .find("span", {"class": "a-offscreen"}).string
        except AttributeError:
            savings = "NA"
        return savings

    def get_percent_saved(self, discount, old_price):
        if discount == "NA" or old_price == "NA":
            return "NA"
        return round(((float(discount.strip("$")) / float(old_price.strip("$"))) * 100), 0)

    def check_valid_payload(self, payload):
        if payload['title'] == "NA":
            return False
        if payload['availability'] != "In Stock.":
            return False
        for price_detail, value in payload['price_details'].items():
            if value == "NA":
                return False
        return True

    def create_text_client(self):
        account_sid = self.get_sid()
        auth_token = self.get_auth_token()
        client = Client(account_sid, auth_token)

        return client

    def get_sid(self):
        return env.TWILIO_SID

    def get_auth_token(self):
        return env.TWILIO_AUTH_TOKEN

    def send_discount_message(self, message):
        outbound_message = self.text_client.messages.create(
            to=env.TWILIO_OUTBOUND_PHONE,
            from_=env.TWILIO_MY_PHONE,
            body=message
        )
        print(outbound_message.sid)

    def reset_state(self):
        self.webpage = None
        self.soup = None


if __name__ == "__main__":
    pl = ProductLookup()
    pl.run()