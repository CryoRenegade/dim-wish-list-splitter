currentWeapon = []
writeToPvE = False
writeToPvP = False
writeToTotal = False

mainFile = "voltron.txt"

pveFile = "writePvE.txt"
pvpFile = "writePvP.txt"
totalFile = "writeTotal.txt"
neitherFile = "writeNeither.txt"

def clearFiles(fileName):
    with open(fileName, mode='w') as clearFile:
        pass

clearFiles(pveFile)
clearFiles(pvpFile)
clearFiles(totalFile)
clearFiles(neitherFile)

def writeToFile(fileName, weaponInfo):    
    with open(fileName, mode='a') as tempFile:
        for i in weaponInfo:
            tempFile.write(i)
        tempFile.write("\n")
        
with open(mainFile, mode='r', encoding='utf-8') as f:
    for l_no, line in enumerate(f):
        
        if 'PvE' in line or "pve" in line or 'PVE' in line:
            writeToPvE = True
        if 'PvP' in line or "pvp" in line or 'PVP' in line:
            writeToPvP = True
                
        writeToTotal = True
        
        if len(line) != 1:
            currentWeapon.append(line)        
        else:
            if writeToPvE:
                writeToFile(pveFile, currentWeapon)
            if writeToPvP:
                writeToFile(pvpFile, currentWeapon)
            if not writeToPvE and not writeToPvP:
                writeToFile(neitherFile, currentWeapon)
                
            writeToFile(totalFile, currentWeapon)
                    
            currentWeapon = []
            writeToPvE = False
            writeToPvP = False
            writeToTotal = False


