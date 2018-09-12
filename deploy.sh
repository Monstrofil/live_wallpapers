# instruction of "how to deploy" this site

# add user to run site from
useradd live_wallpapers

# to install latest python and python-pip
yum install python-pip -y
pip install virtualenv==1.7

# to run commmands as user
su - live_wallpapers

# create project root
mkdir ~/wallpapers
cd wallpapers/