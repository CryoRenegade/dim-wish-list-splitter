# git submodule update --remote

# read lines of file and trip flags
class FileInfo:
    def __init__(self, allLists):
        self.pveFlag = False
        self.pvpFlag = False
        self.mkbFlag = False
        self.ctrFlag = False

        self.dimFlag = False
        self.creditFlag = False

        self.allLists = allLists

        self.mainFile = "./dim-wish-list-sources/voltron.txt"

        self.lineCollection = []
        
        self.clearFiles()
        self.readMain()

    def readMain(self):
        with open(self.mainFile, mode='r', encoding='utf-8') as f:
            for line in f:
                # Non-empty Line
                if len(line) != 1:
                    self.lineCollection.append(line)

                    if 'pve' in line.lower():
                        self.pveFlag = True
                    if 'pvp' in line.lower():
                        self.pvpFlag = True
                    if 'mkb' in line.lower() or "m+kb" in line.lower():
                        self.mkbFlag = True
                    if 'controller' in line.lower():
                        self.ctrFlag = True
                    if 'dimwishlist:item' in line.lower():
                        self.dimFlag = True
                    if 'https://' in line.lower() or 'u/' in line.lower():
                        self.creditFlag = True

                    for listSettings in self.allLists:
                        if any(i in line.lower() for i in listSettings.getSearch()):
                            listSettings.setSearchFlag(True)

                # Empty Line
                else:
                    self.checkWrite()

                    self.pveFlag = False
                    self.pvpFlag = False
                    self.mkbFlag = False
                    self.ctrFlag = False
                    self.dimFlag = False
                    self.creditFlag = False
                    
                    self.lineCollection = []
        
        self.checkWrite()

    def clearFiles(self):
        for curList in self.allLists:
            with open(curList.getFileName(), mode='w') as clearFile:
                pass

    def checkWrite(self):
        for curList in self.allLists:
            if self.lineCollection != []:
                if (eval(curList.getFlags()) and curList.getSearchFlag()) or (not self.dimFlag and self.creditFlag):
                    with open(curList.getFileName(), mode='a') as tempFile:
                        for i in self.lineCollection:
                            tempFile.write(i)
                        tempFile.write("\n")

            curList.resetSearchFlag()

class ListSetting:
    def __init__(self, flags, search, fileName):
        self.flags = flags
        self.search = search
        self.fileName = fileName

        self.searchFlag = True

        if self.search != []:
            self.searchFlag = False

    def getFlags(self):
        return self.flags
    def getSearch(self):
        return self.search
    def getSearchFlag(self):
        return self.searchFlag
    def getFileName(self):
        return self.fileName

    def setSearchFlag(self, newFlag):
        self.searchFlag = newFlag
    
    def resetSearchFlag(self):
        self.searchFlag = True

        if self.search != []:
            self.searchFlag = False

wishLists = []

# create individual lists and add to wishLists
wishLists.append(ListSetting("True", [], "./wishlists/All.txt"))

wishLists.append(ListSetting("self.pveFlag or not self.pvpFlag", [], "./wishlists/PvE.txt"))
wishLists.append(ListSetting("self.pvpFlag", [], "./wishlists/PvP.txt"))

wishLists.append(ListSetting("self.mkbFlag or not self.ctrFlag", [], "./wishlists/MKB.txt"))
wishLists.append(ListSetting("self.ctrFlag", [], "./wishlists/Controller.txt"))

wishLists.append(ListSetting("(self.pveFlag or not self.pvpFlag) and (self.mkbFlag or not self.ctrFlag)", [], "./wishlists/PvE-MKB.txt"))
wishLists.append(ListSetting("(self.pveFlag or not self.pvpFlag) and self.ctrFlag", [], "./wishlists/PvE-Controller.txt"))

wishLists.append(ListSetting("self.pvpFlag and (self.mkbFlag or not self.ctrFlag)", [], "./wishlists/PvP-MKB.txt"))
wishLists.append(ListSetting("self.pvpFlag and self.ctrFlag", [], "./wishlists/PvP-Controller.txt"))

wishLists.append(ListSetting("self.pveFlag and self.pvpFlag", [], "./wishlists/PvE-PvP.txt"))

wishLists.append(ListSetting("(self.pveFlag and self.pvpFlag) and (self.mkbFlag or not self.ctrFlag)", [], "./wishlists/PvE-PvP-MKB.txt"))
wishLists.append(ListSetting("(self.pveFlag and self.pvpFlag) and self.ctrFlag", [], "./wishlists/PvE-PvP-Controller.txt"))

wishLists.append(ListSetting("True", ["pandapaxxy"], "./wishlists/PandaPaxxy.txt"))

FileInfo(wishLists)