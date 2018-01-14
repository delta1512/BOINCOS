#!/bin/bash

# Script that prepares the base system, to be run after arch-chroot
# into the mounted USB
# Authors:
#   - Delta

echo "Beginning chroot installation for BOINCOS-MIN"
echo "Setting locales..."

cd /etc/

cp locale.gen locale.gen.bak
echo "en_US.UTF-8 UTF-8" > locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > locale.conf

echo
echo "Setting hostname and hosts..."

echo "BOINCOS-MIN" > hostname
echo > hosts
echo "127.0.0.1    localhost.localdomain	localhost" >> hosts
echo "::1          localhost.localdomain	localhost" >> hosts
echo "127.0.1.1    BOINCOS-MIN.localdomain	localhost" >> hosts

echo
echo "Installing initial packages..."

pacman -S efibootmgr grub wpa_supplicant dialog intel-ucode sudo

echo
echo "Installing grub for uefi..."
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=BOINCOS --removable --recheck
grub-mkconfig -o /boot/grub/grub.cfg

echo
echo "Downloading grub configuration script..."
cd /tmp/
wget https://raw.githubusercontent.com/delta1512/BOINCOS/master/cross-distro/grub_configure.py
echo "Executing script..."
python3 grub_configure.py

echo
echo "Setting user accounts and appending sudoers..."

useradd -m boincuser
groupadd sudo
usermod -a -G sudo boicuser
chmod u+w sudoers
cp sudoers sudoers.bak
echo >> sudoers
echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> sudoers
chmod -w sudoers

echo
echo "Chroot install complete, please reset root and boincuser passwords"
