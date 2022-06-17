import tkinter as tk
import resources as res


class AccountChecker:
    def __init__(self, master=None):
        # Main window
        self.windowFrame = tk.Tk() if master is None else tk.Toplevel(master)

        # Input Frame
        self.inputFrame = tk.Frame(self.windowFrame)

        # Input Frame Elements
        ## Discord ID Label & Textbox
        self.discord_id_label = tk.Label(self.inputFrame)
        self.discord_id_label.configure(anchor="n", text="Discord User ID")
        self.discord_id_label.place(anchor="nw", relx=0.0, width=120, x=10, y=10)

        self.discord_id_textbox = tk.Entry(self.inputFrame)
        self.discord_id_textbox.configure(justify="center", validate="none")
        _text_ = "244434556638330873"
        self.discord_id_textbox.delete("0", "end")
        self.discord_id_textbox.insert("0", _text_)
        self.discord_id_textbox.place(anchor="nw", width=260, x=130, y=10)

        ## PoE Account Label & Textbox
        self.poe_account_name_label = tk.Label(self.inputFrame)
        self.poe_account_name_label.configure(anchor="n", text="PoE Account Name")
        self.poe_account_name_label.place(anchor="nw", relx=0.0, width=120, x=10, y=40)

        self.poe_account_name_textbox = tk.Entry(self.inputFrame)
        self.poe_account_name_textbox.configure(justify="center")
        _text_ = "tifatits"
        self.poe_account_name_textbox.delete("0", "end")
        self.poe_account_name_textbox.insert("0", _text_)
        self.poe_account_name_textbox.place(anchor="nw", width=260, x=130, y=40)

        ## Check Account Button
        self.check_account_button = tk.Button(self.inputFrame)
        self.check_account_button.configure(text="Check Account", command=lambda: res.check_account(self))
        self.check_account_button.place(anchor="nw", width=380, x=10, y=70)
        self.inputFrame.configure(height=100, width=400)
        self.inputFrame.pack(side="top")

        ## Output Frame
        self.outputFrame = tk.Frame(self.windowFrame)

        # Output Frame Elements
        ## Discord Account Age Label & Textbox
        self.discord_account_age_label = tk.Label(self.outputFrame)
        self.discord_account_age_label.configure(text="Discord Account Age")
        self.discord_account_age_label.place(anchor="nw", width=190, x=10, y=10)

        self.discord_account_age_value = tk.Label(self.outputFrame)
        self.discord_account_age_value.place(anchor="nw", width=190, x=10, y=30)

        ## PoE Account Label & Textbox
        self.poe_account_label = tk.Label(self.outputFrame)
        self.poe_account_label.configure(text="PoE Account")
        self.poe_account_label.place(anchor="nw", width=190, x=200, y=10)

        self.poe_account_value = tk.Label(self.outputFrame)
        self.poe_account_value.place(anchor="nw", width=190, x=200, y=30)

        ## PoE Account Private Label & Textbox
        self.poe_account_private_label = tk.Label(self.outputFrame)
        self.poe_account_private_label.configure(text="PoE Account Private")
        self.poe_account_private_label.place(anchor="nw", width=190, x=10, y=70)

        self.poe_account_private_value = tk.Label(self.outputFrame)
        self.poe_account_private_value.place(anchor="nw", width=190, x=10, y=90)

        ## PoE Account Age Label & Textbox
        self.poe_account_age_label = tk.Label(self.outputFrame)
        self.poe_account_age_label.configure(text="PoE Account Age")
        self.poe_account_age_label.place(anchor="nw", width=190, x=200, y=70)

        self.poe_account_age_value = tk.Label(self.outputFrame)
        self.poe_account_age_value.place(anchor="nw", width=190, x=200, y=90)

        ## PoE Guild Label & Textbox
        self.poe_guild_label = tk.Label(self.outputFrame)
        self.poe_guild_label.configure(text="Guild")
        self.poe_guild_label.place(anchor="nw", width=190, x=10, y=130)

        self.poe_guild_value = tk.Label(self.outputFrame)
        self.poe_guild_value.place(anchor="nw", width=190, x=10, y=150)

        ## PoE Supporter Pack Label & Textbox
        self.poe_supporter_pack_label = tk.Label(self.outputFrame)
        self.poe_supporter_pack_label.configure(text="Supporter Packs")
        self.poe_supporter_pack_label.place(anchor="nw", width=190, x=200, y=130)

        self.poe_supporter_pack_value = tk.Label(self.outputFrame)
        self.poe_supporter_pack_value.place(anchor="nw", width=190, x=200, y=150)

        ## PoE Challenges Label & Textbox
        self.poe_challenges_label = tk.Label(self.outputFrame)
        self.poe_challenges_label.configure(text="Challenges")
        self.poe_challenges_label.place(anchor="nw", width=190, x=10, y=190)

        self.poe_challenges_value = tk.Label(self.outputFrame)
        self.poe_challenges_value.place(anchor="nw", width=190, x=10, y=210)

        ## PoE Characters Label & Textbox
        self.poe_characters_label = tk.Label(self.outputFrame)
        self.poe_characters_label.configure(text="Characters")
        self.poe_characters_label.place(anchor="nw", width=190, x=200, y=190)

        self.poe_characters_value = tk.Label(self.outputFrame)
        self.poe_characters_value.place(anchor="nw", width=190, x=200, y=210)

        ## PoEcom Characer List Label & Textbox
        self.poecom_character_list_label = tk.Label(self.outputFrame)
        self.poecom_character_list_label.configure(text="Pathofexile.com Character List")
        self.poecom_character_list_label.place(anchor="nw", width=380, x=10, y=250)

        self.poecom_character_list_textbox = tk.Entry(self.outputFrame)
        self.poecom_character_list_textbox.place(anchor="nw", width=380, x=10, y=270)

        ## PoEcc Character List Label & Textbox
        self.poecc_character_list_label = tk.Label(self.outputFrame)
        self.poecc_character_list_label.configure(text="Poecc.com Character List")
        self.poecc_character_list_label.place(anchor="nw", width=380, x=10, y=300)

        self.poecc_character_list_textbox = tk.Entry(self.outputFrame)
        self.poecc_character_list_textbox.place(anchor="nw", width=380, x=10, y=320)

        ## Combined Character List Label & Textbox
        self.combined_character_list_label = tk.Label(self.outputFrame)
        self.combined_character_list_label.configure(text="Combined Character List")
        self.combined_character_list_label.place(anchor="nw", width=380, x=10, y=350)

        self.combined_character_list_textbox = tk.Entry(self.outputFrame)
        self.combined_character_list_textbox.place(anchor="nw", width=380, x=10, y=370)

        ## Blacklist Check Command Label & Textbox
        self.blacklist_check_command_label = tk.Label(self.outputFrame)
        self.blacklist_check_command_label.configure(text="Blacklist Check Command")
        self.blacklist_check_command_label.place(anchor="nw", width=380, x=10, y=400)

        self.blacklist_check_command_textbox = tk.Entry(self.outputFrame)
        self.blacklist_check_command_textbox.place(anchor="nw", width=380, x=10, y=420)

        # WindowFrame Configures
        self.outputFrame.configure(height=450, width=400)
        self.outputFrame.pack(side="top")
        self.windowFrame.configure(height=500, width=400)
        self.windowFrame.title("TFT Account Checker")

        # Main widget
        self.mainwindow = self.windowFrame

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = AccountChecker()
    app.run()
