from sys import argv
from os import chdir
from shutil import copyfile

chdir('/boot/grub')

#backup():
#backs up the contents of fileName to fileName.bak
def backup(fileName):
    copyfile(fileName, '/' + fileName + '.bak')

#findEntry():
#looks at the start of each line to find the term within the config
#if found, find the associated curly bracket and do something with the code block

#if writeopt is true: it will remove that code block and rewrite the file
#if writeopt is false: it will collect all corresponding code blocks and
#return them, diregarding the rest of the file and not writing anything
def findEntry(term, writeopt):
    temporaryFile = []
    with open('grub.cfg', 'r') as grubCFG:
        foundEntry = False
        bracketStack = 0
        for line in grubCFG:
            if len(line) > 1:
                if line[:len(term)+10].split()[0] == term:
                    foundEntry = True
            if foundEntry:
                for char in line:
                    if char == '{':
                        bracketStack += 1
                    elif char == '}':
                        bracketStack -= 1
                if bracketStack <= 0:
                    foundEntry = False
                if not writeopt:
                    temporaryFile.append(line)
                continue
            if writeopt:
                temporaryFile.append(line)
    if writeopt:
        with open('grub.cfg', 'w') as grubCFG:
            for line in temporaryFile:
                grubCFG.write(line)
    else:
        return temporaryFile

#makeNovideoEntry():
#should be only run once ever
#takes the new config from the findEntry, changes the name and appends
#a nomodeset flag to the boot arguments
def makeNovideoEntry(entry):
    for i, line in enumerate(entry):
        if line[:9] == 'menuentry':
            name = ""
            occurance = 0
            for char in line:
                if char == "'":
                    name += char
                    occurance += 1
                if occurance > 0:
                    if occurance >= 2:
                        name += char #works for some reason if this is put here
                        break
                    name += char
            line.replace(name, "'New Computer'") #does not successfully replace
            entry[i] = line
        if len(line) > 1:
            if line[:7].split()[0] == 'linux':
                #witnessed the result of the following removing the \n so that
                #the next command appears to be in the same line. Be sure that
                #grub can still operate, else refactor the code to satisfy
                entry[i] = line + 'nomodeset'
    with open('/etc/grub.d/40_custom', 'a') as custom:
        for line in entry:
            custom.write(line)

backup('grub.cfg')
findEntry('submenu', True)
makeNovideoEntry(findEntry('menuentry', False))
