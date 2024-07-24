#!/bin/bash

# Function to configure fail2ban.conf
configure_fail2ban_conf() {
    # Uncomment the allowipv6 = auto line
    sudo sed -i '/allowipv6 =.*/s/^#//g' /etc/fail2ban/fail2ban.conf
}


# Function to configure jail.conf
configure_jail_conf() {
    sudo sed -i '/\[sshd\]/,/backend = .*/ s/backend = .*/backend = systemd/' /etc/fail2ban/jail.conf
}

# Configure fail2ban.conf
configure_fail2ban_conf

# Configure jail.conf
configure_jail_conf

systemctl restart fail2ban
echo "Fail2Ban configuration updated successfully."