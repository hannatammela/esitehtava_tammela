import requests
from collections import Counter
import json

# Rajapinnan osoite
url = "https://jsonplaceholder.typicode.com/posts"

# Haetaan postit
getposts = requests.get(url)
data = getposts.json()

# Tehdään dictionary postien määrälle,
# kaikille sanoille ja lista top 5 sanoille
user_all_posts = {}
user_all_words = {}
user_word_list = {}
all_words_list = []

# Käydään läpi jokainen posti datassa
for content in data:
    id_user = content["userId"]
    words = content["body"].split() # Jaetaan postien tekstit sanoiksi
    all_words = len(words)
    all_words_list.extend(words) #Lisätään sanat yleiseen sanalistaan

    # Jos käyttäjää ei vielä ole sanakirjoissa, alustetaan tiedot
    if id_user not in user_all_posts:
        user_all_posts[id_user] = 0
        user_all_words[id_user] = 0
        user_word_list[id_user] = []

    # Tässä päivitetään käyttäjän tiedot
    user_all_posts[id_user] += 1
    user_all_words[id_user] += all_words
    user_word_list[id_user].extend(words)

# Pääsanakirja JSON-datan tallennusta varten
json_data = {"users": {}}

# Käydään läpi kaikki käyttäjä-ID:t
for id_user in user_all_posts.keys():
    total_posts = user_all_posts[id_user] # Postausten kokonaismäärä
    total_words = user_all_words[id_user] # Sanojen kokonaismäärä
    average_words = total_words / total_posts
    top_5_words_user = Counter(user_word_list[id_user]).most_common(5)

# Tallennetaan tiedot JSONiin
    json_data["users"][id_user] = {
        "Posteja": total_posts,
        "Sanoja": total_words,
        "Sanoja keskimaarin": average_words,
        "Top 5 sanat" : top_5_words_user
}

# Tallennetaan JSONiin nimellä userdata.json
with open ("userdata.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)
