currentWeapon = []

writeToPvE = False
writeToPvP = False

writeToMouse = False
writeToController = False

mainFile = "./dim-wish-list-sources/voltron.txt"

pveFile = "volton-PvE.txt"
pvpFile = "voltron-PvP.txt"

mouseFile = "voltron-MKB.txt"
controllerFile = "voltron-Controller.txt"

pveMouseFile = "voltron-PvE-MKB.txt"

missingTagFile = "voltron-MissingTag.txt"


def clearFiles(fileName):
    with open(fileName, mode='w') as clearFile:
        pass

clearFiles(pveFile)
clearFiles(pvpFile)

clearFiles(mouseFile)
clearFiles(controllerFile)

clearFiles(pveMouseFile)

clearFiles(missingTagFile)


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

        if 'Controller' in line or "controller" in line:
            writeToController = True
        if 'MKB' in line or 'mkb' in line or 'M+KB' in line or 'm+kb' in line:
            writeToMouse = True
        
        
        if len(line) != 1:
            currentWeapon.append(line)  
            
        else:
            if writeToPvE:
                writeToFile(pveFile, currentWeapon)
            if writeToPvP:
                writeToFile(pvpFile, currentWeapon)
            if not writeToPvE and not writeToPvP:
                writeToFile(missingTagFile, currentWeapon)
                
            if writeToController:
                writeToFile(controllerFile, currentWeapon)
            if writeToMouse or not writeToController:
                writeToFile(mouseFile, currentWeapon)

            if writeToPvE and (writeToMouse or not writeToController):
                writeToFile(pveMouseFile, currentWeapon)
                    
            currentWeapon = []
            writeToPvE = False
            writeToPvP = False
            writeToMouse = False
            writeToController = False


