# Main Class for Splitter Program
class Splitter:
    def __init__(self):
        self.mainFile = "./dim-wish-list-sources/voltron.txt"
        
        self.newWeapon()
        
    def newWeapon(self):
        self.pveFlag = self.pvpFlag = self.mkbFlag = self.ctrFlag = False
        self.dimFlag = self.creditFlag = False
        
        self.lineCollection = []

    def readMain(self):
        with open(self.mainFile, mode='r', encoding='utf-8') as f:
            for line in f:
                # Non-empty Line
                if len(line) != 1:
                    self.lineCollection.append(line)

                    # improved flag search in lines
                    relevantLine = ""
                    if '(' in line.lower() and ')' in line.lower():
                        relevantLine = line[line.find('('):line.find(')')+1]
                    if "tags:" in line.lower():
                        relevantLine += " " + line[line.rfind("tags:"):]

                    # Ignore Case
                    relevantLine = relevantLine.lower()
                    line = line.lower()

                    # Relevant Line Flags
                    if not self.pveFlag and 'pve' in relevantLine:
                        self.pveFlag = True
                    if not self.pvpFlag and 'pvp' in relevantLine:
                        self.pvpFlag = True
                    if not self.mkbFlag and ('mkb' in relevantLine or "m+kb" in relevantLine):
                        self.mkbFlag = True
                    if not self.ctrFlag and 'controller' in relevantLine:
                        self.ctrFlag = True
                    
                    # Full Line Flags
                    if not self.dimFlag and 'dimwishlist:item' in line:
                        self.dimFlag = True
                    if not self.creditFlag and 'https://' in line or 'u/' in line:
                        self.creditFlag = True

                    # checks line for search flag
                    for listSettings in flag_search_file:
                        if ( not listSettings.get("searchFlag") 
                            and any(i in line for i in listSettings.get("search")) ):
                            listSettings["searchFlag"] = True

                # Empty Line
                else:
                    self.checkWrite()
                    self.newWeapon()
        
        self.checkWrite()

    def checkWrite(self):
        for curWishList in flag_search_file:
            if self.lineCollection != []:
                if ( (curWishList.get("flag", lambda: None)() and curWishList.get("searchFlag")) 
                    or (not self.dimFlag and self.creditFlag) ):
                    with open(curWishList.get("file"), mode='a') as tempFile:
                        for i in self.lineCollection:
                            tempFile.write(i)
                        tempFile.write("\n")

            if curWishList.get("search") == []:
                curWishList["searchFlag"] = True
            else:
                curWishList["searchFlag"] = False

mainObj = Splitter()

# -------------------------------------------
# Dictionary of All Filters
flag_search_file = []

# -------------------------------------------
# No Filters
flag_search_file.append({"flag": lambda: True, 
                        "search": [], "searchFlag": True,"file": "./wishlists/All.txt"})

# -------------------------------------------
# Gamemode Filters
flag_search_file.append({"flag": lambda: mainObj.pveFlag or not mainObj.pvpFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE.txt"})
flag_search_file.append({"flag": lambda: mainObj.pvpFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvP.txt"})

# -------------------------------------------
# Input Filters
flag_search_file.append({"flag": lambda: mainObj.mkbFlag or not mainObj.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/MKB.txt"})
flag_search_file.append({"flag": lambda: mainObj.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/CTR.txt"})

# -------------------------------------------
# Separate PvE / PvP Filters
flag_search_file.append({"flag": lambda: (mainObj.pveFlag or not mainObj.pvpFlag) and (mainObj.mkbFlag or not mainObj.ctrFlag), 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-MKB.txt"})
flag_search_file.append({"flag": lambda: (mainObj.pveFlag or not mainObj.pvpFlag) and mainObj.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-CTR.txt"})

flag_search_file.append({"flag": lambda: mainObj.pvpFlag and (mainObj.mkbFlag or not mainObj.ctrFlag), 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvP-MKB.txt"})
flag_search_file.append({"flag": lambda: mainObj.pvpFlag and mainObj.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvP-CTR.txt"})

# -------------------------------------------
# Both PvE / PvP Filters
flag_search_file.append({"flag": lambda: mainObj.pveFlag and mainObj.pvpFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-PvP.txt"})

flag_search_file.append({"flag": lambda: (mainObj.pveFlag and mainObj.pvpFlag) and (mainObj.mkbFlag or not mainObj.ctrFlag), 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-PvP-MKB.txt"})
flag_search_file.append({"flag": lambda: (mainObj.pveFlag and mainObj.pvpFlag) and mainObj.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-PvP-CTR.txt"})

# -------------------------------------------
# PandaPaxxy Filters
flag_search_file.append({"flag": lambda: True, 
                        "search": ["pandapaxxy"], "searchFlag": False,"file": "./wishlists/PandaPaxxy.txt"})

flag_search_file.append({"flag": lambda: (mainObj.pveFlag or not mainObj.pvpFlag) and (mainObj.mkbFlag or not mainObj.ctrFlag), 
                        "search": ["pandapaxxy"], "searchFlag": False,"file": "./wishlists/PandaPaxxy-PvE-MKB.txt"})
flag_search_file.append({"flag": lambda: (mainObj.pveFlag or not mainObj.pvpFlag) and mainObj.ctrFlag, 
                        "search": ["pandapaxxy"], "searchFlag": False,"file": "./wishlists/PandaPaxxy-PvE-CTR.txt"})

flag_search_file.append({"flag": lambda: mainObj.pvpFlag and (mainObj.mkbFlag or not mainObj.ctrFlag), 
                        "search": ["pandapaxxy"], "searchFlag": False,"file": "./wishlists/PandaPaxxy-PvP-MKB.txt"})
flag_search_file.append({"flag": lambda: mainObj.pvpFlag and mainObj.ctrFlag, 
                        "search": ["pandapaxxy"], "searchFlag": False,"file": "./wishlists/PandaPaxxy-PvP-CTR.txt"})

# -------------------------------------------
# Clear Previous Files
for curWishList in flag_search_file:
    with open(curWishList.get("file"), mode='w') as clearFile:
        pass

# -------------------------------------------
# Start Program
mainObj.readMain()