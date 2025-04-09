import tkinter as tk
from tkinter import ttk, TclError
from tkinter.constants import SUNKEN, RAISED, HORIZONTAL, DISABLED, NORMAL
import pickle
import atexit
from xmlrpc.client import APPLICATION_ERROR

from Weapons import Tiers, W, SC, MC, U, O, BR
import random

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):

    def clearframe(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
    def disableframe(self, frame):
        for widget in frame.winfo_children():
            try:
                widget.config(state=DISABLED)
            except TclError:
                pass
    def enableframe(self, frame):
        for widget in frame.winfo_children():
            try:
                widget.config(state=NORMAL)
            except TclError:
                pass
    def select_level(self, level_name):
        for self.name, self.level in self.levels.items():
            if self.name == level_name:
                self.level.config(relief=tk.SUNKEN, state=tk.DISABLED)
                self.Level = level_name
            else:
                self.level.config(relief=RAISED, state=tk.NORMAL)
    def select_style(self, style_name):
        for self.sname, self.style in self.styles.items():
            if self.sname == style_name:
                self.style.config(relief=tk.SUNKEN, state=tk.DISABLED)
                self.Style = style_name
            else:
                self.style.config(relief=RAISED, state=tk.NORMAL)

            if self.Style != "Normal":
                self.disableframe(self.levelWindow)
                self.disableframe((self.sliderWindow))
                self.intheworks.place(x=600, y=190)
            else:
                self.enableframe(self.levelWindow)
                self.enableframe(self.sliderWindow)
                self.intheworks.place_forget()

    def select_bottom_window(self, bottomframe):
        for self.framename, self.frame in self.frames.items():
            if self.framename == bottomframe:
                self.frame.config(relief=tk.SUNKEN, state=DISABLED)
                if self.framename == "Main Settings":
                    self.BottomFrame1.place(x=1, y=225, width=864, height=333)
                else:
                    self.BottomFrame1.place_forget()
                if self.framename == "Saves":
                    self.BottomFrame2.place(x=1, y=225, width=864, height=333)
                else:
                    self.BottomFrame2.place_forget()

            else:
                self.frame.config(relief=RAISED, state=NORMAL)
    def printplayer(self, player, frame):
        pbuild = ""
        pbuild2 = ""
        count = 0
        for weapon in player:
            if count > 18:
                pbuild2 += "\n" + weapon[0]
            else:
                pbuild += "\n" + weapon[0]
                count = pbuild.count("\n")

        playerframe = tk.Frame(frame, border=3, relief='ridge')
        playerbuild = tk.Label(playerframe, text=f"Player {self.l}:" + pbuild, justify='left')
        playerframe.pack(side='left')
        playerbuild.grid(column=0, row=0, sticky='n')

        playerframe2 = tk.Frame(playerframe, bg='')
        playerbuild2 = tk.Label(playerframe2, text=pbuild2, justify='left')
        if count > 18:
            playerframe2.grid(column=1, row=0, sticky='n')
        playerbuild2.pack()
        self.l += 1
    def seed_encode(self, Player, Style, Level, SeedInts, Subclass, Main_Class):

        style_check = ["Normal", "Subclass", "Main Class"]
        level_check = ["Baby", "Normal", "Hard", "Impossible"]
        seed = "{:02d}".format(Player)
        style = str(style_check.index(Style))
        seed += style
        if style == "0":
            seed += str(level_check.index(Level))
        if style == "0":
            for ints in SeedInts:
                seed += "{:02d}".format(ints)
        if style == "1":
            for ints in Subclass:
                seed += "{:02d}".format(ints)
        if style == "2":
            for ints in Main_Class:
                seed += "{:02d}".format(ints)

        savefile = ["  " + self.seedname.get() + "                                       ", seed]
        self.seedname.delete(0, tk.END)
        with open("seeds.txt", "ab") as file:
            pickle.dump(savefile, file)
        self.seedlistbox.insert(tk.END, savefile)
    def seed_decode(self, seed):

        p = 0
        y = 0
        player = []
        style_check = ["Normal", "Subclass", "Main Class"]
        level_check = ["Baby", "Normal", "Hard", "Impossible"]

        # First 2 digits of seed is player count
        players = int(seed[0:2])

        # 3rd digit is the style
        style = style_check[int(seed[2])]

        # If the style is normal than use the 4th place as level
        if style == "Normal":
            level = level_check[int(seed[3])]
            seed = seed[4:len(seed)]
        else:
            level = ""
            seed = seed[3:len(seed)]

        while p < players:

            seedints = []
            if style == "Normal":
                x = 0
                while x < 18:
                    seedints.append(Tiers[x][int(seed[y:y + 2])])
                    y += 2
                    x += 1
                if level == "Impossible":
                    seedints.append(W[172])
            if style == "Subclass":
                seedints = [SC[int(seed)]]
                y += 2

            if style == "Main Class":
                seedints = [MC[int(seed[y:y + 2])]]
                y += 2

            player.append(seedints)
            p += 1
        self.l = 1
        if self.weaponframe.winfo_children():
            self.clearframe(self.weaponframe)
        for playa in player:
            self.printplayer(playa, self.weaponframe)
    def seed_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            selected_item = widget.get(selection[0])
            self.seed_decode(selected_item[1])
    def delete_seed(self):
        try:
            selection = self.seedlistbox.curselection()[0]
            self.seedlistbox.delete(selection)
            self.clearframe(self.weaponframe)
        except IndexError:
            pass
        with open("seeds.txt", "wb") as file:
            file.truncate(0)
        tempload = []
        for i in range(self.seedlistbox.size()):
            tempload.append(self.seedlistbox.get(i))

        with open("seeds.txt", "ab") as file:
            for seed in tempload:
                pickle.dump(seed, file)

    def randomize(self):
        try:
            if len(self.seedname.get()) == 0:
                self.nameplease.place(x=self.seednamex + 190, y=self.seednamey)
            else:

                self.nameplease.place_forget()
                #  self.generateButton.config(relief=SUNKEN, state=DISABLED)
                p = 0
                self.l = 1
                self.player = []
                self.seedints = []
                # randomizer
                while p < self.players.get():
                    # Standard Randomizer
                    if self.Style == "Normal":

                        build = []
                        y = 0
                        while y < len(Tiers):

                            choice = random.randint(0, len(Tiers[y]) - 1)
                            build.append(Tiers[y][choice])

                            if self.Level == "":
                                del self.Level
                            if self.Level == "Baby":
                                while (build[y][8] in (O[0], O[1], O[2], O[7], O[8])) or (build[y][7] in (U[0], U[1])):
                                    choice = random.randint(0, len(Tiers[y]) - 1)
                                    build[y] = Tiers[y][choice]
                            if self.Level == "Normal":
                                while build[y][8] in (O[0], O[1], O[7]) or (build[y][7] in U[0]):
                                    choice = random.randint(0, len(Tiers[y]) - 1)
                                    build[y] = Tiers[y][choice]
                            if self.Level == "Hard":
                                while build[y][8] in O[7]:
                                    choice = random.randint(0, len(Tiers[y]) - 1)
                                    build[y] = Tiers[y][choice]
                            if self.Level == "Impossible":
                                while build[y][7] in (U[5], U[6]):
                                    del build[y]
                                    choice = random.randint(0, len(Tiers[y]) - 1)
                                    build.append(Tiers[y][choice])

                            # Ensures it does not generate the same 2 summoning items
                            if len(build) == 14:
                                while (build[13][0] in build[12][0]) or build[13][0] == "Terraprisma":
                                    del build[13]

                                    choice = random.randint(0, len(Tiers[y]) - 1)
                                    build.append(Tiers[y][choice])

                            # Ensures it does not generate the same 2 throwable
                            if len(build) == 18:
                                while build[17][0] in build[16][0]:
                                    del build[17]

                                    choice = random.randint(0, len(Tiers[y]) - 1)
                                    build.append(Tiers[y][choice])
                            y += 1

                            self.seedints.append(choice)

                        if self.Level == "Impossible":
                            build.append(W[172])



                    # Subclass Randomizer
                    if self.Style == "Subclass":
                        pass
                        #
                        # self.subclass = []
                        # build = []
                        # y = 0
                        # choice = random.randint(1, len(SC) - 4)
                        # x = 0
                        # while choice == SC[2]:
                        #     choice = random.randint(1, len(SC -4))
                        # self.subclass.append(choice)
                        # if (choice == 1) or (choice == 2):
                        #
                        #     while x < len(W):
                        #
                        #         if SC[15] in W[x][4]:
                        #             build.append([W[x]])
                        #         x += 1
                        #
                        # while y < len(Tiers):
                        #     x = 0
                        #     while x < len(Tiers[y]):
                        #
                        #         if SC[choice] in Tiers[y][x][4]:
                        #             build.append(Tiers[y][x])
                        #
                        #         x += 1
                        #
                        #     y += 1
                     # Main Class Randomizer
                    if self.Style == "Main Class":
                         pass
                    #     build = []
                    #     y = 0
                    #     choice = random.randint(0, 4)
                    #     self.main_class = choice
                    #     x = 0
                    #     while y < len(Tiers):
                    #         x = 0
                    #         while x < len(Tiers[y]):
                    #             if MC[choice] in Tiers[y][x][3]:
                    #                 build.append(Tiers[y][x])
                    #             if MC[choice] == "TrueMelee":
                    #                 if MC[4] in Tiers[y][x][3]:
                    #                     build.append(Tiers[y][x])
                    #             if MC[choice] == "Ranger":
                    #                 if MC[5] in Tiers[y][x][3]:
                    #                     build.append(Tiers[y][x])
                    #             x += 1
                    #         y += 1

                    self.player.append(build)
                    del build
                    p += 1

                self.seed_encode(self.players.get(), self.Style, self.Level, self.seedints, self.subclass, self.main_class)
                if self.weaponframe.winfo_children():
                    self.clearframe(self.weaponframe)
                for player in self.player:
                    self.printplayer(player, self.weaponframe)

        except UnboundLocalError:
            pass
        except AttributeError:
            pass

    def __init__(self):
        super().__init__()

        self.subclass = ""
        self.main_class = ""
        self.seedints = []
        self.Style = ""
        self.Level = ""

        # Window settings
        self.title("Terraria Randomizer")
        self.iconbitmap("C:/Users/zachl/PycharmProjects/Terraria Randomizer/venv/icon.ico")
        self.geometry("864x558")
        self.resizable(False, False)

        # Top Frame
        topframe = tk.Frame(self, bg="lightgray", border=3, relief='groove')
        topframe.place(x=1, y=1, width=864, height=220)

        # Name entry thing
        self.seednamex = 5; self.seednamey = 160
        self.seedname = tk.Entry(topframe)
        seednamelabel = tk.Label(topframe, text="File Name:", bg='lightgray')
        seednamelabel.place(x=self.seednamex, y=self.seednamey)
        self.seedname.place(x=self.seednamex + 64, y=self.seednamey + 1)
        self.nameplease = tk.Label(topframe, text='Please name your file', fg='red', bg= 'lightgray')

        # in the works
        self.intheworks = tk.Label(topframe, text="In the Works", fg='red', bg='lightgray')
        self.email = tk.Label(topframe, text="""beta v1.6
v1 is currently in the works.""", bg='lightgray', fg='darkgray', justify='left')
        info = tk.Label(topframe, text="""The goal of the randomizer is to beat
moon lord and obtain every one of the
weapons listed.""", bg='lightgray', justify='left')
        info.place(x=10, y=70)
        self.email.place(x=10, y=10)

        # April 6, 2025
        # DONE make the individual player builds appear on a bottom frame except for subclass just showing up as ffffffffff

        # April 7, 2025
        # DONE finish the seed listbox and add a button to delete old save.

        # April 8, 2025
        # def Things Left to implement maybe
        # def start logging what I do every day.
        # def Box for version    <--4 spaces.... Most important.
        # def Rename seed (entry, button) I didn,t mean to name my file 2 big guys, and they bust on my eyes. :o
        # def Export seed (button, listbox) Share with friends.
        # def import seed (entry, button) Eat your friends
        # def button to mark seed as completed and move to new txt file #hahhahahhaahahahhahahhaahhaahhaahahh_imagine.
        # may bottom frame for advanced settings. What are the advanced settings? i d k.probly just randomize equips... but then I have to make data for every equipable item... kill me I need to do it. :(
        # def bottom frame for information/links. Send money pls UwU
        # def bottom frame for completed seeds # look I beat the game and was using the ruler :sunglasses_emoji:
        # def fix the seed decoding for main class and subclass seeds

        # April 9, 2025
        # doing another day make a scroll for the player build loadouts
        # click button to append seed to clipboard.
        # polish up what I have and start working on next version

        # Bottom frame selector
        frameselectbuttons = tk.Frame(self, bg='')
        frameselectbuttons.place(x=10, y=203)
        self.frames = {}
        self.frame_names = ["Main Settings", "Saves"]

        for frame_name in self.frame_names:
            self.frame = tk.Button(frameselectbuttons, text=frame_name, relief=RAISED, width=20, height=1,
                                   command=lambda n=frame_name: self.select_bottom_window(n))
            self.frame.pack(side='left', padx=2)
            self.frames[frame_name] = self.frame
            self.frames["Main Settings"].config(relief=SUNKEN, state=DISABLED)

        # Main Bottom Window
        self.BottomFrame1 = tk.Frame(self, bg="lightgray", borderwidth=3, relief="groove")
        self.BottomFrame1.place(x=1, y=225, width=864, height=333)

        # Window for randomizer style
        StyleWindow = tk.Frame(self.BottomFrame1, borderwidth=3, relief="groove", bg="lightgray")
        StyleWindow.place(x=397, y=5, width=457, height=258)

        self.generateButton = tk.Button(self.BottomFrame1, text="Generate", width=64, height=3, command=self.randomize)
        self.generateButton.place(x=397, y=265)
        styleButtons = tk.Frame(StyleWindow)
        styleButtons.grid(column=0, row=0)
        self.styles = {}
        self.style_names = ["Normal", "Subclass", "Main Class"]
        
        for sname in self.style_names:
            self.style = tk.Button(styleButtons, text=sname, relief=tk.RAISED, width=20, height=2,
                                   command=lambda n=sname: self.select_style(n))
            self.style.pack(side=tk.LEFT, padx=.4)
            self.styles[sname] = self.style
        ExplainWindow = """Normal:
Standard Randomizer, Utilizes the difficulties to the left, you will be allowed
weapons for every stage of the game, along with 2 summons, 2 sentries,
and 2 consumable weapons.

Subclass:
Recommended for playing with multiple people. Generates a random subclass for
you to play as.

Main Class:
Recommended for someone who just wants to play the game but cannot decide
what class they want to play as.
"""
        styleExplain = tk.Label(StyleWindow, text=ExplainWindow, justify='left', bg="lightgray")
        styleExplain.grid(column=0, row=1)
            
        # Window for Player slider
        self.PlayersWindow = tk.Frame(self.BottomFrame1, borderwidth=3, relief="groove", bg="lightgray")
        self.PlayersWindow.place(x=4, y=5)
        playerLabel = tk.Label(self.PlayersWindow, text="Players", bg="lightgray")
        playerLabel.pack()
        self.players = tk.Scale(self.PlayersWindow, from_=1, to=4, orient=HORIZONTAL, length=376, border=2,
                                relief="raised")
        self.players.pack()
        
        
        # Window for difficulty selector
        self.levelWindow = tk.Frame(self.BottomFrame1, bg="lightgray", borderwidth=3, relief="groove", width=378)
        self.levelWindow.place(x=4, y=75)
        
        self.sliderWindow = tk.Frame(self.levelWindow, bg="lightgray")
        self.sliderWindow.grid(column=1, row=0)
        self.levels = {}
        self.level_names = ["Baby", "Normal", "Hard", "Impossible"]
        for name in self.level_names:
            self.level = tk.Button(self.sliderWindow, text=name, relief=tk.RAISED, width=12, height=2,
                                   command=lambda n=name: self.select_level(n), state=DISABLED)
            self.level.pack(side=tk.LEFT, padx=1)
            self.levels[name] = self.level

        explainWindow = tk.Frame(self.levelWindow)
        explainWindow.grid(column=1, row=1)
        lvlExplain = """Baby:
Does not include any hard to obtain, or trash weapons.

Normal:
Includes everything except a couple of items that could
softlock the game. (ruler)

Hard:
Includes all weapons except the most most overpowered ones

Impossible:
Might be tough
"""
        lvlExplain = tk.Label(explainWindow, text=lvlExplain, justify='left', bg="lightgray")
        lvlExplain.pack()

        # Saves Window
        self.BottomFrame2 = tk.Frame(self, bg="lightgray", borderwidth=3, relief="groove")


        self.seedframe = tk.Frame(self.BottomFrame2, border=3, relief='groove')
        self.seedframe.place(x=5, y=5)
        seedscrollbar = tk.Scrollbar(self.seedframe)
        seedframelabel = tk.Label(self.seedframe, text="Saves:")
        seedframelabel.pack()
        seedscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.seedslist = []
        try:
            with open("seeds.txt", "rb") as file:
                while True:
                    try:
                        self.seedslist.append(pickle.load(file))
                    except EOFError:
                        break
        except:
            pass
        self.seedlistbox = tk.Listbox(self.seedframe, height=16, width=20 ,border=2, yscrollcommand=seedscrollbar.set)
        self.seedlistbox.xview_scroll(500, tk.UNITS)
        self.seedlistbox.pack(padx=1)
        seedscrollbar.config(command=self.seedlistbox.yview)
        for seed in self.seedslist:
            self.seedlistbox.insert(tk.END, seed)

        self.seedlistbox.bind('<<ListboxSelect>>', self.seed_select)

        seeddeletebutton = tk.Button(self.seedframe, text="Delete", command=self.delete_seed, width=16)
        seeddeletebutton.pack()

        # window to print build for 1 player
        self.weaponframe = tk.Frame(self.BottomFrame2, bg='lightgray')
        self.weaponframe.place(x=853, y=5, anchor='ne')
        # self.weaponframe = tk.Canvas(self.BottomFrame2, bg='lightgray', width=682, height=305, border=3, relief='groove')
        # self.weaponframe.place(x=160, y=5)


if __name__ == "__main__":
    main()