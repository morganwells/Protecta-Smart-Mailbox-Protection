# Send Message to Line via IFTTT
import requests

def send_message(event, val1, val2, val3, api_key):
    url = "https://maker.ifttt.com/trigger/" + event +"/with/key/" + api_key
    x = requests.post(url, data = {"value1" : val1, "value2" : val2, "value3" : val3 })
    print(x.text)