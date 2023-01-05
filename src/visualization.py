import customtkinter as ctk
from tkinter import *
import random

from queue import Queue

charColors = {
    'P': 'gray90',
    'T': 'gold',
    'M': 'black',
    'A': 'red'
}

bgColors = {
    'A': 'yellow',
    'T': 'gray30'
}

_colors = ["steel blue", "tan4", "HotPink4", "burlywood3", "medium sea green", "PaleGreen4", "LightPink3",
          "sienna1", "sienna3", "light goldenrod", "CadetBlue4", "blue violet", "sandy brown",
          "dark khaki"]

def random_color(nRegions):
    colors = ['blue']
    if nRegions - 1 > len(_colors):
        temp = random.sample(range(0, 0xFFFFFF + 1, 300), k=nRegions - 1)
        for c in temp:
            colors.append('#%06X' % c)
    else:
        colors += random.sample(_colors, k=nRegions - 1)
    return colors

class Visualization:
    def __init__(self, myMap, nRegions):
        
        self.map = myMap
        self.regions = nRegions
        self.tabsList = []
        
        self.w = len(myMap)
        self.h = len(myMap[0])
        self.colors = random_color(nRegions)
        
        self.root = ctk.CTk()
        self.root.title("Map Visualization")
        self.root.geometry("1600x1000")
        
        ctk.set_appearance_mode("dark")
        
        self.tabs = ctk.CTkTabview(self.root)
        self.tabs.pack()
        
        self.cell_font_size = (
            10 if self.w >= 64 else 14 if self.w >= 32 else 22
        )
        
        # Create frame Introduction
        intro = self.tabs.add("Introduction")
        
        ctk.CTkLabel(master=intro, text='Welcome to the visualization of the map', font=(
            'Roboto', 20)).grid(row=0, column=0, columnspan=2)
        ctk.CTkLabel(master=intro, text='Besides the regions, the map also has some following parts:', font=(
            'Roboto', 20)).grid(row=1, column=0, columnspan=2)
        ctk.CTkLabel(master=intro, text='1. The agent, denote by "A"', font=(
            'Roboto', 20)).place(x=0, y=80)
        ctk.CTkLabel(master=intro, text='2. The pirate, denote by "Pi"', font=(
            'Roboto', 20)).place(x=0, y=120)
        ctk.CTkLabel(master=intro, text='3. The yellow cell illustrates the treasure', font=(
            'Roboto', 20)).place(x=0, y=160)
        ctk.CTkLabel(master=intro, text='4. The green cells illustrates the hints given by the pirate', font=(
            'Roboto', 20)).place(x=0, y=200)
        ctk.CTkLabel(master=intro, text='5. The white cells illustrates those areas has been removed by the agent', font=(
            'Roboto', 20)).place(x=0, y=240)
        
        self.tabsList.append(intro)
        
        self.tabs.set("Introduction")
        
    def createNewTab(self, nRound, agent, pirate, treasure, hintTiles, removeTiles, freed, logs):
        curTab = self.tabs.add(f"R{nRound}")
        
        mapSize = 900
        cellWidth = mapSize // self.w
        cellHeight = mapSize // self.h
        
        # create map display
        mapDisplay = ctk.CTkFrame(curTab)
        mapDisplay.grid(row=0, column=0, padx=20, pady=20)
        
        # horizontal grid of map display
        xcoor = ctk.CTkCanvas(master=mapDisplay, width=mapSize, height=cellHeight,
                              bg='gray30', highlightthickness=0)
        xcoor.grid(row=0, column=1)
        
        # vertical grid of map display
        ycoor = ctk.CTkCanvas(master=mapDisplay, width=cellWidth, height=mapSize,
                              bg='gray30', highlightthickness=0)
        ycoor.grid(row=1, column=0)
        
        # the map
        map = ctk.CTkCanvas(master=mapDisplay, width=mapSize, height=mapSize, highlightthickness=0)
        map.grid(row=1, column=1)
        
        for r in range(self.w):
            for c in range(self.h):
                cell = r * self.w + c
                
                cellType = None if self.map[r][c][-1] not in ['M', 'P'] else self.map[r][c][-1]
                region = int(self.map[r][c]) if cellType is None and 'T' not in self.map[r][c] else int(self.map[r][c][:-1])
                
                if r == 0:
                    xcoor.create_text((c + 0.5)*cellWidth,
                                        0.5 * cellHeight,
                                        text=c,
                                        anchor="center",
                                        font=("Roboto bold",
                                            self.cell_font_size
                                        ),
                                        tags="text",
                                        fill="white")
                if c == 0:
                    ycoor.create_text(0.5 * cellWidth,
                                        (r + 0.5) * cellHeight,
                                        text=r,
                                        anchor="center",
                                        font=("Roboto bold",
                                            self.cell_font_size
                                        ),
                                        tags="text",
                                        fill="white")
                if cell in hintTiles:
                    map.create_rectangle(c * cellWidth, # x top left corner
                                            r * cellHeight,  # y top left corner
                                            # x bot right corner
                                            (c+1) * \
                                            cellWidth,
                                            # y bot right corner
                                            (r+1) * \
                                            cellHeight,
                                            tags="hint",
                                            outline='red',
                                            fill = 'thistle4' if cell in removeTiles and region != 0 else self.colors[region])
                else:
                    map.create_rectangle(c * cellWidth,  # y top left corner
                                            r * cellHeight,  # x top left corner
                                            # y bot right corner
                                            (c+1) * \
                                            cellWidth,
                                            # x bot right corner
                                            (r+1) * \
                                            cellHeight,
                                            fill = 'thistle4' if cell in removeTiles and region != 0 else self.colors[region])
                
                if region == 0:
                    map.create_rectangle(c * cellWidth,  # y top left corner
                                            r * cellHeight,  # x top left corner
                                            # y bot right corner
                                            (c+1) * \
                                            cellHeight,
                                            # x bot right corner
                                            (r+1) * \
                                            cellWidth,
                                            tags="water",
                                            fill = self.colors[region])
                # treasure
                if treasure == cell:
                    map.create_rectangle((c+0.15) * cellWidth,
                                            (r+0.15) * cellHeight,
                                            (c+0.85) *
                                            cellWidth,
                                            (r+0.85) *
                                            cellHeight,
                                            tags='agent',
                                            fill="red")
                    
                    map.create_text((c+0.5) * cellWidth,
                                        (r+0.5) * cellHeight,
                                        text='T',
                                        anchor="center",
                                        font=(
                                            "Roboto bold", self.cell_font_size
                                        ),
                                        tags="text",
                                        fill=charColors['T']
                                    )
                
                if cellType is not None:
                    map.create_text((c+0.5) * cellWidth,
                                        (r+0.5) * cellHeight,
                                        text=cellType,
                                        anchor="center",
                                        font=(
                                            "Roboto bold", self.cell_font_size
                                        ),
                                        tags="text",
                                        fill=charColors[cellType]
                                    )
                
                if agent == cell:
                    map.create_rectangle((c) * cellWidth,
                                            (r + 0.5) * cellHeight,
                                            (c+0.5) *
                                            cellWidth,
                                            (r + 1) *
                                            cellHeight,
                                            tags='agent',
                                            fill="yellow")

                    map.create_text((c+0.25)*cellWidth,
                                        (r+0.75) *
                                        cellHeight,
                                        text='A',
                                        anchor="center",
                                        font=("Roboto bold",
                                                self.cell_font_size - 5),
                                        tags="text",
                                        fill=charColors['A'])
                
                if freed and pirate == cell:
                    map.create_rectangle((c+0.5)*cellWidth,
                                            (r + 0.5) * cellHeight,
                                            (c+1) *
                                            cellWidth,
                                            (r+1) *
                                            cellHeight,
                                            tags='agent',
                                            fill="PaleVioletRed4")

                    map.create_text((c+0.75)*cellWidth,
                                        (r+0.75) *
                                        cellHeight,
                                        text='Pi',
                                        anchor="center",
                                        font=("Roboto bold",
                                                self.cell_font_size - 5),
                                        tags="text",
                                        fill="black")
                map.tag_raise("water")
                map.tag_raise("hint")
                map.tag_raise("agent")
                map.tag_raise("text")
                    
        # create log
        log = ctk.CTkFrame(curTab)
        log.grid(row=0, column=1, padx=20, pady=20)
    
        header = ctk.CTkLabel(log, text="LOGS", font=("Roboto", 24))
        header.grid(row=0, column=0)
        
        textBox = ctk.CTkTextbox(log, width=500, height=500, font=("Roboto", 15))
        textBox.grid(row=1, column=0, pady=10)
        textBox.configure(state="normal")
        
        for s in logs:
            textBox.insert(ctk.END, f"> {s}\n")
            
        textBox.configure(state="disabled")
        
    def addLastTab(self, isWin):
        curFrame = self.tabs.add("Result")
        if isWin:
            Label(curFrame, text='WIN', bg='green',
                  fg='white', font=('Roboto', 20)).pack()
        else:
            Label(curFrame, text='LOSE', bg='red',
                  fg='white', font=('Roboto', 20)).pack()
        
    def showVisualization(self):
        self.root.mainloop()