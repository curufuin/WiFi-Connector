This Code is designed to search for an open wifi with the best signal, or an encrypted wifi for which you have the credentials on a custom rasbian router.  I am going to assume you have a rasberry pi, with raspbian on it and an external wifi adapter named wlan1 as well as the onboard wlan0.

Login to the pi using SSH:

ssh pi@(Pi's IP here)
The default password will be "raspberry".  If you changed that, then use the updated password, if not you should at the end of this as your router will be visible to any network you are connected to.

Get these dependancies:

sudo apt-get install python-pip hostapd dnsmasq git

stop hostapd and dnsmasq:

sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

Then configure a static IP for wlan0 in /etc/dhcpcd.conf:

interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant

192.168.4.1 is the static IP for wlan0.

Backup the default dnsmasq configuration file:

sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig

Edit /etc/dnsmasq.conf with your favorite editor and add the following:

interface=wlan0    
  dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h

Configure hostapd:

touch /etc/hostapd/hostapd.conf

and edit /etc/hostapd/hostapd.conf to contain the following:

interface=wlan0
driver=nl80211
ssid=NETWORK
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=PASSWORD

wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

Then Edit /etc/default/hostapd:

DAEMON_CONF="/etc/hostapd/hostapd.conf"

Forward the traffic between the interfaces, in the /etc/sysctl.conf uncomment:

#net.ipv4.ip_forward=1

it should read:

net.ipv4.ip_forward=1

Enable ip masquerading on wlan1:

sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT 

Save the iptables rules:

sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

Add the following line to /etc/rc.local:

iptables-restore < /etc/iptables.ipv4.nat

and:

sudo reboot

Now grab these dependancies:

sudo pip install wifi wireless netifaces 

create a folder for the project and clone the repository:

git clone https://github.com/curufuin/WiFi-Connector

blacklist.txt is an essid blacklist file.  One entry per line.

passwords.txt contains passwords for secure wifi.  One entry per line

edit the crontab as follows:

sudo crontab -e

* * * * * /usr/bin/sudo /usr/bin/python (path to connector.py) >> (path to log file) 2>&1

Edit /etc/dnsmasq.conf file to us a specific dns server.  You can use any dns you want, but this is how it would look for the Chaos Computer Club DNS:

server=213.73.91.35

You can find other servers here:

https://anonymous-proxy-servers.net/wiki/index.php/Censorship-free_DNS_servers 

Finally: 

sudo reboot
