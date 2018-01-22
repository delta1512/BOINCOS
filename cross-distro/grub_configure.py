from os import chdir
from shutil import copyfile

chdir('/boot/grub')

#backup():
#Backs up the contents of "fileName" to /srv/fileName.bak
def backup(fileName):
    copyfile(fileName, '/root/' + fileName + '.bak')

#writeListToFile()
#Writes the contets of a list to a file defined by "directory"
def writeListToFile(directory, data):
    with open(directory, 'w') as f:
        for line in data:
            f.write(line)

#findEntry():
#Looks at the start of each line to find the "term" within the config.
#If found, find the associated curly brackets to define a code block.

#if writeopt is True: it will remove that code block and rewrite the file
#if writeopt is False: it will collect all corresponding code blocks and
#                       return them, does not write anything.
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
        writeListToFile('grub.cfg', temporaryFile)
    else:
        return temporaryFile

#entryPostProcess():
#Modifies a grub menuentry name and optionally sets nomodeset flag on kernel params
def entryPostProcess(entry, boot_name, nomodeset):
    for i, line in enumerate(entry):
        if line[:9] == 'menuentry':
            entry[i] = line.replace("'Arch Linux'", boot_name)
        if (len(line) > 1) and nomodeset:
            if line[:7].split()[0] == 'linux':
                entry[i] = line[:len(line)-1] + ' nomodeset\n'
    return entry

#reconstructGrubCFG()
#Takes the stripped grub.cfg and appends the passed "entries" before updating the file
def reconstructGrubCFG(entries):
    temporaryFile = []
    with open('grub.cfg', 'r') as grubCFG:
        for line in grubCFG:
            if "### BEGIN /etc/grub.d/10_linux ###" in line:
                temporaryFile.append(line)
                for l in entries:
                    temporaryFile.append(l)
            else:
                temporaryFile.append(line)
    writeListToFile('/boot/grub/grub.cfg', temporaryFile)

backup('grub.cfg') # First backup the original config, just incase
findEntry('submenu', True) # Remove the default submenu and corresponding entries
default_entry = findEntry('menuentry', False) # Define the default
backup_entry = findEntry('menuentry', False) # Re-define the default to solve variable reference bug
findEntry('menuentry', True) # Remove the remaining menuentry
# Generate required menuentries from default templates
final_entry = entryPostProcess(default_entry, "'BOINCOS'", False)
final_entry1 = entryPostProcess(backup_entry, "'BOINCOS - KMS failure fallback'", True)
reconstructGrubCFG(final_entry + final_entry1) # Merge and write them to the config
