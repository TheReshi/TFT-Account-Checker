import json, re, requests, webbrowser
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree
import config as cfg

# The main funcion after pressing the Check Account button
def check_account(app):
    poe_account_name = app.poe_account_name_textbox.get()
    discord_id = app.discord_id_textbox.get()

    if check_input_error(app, discord_id, poe_account_name):
        return

    discord_account_age = get_discord_account_age(discord_id)
    set_discord_account_age(app, discord_account_age)
    poe_account_url = get_poe_account_url(poe_account_name)
    set_poe_account_name(app, poe_account_url)
    # app.poe_account_value.bind("<Button-1>", lambda e: webbrowser.open_new(poe_account_url))
    # app.poe_account_value.configure(text=f"{app.poe_account_name_textbox.get().upper()}", fg=cfg.link_color, cursor=cfg.link_cursor, font=cfg.link_font)
    overview_soup = get_overview_soup(poe_account_name)
    if not check_profile_existence(app, overview_soup):
        return
    poe_account_info = get_poe_account(overview_soup, poe_account_name)

    if set_poe_account_private(app, poe_account_info):
        return
    set_poe_account_age(app, poe_account_info)
    set_poe_account_guild(app, poe_account_info)
    set_poe_account_supporter_pack(app, poe_account_info)
    set_poe_account_challenges(app, poe_account_info)
    set_poe_account_characters(app, poe_account_info)
    set_poe_account_textboxes(app, poe_account_info, discord_id)
    app.create_character_window(poe_account_info)

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
    return sorted(poecom_character_data, key=lambda character: int(character['level']), reverse=True)

# Get characters from poecc.com
def get_poecc_character_data(poe_account_name):
    headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' }
    page = requests.get(f"https://poecc.com/?name=viewaccount&accountName={poe_account_name}", headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    document_object_model = etree.HTML(str(soup))
    poecc_character_data = document_object_model.xpath('//*[@id="html"]/body/table/tr[2]/td/table/tr/td/table[2]/tr')
    return poecc_character_data

# Returns pathofexile.com URL
def get_poe_account_url(poe_account_name):
    return f"https://www.pathofexile.com/account/view-profile/{poe_account_name}"

# If the account is Private, returns False. Else, it proceeds with gathering all the neccessary data.
def get_poe_account(overview_soup, poe_account_name):
    overview_soup = get_overview_soup(poe_account_name)

    if not PoEAccount.get_account_private(None, overview_soup):
        poecom_character_data = get_poecom_character_data(poe_account_name)
        poecc_character_data = get_poecc_character_data(poe_account_name)
        return PoEAccount(overview_soup, poecom_character_data, poecc_character_data, poe_account_name)
    return False

# Resets the output fields (after PoE Account Private) of the app
def reset_output_fields_post_private(app):
    app.poe_account_age_value.configure(text="")
    app.poe_guild_value.configure(text="")
    app.poe_supporter_pack_value.configure(text="")
    app.poe_challenges_value.configure(text="")
    app.poe_characters_value.unbind("<Button-1>")
    app.poe_characters_value.configure(text="", cursor="arrow")
    unlock_output_textboxes(app)
    app.poecom_character_list_textbox.delete("0", "end")
    app.poecc_character_list_textbox.delete("0", "end")
    app.combined_character_list_textbox.delete("0", "end")
    app.blacklist_check_command_textbox.delete("0", "end")
    app.unrestrict_command_textbox.delete("0", "end")
    lock_output_textboxes(app)

# Resets the output fields (after PoE Account Name) of the app
def reset_output_fields_post_account_name(app):
    app.poe_account_private_value.configure(text="")
    reset_output_fields_post_private(app)

# Resets the output fields of the app
def reset_output_fields(app):
    app.discord_account_age_value.configure(text=f"")
    app.poe_account_value.unbind("<Button-1>")
    app.poe_account_value.configure(text=f"", cursor="arrow")
    # app.poe_account_private_value.configure(text="")
    reset_output_fields_post_private(app)

def check_input_error(app, discord_id, poe_account_name):
    if len(discord_id.strip()) < 16 or len(discord_id.strip()) > 18 or not discord_id.strip().isdigit():
        # app.input_error_label.configure(text="Incorrect Discord User ID")
        set_error_message(app, "Incorrect Discord User ID")
        reset_output_fields(app)
        app.close_character_window()
        return True
    
    if not poe_account_name:
        # app.input_error_label.configure(text="Missing PoE Account Name")
        set_error_message(app, "Missing PoE Account Name")
        reset_output_fields(app)
        app.close_character_window()
        return True

    # app.input_error_label.configure(text="")
    clear_error_message(app)
    return False

def unlock_output_textboxes(app):
    app.poecom_character_list_textbox.configure(state='normal')
    app.poecc_character_list_textbox.configure(state='normal')
    app.combined_character_list_textbox.configure(state='normal')
    app.blacklist_check_command_textbox.configure(state='normal')
    app.unrestrict_command_textbox.configure(state='normal')

def lock_output_textboxes(app):
    app.poecom_character_list_textbox.configure(state='readonly')
    app.poecc_character_list_textbox.configure(state='readonly')
    app.combined_character_list_textbox.configure(state='readonly')
    app.blacklist_check_command_textbox.configure(state='readonly')
    app.unrestrict_command_textbox.configure(state='readonly')

def set_discord_account_age(app, discord_account_age):
    if discord_account_age >= cfg.good_discord_account_age:
        app.discord_account_age_value.configure(text=f"{discord_account_age} Days", foreground=cfg.good_value_color)
    else:
        app.discord_account_age_value.configure(text=f"{discord_account_age} Days", foreground=cfg.bad_value_color)

def set_poe_account_private(app, poe_account_info):
    if not poe_account_info:
        app.poe_account_private_value.configure(text="Yes", foreground=cfg.bad_value_color)
        reset_output_fields_post_private(app)
        app.close_character_window()
        return True

    app.poe_account_private_value.configure(text="No", foreground=cfg.good_value_color)
    return False

def set_poe_account_age(app, poe_account_info):
    if poe_account_info.account_age >= cfg.good_poe_account_age:
        app.poe_account_age_value.configure(text=f"{poe_account_info.account_age} Days", foreground=cfg.good_value_color)
    else:
        app.poe_account_age_value.configure(text=f"{poe_account_info.account_age} Days", foreground=cfg.bad_value_color)

def set_poe_account_guild(app, poe_account_info):
    if poe_account_info.guild:
        app.poe_guild_value.configure(text="Yes", foreground=cfg.good_value_color)
    else:
        app.poe_guild_value.configure(text="No", foreground=cfg.bad_value_color)

def set_poe_account_supporter_pack(app, poe_account_info):
    if poe_account_info.supporter_pack == 0:
        app.poe_supporter_pack_value.configure(text="No", foreground=cfg.bad_value_color)
    else:
        app.poe_supporter_pack_value.configure(text=f"Yes ({poe_account_info.supporter_pack})", foreground=cfg.good_value_color)

def set_poe_account_challenges(app, poe_account_info):
    if int(poe_account_info.challenges) >= cfg.good_challenge_number:
        app.poe_challenges_value.configure(text=poe_account_info.challenges, foreground=cfg.good_value_color)
    else:
        app.poe_challenges_value.configure(text=poe_account_info.challenges, foreground=cfg.bad_value_color)

def set_poe_account_characters(app, poe_account_info):
    status = get_character_quality(poe_account_info.characters)
    app.poe_characters_value.bind("<Button-1>", lambda e: app.create_character_window(poe_account_info))
    if status == 0:
        app.poe_characters_value.configure(text=len(poe_account_info.characters), foreground=cfg.lowlevel_color, cursor=cfg.link_cursor, font=cfg.link_font)
    elif status == 1:
        app.poe_characters_value.configure(text=len(poe_account_info.characters), foreground=cfg.standard_highlevel_color, cursor=cfg.link_cursor, font=cfg.link_font)
    else:
        app.poe_characters_value.configure(text=len(poe_account_info.characters), foreground=cfg.league_highlevel_color, cursor=cfg.link_cursor, font=cfg.link_font)

def set_poe_account_textboxes(app, poe_account_info, discord_id):
    unlock_output_textboxes(app)
    delete_output_textbox_contents(app)
    app.poecom_character_list_textbox.insert("0", ','.join(poe_account_info.poecom_characters))
    app.poecc_character_list_textbox.insert("0", ','.join(poe_account_info.poecc_characters))
    app.combined_character_list_textbox.insert("0", ','.join(poe_account_info.combined_characters))
    app.blacklist_check_command_textbox.insert("0", f"!blacklist check {','.join(poe_account_info.combined_characters)}")
    app.unrestrict_command_textbox.insert("0", f"?role {discord_id.strip()} trade restricted")
    lock_output_textboxes(app)

def delete_output_textbox_contents(app):
    app.poecom_character_list_textbox.delete("0", "end")
    app.poecc_character_list_textbox.delete("0", "end")
    app.combined_character_list_textbox.delete("0", "end")
    app.blacklist_check_command_textbox.delete("0", "end")
    app.unrestrict_command_textbox.delete("0", "end")

## Returns if there any qualified characters accoding to cfg.min_character_level
### 0: No characters above cfg.min_character_level
### 1: At least 1 character above cfg.min_character_level in Standard
### 2: At least 1 character above cfg.min_character_level in League
def get_character_quality(characters):
    status = 0
    for character in characters:
        if int(character["level"]) > cfg.min_character_level:
            if "Standard" in character["league"]:
                status = 1
            else:
                return 2

    return status

def open_character_window(app, poe_account):
    app.create_character_window(poe_account)

def check_profile_existence(app, overview_soup):
    if "Profile Not Found" in overview_soup.text:
        set_error_message(app, "Profile does not exist!")
        reset_output_fields_post_account_name(app)
        app.close_character_window()
        return False
    return True

def set_poe_account_name(app, poe_account_url):
    app.poe_account_value.bind("<Button-1>", lambda e: webbrowser.open_new(poe_account_url))
    app.poe_account_value.configure(text=f"{app.poe_account_name_textbox.get().upper()}", fg=cfg.link_color, cursor=cfg.link_cursor, font=cfg.link_font)

def set_error_message(app, message):
    app.input_error_label.configure(text=message)

def clear_error_message(app):
    app.input_error_label.configure(text='')

# PoEAccount class, contains every info about the account. This is showed in the app.
class PoEAccount:
    def __init__(self, overview_soup, poecom_character_data, poecc_character_data, poe_account_name, auto_gen=True):
        self.poe_account_name = poe_account_name
        self.private = False
        self.account_age = 0
        self.guild = False
        self.supporter_pack = 0
        self.challenges = 0
        self.characters = 0
        self.poecom_characters = []
        self.poecc_characters = []
        self.combined_characters = []

        if auto_gen:
            self.private = self.get_account_private(overview_soup)
            if not self.private:
                self.set_information(overview_soup, poecom_character_data, poecc_character_data, poe_account_name)

    # Basic automatic setter calls for all required data.
    def set_information(self, overview_soup, poecom_character_data, poecc_character_data, poe_account_name):
        basic_information = overview_soup.find_all("div", {"class": "profile-box profile"})
        supporter_packs = overview_soup.find_all("div", {"class": "badges clearfix"})
        achievements = overview_soup.find_all("div", {"class": "info challenges"})
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
        challenges = str(overview_soup)
        match = re.findall(r"(\d+)\/\d+", challenges)
        self.challenges = match[0]

    def set_characters(self, poecom_character_data):
        self.characters = poecom_character_data

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
