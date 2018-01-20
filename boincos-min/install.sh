#!/bin/bash

# Script that finalises the system, to be run after reboot and chroot-install.sh
# on a non-root user account
# Authors:
#   - Delta

ping -c 1 archlinux.org

if [ $? != 0 ]; then
  echo "You are not connected to the internet, exiting..."
  exit 1
fi

echo "Installing all packages..."

sudo pacman -S --needed htop bmon sudo openssh ufw lm_sensors netcat screen \
                boinc-nox boinctui git base-devel xf86-video-intel \
                xf86-video-amdgpu xf86-video-ati nvidia opencl-mesa \
                opencl-nvidia ocl-icd

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
echo -e "[Unit]
Description=BOINC Daemon\n
[Service]
User=boinc
Nice=19
ExecStart=/usr/bin/boinc_client --dir /var/lib/boinc --redirectio --allow_gui_rpc\n
[Install]
WantedBy=multi-user.target" | sudo tee /var/lib/systemd/system/boinc.service
cd /home/boincuser/
echo "alias man boincos-helper='boincos-helper --help'
alias boincos='boincos-helper --help'
alias help='boincos-helper --help'
alias ?='boincos-helper --help'"
cd /tmp/
git clone https://github.com/delta1512/BOINCOS.git
cd BOINCOS/boincos-min/
sudo mkdir /opt/helper/
sudo chown -R boincuser:boincuser /opt/helper/
sudo mv *.py /opt/helper/
sudo mv fwset /usr/bin/
sudo mv boincos-helper /usr/bin/
mv bashrc /home/boincuser/.bashrc
sudo mv helper.man /opt/helper/
sudo chmod +x /usr/bin/fwset /usr/bin/boincos-helper
sudo chmod -w /usr/bin/fwset /usr/bin/boincos-helper
sudo chmod -R -w /opt/helper/
sudo chmod -R +rx /opt/helper/
cd /usr/bin/
sudo ln -sf python2.7 python
cd /
sudo systemctl enable boinc
sudo systemctl enable sshd
sudo netctl enable eth
fwset reset
fwset off

echo
echo "Initialising and configuring BOINC..."

sudo systemctl start boinc
sudo usermod -a -G boinc boincuser
cd /var/lib/
sleep(120) # Wait for the BOINC client to generate all necessary files
echo "boincos" | sudo tee boinc/gui_rpc_auth.cfg
sudo chown -R boinc:boinc boinc/
sudo chmod -R ug+rw boinc/
cd /

echo
echo "Cleaning up installation..."

sudo pacman -Scc
sudo rm /etc/netctl/wifi
sudo journalctl --flush --rotate
sudo journalctl --vacuum-size=1M
echo > /home/boincuser/.bash_history
sudo mv /root/sudoers.bak /tmp/
sudo rm -rf /root/*

echo
echo "Moving to final security steps..."

read -p "Perform security lockout? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
  sudo passwd -l root
  cd /etc/
  sudo chmod u+w sudoers
  sudo mv /tmp/sudoers.bak sudoers
  echo "%sudo ALL=(ALL) NOPASSWD: /usr/bin/pacman -Syu,/usr/bin/reboot,/usr/bin/shutdown,/usr/bin/ufw,/usr/bin/systemctl" \
  | sudo tee -a sudoers
  sudo chmod -w sudoers
  cd /
else
  exit 0
fi
