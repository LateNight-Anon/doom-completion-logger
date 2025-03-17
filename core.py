def installLibrary(moduleName: str) -> None: 
    from subprocess import check_call
    from sys import executable
    check_call([executable, "-m", "pip", "install", moduleName])
    print('.', end = '')
    match moduleName:
        case "pillow": from PIL import ImageTk, Image
        case "customtkinter": from customtkinter import CTk, CTkScrollbar, CTkScrollableFrame, CTkLabel, CTkButton, CTkEntry, CTkCanvas, CTkRadioButton, set_appearance_mode, CTkSlider
        case "pygame": from pygame import mixer

print("booting.", end = '')
try:
    from sqlite3 import connect
    from tkinter import *
    from tkinter import messagebox, font, filedialog, ttk
    try: from customtkinter import CTk, CTkScrollbar, CTkScrollableFrame, CTkLabel, CTkButton, CTkEntry, CTkCanvas, CTkRadioButton, set_appearance_mode, CTkSlider
    except ModuleNotFoundError: installLibrary("customtkinter")
    from csv import reader
    from hashlib import sha3_384, sha256
    from json import *
    from threading import Thread
    from time import sleep
    from typing import List, Tuple, Dict
    from math import ceil
    try: from PIL import ImageTk, Image
    except ModuleNotFoundError: installLibrary("pillow")
    try:
        from os import environ #os is exclusively used for stopping the pygame welcome message
        environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #stops the pygame welcome message from printing
        from pygame import mixer
    except ModuleNotFoundError: installLibrary("pygame")
    print('.', end = '')
except ModuleNotFoundError:
    print("your installation of python3 is missing critical standard modules")
    exit()
print('.')
print("complete")

#custom errors
class rangeError(Exception): pass

hideNoWadLabel = lambda: noWadMsg.place(x = 1000, y = 0)
showNoWadLabel = lambda: noWadMsg.place(x = 1000, y = 0)
playSound = lambda fileName: [mixer.music.load(fileName), mixer.music.play()]
clearFile = lambda fileName: open(fileName, 'w').close() #abstraction to wipe a file

#label object that will exclusively be placed on the canvas
class canvasLabel:
    construct = xPos = yPos = txt = None #all attributes

    def __init__(self, canvas: int, xPos: int, yPos: int, txt: str, colorMode: str) -> None:
        self.xPos = xPos
        self.yPos = yPos
        self.txt = txt
        self.construct = showcaseFrames[canvas].create_text(xPos, yPos, text = txt, fill = colorMode, font = ("Arial", 10)) #the label itself

    #methods
    def getXPostion(self) -> int: return self.xPos
    def getYPostion(self) -> int: return self.yPos
    def dependantPlace(self, xPos: int, yPos: int) -> None: self.construct.place(x = xPos, y = yPos)
    def remove(self) -> None: self.construct.destroy()

class quickCreateWindow(Tk): #unfinished
    def __init__(self, title: str, geometry: str, resizableX: bool, resizableY: bool) -> None:
        self.win = CTk()
        self.win.title(title)
        self.win.geometry(geometry)
        self.win.resizable(width = resizableX, height = resizableY)
    
    def title(self, text: str) -> None: self.win.title(text)
    def geometry(self, dimensions: str = None, x: int = None, y: int = None) -> None: 
        if dimensions != None: self.win.geometry(dimensions)
        else: self.win.geometry(f"{x}x{y}")

def fatalError(errorID: str) -> None:
    messagebox.showinfo(title = "fatal error", message = "fatal error detected\ncontact admins with error code\nerrorCode: " + errorID)
    [app.destroy(), exit()]

def createErrorMessage(canvas: Tk, message: str) -> None:
    errorMsg = CTkLabel(canvas, text = message, font = ("Arial", 25), fg_color = "red")
    errorMsg.place(x = 200, y = 50)
    sleep(1.5)
    errorMsg.destroy()

#wad sorting algorithms
def sortwadsByIntVals(wadsToBeSorted: List[Tuple[any]], catagory: str | int) -> List[Tuple[any]]:
    match catagory:
        case "difficulty": catagory = 2
        case "map count": catagory = 3
    sortedWads: List[Tuple[any]] = []
    while len(wadsToBeSorted):
        greatestIndex: int = 0
        for i, wad in enumerate(wadsToBeSorted):
            if int(wad[2]) > int(wadsToBeSorted[i][2]): greatestIndex = i
        sortedWads.append(wadsToBeSorted.pop(greatestIndex))
    return sortedWads

def searchForText(wadsToBeSearched: List[Tuple[any]], value: str) -> bool:
    for wad in wadsToBeSearched:
        if wad == value: return True
    return False

def searchForIntegerValue(wadsToBeSearched: List[Tuple[any]], value: int) -> bool: #unfinished
    wadsToBeSearched = sortwadsByIntVals(wadsToBeSearched)
    bottom: int = 0
    top: int = len(wadsToBeSearched) - 1
    middle: int = round(len(wadsToBeSearched) / 2, 0)
    while True:
        if value > wadsToBeSearched[middle]:
            bottom = middle
            middle = ceil(top / bottom)
        elif value < wadsToBeSearched[middle]:
            top = middle
            middle = ceil(top / bottom)
        elif middle == value: return True
        if middle == top or middle == bottom: break
    return False

def alphabeticalSort(wadsToBeSorted: List[Tuple[any]], charIndex: int = 0) -> List[Tuple[any]]: #unfinished
    def selection() -> str:
        wadsToBeSorted = (wad[0] for wad in wadsToBeSorted)
        lowestCharIndex: int = 0
        for i, wad in enumerate(wadsToBeSorted):
            if ord(wad[charIndex]) < ord(wad[i][charIndex]): lowestCharIndex = i
        lowestChar: chr = wadsToBeSearched[lowestCharIndex][0]
        equalCharArray: Tuple[str] = (wad for wad in wadsToBeSorted if wad[0] == lowestChar)
        if len(equalCharArray) > 0: return selection() 
        return 

    wadsToBeSorted = (wad[0] for wad in wadsToBeSorted)
    sortedWads: List[str] = []
    while len(sortedWads) != len(wadsToBeSorted): sortedWads.append(selection())

def checkIfSortHasChanged() -> None:
    global wads
    currentSelection: int = 0
    while True:
        if app.state() != "normal": return
        if sortSelection.value != currentSelection:
            currentSelection = sortSelection.value
            match currentSelection:
                case 0: break
                case 1:
                    wads = sortwadsByIntVals(wads, 2)
                    break
                case 2:
                    wads = sortwadsByIntVals(wads, 3)
                    break
                case 3: break 

def inputWad() -> None:
    def addWad(name: str, fileName: str, difficulty: float, maps: int) -> None:
        global wads
        try:
            difficulty = float(difficulty)
            maps = int(maps)
            if maps < 1: raise rangeError()
            if difficulty > 10 or difficulty <= 0: raise rangeError
        except ValueError: Thread(target = createErrorMessage, args = (inputScreen, "invalid data type",)).start()
        except rangeError: Thread(target = createErrorMessage, args = (inputScreen, "data out of range",)).start()
        else:
            databaseCursor.execute(f"INSERT INTO [wad] ([title], [fileName], [difficulty], [maps]) VALUES('{name}', '{fileName}', {difficulty}, {maps})")
            databaseConnection.commit()
            wads = databaseCursor.execute("SELECT * FROM wad").fetchall() 
            if noWadMsg != None: noWadMsg.destroy()

    inputScreen = CTk()
    inputScreen.title("input a wad")
    inputScreen.geometry("250x500")
    inputScreen.resizable(width = False, height = False)
    CTkLabel(inputScreen, text = "Add wad:", font = ("Arial", 20)).pack(pady = 15)
    CTkLabel(inputScreen, text = "name", font = ("Arial", 15)).pack(pady = 5)
    nameEntry = CTkEntry(inputScreen, font = ("Arial", 20), border_width = 2)
    nameEntry.pack(pady = 10)
    CTkLabel(inputScreen, text = "file name", font = ("Arial", 15)).pack(pady = 5)
    fileEntry = CTkEntry(inputScreen, font = ("Arial", 20), border_width = 2)
    fileEntry.pack(pady = 10)
    CTkLabel(inputScreen, text = "difficulty", font = ("Arial", 15)).pack(pady = 5)
    difficultyEntry = CTkEntry(inputScreen, font = ("Arial", 20), border_width = 2)
    difficultyEntry.pack(pady = 10)
    CTkLabel(inputScreen, text = "map count", font = ("Arial", 15)).pack(pady = 5)
    mapEntry = CTkEntry(inputScreen, font = ("Arial", 20), border_width = 2)
    mapEntry.pack(pady = 10)
    CTkButton(inputScreen, text = "submit", font = ("Arial", 15), border_width = 3, command = lambda: addWad(nameEntry.get(), fileEntry.get(), difficultyEntry.get(), mapEntry.get())).pack(pady = 10)

    inputScreen.mainloop()

def addWadByFile() -> None:
    global wads, noWadMsg
    filePath: str = filedialog.askopenfilename()
    if filePath == "": return
    try: file = open(filePath, 'r')
    except FileNotFoundError: fatalError("001")
    else:
        del filePath
        with file as completionDoc:
            completionData = [line for line in reader(completionDoc)]
            try:
                for line in completionData: 
                    line[2] = round(float(line[2]), 2)
                    if int(line[2]) == line[2]: line[2] = int(line[2])
                    if '.' not in line[3]: line[3] = int(line[3])
                    else: raise ValueError()
                    if line[2] > 10 or line[2] < 0 or line[3] < 1: raise rangeError()
                    databaseCursor.execute(f"INSERT INTO [wad] ([title], [fileName], [difficulty], [maps]) VALUES('{line[0]}', '{line[1]}', {line[2]}, {line[3]})")
                    databaseConnection.commit()
            except ValueError: Thread(target = createErrorMessage, args = (mainFrame, "value in file is of wrong data type")).start()
            except rangeError: Thread(target = createErrorMessage, args = (mainFrame, "value in file is out of range")).start()
            wads = databaseCursor.execute("SELECT * FROM wad").fetchall()
            hideNoWadLabel() #move off screen

def removeWad() -> None:
    def verifyWad(searchCatagoryIndicator: int, name: str) -> None:
        def duplicateCheck(catagory: int, value: str) -> bool:
            countOfUniqueItems: Dict[any, int] = {}
            for wad in wads:
                try: countOfUniqueItems[wad[catagory]] += 1
                except Exception: countOfUniqueItems[wad[catagory]] = 1 #get proper exception after system is developed
            for key in tuple(countOfUniqueItems.keys()):
                if countOfUniqueItems[key] > 1: return True
            return False
        
        def dbInteractions(command: str) -> None:
            global wads, scrollCount
            databaseCursor.execute(command)
            databaseConnection.commit()
            wads = databaseCursor.execute("SELECT * FROM wad").fetchall()
            scrollCount = 0

        if duplicateCheck(searchCatagoryIndicator, name): 
            if messagebox.askquestion(title = "Warning!", message = "There are mutiple wads with the same information as this, do you want to wipe all wads with this info?") == "yes": response: bool = True
            else: response: bool = False
        else: response: bool = False
        match searchCatagoryIndicator:
            case 1: tupleIndex: int = 0
            case 2: tupleIndex: int = 1
            case 3: tupleIndex: int = 2
            case 4: tupleIndex: int = 3
        del searchCatagoryIndicator
        for wad in wads:
            if wad[tupleIndex] == name:
              match tupleIndex:
                case 0:
                    if not response: return dbInteractions(f"DELETE FROM wad WHERE ROWID IN (SELECT MIN(ROWID) as row_id FROM wad WHERE title = '{name}')")
                    else:
                        dbInteractions(f"DELETE FROM wad WHERE title = '{name}'")
                        break
                case 1:
                    if not response: return dbInteractions(f"DELETE FROM wad WHERE ROWID IN (SELECT MIN(ROWID) as row_id FROM wad WHERE fileName = '{name}')")
                    else:
                        dbInteractions(f"DELETE FROM wad WHERE fileName = '{name}'")
                        break
                case 2: 
                    if not response: return dbInteractions(f"DELETE FROM wad WHERE ROWID IN (SELECT MIN(ROWID) as row_id FROM wad WHERE difficulty = '{name}')")
                    else:
                        dbInteractions(f"DELETE FROM wad WHERE difficulty = {name}")
                        break
                case 3: 
                    if not response: return dbInteractions(f"DELETE FROM wad WHERE ROWID IN (SELECT MIN(ROWID) as row_id FROM wad WHERE maps = '{name}')")
                    else:
                        dbInteractions(f"DELETE FROM wad WHERE maps = {name}")
                        break
        Thread(target = createErrorMessage, args = (removeScreen, f"invalid inputs, no item with attribute {name} exists")).start()\

    def wipeWad() -> None:
        global wads, scrollCount
        if messagebox.askquestion(title = "Warning!", message = "Do you really want to wipe all wads currently in the database?", icon = "warning") == "yes": 
            databaseCursor.execute("DELETE FROM wad")
            databaseConnection.commit()
            wads = []
            scrollCount = 0
            messagebox.showinfo(title = "confirmation", message = "all wads succesfully deleted")
            noWadMsg.place(x = 100, y = 500)
        else: messagebox.showinfo(title = "confirmation", message = "wad deletion cancelled")

    selectedOption = IntVar(value = 1)

    removeScreen = CTk()
    removeScreen.title("remove a wad")
    removeScreen.geometry("500x500")
    removeScreen.resizable(width = False, height = False)
    CTkLabel(removeScreen, text = "remove a wad", font = ("Arial", 25)).pack(pady = 15)
    CTkRadioButton(removeScreen, text = "delete by name", variable = selectedOption, value = 1).pack(pady = 10)
    CTkRadioButton(removeScreen, text = "delete by file name", variable = selectedOption, value = 2).pack(pady = 10)
    CTkRadioButton(removeScreen, text = "delete by difficulty", variable = selectedOption, value = 3).pack(pady = 10)
    CTkRadioButton(removeScreen, text = "delete by map count", variable = selectedOption, value = 4).pack(pady = 10)
    dataEntry = CTkEntry(removeScreen, font = ("Arial", 20), border_width = 3)
    dataEntry.pack(pady = 15)
    CTkButton(removeScreen, text = "submit", font = ("Arial", 15), border_width = 3, command = lambda: verifyWad(selectedOption.get(), dataEntry.get())).pack(pady = 15)
    CTkButton(removeScreen, text = "remove all wads", font = ("Arial", 15), border_width = 3, command = wipeWad).pack(pady = 15)
    
    removeScreen.mainloop()

def drawCanvasLoop() -> None:
    def canvasPlacement(frame1: int, frame2: int) -> None:
        try:
            showcaseFrames[frame1].place(x = 110, y = 550)
            showcaseFrames[frame2].place(x = 2000, y = 2000)
            showcaseFrames[frame2].delete("all")
        except Exception: pass

    frameOneIsToChangeZOrder: bool = False
    try:
        while True:
            for i in range(2):
                yCord: int = 150
                ignoreSteps: int = scrollCount
                for wad in wads:
                    if not ignoreSteps:
                        showcaseFrames[i].create_rectangle(25, yCord, 350, yCord - 130, width = 3, outline = colorMode)
                        canvasLabel(i, (60 + len("title: ")) + (len(wad[0]) / 2) * 1.5, yCord - 110, f"title: {wad[0]}", colorMode)
                        canvasLabel(i, (80 + len("file name: ")) + (len(wad[1]) / 2) * 1.5, yCord - 88, f"file name: {wad[1]}", colorMode)
                        canvasLabel(i, (56 + len("difficulty: ")) + (len(str(wad[2])) / 2) * 1.5, yCord - 66, f"difficulty: {wad[2]}", colorMode)
                        canvasLabel(i, (57 + len("map count: ")) + (len(str(wad[3])) / 2) * 1.5, yCord - 44, f"map count: {wad[3]}", colorMode)
                        yCord += 150
                    else: ignoreSteps -= 1
                sleep(0.5)
            if frameOneIsToChangeZOrder: canvasPlacement(1, 0)
            else: canvasPlacement(0, 1)
            frameOneIsToChangeZOrder = not frameOneIsToChangeZOrder
            del yCord, ignoreSteps
    except Exception: return #terminates thread if app closes at wrong point in code

#changes the amount of elements to skip when adding elements to the canvas
def changeScrollCount(isToMoveUp: bool) -> None:
    global scrollCount
    if isToMoveUp and scrollCount != 0: scrollCount -= 1
    elif not isToMoveUp and scrollCount != len(wads) - 2: scrollCount += 1
    if scrollCount == 0: upArrowLabel.configure(text = '')
    else: upArrowLabel.configure(text = '▲')
    if scrollCount == len(wads) - 2: downArrowLabel.configure(text = '')
    else: downArrowLabel.configure(text = '▼')
    scrollCountLabel.configure(text = scrollCount)

def changeKillCount() -> None:
    def onSubmit(userInput: str, increase: bool) -> None:
        try:
            if '.' in userInput or '-' in userInput: raise rangeError()
            userInput = int(userInput)
            with open("data/killCount.csv", 'r')  as killCountFile:
                killCount: int = int(next(reader(killCountFile))[0])
                if increase: killCount += userInput
                else: killCount -= userInput
                if killCount < 0: raise rangeError()
                with open("data/killCount.csv", 'w') as killCountFile: killCountFile.write(str(killCount))
                killCountLabel.configure(text = f"kill count: {str(killCount)}")
        except ValueError: Thread(target = createErrorMessage, args = (changeKillCountWindow, "value is not an integer",)).start()
        except rangeError: Thread(target = createErrorMessage, args = (changeKillCountWindow, "value is out of an acceptable range",)).start()

    changeKillCountWindow = Tk()
    changeKillCountWindow.title("change kill count")
    changeKillCountWindow.resizable(width = False, height = False)
    changeKillCountWindow.geometry("500x200")
    CTkLabel(changeKillCountWindow, text = "change kill count:", font = ("Arial", 20)).place(x = 20, y = 20)
    userInputBox = Entry(changeKillCountWindow, font = ("Arial", 25), border_width = 3, width = 12)
    userInputBox.place(x = 20, y = 80)
    CTkButton(changeKillCountWindow, text = '+', font = ("Arial", 20), border_width = 3, command = lambda: onSubmit(userInputBox.get(), True)).place(x = 300, y = 70)
    CTkButton(changeKillCountWindow, text = '-', font = ("Arial", 20), border_width = 3, command = lambda: onSubmit(userInputBox.get(), False)).place(x = 350, y = 70)

def bindKeyInputs(moveUpKey: str = "<Up>", moveDownKey: str = "<Down>") -> None:
    app.bind(moveUpKey, lambda event: changeScrollCount(True))
    app.bind(moveDownKey, lambda event: changeScrollCount(False))
    app.bind("a", changeKillCount)
    app.bind("r", removeWad )
    app.bind("c", changeKillCount)
    app.bind("f", addWadByFile)
    app.bind("s", settings)

def settingsScreen() -> None:
    def submit() -> None:
        settings["volume"] = volumeSlider.get()
        settings["colorMode"] = selectedMode
        if fontEntry.get() in font.families(): settings["font"] = fontEntry.get()
        else:
            match "".join(char for char in (fontEntry.get()).lower() if char != ' '):
                case "arial": settings["font"] = "Arial"
                case "timesnewroman": settings["font"] = "Times New Roman"
                case "rubik": settings["font"] = "Times New Roman"
                case "Vivaldi": settings["font"] = "Vivaldi"
                case "liberationmono": settings["font"] = "Liberation Mono"
                case "opensymbol": settings["font"] = "OpenSymbol"
                case "yugothicuisemilight": settings["font"] = "Yu Gothic UI Semilight"
                case "modernno.20": settings["font"] = "Modern No. 20"
                case _: 
                    Thread(target = createErrorMessage, args = (settingsApp, "font is not available")).start()
                    return
        try: settingsFile = open("data/settings.json", 'w')
        except FileNotFoundError: fatalError("004")
        else: settingsFile.write(settings.dumps())

    def changeButtonColors(col1: str, col2: str) -> None:
        lightButton.configure(fg_color = col1)
        darkButton.configure(fg_color = col2)

    def changeMode(mode: str) -> None:
        selectedMode = mode
        if mode == "light": changeButtonColors("green", "grey25")
        else: changeButtonColors("grey25", "green")

    selectedMode: str = "light" if colorMode == "black" else "dark"
    settingsApp = Tk()
    settingsApp.configure(bg = "grey17")
    settingsApp.title("settings")
    settingsApp.geometry("500x600")
    settingsApp.resizable(width = False, height = False)
    CTkLabel(settingsApp, text = "settings", font = ("Arial", 45)).pack(pady = 15)
    CTkLabel(settingsApp, text = "display mode:", font = ("Arial", 15)).pack(pady = (30, 10))
    lightButton = CTkButton(settingsApp, text = "light", font = ("Arial", 30), command = lambda: changeMode("light"))
    lightButton.pack(pady = 5)
    darkButton = CTkButton(settingsApp, text = "dark", font = ("Arial", 30), command = lambda: changeMode("dark"))
    darkButton.pack(pady = 5)
    if colorMode == "black": changeButtonColors("green", "grey25")
    else: changeButtonColors("grey25", "green")
    volumeSlider = CTkSlider(settingsApp, from_ = 0, to = 100)
    CTkLabel(settingsApp, text = "volume:", font = ("Arial", 15)).pack(pady = (15, 5))
    volumeSlider.pack(pady = 5)
    CTkLabel(settingsApp, text = "default font: ", font = ("Arial", 15))
    fontEntry = CTkEntry(settingsApp, font = ("Arial", 25))
    fontEntry.pack(pady = 10)
    CTkButton(settingsApp, text = "submit", font = ("Arial", 25), command = submit).pack(pady = 15)

#establishing database and defining simple variables
app = CTk()
databaseConnection = connect("completions.db")
databaseCursor = databaseConnection.cursor()
wads: List[Tuple[any]] = databaseCursor.execute("SELECT * FROM wad").fetchall()
scrollCount: int = 0 #how many elements to skip when drawing the canvas elements
try: settingsFile = open("data/settings.json")
except FileNotFoundError: fatalError("002")
else: 
    settings: Dict[any, any] = load(settingsFile)
    settingsFile.close()
    del settingsFile
#assign color mode
if settings["colorMode"] == "light": 
    set_appearance_mode("light")
    colorMode: str = "black"
elif settings["colorMode"] == "dark": 
    set_appearance_mode("dark")
    colorMode: str = "white"
else: fatalError("003.1")
#assign font
if settings["font"] in font.families(): font: str = settings["font"]
else: fatalError("003.2")
#set volume
try:
    volume: int = int(settings["volume"])
    if float(settings["volume"]) != volume or volume < 0 or volume > 100: raise rangeError()
except ValueError: fatalError("003.3")
except rangeError: fatalError("003.4")
#non-canvas related UI elements
app.title("completions list")
app.resizable(width = False, height = False)
app.geometry("500x1300")
app.configure(bg = "white")
mainFrame = CTkScrollableFrame(master = app, border_width = 4)
mainFrame.pack(fill = "both", expand = 1)
#widgets
CTkLabel(mainFrame, text = "Doom Completions", font = ("Arial", 35)).pack(pady = 30)
CTkButton(mainFrame, text = "Add Wad", font = ("Arial", 20),  border_width = 3, command = inputWad, fg_color = "green", corner_radius = 360).pack(pady = 15)
CTkButton(mainFrame, text = "Add Wads By File", font = ("Arial", 20), border_width = 3, command = addWadByFile, fg_color = "grey10", corner_radius = 360).pack(pady = 15)
CTkButton(mainFrame, text = "remove Wad", font = ("Arial", 20), border_width = 3, command = removeWad, fg_color = "red", corner_radius = 360).pack(pady = 15)
CTkButton(mainFrame, text = "change kill count", font = ("Arial", 20), border_width = 3, command = changeKillCount, fg_color = "orange", corner_radius = 360).pack(pady = 15)
#kill count
with open("data/killCount.csv", 'r') as killCountFile:
    killCount: str = "kill count: " + next(reader(killCountFile))[0]
    killCountLabel: Label = Label(mainFrame, text = killCount, font = ("Arial", 20))
    killCountLabel.pack(pady = 20)
upArrowLabel = Label(mainFrame, text = '', font = ("Arial", 30))
upArrowLabel.pack(pady = 10)
CTkButton(mainFrame, text = "▲", width = 40, font = ("Arial", 25), border_width = 3, command = lambda: changeScrollCount(True), corner_radius = 360).place(x = 420, y = 215)
CTkButton(mainFrame, text = "▼", width = 40, font = ("Arial", 25), border_width = 3, command = lambda: changeScrollCount(False), corner_radius = 360).place(x = 420, y = 325)
scrollCountLabel = CTkLabel(mainFrame, text = '0', font = ("Arial", 25))
scrollCountLabel.place(x = 720, y = 350)
showcaseFrames: Tuple[Canvas] = (CTkCanvas(mainFrame, width = 350, height = 500, bg = "grey17", highlightbackground="grey17"), CTkCanvas(mainFrame, width = 350, height = 500, bg = "grey17", highlightbackground="grey17"))
showcaseFrames[0].place(x = 110, y = 550)
showcaseFrames[1].place(x = 2000, y = 2000)
downArrowLabel = CTkLabel(mainFrame, text = '', font = ("Arial", 30))
downArrowLabel.pack(pady = (350, 10))
sortSelection = IntVar(mainFrame, 0)
CTkRadioButton(mainFrame, text = "sort by date added", variable = sortSelection, value = 0).pack(pady = (250, 5))
CTkRadioButton(mainFrame, text = "sort by difficulty", variable = sortSelection, value = 1).pack(pady = 5)
CTkRadioButton(mainFrame, text = "sort by map count", variable = sortSelection, value = 2).pack(pady = 5)
CTkRadioButton(mainFrame, text = "sort by alphabetical order", variable = sortSelection, value = 3).pack(pady = 5)
CTkButton(mainFrame, text = "⚙", font = ("Arial", 30), width = 30, border_width = 3, command = settingsScreen, fg_color = "grey", corner_radius = 360).place(x = 5, y = 5)
mixer.init() #initialise audio
if settings["keyboardInputs"] == "true": bindKeyInputs() 

#loop to draw blobs
noWadMsg = CTkLabel(mainFrame, text = "you have no wads in the database. add wads manually or through a file", font = ("Arial", 25), wraplength = 300)
if len(wads): 
    Thread(target = drawCanvasLoop).start()
    hideNoWadLabel() #hide label
else: noWadMsg.place(x = 100, y = 500)

app.mainloop()