#HOW TO:

1. Create a new virtual environment and source it.
2. Create an env.py file and populate it with the following:
- TWILIO_SID=< Your Twilio Account SID >
- TWILIO_AUTH_TOKEN=< Your Twilio Auth Token >
- TWILIO_MY_PHONE=< your phone number that will receive messages >
- TWILIO_OUTBOUND_PHONE=< the twilio number that will send texts >
3. Create an "items.csv" file in root directory. This is where you will store urls/
4. Run `pip install -r requirements.txt` in your virtual environment
5. Run `product_update.py` and enter in as many urls for products as you want.
6. Run `product_lookup_driver.py` to check for discounts and send you texts!