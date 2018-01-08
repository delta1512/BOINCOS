#!/bin/bash

# Script that finalises the system, to be run after reboot and chroot-install.sh
# Authors:
#   - Delta

ping -c 1 archlinux.org

if [ $? != 0 ]; then
  echo "You are not connected to the internet, exiting..."
  exit 1
fi

echo "Installing all packages..."

sudo pacman -S htop bmon sudo openssh ufw lm_sensors netcat screen boinc-nox \
                boinctui git base-devel xf86-video-intel xf86-video-amdgpu \
                xf86-video-ati nvidia opencl-mesa opencl-nvidia ocl-icd

echo
echo 'Fetching Intel OpenCL sources and dependencies...'

cd /tmp/
git clone https://aur.archlinux.org/ncurses5-compat-libs.git
git clone https://aur.archlinux.org/intel-opencl-runtime.git

echo
echo "Installing source packages..."

cd ncurses5-compat-libs/
gpg --recv-key C52048C0C0748FEE227D47A2702353E0F7E48EDB
makepkg -si

cd ../intel-opencl-runtime/
makepkg -si
cd /

echo
echo "Configuring system..."

echo "/usr/lib" | sudo tee /etc/ld.so.conf.d/00-usrlib.conf
echo -e "\nPermitRootLogin no" | sudo tee -a /etc/ssh/sshd_config
cd /etc/netctl
cp examples/ethernet-dhcp eth
cd /
echo -e "<cc_config>\n\t<options>\n\t\t<use_all_gpus>1</use_all_gpus>\n\t</options>\n</cc_config>" \
        | sudo tee /var/lib/boinc/cc_config.xml
sudo systemctl enable boinc
sudo systemctl enable sshd
sudo netctl enable eth
sudo ufw enable
