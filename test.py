import json, requests

cookies = {
    'POESESSID': '8fa5335a3f35bf68a60558c6806faf4d',
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
}

response = requests.get('https://api.pathofexile.com/league', cookies=cookies, headers=headers)
leagues = json.loads(response.text)

for league in leagues['leagues']:
    print(league['id'])