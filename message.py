# Send Message to phone using Push Safer
# def send_message(
import urllib3
urllib3.disable_warnings()

from urllib.parse import urlencode
from urllib.request import Request, urlopen

def send_message(api_key, mes_text, mes_title):
    print(api_key)


    url = 'https://www.pushsafer.com/api' # Set destination URL here
    post_fields = {                       # Set POST fields here
        "t" : mes_title,
        "m" : mes_text,
        #"s" : sound,
        #"v" : vibration,
        #"i" : icon,
        #"c" : iconcolor,
        #"d" : device,
        #"u" : url,
        #"ut" : urltitle,
        "k" : api_key
        }

    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()
    print(json)
    print("message sent")


