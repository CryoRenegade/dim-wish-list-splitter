# Stores Flags for Gamemode, Input, and Other 
class WeaponInfo:
    def __init__(self):
        self.newWeapon()

    def newWeapon(self):
        self.pveFlag = self.pvpFlag = self.mkbFlag = self.ctrFlag = False
        self.dimFlag = self.creditFlag = False
        
        self.lineCollection = []

# Global object of WeaponInfo
curWeapon = WeaponInfo()

# Main Class for Splitter Program
class Splitter:
    def __init__(self):
        self.mainFile = "./dim-wish-list-sources/voltron.txt"
        
        self.clearFiles()
        self.readMain()

    def clearFiles(self):
        for curWishList in flag_search_file:
            with open(curWishList.get("file"), mode='w') as clearFile:
                pass

    def readMain(self):
        with open(self.mainFile, mode='r', encoding='utf-8') as f:
            for line in f:
                # Non-empty Line
                if len(line) != 1:
                    curWeapon.lineCollection.append(line)

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
                    if not curWeapon.pveFlag and 'pve' in relevantLine:
                        curWeapon.pveFlag = True
                    if not curWeapon.pvpFlag and 'pvp' in relevantLine:
                        curWeapon.pvpFlag = True
                    if not curWeapon.mkbFlag and ('mkb' in relevantLine or "m+kb" in relevantLine):
                        curWeapon.mkbFlag = True
                    if not curWeapon.ctrFlag and 'controller' in relevantLine:
                        curWeapon.ctrFlag = True
                    
                    # Full Line Flags
                    if not curWeapon.dimFlag and 'dimwishlist:item' in line:
                        curWeapon.dimFlag = True
                    if not curWeapon.creditFlag and 'https://' in line or 'u/' in line:
                        curWeapon.creditFlag = True

                    # checks line for search flag
                    for listSettings in flag_search_file:
                        if ( not listSettings.get("searchFlag") 
                            and any(i in line for i in listSettings.get("search")) ):
                            listSettings["searchFlag"] = True

                # Empty Line
                else:
                    self.checkWrite()
                    curWeapon.newWeapon()
        
        self.checkWrite()

    def checkWrite(self):
        for curWishList in flag_search_file:
            if curWeapon.lineCollection != []:
                if ( (curWishList.get("flag", lambda: None)() and curWishList.get("searchFlag")) 
                    or (not curWeapon.dimFlag and curWeapon.creditFlag) ):
                    with open(curWishList.get("file"), mode='a') as tempFile:
                        for i in curWeapon.lineCollection:
                            tempFile.write(i)
                        tempFile.write("\n")

            if curWishList.get("search") == []:
                curWishList["searchFlag"] = True
            else:
                curWishList["searchFlag"] = False

# -------------------------------------------
# Dictionary of All Filters
flag_search_file = []

# -------------------------------------------
# No Filters
flag_search_file.append({"flag": lambda: True, 
                        "search": [], "searchFlag": True,"file": "./wishlists/All.txt"})

# -------------------------------------------
# Gamemode Filters
flag_search_file.append({"flag": lambda: curWeapon.pveFlag or not curWeapon.pvpFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE.txt"})
flag_search_file.append({"flag": lambda: curWeapon.pvpFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvP.txt"})

# -------------------------------------------
# Input Filters
flag_search_file.append({"flag": lambda: curWeapon.mkbFlag or not curWeapon.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/MKB.txt"})
flag_search_file.append({"flag": lambda: curWeapon.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/CTR.txt"})

# -------------------------------------------
# PvE or PvP Filters
flag_search_file.append({"flag": lambda: (curWeapon.pveFlag or not curWeapon.pvpFlag) and (curWeapon.mkbFlag or not curWeapon.ctrFlag), 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-MKB.txt"})
flag_search_file.append({"flag": lambda: (curWeapon.pveFlag or not curWeapon.pvpFlag) and curWeapon.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-CTR.txt"})

flag_search_file.append({"flag": lambda: curWeapon.pvpFlag and (curWeapon.mkbFlag or not curWeapon.ctrFlag), 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvP-MKB.txt"})
flag_search_file.append({"flag": lambda: curWeapon.pvpFlag and curWeapon.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvP-CTR.txt"})

# -------------------------------------------
# PvE and PvP Filters
flag_search_file.append({"flag": lambda: curWeapon.pveFlag and curWeapon.pvpFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-PvP.txt"})

flag_search_file.append({"flag": lambda: (curWeapon.pveFlag and curWeapon.pvpFlag) and (curWeapon.mkbFlag or not curWeapon.ctrFlag), 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-PvP-MKB.txt"})
flag_search_file.append({"flag": lambda: (curWeapon.pveFlag and curWeapon.pvpFlag) and curWeapon.ctrFlag, 
                        "search": [], "searchFlag": True,"file": "./wishlists/PvE-PvP-CTR.txt"})

# -------------------------------------------
# Search Filters
flag_search_file.append({"flag": lambda: True, 
                        "search": ["pandapaxxy"], "searchFlag": False,"file": "./wishlists/PandaPaxxy.txt"})

# Start Program
Splitter()