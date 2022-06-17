import json, re, requests, webbrowser
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree

# The main funcion after pressing the Check Account button
def check_account(app):
    poe_account_name = app.poe_account_name_textbox.get()
    discord_account_age = get_discord_account_age(app.discord_id_textbox.get())
    app.discord_account_age_value.configure(text=f"{discord_account_age} Days")
    poe_account_url = get_poe_account_url(poe_account_name)
    app.poe_account_value.bind("<Button-1>", lambda e: webbrowser.open_new(poe_account_url))
    app.poe_account_value.configure(text=f"{app.poe_account_name_textbox.get().upper()}", fg="blue", cursor="hand2")
    poe_account_info = get_poe_account(poe_account_name)

    if not poe_account_info:
        app.poe_account_private_value.configure(text="Yes")
        reset_fields(app)
        return

    app.poe_account_private_value.configure(text="No")
    app.poe_account_age_value.configure(text=f"{poe_account_info.account_age} Days")

    if poe_account_info.guild:
        app.poe_guild_value.configure(text="Yes")
    else:
        app.poe_guild_value.configure(text="No")

    if poe_account_info.supporter_pack == 0:
        app.poe_supporter_pack_value.configure(text="No")
    else:
        app.poe_supporter_pack_value.configure(text=f"Yes ({poe_account_info.supporter_pack})")

    app.poe_challenges_value.configure(text=poe_account_info.challenges)
    app.poe_characters_value.configure(text=poe_account_info.characters)

    app.poecom_character_list_textbox.delete("0", "end")
    app.poecc_character_list_textbox.delete("0", "end")
    app.combined_character_list_textbox.delete("0", "end")
    app.blacklist_check_command_textbox.delete("0", "end")

    app.poecom_character_list_textbox.insert("0", ','.join(poe_account_info.poecom_characters))
    app.poecc_character_list_textbox.insert("0", ','.join(poe_account_info.poecc_characters))
    app.combined_character_list_textbox.insert("0", ','.join(poe_account_info.combined_characters))
    app.blacklist_check_command_textbox.insert("0", f"!blacklist check {','.join(poe_account_info.combined_characters)}")

# Check Discord Account Age
def get_discord_account_age(discord_id):
    binary = bin(int(discord_id))
    m = 66 - len(binary)
    unixbin = str(binary)[0:42-(m-2)]
    unix = int(unixbin, 2) + 1420070400000
    timestamp = unix / 1000
    date = datetime.utcfromtimestamp(timestamp)
    return (datetime.now() - date).days

# Get HTML from the Overview page
def get_overview_soup(poe_account_name):
    headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' }
    URL = f"https://www.pathofexile.com/account/view-profile/{poe_account_name}"
    page = requests.get(URL, headers=headers)
    overview_soup = BeautifulSoup(page.content, "html.parser")
    return overview_soup

# Get characters from the pathofexile.com Character page
def get_poecom_character_data(poe_account_name):
    headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' }
    data = { 'accountName': poe_account_name }
    response = requests.post('https://www.pathofexile.com/character-window/get-characters', headers=headers, data=data)
    poecom_character_data = json.loads(response.text)
    return poecom_character_data

# Get characters from poecc.com
def get_poecc_character_data(poe_account_name):
    headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' }
    page = requests.get(f"https://poecc.com/?name=viewaccount&accountName={poe_account_name}", headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    documentObjectModel = etree.HTML(str(soup))
    poecc_character_data = documentObjectModel.xpath('//*[@id="html"]/body/table/tr[2]/td/table/tr/td/table[2]/tr')
    return poecc_character_data

# Returns pathofexile.com URL
def get_poe_account_url(poe_account_name):
    return f"https://www.pathofexile.com/account/view-profile/{poe_account_name}"

# If the account is Private, returns False. Else, it proceeds with gathering all the neccessary data.
def get_poe_account(poe_account_name):
    overview_soup = get_overview_soup(poe_account_name)
    if not PoEAccount.get_account_private(None, overview_soup):
        poecom_character_data = get_poecom_character_data(poe_account_name)
        poecc_character_data = get_poecc_character_data(poe_account_name)
        return PoEAccount(overview_soup, poecom_character_data, poecc_character_data, poe_account_name)
    return False

# Resets the output fields of the app
def reset_fields(app):
    app.poe_account_age_value.configure(text=f"")
    app.poe_guild_value.configure(text="")
    app.poe_supporter_pack_value.configure(text="")
    app.poe_challenges_value.configure(text="")
    app.poe_characters_value.configure(text="")
    app.poecom_character_list_textbox.delete("0", "end")
    app.poecc_character_list_textbox.delete("0", "end")
    app.combined_character_list_textbox.delete("0", "end")
    app.blacklist_check_command_textbox.delete("0", "end")

# PoEAccount class, contains every info about the account. This is showed in the app.
class PoEAccount:
    def __init__(self, overview_soup, poecom_character_data, poecc_character_data, poe_account_name):
        self.private = self.get_account_private(overview_soup)
        self.account_age = 0
        self.guild = False
        self.supporter_pack = 0
        self.challenges = 0
        self.characters = 0
        self.poecom_characters = []
        self.poecc_characters = []
        self.combined_characters = []

        if not self.private:
            self.set_information(overview_soup, poecom_character_data, poecc_character_data, poe_account_name)

    # Basic setter calls for all required data.
    def set_information(self, overview_soup, poecom_character_data, poecc_character_data, poe_account_name):
        basic_information = overview_soup.find_all("div", {"class": "profile-box profile"})
        supporter_packs = overview_soup.find_all("div", {"class": "badges clearfix"})
        achievements = overview_soup.find_all("div", {"class": "profile-box achievements"})
        self.set_account_age(basic_information)
        self.set_guild(basic_information)
        self.set_supporter_pack(supporter_packs)
        self.set_challenges(achievements)
        self.set_characters(poecom_character_data)
        self.set_poecom_characters(poecom_character_data)
        self.set_poecc_characters(poecc_character_data)
        self.set_combined_characters()
        return

    def get_account_private(self, overview_soup):
        if "Characters" not in str(overview_soup.find_all("div", {"class": "tab-links"})):
            return True
        return False

    def set_account_age(self, overview_soup):
        join_date = datetime.strptime(' '.join([i for i in re.split(' |,|<br/>', str(overview_soup[0]).split('\n')[12]) if i]), "%b %d %Y")
        self.account_age = (datetime.now() - join_date).days

    def set_guild(self, overview_soup):
        if "a href" in str(overview_soup[0]).split('\n')[3]:
            self.guild = True
        else:
            self.guild = False

    def set_supporter_pack(self, overview_soup):
        self.supporter_pack = str(overview_soup).count('<div class="badge">')

    def set_challenges(self, overview_soup):
        challenges = str(overview_soup).split('\n')[3]
        match = re.findall(r"(\d+)\/\d+", challenges)
        self.challenges = match[0]

    def set_characters(self, poecom_character_data):
        self.characters = len(poecom_character_data)

    def set_poecom_characters(self, poecom_character_data):
        poecom_characters = []
        for character in poecom_character_data:
            poecom_characters.append(character['name'])
        self.poecom_characters = sorted(poecom_characters)

    def set_poecc_characters(self, poecc_character_data):
        poecc_characters = []
        for character in poecc_character_data[1:]:
            poecc_characters.append(character.xpath('td[1]/a')[0].text)
        self.poecc_characters = sorted(poecc_characters)

    def set_combined_characters(self):
        self.combined_characters = sorted(list(set(self.poecom_characters + self.poecc_characters)))
