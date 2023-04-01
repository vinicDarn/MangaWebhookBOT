import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import json
import random
import re


config = json.loads(open("config.json", "r").read())
webhook_url = config["webhook"]
delay = config["delay"]
urlmanga = 'https://mangaupdates.com/releases.html'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

# webhook stuff
webhook = DiscordWebhook(url=webhook_url, username='Mangá Updater')


# Get the updates
while True:
    print("Making a request HTTP and extract informations from HTML")
    response = requests.get(urlmanga, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        posts = soup.find('div', {'class': 'col-6 pbreak'})
    except:
        print('ERRO: Div not found')
        input()
        exit()

    print("Searching news updates")
    if len(posts) > count:
        print("Creating new Embed Object")
        title = posts.find('a').text
        detailsURL = posts.a.get('href')
        image = requests.get(detailsURL, headers=header).text
        imgen = BeautifulSoup(image, 'html.parser')
        imge1 = imgen.find(
            'div', {"class": "row no-gutters flex-fill flex-nowrap"})
        imge = imge1.find(
            'div', {"class": "col d-flex flex-column center-side-bar flex-shrink-1"})
        img = imge.find('img', {"class": "img-fluid"}).get('src')
        capdiv = soup.find('div', {'class': 'col-2 pl-1 pbreak'}).text
        cap = int(re.search(r'\d+', capdiv).group())
        print(img)
        msg = random.choice(config["mensagens"])
        embed = DiscordEmbed(title=msg.format(title, cap))
        webhook.add_embed(embed)

        print("Sending...")
        response = webhook.execute()

        if response.status_code == 200:
            print("Message sended with sucess")
        else:
            print("Error: message dont as been sended")

    print("Waiting the delay")
    time.sleep(delay)
