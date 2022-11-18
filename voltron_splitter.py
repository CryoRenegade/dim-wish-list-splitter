# Main Class for Splitter Program
from asyncio.windows_events import NULL


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
                    tempLine = line
                    relevantLine = ""
                    while tempLine.find("(") != -1 and tempLine.find(')', tempLine.find('(')) != -1:
                        tarString = tempLine[tempLine.find('('):tempLine.find(')', tempLine.find('('))+1]
                        relevantLine += " " + tarString;
                        tempLine = tempLine.split(tarString, 1)[1]

                    # tag search in lines
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
                        if ("search" in listSettings):
                            if (not listSettings.get("searchFlag") 
                                and any(i in line for i in listSettings.get("search")) ):
                                listSettings["searchFlag"] = True

                    # check line for exclude flag
                    for listSettings in flag_search_file:
                        if ("exclude" in listSettings):
                            if (not listSettings.get("excludeFlag") 
                                and any(i in line for i in listSettings.get("exclude")) ):
                                listSettings["excludeFlag"] = True

                # Empty Line
                else:
                    self.checkWrite()
                    self.newWeapon()
        
        self.checkWrite()

    def checkWrite(self):
        for curWishList in flag_search_file:
            if self.lineCollection != []:
                if (
                    ( # Checks flags 
                    (curWishList.get("flag", lambda: None)() or curWishList.get("flag") is None)
                    and (curWishList.get("searchFlag") or curWishList.get("search") is None) 
                    and (not curWishList.get("excludeFlag") or curWishList.get("exclude") is None) 
                    ) # Checks for Dim Link or Credits
                    or (not self.dimFlag and self.creditFlag) ):
                    with open(curWishList.get("file"), mode='a') as tempFile:
                        for i in self.lineCollection:
                            tempFile.write(i)
                        tempFile.write("\n")

            if ("search" in curWishList):
                curWishList["searchFlag"] = False
            if ("exclude" in curWishList):
                curWishList["excludeFlag"] = False

mainObj = Splitter()

# -----------------------------------------------------------------------------------------------------------------------------
# Dictionary of All Filters
flag_search_file = []

# -------------------------------------------
# No Filters
flag_search_file.append({"file": "./wishlists/All.txt"})

# -------------------------------------------
# Gamemode Filters
flag_search_file.append({"flag": lambda: mainObj.pveFlag or not mainObj.pvpFlag, 
                        "file": "./wishlists/PVE.txt"})
flag_search_file.append({"flag": lambda: mainObj.pvpFlag, 
                        "file": "./wishlists/PVP.txt"})

# -------------------------------------------
# Input Filters
flag_search_file.append({"flag": lambda: mainObj.mkbFlag or not mainObj.ctrFlag, 
                        "file": "./wishlists/MKB.txt"})
flag_search_file.append({"flag": lambda: mainObj.ctrFlag, 
                        "file": "./wishlists/CTR.txt"})

# -------------------------------------------
# Separate PvE / PvP Filters
flag_search_file.append({"flag": lambda: (mainObj.pveFlag or not mainObj.pvpFlag) and (mainObj.mkbFlag or not mainObj.ctrFlag), 
                        "file": "./wishlists/MKB_PVE.txt"})
flag_search_file.append({"flag": lambda: mainObj.pvpFlag and (mainObj.mkbFlag or not mainObj.ctrFlag), 
                        "file": "./wishlists/MKB_PVP.txt"})

flag_search_file.append({"flag": lambda: (mainObj.pveFlag or not mainObj.pvpFlag) and mainObj.ctrFlag, 
                        "file": "./wishlists/CTR_PVE.txt"})
flag_search_file.append({"flag": lambda: mainObj.pvpFlag and mainObj.ctrFlag, 
                        "file": "./wishlists/CTR_PVP.txt"})

# -------------------------------------------
# PandaPaxxy Filters
flag_search_file.append({"search": ["pandapaxxy"], "searchFlag": False,
                        "file": "./wishlists/Panda.txt"})

flag_search_file.append({"flag": lambda: mainObj.mkbFlag or not mainObj.ctrFlag, 
                        "search": ["pandapaxxy"], "searchFlag": False,
                        "file": "./wishlists/Panda_MKB.txt"})
flag_search_file.append({"flag": lambda: (mainObj.pveFlag or not mainObj.pvpFlag) and (mainObj.mkbFlag or not mainObj.ctrFlag), 
                        "search": ["pandapaxxy"], "searchFlag": False,
                        "file": "./wishlists/Panda_MKB_PVE.txt"})
flag_search_file.append({"flag": lambda: mainObj.pvpFlag and (mainObj.mkbFlag or not mainObj.ctrFlag), 
                        "search": ["pandapaxxy"], "searchFlag": False,
                        "file": "./wishlists/Panda_MKB_PVP.txt"})

flag_search_file.append({"flag": lambda: mainObj.ctrFlag, 
                        "search": ["pandapaxxy"], "searchFlag": False,
                        "file": "./wishlists/Panda_CTR.txt"})
flag_search_file.append({"flag": lambda: (mainObj.pveFlag or not mainObj.pvpFlag) and mainObj.ctrFlag, 
                        "search": ["pandapaxxy"], "searchFlag": False,
                        "file": "./wishlists/Panda_CTR_PVE.txt"})                        
flag_search_file.append({"flag": lambda: mainObj.pvpFlag and mainObj.ctrFlag, 
                        "search": ["pandapaxxy"], "searchFlag": False,
                        "file": "./wishlists/Panda_CTR_PVP.txt"})

# -------------------------------------------
# God Filters
flag_search_file.append({"flag": lambda: mainObj.mkbFlag or not mainObj.ctrFlag, 
                        "search": ["god-"], "searchFlag": False,
                        "file": "./wishlists/MKB_GOD.txt"})

# -------------------------------------------
# Exclude YeezyGT - Input Filters
flag_search_file.append({"flag": lambda: mainObj.mkbFlag or not mainObj.ctrFlag, 
                        "exclude": ["yeezygt"], "excludeFlag" : False, 
                        "file": "./wishlists/MKB_!Yeezy.txt"})

# -------------------------------------------
# Exclude YeezyGT and Backup Rolls - Input Filters
flag_search_file.append({"flag": lambda: mainObj.mkbFlag or not mainObj.ctrFlag, 
                        "exclude": ["yeezygt", "backup roll"], "excludeFlag" : False, 
                        "file": "./wishlists/MKB_!Backup_!Yeezy.txt"})

# -------------------------------------------
# Exclude Backup Rolls - Input Filters
flag_search_file.append({"flag": lambda: mainObj.mkbFlag or not mainObj.ctrFlag, 
                        "exclude": ["backup roll"], "excludeFlag" : False, 
                        "file": "./wishlists/MKB_!Backup.txt"})

# -----------------------------------------------------------------------------------------------------------------------------
# Clear Previous Files
for curWishList in flag_search_file:
    with open(curWishList.get("file"), mode='w') as clearFile:
        pass

# -------------------------------------------
# Start Program
mainObj.readMain()