from os import chdir
from shutil import copyfile

chdir('/boot/grub')

#backup():
#backs up the contents of fileName to fileName.bak
def backup(fileName):
    copyfile(fileName, '/' + fileName + '.bak')

'''def changeBootEntryName(new_name, line):
    current_name = ""
    apostrophe_count = 0
    for char in line:
        if char == "'":
            apostrophe_count += 1
        if apostrophe_count > 0:
            current_name += char
            if apostrophe_count >= 2:
                break
    return line.replace(current_name, new_name)'''

def writeListToFile(directory, data):
    with open(directory, 'w') as f:
        for line in data:
            f.write(line)

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
        writeListToFile('grub.cfg', temporaryFile)
    else:
        return temporaryFile

#entryPostProcess():
def entryPostProcess(entry, boot_name, nomodeset):
    for i, line in enumerate(entry):
        if line[:9] == 'menuentry':
            entry[i] = line.replace("'Arch Linux'", boot_name)
        if (len(line) > 1) and nomodeset:
            if line[:7].split()[0] == 'linux':
                entry[i] = line[:len(line)-1] + ' nomodeset\n'
    return entry

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
    writeListToFile('grub.cfg', temporaryFile)

backup('grub.cfg')
findEntry('submenu', True)
default_entry = findEntry('menuentry', False)
backup_entry = findEntry('menuentry', False)
findEntry('menuentry', True)
final_entry = entryPostProcess(default_entry, "'BOINCOS'", False)
final_entry1 = entryPostProcess(backup_entry, "'BOINCOS - KMS failure fallback'", True)
#writeListToFile('/tmp/test.cfg', entryPostProcess(default_entry, "'BOINCOS'", False))
#writeListToFile('/tmp/test.cfg.1', entryPostProcess(backup, "'BOINCOS - KMS failure fallback'", True))
reconstructGrubCFG(final_entry + final_entry1)
