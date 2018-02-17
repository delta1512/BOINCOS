#!/bin/bash

# Script that prepares the base system, to be run after arch-chroot
# into the mounted USB
# Authors:
#   - Delta

echo "Beginning chroot installation for BOINCOS-MIN"
echo "Setting locales..."

cd /etc/

cp locale.gen /root/locale.gen.bak
echo "en_US.UTF-8 UTF-8" > locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > locale.conf

chmod +rw locale.gen locale.conf

echo
echo "Setting hostname and hosts..."

echo "BOINCOS-MIN" > hostname
echo > hosts
echo "127.0.0.1    localhost.localdomain	localhost" >> hosts
echo "::1          localhost.localdomain	localhost" >> hosts
echo "127.0.1.1    BOINCOS-MIN.localdomain	BOINCOS-MIN" >> hosts

echo "KEYMAP=us" > vconsole.conf

echo
echo "Installing initial packages..."

pacman -S efibootmgr grub wpa_supplicant dialog intel-ucode sudo wget python2

echo
echo "Installing grub for uefi..."
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=BOINCOS --removable --recheck
grub-mkconfig -o /boot/grub/grub.cfg

echo
echo "Downloading grub configuration script..."
cd /tmp/
wget https://raw.githubusercontent.com/delta1512/BOINCOS/master/cross-distro/grub_configure.py
echo "Executing script..."
python2 grub_configure.py

echo
echo "Setting user accounts and appending sudoers..."

cd /etc/
useradd -m boincuser
groupadd sudo
groupadd net
usermod -a -G sudo boincuser
usermod -a -G net boincuser
chmod u+w sudoers
cp sudoers /root/sudoers.bak
echo >> sudoers
echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> sudoers
chmod -w sudoers

echo
echo "Fetching the next installation script..."

cd /root/
wget https://raw.githubusercontent.com/delta1512/BOINCOS/master/boincos-min/install.sh

echo
echo "Chroot install complete, please reset root and boincuser passwords"
