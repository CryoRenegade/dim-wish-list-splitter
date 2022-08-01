#list to store weapon info
currentWeapon = []

#flags for weapon tags
writeToPvE = False
writeToPvP = False
writeToMouse = False
writeToController = False

#voltron file in submodule
mainFile = "./dim-wish-list-sources/voltron.txt"

#main files in main repo
pveFile = "volton-PvE.txt"
pvpFile = "voltron-PvP.txt"
mouseFile = "voltron-MKB.txt"
controllerFile = "voltron-Controller.txt"

#combined flag files
pveMouseFile = "voltron-PvE-MKB.txt"
pvpMouseFile = "voltron-PvP-MKB.txt"
pveControllerFile = "voltron-PvE-Controller.txt"
pvpControllerFile = "voltron-PvP-Controller.txt"

#function to open and clean files
def clearFiles(fileName):
    with open(fileName, mode='w') as clearFile:
        pass

#clears al main files
clearFiles(pveFile)
clearFiles(pvpFile)
clearFiles(mouseFile)
clearFiles(controllerFile)

#clears all combined files
clearFiles(pveMouseFile)
clearFiles(pvpMouseFile)
clearFiles(pveControllerFile)
clearFiles(pvpControllerFile)

#function to write weapon info to file
def writeToFile(fileName, weaponInfo):    
    with open(fileName, mode='a') as tempFile:
        for i in weaponInfo:
            tempFile.write(i)
        tempFile.write("\n")
        
#function to read voltron file in submodule
#collect weapon info and trigger flags
#which then write to seperate files
with open(mainFile, mode='r', encoding='utf-8') as f:
    for l_no, line in enumerate(f):
        
        #Checks for PvE and PvP
        if 'PvE' in line or "pve" in line or 'PVE' in line:
            writeToPvE = True
        if 'PvP' in line or "pvp" in line or 'PVP' in line:
            writeToPvP = True

        #Checks for Controller or Mouse
        if 'Controller' in line or "controller" in line:
            writeToController = True
        if 'MKB' in line or 'mkb' in line or 'M+KB' in line or 'm+kb' in line:
            writeToMouse = True
        
        #If line isn't empty add to current weapon
        if len(line) != 1:
            currentWeapon.append(line)  
            
        #Line is empty so finished current weapon info
        else:
            #Handle if No flags Triggered
            #No PvE and PvP = PvE and PvP
            if not writeToPvE and not writeToPvP:
                writeToPvE = True
                writeToPvP = True
            
            #No Controller or Mouse = Mouse
            if not writeToController and not writeToMouse:
                writeToMouse = True
            #------------------------------------
            #Main Flags
            if writeToPvE:
                writeToFile(pveFile, currentWeapon)
            if writeToPvP:
                writeToFile(pvpFile, currentWeapon)
            if writeToController:
                writeToFile(controllerFile, currentWeapon)
            if writeToMouse:
                writeToFile(mouseFile, currentWeapon)

            #------------------------------------
            #Combined Flags
            if writeToPvE and writeToMouse:
                writeToFile(pveMouseFile, currentWeapon)
            
            if writeToPvP and writeToMouse:
                writeToFile(pvpMouseFile, currentWeapon)
                
            if writeToPvE and writeToController:
                writeToFile(pveControllerFile, currentWeapon)
            
            if writeToPvP and writeToController:
                writeToFile(pvpControllerFile, currentWeapon)
                  
            currentWeapon = []
            writeToPvE = False
            writeToPvP = False
            writeToMouse = False
            writeToController = False


