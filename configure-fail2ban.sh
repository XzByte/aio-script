#!/bin/bash
echo "Configuring fail2ban after installing (when necessary), and before running main script (main.py)"
configure_fail2ban_conf() {
    sudo sed -i '/allowipv6 =.*/s/^#//g' /etc/fail2ban/fail2ban.conf
}

configure_jail_conf() {
    sudo sed -i '/\[sshd\]/,/backend = .*/ s/backend = .*/backend = systemd/' /etc/fail2ban/jail.conf
}

configure_fail2ban_conf

configure_jail_conf

systemctl restart fail2ban
echo "Fail2Ban configuration updated successfully."