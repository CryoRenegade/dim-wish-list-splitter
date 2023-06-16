import re
from collections import OrderedDict
from collections import Counter
import copy
#import sys

# Dictionary for each weapon, values are tags and rolls
allWeapons = {}
# Array of credit information
creditAry = []

def main():
    readFile("./dim-wish-list-sources/voltron.txt")
    #readFile("./temp.txt")

def readFile(filePath):
    with open(filePath, mode='r', encoding='utf-8') as f:
        fileLines = f.readlines()
        # Temp array to hold info for current weapon
        weaponAry = []
        
        for i, curLine in enumerate(fileLines):
            # Content in line, add to weapon
            if len(curLine) > 1:
                weaponAry.append(curLine)

            # Empty line or last line, inspect weapon and reset weaponAry
            if (weaponAry != [] and (i == len(fileLines)-1 or len(curLine) <= 1)):
                inspectWeapon(weaponAry)
                weaponAry = []
                
        # Look at wishlist options after reading file
        inspectWishlistConfig()

# Get itemID, add to Dict: { itemid: [[tags, roll], [tags, roll], ...] }
def inspectWeapon(_weaponAry):
    # Reverse loop weapon to get itemID
    rWeaponAry = copy.copy(_weaponAry)
    rWeaponAry.reverse()
    weaponTags = ""
    itemID = -1

    for curLine in rWeaponAry:
        # Finding Tags ------------------------------------
        curLine = curLine.lower()

        # When DIM line, get itemID
        if ("dimwishlist:item=" in curLine):                                
            # Get's itemID
            itemID = curLine[curLine.index("dimwishlist:item=") + 17: curLine.index("&perks=")]
            # Add itemID to tags
            if ("itemID:" not in weaponTags):
                weaponTags += " | itemID:" + itemID + "/itemID"

        # Search Every Line For:  ---------------------------
        if ("dimwishlist:item=" in curLine):                                
            if ("_dim" not in weaponTags):
                weaponTags += " | _dim "
            
         # Check to add credit tag
        if ("https://" in curLine or "u/" in curLine):
            weaponTags += " | _credits "

        # Check for custom tags
        if ("god-" in curLine):
            weaponTags += " | god- "
        if ("first-" in curLine):
            weaponTags += " | first- "
        if ("backup roll" in curLine):
            weaponTags += " | backup roll "
        if ("pandapaxxy" in curLine):
            weaponTags += " | pandapaxxy "

        # Search in Specific Area ----------------------------------------
        # All text between '(...)'
        pTags = re.findall(r"(?<=\().+?(?=\))", curLine)
        weaponTags += " | " + " | ".join(str(i) for i in pTags)

        # All text between '[...]'
        bTags = re.findall(r"(?<=\[).+?(?=\])", curLine)
        weaponTags += " | " + " | ".join(str(i) for i in bTags)
    
        # All text after tags:
        if ("tags:" in curLine):
            weaponTags += " | " + curLine[curLine.index("tags:"):]            
        
    # Change all m+kb to mkb
    weaponTags = weaponTags.replace("m+kb", "mkb")
    
    # If weapon is mising Input or Gamemode tag add default of MKB and PVE
    if (not re.search("mkb|controller", weaponTags)):
        weaponTags += " | mkb "
    if (not re.search("pve|pvp", weaponTags)):
        weaponTags += " | pve "

    # Add weapon tags and rolls to dictonary for all weapons
    if (itemID not in allWeapons and itemID != -1):
        allWeapons[itemID] = []
    if (itemID != -1):
        allWeapons[itemID].append([weaponTags, _weaponAry])

    # Add credit info to credit array
    if (itemID == -1 and "_dim" not in weaponTags and "_credit" in weaponTags):
        creditAry.append(_weaponAry)

# Look at wishlist options after reading file
# { itemid: [[tags, roll], [tags, roll], ...] }
def inspectWishlistConfig():
    for wishlist in listConfigs:
        # Write Credits to File
        for credits in creditAry:
            writeToFile(wishlist, credits)

        # Get all Keys for weapon ID
        for itemID in allWeapons.keys():
            # Array for roll sets that pass check
            allowedRecs = []
            for weaponInfo in allWeapons.get(itemID):
                tags = weaponInfo[0]
                weaponAry = weaponInfo[1]

                if (checkFilters(wishlist, tags) == False):
                    continue

                weaponAry = perkAdjustments(wishlist, weaponAry)

                allowedRecs.append(weaponAry)
            
            if ("dupes" not in wishlist):
                writeToFile(wishlist, allowedRecs)
                continue

            # Array storing lines that include dim rolls
            allDims = []
            for curRec in allowedRecs:
                for curLine in curRec:
                    if ("dimwishlist:item=" in curLine):
                        allDims.append(curLine)

            # Find dupe count and limit perks
            perkCount = dict(Counter(allDims))
            reqCount = min(int(wishlist.get("dupes") * len(allWeapons.get(itemID)) / 10), wishlist.get("dupes"))
            allowedPerks = {key for key, value in perkCount.items() if value >= reqCount}
            #allowedPerks = {key for key, value in perkCount.items() if value >= 2}
            
            allowedRecs = getAllowedPerks(allowedRecs, allowedPerks)

            writeToFile(wishlist, allowedRecs)

# Checks weapon perks and removes those which aren't allowed
def getAllowedPerks(_allowedRecs, allowedPerks):
    if (len(allowedPerks) <= 0):
        return _allowedRecs
    
    allowedRecs = []
    for index, curRec in enumerate(_allowedRecs):
        allowedRecs.append([])
        for curLine in curRec:
            if ("dimwishlist:item=" not in curLine):
                allowedRecs[index].append(curLine)
            elif (curLine in allowedPerks):
                allowedRecs[index].append(curLine)
    
    return allowedRecs

# Removes Origin Trait Column
# Limits Perk Columns if Wishlist wants
def perkAdjustments(wishlist, _weaponAry):
    weaponAry = []
    for curLine in _weaponAry:
        if ("dimwishlist:item=" in curLine):
            if ("\n" not in curLine):
                curLine += "\n"
            allPerks = curLine[curLine.index("&perks=")+7:curLine.index("\n")].split(",")

            # Remove Origin Perk
            if (len(allPerks) > 4):                                
                selPerks = [allPerks[i] for i in [0, 1, 2, 3]]
                allPerks = selPerks
            
            if ("perks" in wishlist and len(allPerks) >= len(wishlist.get("perks"))):
                selPerks = [allPerks[i - 5 + len(allPerks)] for i in wishlist.get("perks")]
                # selPerks = [allPerks[i] for i in [len(allPerks)-2, len(allPerks)-1]]
                curLine = curLine[:curLine.index("&perks=")+7] + ",".join(str(i) for i in selPerks) + "\n"
        
        weaponAry.append(curLine)

    # Remove duplicates
    weaponAry = list(OrderedDict.fromkeys(weaponAry))

    # Limits Duplicates
    #if ("dupes" in wishlist):
    #    perkCount = OrderedDict(Counter(weaponAry))
    #    newWeapon = []
    #    # newWeapon = {key for key, value in perkCount.items() if value < wishlist.get("dupes")}
    #    for key, val in perkCount.items():
    #        if (val > int(wishlist.get("dupes"))):
    #            val = int(wishlist.get("dupes"))
    #        for i in range(val):
    #            newWeapon.append(key)
    #    return newWeapon

    return weaponAry

# Single [] = and (ex. [] and [])
# Mutlieple in [] = or (ex. [x or y] and [a or b])
def checkFilters(wishlist, tags):
    if ("_dim" in tags):
        if ("include" in wishlist):

            for curFilter in wishlist.get("include"):
                filterSplit = curFilter.split(" ")
                if (len(filterSplit) <= 1):
                    if (curFilter not in tags):
                        return False
                else:
                    if (not any(i in tags for i in curFilter.split(" "))):
                        return False       

        if ("exclude" in wishlist):
            if (any(i in tags for i in wishlist.get("exclude"))):
                return False
    elif ("_credit" not in tags):
        return False

    return True

# weaponAry = 2D Array
def writeToFile(wishlist, weaponAry):   
    with open(wishlist.get("path"), mode='a', encoding='utf-8') as file:
        for rec in weaponAry:
            for line in rec:
                file.write(line)
            file.write("\n")

# -----------------------------------------------------------------------------------------------------------------------------
# Array of Wishlists
# Each Wishlist is a Dictionary with 
#   Flag - True / False for Filter Options
#   Include / Exclude Filter - Using AND logic: PVE, PVP, MKB, Controller, Backup Roll, God, etc. 
#   Logic - ["A", "B"] = A and B, ["A B"] = A or B
#   Perk Columns - "" or "1, 2, 3, 4" for All or "3, 4" for 3rd and 4th, etc.  
#   Grouping Options - Combines Recommendations per Weapon ex. 0 for all combines or 2 for at least 2 recommendations
#   Destination Path - Location and Name for Wishlist
listConfigs = []

# -------------------------------------------
# No Filters
listConfigs.append({"path": "./wishlists/All.txt"})

# -------------------------------------------
# Gamemode Filters
listConfigs.append({"include": ["PVE"], 
                    "path": "./wishlists/PVE.txt"})
listConfigs.append({"include": ["PVP"], 
                    "path": "./wishlists/PVP.txt"})

# -------------------------------------------
# Input Filters
listConfigs.append({"include": ["MKB"], 
                    "path": "./wishlists/MKB.txt"})
listConfigs.append({"include": ["Controller"], 
                    "path": "./wishlists/CTR.txt"})

# -------------------------------------------
# Input Filters | 3rd and 4th Columns
listConfigs.append({"include": ["MKB"],
                    "perks": [3, 4],
                    "path": "./wishlists/MKB_Perks.txt"})
listConfigs.append({"include": ["Controller"],
                    "perks": [3, 4], 
                    "path": "./wishlists/CTR_Perks.txt"})

# -------------------------------------------
# Input Filters | 3rd and 4th Columns | At Least 2 Dupes
listConfigs.append({"include": ["MKB"],
                    "perks": [3, 4],
                    "dupes": 2,
                    "path": "./wishlists/MKB_Perks_D2.txt"})
listConfigs.append({"include": ["Controller"],
                    "perks": [3, 4],
                    "dupes": 2, 
                    "path": "./wishlists/CTR_Perks_D2.txt"})

# -------------------------------------------
# Input_Gamdemode Filters
listConfigs.append({"include": ["MKB", "PVE"], 
                    "path": "./wishlists/MKB_PVE.txt"})
listConfigs.append({"include": ["MKB", "PVP"], 
                    "path": "./wishlists/MKB_PVP.txt"})
listConfigs.append({"include": ["Controller", "PVE"], 
                    "path": "./wishlists/CTR_PVE.txt"})
listConfigs.append({"include": ["Controller", "PVP"], 
                    "path": "./wishlists/CTR_PVP.txt"})

# -------------------------------------------
# PandaPaxxy Filters
listConfigs.append({"include": ["pandapaxxy"], 
                    "path": "./wishlists/Panda.txt"})

listConfigs.append({"include": ["MKB", "pandapaxxy"], 
                    "path": "./wishlists/MKB_Panda.txt"})
listConfigs.append({"include": ["MKB", "PVE", "pandapaxxy"],
                    "path": "./wishlists/MKB_Panda_PVE.txt"})
listConfigs.append({"include": ["MKB", "PVP", "pandapaxxy"], 
                    "path": "./wishlists/MKB_Panda_PVP.txt"})

listConfigs.append({"include": ["Controller", "pandapaxxy"], 
                    "path": "./wishlists/CTR_Panda.txt"})
listConfigs.append({"include": ["Controller", "PVE", "pandapaxxy"], 
                    "path": "./wishlists/CTR_Panda_PVE.txt"})                        
listConfigs.append({"include": ["Controller", "PVP", "pandapaxxy"],
                    "path": "./wishlists/CTR_Panda_PVP.txt"})

listConfigs.append({"include": ["MKB", "pandapaxxy"],
                    "perks": [3,4],
                    "path": "./wishlists/MKB_Panda_Perks.txt"})

# -------------------------------------------
# God Filters
listConfigs.append({"include": ["MKB"],
                    "include": ["god- first-"], 
                    "path": "./wishlists/MKB_God.txt"})

# -------------------------------------------
# Exclude Backup Rolls - Input Filters
listConfigs.append({"include": ["MKB"],
                    "exclude": ["Backup Roll"],
                    "path": "./wishlists/MKB_!Backup.txt"})
                
listConfigs.append({"include": ["MKB"],
                    "exclude": ["Backup Roll"],
                    "perks": [3,4],
                    "path": "./wishlists/MKB_!Backup_Perks.txt"})

listConfigs.append({"include": ["MKB"],
                    "exclude": ["Backup Roll"],
                    "perks": [3,4],
                    "dupes": 2,
                    "path": "./wishlists/MKB_!Backup_Perks_D2.txt"})

# -----------------------------------------------------------------------------------------------------------------------------
# Clear Existing Files
def cleanExistingFiles():
    for wishlist in listConfigs:
        with open(wishlist.get("path"), mode='w') as clearFile:
            pass
        if ("include" in wishlist):
            wishlist["include"] = [i.lower() for i in wishlist.get("include")]
        if ("exclude" in wishlist):
            wishlist["exclude"] = [i.lower() for i in wishlist.get("exclude")]

#test()

#print(sys.getfilesystemencoding())
cleanExistingFiles()
main()
