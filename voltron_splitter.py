# git submodule update --remote

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
        for curWishList in self.allWishLists:
            if curWeapon.lineCollection != []:
                if (eval(curWishList.flags) and curWishList.searchFlag) or (not curWeapon.dimFlag and curWeapon.creditFlag):
                    with open(curWishList.fileName, mode='a') as tempFile:
                        for i in curWeapon.lineCollection:
                            tempFile.write(i)
                        tempFile.write("\n")

            curWishList.resetSearchFlag()

class ListSetting:
    def __init__(self, flags, search, fileName):
        self.flags = flags
        self.search = search
        self.fileName = fileName

        self.searchFlag = True
        self.resetSearchFlag
    
    def resetSearchFlag(self):
        self.searchFlag = True

        if self.search != []:
            self.searchFlag = False

wishLists = []

# create individual lists and add to wishLists
wishLists.append(ListSetting("True", [], "./wishlists/All.txt"))

wishLists.append(ListSetting("curWeapon.pveFlag or not curWeapon.pvpFlag", [], "./wishlists/PvE.txt"))
wishLists.append(ListSetting("curWeapon.pvpFlag", [], "./wishlists/PvP.txt"))

wishLists.append(ListSetting("curWeapon.mkbFlag or not curWeapon.ctrFlag", [], "./wishlists/MKB.txt"))
wishLists.append(ListSetting("curWeapon.ctrFlag", [], "./wishlists/Controller.txt"))

wishLists.append(ListSetting("(curWeapon.pveFlag or not curWeapon.pvpFlag) and (curWeapon.mkbFlag or not curWeapon.ctrFlag)", [], "./wishlists/PvE-MKB.txt"))
wishLists.append(ListSetting("(curWeapon.pveFlag or not curWeapon.pvpFlag) and curWeapon.ctrFlag", [], "./wishlists/PvE-Controller.txt"))

wishLists.append(ListSetting("curWeapon.pvpFlag and (curWeapon.mkbFlag or not curWeapon.ctrFlag)", [], "./wishlists/PvP-MKB.txt"))
wishLists.append(ListSetting("curWeapon.pvpFlag and curWeapon.ctrFlag", [], "./wishlists/PvP-Controller.txt"))

wishLists.append(ListSetting("curWeapon.pveFlag and curWeapon.pvpFlag", [], "./wishlists/PvE-PvP.txt"))

wishLists.append(ListSetting("(curWeapon.pveFlag and curWeapon.pvpFlag) and (curWeapon.mkbFlag or not curWeapon.ctrFlag)", [], "./wishlists/PvE-PvP-MKB.txt"))
wishLists.append(ListSetting("(curWeapon.pveFlag and curWeapon.pvpFlag) and curWeapon.ctrFlag", [], "./wishlists/PvE-PvP-Controller.txt"))

wishLists.append(ListSetting("True", ["pandapaxxy"], "./wishlists/PandaPaxxy.txt"))

FileInfo(wishLists)