# git submodule update --remote

#voltron file in submodule
mainFile = "./dim-wish-list-sources/voltron.txt"

pveFlag = False
pvpFlag = False
mkbFlag = False
ctrFlag = False
dimFlag = False

listSettings = [
                {
                "flags": "pveFlag or not pvpFlag", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/PvE.txt"
                },
                {
                "flags": "pvpFlag", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/PvP.txt"
                },
                {
                "flags": "mkbFlag or not ctrFlag", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/MKB.txt"
                },
                {
                "flags": "ctrFlag", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/Controller.txt"
                },
                {
                "flags": "(pveFlag or not pvpFlag) and (mkbFlag or not ctrFlag)", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/PvE-MKB.txt"
                },
                {
                "flags": "(pveFlag or not pvpFlag) and ctrFlag", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/PvE-Controller.txt"
                },
                {
                "flags": "pvpFlag and (mkbFlag or not ctrFlag)", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/PvP-MKB.txt"
                },
                {
                "flags": "pvpFlag and ctrFlag", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/PvP-Controller.txt"
                },
                {
                "flags": "pveFlag and pvpFlag", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/PvE-PvP.txt"
                },
                {
                "flags": "(pveFlag and pvpFlag) and (mkbFlag or not ctrFlag)", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/PvE-PvP-MKB.txt"
                },
                {
                "flags": "(pveFlag and pvpFlag) and ctrFlag", 
                "search":[], "searchFlag": False,
                "FileName":"./wishlists/PvE-PvP-Controller.txt"
                },
                {
                "flags": "False", 
                "search":["pandapaxxy"], "searchFlag": False,
                "FileName":"./wishlists/PandaPaxxy.txt"
                }
                ]

lineCollection = []

#function to open and clean files
def clearFiles(wishListAll):
    for curList in wishListAll:
        with open(curList["FileName"], mode='w') as clearFile:
            pass

def checkWrite():
    for listParams in listSettings:
        if lineCollection != []:
            if (eval(listParams["flags"]) or listParams["searchFlag"]) or not dimFlag:
                with open(listParams["FileName"], mode='a') as tempFile:
                    for i in lineCollection:
                        tempFile.write(i)
                    tempFile.write("\n")

        listParams["searchFlag"] = False

clearFiles(listSettings)

with open(mainFile, mode='r', encoding='utf-8') as f:
    for line in f:
        #Non-empty Line. Add to Weapon. Check for Flags
        if len(line) != 1:
            lineCollection.append(line)
            
            if 'pve' in line.lower():
                pveFlag = True
            if 'pvp' in line.lower():
                pvpFlag = True
            if 'mkb' in line.lower() or "m+kb" in line.lower():
                mkbFlag = True
            if 'controller' in line.lower():
                ctrFlag = True
            if 'dimwishlist:item' in line.lower():
                dimFlag = True
            
            for listParams in listSettings:
                if any(i in line.lower() for i in listParams["search"]):
                    listParams["searchFlag"] = True
                    
        #Empty Line. Add Weapon to WishLists. Reset Flags
        else:
            checkWrite()
            
            pveFlag = False
            pvpFlag = False
            mkbFlag = False
            ctrFlag = False
            dimFlag = False
            
            lineCollection = []
        
     
    checkWrite()
