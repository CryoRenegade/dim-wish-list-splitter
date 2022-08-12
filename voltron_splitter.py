from logging import captureWarnings

class WeaponInfo:
    def __init__(self):
        self.newWeapon()

    def newWeapon(self):
        self.pveFlag = False
        self.pvpFlag = False
        self.mkbFlag = False
        self.ctrFlag = False

        self.dimFlag = False
        self.creditFlag = False
        
        self.lineCollection = []

curWeapon = WeaponInfo()

# read lines of file and trip flags
class FileInfo:
    def __init__(self, allLists):
        self.allWishLists = allLists

        self.mainFile = "./dim-wish-list-sources/voltron.txt"
        
        self.clearFiles()
        self.readMain()

    def clearFiles(self):
        for curWishList in self.allWishLists:
            with open(curWishList.fileName, mode='w') as clearFile:
                pass

    def readMain(self):
        with open(self.mainFile, mode='r', encoding='utf-8') as f:
            for line in f:
                # Non-empty Line
                if len(line) != 1:
                    curWeapon.lineCollection.append(line)

                    if not curWeapon.pveFlag and 'pve' in line.lower():
                        curWeapon.pveFlag = True
                    if not curWeapon.pvpFlag and 'pvp' in line.lower():
                        curWeapon.pvpFlag = True
                    if not curWeapon.mkbFlag and 'mkb' in line.lower() or "m+kb" in line.lower():
                        curWeapon.mkbFlag = True
                    if not curWeapon.ctrFlag and 'controller' in line.lower():
                        curWeapon.ctrFlag = True
                    if not curWeapon.dimFlag and 'dimwishlist:item' in line.lower():
                        curWeapon.dimFlag = True
                    if not curWeapon.creditFlag and 'https://' in line.lower() or 'u/' in line.lower():
                        curWeapon.creditFlag = True

                    for listSettings in self.allWishLists:
                        if any(i in line.lower() for i in listSettings.search):
                            listSettings.searchFlag = True

                # Empty Line
                else:
                    self.checkWrite()
                    curWeapon.newWeapon()
        
        self.checkWrite()

    def checkWrite(self):
        updateFlags()

        for curWishList in self.allWishLists:
            if curWeapon.lineCollection != []:
                if (curWishList.flags and curWishList.searchFlag) or (not curWeapon.dimFlag and curWeapon.creditFlag):
                    with open(curWishList.fileName, mode='a') as tempFile:
                        for i in curWeapon.lineCollection:
                            tempFile.write(i)
                        tempFile.write("\n")

            curWishList.resetSearchFlag()

class ListSetting:
    def __init__(self, search, fileName):
        self.flags = False
        self.search = search
        self.fileName = fileName

        self.searchFlag = True
        self.resetSearchFlag()

    def resetSearchFlag(self):
        self.searchFlag = True

        if self.search != []:
            self.searchFlag = False

wishLists = []

wishLists.append(ListSetting([], "./wishlists/All.txt"))

wishLists.append(ListSetting([], "./wishlists/PvE.txt"))
wishLists.append(ListSetting([], "./wishlists/PvP.txt"))

wishLists.append(ListSetting([], "./wishlists/MKB.txt"))
wishLists.append(ListSetting([], "./wishlists/Controller.txt"))

wishLists.append(ListSetting([], "./wishlists/PvE-MKB.txt"))
wishLists.append(ListSetting([], "./wishlists/PvE-Controller.txt"))

wishLists.append(ListSetting([], "./wishlists/PvP-MKB.txt"))
wishLists.append(ListSetting([], "./wishlists/PvP-Controller.txt"))

wishLists.append(ListSetting([], "./wishlists/PvE-PvP.txt"))

wishLists.append(ListSetting([], "./wishlists/PvE-PvP-MKB.txt"))
wishLists.append(ListSetting([], "./wishlists/PvE-PvP-Controller.txt"))

wishLists.append(ListSetting(["pandapaxxy"], "./wishlists/PandaPaxxy.txt"))

flagExpressions = {
    0: lambda: True,
    1: lambda: curWeapon.pveFlag or not curWeapon.pvpFlag,
    2: lambda: curWeapon.pvpFlag,
    3: lambda: curWeapon.mkbFlag or not curWeapon.ctrFlag,
    4: lambda: curWeapon.ctrFlag,
    5: lambda: (curWeapon.pveFlag or not curWeapon.pvpFlag) and (curWeapon.mkbFlag or not curWeapon.ctrFlag),
    6: lambda: (curWeapon.pveFlag or not curWeapon.pvpFlag) and curWeapon.ctrFlag,
    7: lambda: curWeapon.pvpFlag and (curWeapon.mkbFlag or not curWeapon.ctrFlag),
    8: lambda: curWeapon.pvpFlag and curWeapon.ctrFlag,
    9: lambda: curWeapon.pveFlag and curWeapon.pvpFlag,
    10: lambda: (curWeapon.pveFlag and curWeapon.pvpFlag) and (curWeapon.mkbFlag or not curWeapon.ctrFlag),
    11: lambda: (curWeapon.pveFlag and curWeapon.pvpFlag) and curWeapon.ctrFlag,
    12: lambda: True
}

def updateFlags():
    for index in range(len(wishLists)):
        wishLists[index].flags = flagExpressions.get(index, lambda: None)()

FileInfo(wishLists)