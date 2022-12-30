from tkinter import *
from tkinter import ttk
import random


def random_color(nRegions):
    colors = ['blue']
    for i in range(nRegions - 1):
        colors.append('#%06X' % random.randint(0, 0xFFFFFF))
    return colors


class MyVisualization:
    def __init__(self, myMap, nRegions, agentLocation):
        self.myMap = myMap
        self.colors = random_color(nRegions)

        self.root = Tk()
        self.root.title("Map Visualization")
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack()  # tabs.pack(fill=BOTH, expand=TRUE)

        self.lst_tabs = []

        self.root.geometry("1500x800+150+100")

        # init introduction tab
        introFrame = ttk.Frame(self.tabs)
        self.tabs.add(introFrame, text='Introduction')
        self.lst_tabs.append(introFrame)
        Label(introFrame, text='Welcome to the visualization of the map', font=(
            'Arial', 20)).grid(row=0, column=0, columnspan=2)
        Label(introFrame, text='Besides the regions, the map also has some following parts:', font=(
            'Arial', 20)).grid(row=1, column=0, columnspan=2)
        Label(introFrame, text='1. The agent, denote by "A"', font=(
            'Arial', 20)).place(x=0, y=80)
        Label(introFrame, text='2. The pirate, denote by "Pi"', font=(
            'Arial', 20)).place(x=0, y=120)
        Label(introFrame, text='3. The yellow cell illustrates the treasure', font=(
            'Arial', 20)).place(x=0, y=160)
        Label(introFrame, text='4. The green cells illustrates the hints given by the pirate', font=(
            'Arial', 20)).place(x=0, y=200)
        Label(introFrame, text='5. The white cells illustrates those areas has been removed by the agent', font=(
            'Arial', 20)).place(x=0, y=240)

        # init first R1 tab
        curFrame = ttk.Frame(self.tabs)
        self.tabs.add(curFrame, text='R1')
        self.lst_tabs.append(curFrame)
        for i in range(len(self.myMap)):
            for j in range(len(self.myMap[i])):
                if self.myMap[i][j] == '0':
                    Label(curFrame, text=self.myMap[i][j], bg='#e5e4e3', fg='blue').grid(
                        row=i, column=j)
                elif 'T' in myMap[i][j]:
                    Label(curFrame, text=self.myMap[i][j], bg="yellow", fg=self.colors[int(
                        self.myMap[i][j][0])]).grid(row=i, column=j)
                else:
                    Label(curFrame, text=self.myMap[i][j], bg="#e5e4e3", fg=self.colors[int(
                        self.myMap[i][j][0])]).grid(row=i, column=j)

        Label(curFrame, text='A', bg='#b0e0e6', fg='red').grid(
            row=agentLocation[0], column=agentLocation[1])

    def showVisualization(self):
        self.root.mainloop()

    def updateHintToTab(self, myMap, nRound, listOfTilesHint, agentLocation, pirateLocation, isPirateFree):
        curFrame = self.lst_tabs[nRound]
        for tile in listOfTilesHint:
            tile_x = tile // len(myMap[0])
            tile_y = tile % len(myMap[0])
            if 'T' in self.myMap[tile_x][tile_y]:
                Label(curFrame, text=self.myMap[tile_x][tile_y], bg="yellow", fg=self.colors[int(
                    self.myMap[tile_x][tile_y][0])]).grid(row=tile_x, column=tile_y)
            elif agentLocation[0] == tile_x and agentLocation[1] == tile_y:
                continue
            elif isPirateFree and pirateLocation[0] == tile_x and pirateLocation[1] == tile_y:
                Label(curFrame, text='Pi', bg='#b0e0e6', fg='black').grid(
                    row=pirateLocation[0], column=pirateLocation[1])
            else:
                Label(curFrame, text=self.myMap[tile_x][tile_y], bg='green', fg=self.colors[int(
                    self.myMap[tile_x][tile_y][0])]).grid(row=tile_x, column=tile_y)

    def addNewTab(self, myMap, nRound, removedTiles, agentLocation, pirateLocation, isPirateFree):
        curFrame = ttk.Frame(self.tabs)
        self.tabs.add(curFrame, text=f'R{nRound}')
        self.lst_tabs.append(curFrame)

        for i in range(len(self.myMap)):
            for j in range(len(self.myMap[i])):
                if self.myMap[i][j] == '0':
                    Label(curFrame, text=self.myMap[i][j], bg='#e5e4e3', fg='blue').grid(
                        row=i, column=j)
                elif 'T' in myMap[i][j]:
                    Label(curFrame, text=self.myMap[i][j], bg="yellow", fg=self.colors[int(
                        self.myMap[i][j][0])]).grid(row=i, column=j)
                else:  # ececec
                    Label(curFrame, text=self.myMap[i][j], bg="#e5e4e3", fg=self.colors[int(
                        self.myMap[i][j][0])]).grid(row=i, column=j)

        Label(curFrame, text='A', bg='#b0e0e6', fg='red').grid(
            row=agentLocation[0], column=agentLocation[1])

        if isPirateFree:
            Label(curFrame, text='Pi', bg='#b0e0e6', fg='black').grid(
                row=pirateLocation[0], column=pirateLocation[1])

        for tile in removedTiles:
            tile_x = tile // len(myMap[0])
            tile_y = tile % len(myMap[0])
            if self.myMap[tile_x][tile_y] == '0' or (agentLocation[0] == tile_x and agentLocation[1] == tile_y) or (isPirateFree and pirateLocation[0] == tile_x and pirateLocation[1] == tile_y):
                continue
            elif 'T' in self.myMap[tile_x][tile_y]:
                Label(curFrame, text=self.myMap[i][j], bg="yellow", fg=self.colors[int(
                    self.myMap[tile_x][tile_y][0])]).grid(row=tile_x, column=tile_y)
            elif 'M' in self.myMap[tile_x][tile_y]:
                Label(curFrame, text='_M', bg='white', fg='brown').grid(
                    row=tile_x, column=tile_y)
            else:
                Label(curFrame, text='__', bg='white', fg='white').grid(
                    row=tile_x, column=tile_y)

    def updateLastHintToTab(self, nRound, listOfTilesHint, agentLocation, pirateLocation, isPirateFree):
        curFrame = self.lst_tabs[nRound]
        for tile in listOfTilesHint:
            tile_x = tile // len(self.myMap[0])
            tile_y = tile % len(self.myMap[0])
            if 'T' in self.myMap[tile_x][tile_y]:
                Label(curFrame, text=self.myMap[tile_x][tile_y], bg="yellow", fg=self.colors[int(
                    self.myMap[tile_x][tile_y][0])]).grid(row=tile_x, column=tile_y)
            elif agentLocation[0] == tile_x and agentLocation[1] == tile_y:
                continue
            elif isPirateFree and pirateLocation[0] == tile_x and pirateLocation[1] == tile_y:
                Label(curFrame, text='Pi', bg='#b0e0e6', fg='black').grid(
                    row=pirateLocation[0], column=pirateLocation[1])
            else:
                Label(curFrame, text=self.myMap[tile_x][tile_y], bg='green', fg=self.colors[int(
                    self.myMap[tile_x][tile_y][0])]).grid(row=tile_x, column=tile_y)

    def addLastTab(self, isWin):
        curFrame = ttk.Frame(self.tabs)
        self.tabs.add(curFrame, text='Result')
        self.lst_tabs.append(curFrame)
        if isWin:
            Label(curFrame, text='WIN', bg='green', fg='white').pack()
        else:
            Label(curFrame, text='LOSE', bg='red', fg='white').pack()
