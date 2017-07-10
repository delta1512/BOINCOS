from sys import argv
from os import chdir
from shutil import copyfile

chdir('/boot/grub')

#backup():
#backs up the contents of fileName to fileName.bak
def backup(fileName):
    copyfile(fileName, '/' +fileName + '.bak')

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
                    occurance += 1
                if occurance > 0:
                    name += char
                    if occurance >= 2:
                        break
            entry[i] = line.replace(name, "'New Computer'")
        if len(line) > 1:
            if line[:7].split()[0] == 'linux':
                entry[i] = line[:len(line)-1] + ' nomodeset\n'
    with open('/etc/grub.d/40_custom', 'a') as custom:
        for line in entry:
            custom.write(line)

#makeDefaultEntry():
#checks the /etc/default/grub file to see if it has the necessary GRUB_DEFAULT
#flag. If yes, leave it as is, else leave as is
def makeDefaultEntry():
    temporaryFile = []
    needsLine = False
    with open('/etc/default/grub', 'r') as grubFlags:
        for line in grubFlags:
            if (line[:12] == 'GRUB_DEFAULT') and (line[13:] != "'New Computer'"):
                needsLine = True
                continue
            temporaryFile.append(line)
        if needsLine:
            with open('/etc/default/grub', 'w') as grubFlags:
                for line in temporaryFile:
                    grubFlags.write(line)
                grubFlags.write("\nGRUB_DEFAULT='New Computer'")
