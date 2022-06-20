import tkinter as tk
import tkinter.ttk as ttk

from numpy import char
import resources as res
import config as cfg


class AccountChecker:
    def __init__(self, master=None):
        if cfg.DEBUG:
            print("Debug mode is ON!")

        # Main window
        self.windowFrame = tk.Tk() if master is None else tk.Toplevel(master)

        # Input Frame
        self.inputFrame = tk.Frame(self.windowFrame)

        # Input Frame Elements
        ## Discord ID Label & Textbox
        self.discord_id_label = tk.Label(self.inputFrame)
        self.discord_id_label.configure(anchor="n", text="Discord User ID", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.discord_id_label.place(anchor="nw", relx=0.0, width=140, x=10, y=10)

        self.discord_id_textbox = tk.Entry(self.inputFrame)
        self.discord_id_textbox.configure(justify="center", font=cfg.value_font)
        if cfg.DEBUG:
            self.discord_id_textbox.insert("0", "1231231231231233")
        self.discord_id_textbox.place(anchor="nw", width=240, x=150, y=10)

        ## PoE Account Label & Textbox
        self.poe_account_name_label = tk.Label(self.inputFrame)
        self.poe_account_name_label.configure(anchor="n", text="PoE Account Name", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poe_account_name_label.place(anchor="nw", relx=0.0, width=140, x=10, y=40)

        self.poe_account_name_textbox = tk.Entry(self.inputFrame)
        self.poe_account_name_textbox.configure(justify="center", font=cfg.value_font)
        if cfg.DEBUG:
            self.poe_account_name_textbox.insert("0", "Reshike")
        self.poe_account_name_textbox.place(anchor="nw", width=240, x=150, y=40)

        ## Check Account Button
        self.check_account_button = tk.Button(self.inputFrame)
        self.check_account_button.configure(text="Check Account", command=lambda: res.check_account(self), font=cfg.button_font)
        self.check_account_button.place(anchor="nw", width=380, x=10, y=70)


        ## Input Error Label & Textbox
        self.input_error_label = tk.Label(self.inputFrame)
        self.input_error_label.configure(anchor="n", foreground=cfg.error_font_color, text="", font=cfg.error_font, bg=cfg.bg_color)
        self.input_error_label.place(anchor="nw", relx=0.0, width=380, x=10, y=95)

        # Pack Input Frame
        self.inputFrame.configure(height=120, width=400, bg=cfg.bg_color)
        self.inputFrame.pack(side="top")

        ## Output Frame
        self.outputFrame = tk.Frame(self.windowFrame)

        # Output Frame Elements
        ## Discord Account Age Label & Textbox
        self.discord_account_age_label = tk.Label(self.outputFrame)
        self.discord_account_age_label.configure(text="Discord Account Age", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.discord_account_age_label.place(anchor="nw", width=190, x=10, y=0)

        self.discord_account_age_value = tk.Label(self.outputFrame)
        self.discord_account_age_value.configure(font=cfg.value_font, bg=cfg.bg_color)
        self.discord_account_age_value.place(anchor="nw", width=190, x=10, y=20)

        ## PoE Account Label & Textbox
        self.poe_account_label = tk.Label(self.outputFrame)
        self.poe_account_label.configure(text="PoE Account", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poe_account_label.place(anchor="nw", width=190, x=200, y=0)

        self.poe_account_value = tk.Label(self.outputFrame)
        self.poe_account_value.configure(font=cfg.value_font, bg=cfg.bg_color)
        self.poe_account_value.place(anchor="nw", width=190, x=200, y=20)

        ## PoE Account Private Label & Textbox
        self.poe_account_private_label = tk.Label(self.outputFrame)
        self.poe_account_private_label.configure(text="PoE Account Private", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poe_account_private_label.place(anchor="nw", width=190, x=10, y=50)

        self.poe_account_private_value = tk.Label(self.outputFrame)
        self.poe_account_private_value.configure(font=cfg.value_font, bg=cfg.bg_color)
        self.poe_account_private_value.place(anchor="nw", width=190, x=10, y=70)

        ## PoE Account Age Label & Textbox
        self.poe_account_age_label = tk.Label(self.outputFrame)
        self.poe_account_age_label.configure(text="PoE Account Age", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poe_account_age_label.place(anchor="nw", width=190, x=200, y=50)

        self.poe_account_age_value = tk.Label(self.outputFrame)
        self.poe_account_age_value.configure(font=cfg.value_font, bg=cfg.bg_color)
        self.poe_account_age_value.place(anchor="nw", width=190, x=200, y=70)

        ## PoE Guild Label & Textbox
        self.poe_guild_label = tk.Label(self.outputFrame)
        self.poe_guild_label.configure(text="Guild", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poe_guild_label.place(anchor="nw", width=190, x=10, y=100)

        self.poe_guild_value = tk.Label(self.outputFrame)
        self.poe_guild_value.configure(font=cfg.value_font, bg=cfg.bg_color)
        self.poe_guild_value.place(anchor="nw", width=190, x=10, y=120)

        ## PoE Supporter Pack Label & Textbox
        self.poe_supporter_pack_label = tk.Label(self.outputFrame)
        self.poe_supporter_pack_label.configure(text="Supporter Packs", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poe_supporter_pack_label.place(anchor="nw", width=190, x=200, y=100)

        self.poe_supporter_pack_value = tk.Label(self.outputFrame)
        self.poe_supporter_pack_value.configure(font=cfg.value_font, bg=cfg.bg_color)
        self.poe_supporter_pack_value.place(anchor="nw", width=190, x=200, y=120)

        ## PoE Challenges Label & Textbox
        self.poe_challenges_label = tk.Label(self.outputFrame)
        self.poe_challenges_label.configure(text="Challenges", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poe_challenges_label.place(anchor="nw", width=190, x=10, y=150)

        self.poe_challenges_value = tk.Label(self.outputFrame)
        self.poe_challenges_value.configure(font=cfg.value_font, bg=cfg.bg_color)
        self.poe_challenges_value.place(anchor="nw", width=190, x=10, y=170)

        ## PoE Characters Label & Textbox
        self.poe_characters_label = tk.Label(self.outputFrame)
        self.poe_characters_label.configure(text="Characters", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poe_characters_label.place(anchor="nw", width=190, x=200, y=150)

        self.poe_characters_value = tk.Label(self.outputFrame)
        self.poe_characters_value.configure(font=cfg.value_font, bg=cfg.bg_color)
        self.poe_characters_value.place(anchor="nw", width=190, x=200, y=170)

        ## PoEcom Characer List Label & Textbox
        self.poecom_character_list_label = tk.Label(self.outputFrame)
        self.poecom_character_list_label.configure(text="Pathofexile.com Character List", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poecom_character_list_label.place(anchor="nw", width=380, x=10, y=200)

        self.poecom_character_list_textbox = tk.Entry(self.outputFrame)
        self.poecom_character_list_textbox.configure(font=cfg.value_font, state="readonly")
        self.poecom_character_list_textbox.bind("<Button-1>", self.copy_to_clipboard)
        self.poecom_character_list_textbox.place(anchor="nw", width=380, x=10, y=220)

        ## PoEcc Character List Label & Textbox
        self.poecc_character_list_label = tk.Label(self.outputFrame)
        self.poecc_character_list_label.configure(text="Poecc.com Character List", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.poecc_character_list_label.place(anchor="nw", width=380, x=10, y=250)

        self.poecc_character_list_textbox = tk.Entry(self.outputFrame)
        self.poecc_character_list_textbox.configure(font=cfg.value_font, state="readonly")
        self.poecc_character_list_textbox.bind("<Button-1>", self.copy_to_clipboard)
        self.poecc_character_list_textbox.place(anchor="nw", width=380, x=10, y=270)

        ## Combined Character List Label & Textbox
        self.combined_character_list_label = tk.Label(self.outputFrame)
        self.combined_character_list_label.configure(text="Combined Character List", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.combined_character_list_label.place(anchor="nw", width=380, x=10, y=300)

        self.combined_character_list_textbox = tk.Entry(self.outputFrame)
        self.combined_character_list_textbox.configure(font=cfg.value_font, state="readonly")
        self.combined_character_list_textbox.bind("<Button-1>", self.copy_to_clipboard)
        self.combined_character_list_textbox.place(anchor="nw", width=380, x=10, y=320)

        ## Blacklist Check Command Label & Textbox
        self.blacklist_check_command_label = tk.Label(self.outputFrame)
        self.blacklist_check_command_label.configure(text="Blacklist Check Command", font=cfg.label_font, bg=cfg.bg_color, foreground=cfg.label_font_color)
        self.blacklist_check_command_label.place(anchor="nw", width=380, x=10, y=350)

        self.blacklist_check_command_textbox = tk.Entry(self.outputFrame)
        self.blacklist_check_command_textbox.configure(font=cfg.value_font, state="readonly")
        self.blacklist_check_command_textbox.bind("<Button-1>", self.copy_to_clipboard)
        self.blacklist_check_command_textbox.place(anchor="nw", width=380, x=10, y=370)

        # WindowFrame Configures
        self.outputFrame.configure(height=400, width=400, bg=cfg.bg_color)
        self.outputFrame.pack(side="top")
        self.windowFrame.configure(height=520, width=400, bg=cfg.bg_color)
        self.windowFrame.title("TFT Account Checker")

        # Main widget
        self.mainwindow = self.windowFrame

    def run(self):
        self.mainwindow.mainloop()

    def copy_to_clipboard(self, event):
        textbox_value = event.widget.get()
        self.windowFrame.clipboard_clear()
        self.windowFrame.clipboard_append(textbox_value)
        self.windowFrame.after(50, self.select_all, event.widget)

    def select_all(self, widget):
        widget.select_range(0, 'end')
        widget.icursor('end')

    def create_character_window(self, poe_account):
        self.character_window = tk.Toplevel(self.windowFrame)
        self.character_window.wm_title(f"Characters of {poe_account.poe_account_name}")
        self.character_table = ttk.Treeview(self.character_window, show='headings', height=len(poe_account.characters))
        self.character_table.pack(fill="both", side="top")
        self.character_window.configure(height=300, width=340)
        self.character_window.pack_propagate(1)

        self.character_table['columns'] = ('character_name', 'league', 'class', 'level')

        self.character_table.column("character_name", anchor=tk.CENTER, width=130)
        self.character_table.column("league", anchor=tk.CENTER, width=80)
        self.character_table.column("class", anchor=tk.CENTER, width=80)
        self.character_table.column("level", anchor=tk.CENTER, width=50)

        self.character_table.heading("character_name", text="Character Name", anchor=tk.CENTER)
        self.character_table.heading("league", text="League", anchor=tk.CENTER)
        self.character_table.heading("class", text="Class", anchor=tk.CENTER)
        self.character_table.heading("level", text="Level", anchor=tk.CENTER)

        counter = 0
        for character in poe_account.characters:
            self.add_character_to_table(self.character_table, character, counter)
            counter += 1

        self.character_table.tag_configure('league_highlevel', background=cfg.league_highlevel_color)
        self.character_table.tag_configure('standard_highlevel', background=cfg.standard_highlevel_color)
        self.character_table.tag_configure('lowlevel', background=cfg.lowlevel_color)

    def add_character_to_table(self, table, character_data, counter):
        if "Standard" not in character_data["league"] and int(character_data["level"]) >= cfg.min_character_level:
            table.insert(parent='', index='end', iid=counter, text='', values=(character_data["name"], character_data["league"], character_data["class"], character_data["level"]), tags=('league_highlevel',))
        elif "Standard" in character_data["league"] and int(character_data["level"]) >= cfg.min_character_level:
            table.insert(parent='', index='end', iid=counter, text='', values=(character_data["name"], character_data["league"], character_data["class"], character_data["level"]), tags=('standard_highlevel',))
        else:
            table.insert(parent='', index='end', iid=counter, text='', values=(character_data["name"], character_data["league"], character_data["class"], character_data["level"]), tags=('lowlevel',))


if __name__ == "__main__":
    app = AccountChecker()
    app.run()
