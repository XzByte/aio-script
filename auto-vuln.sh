#!/bin/bash
echo "Don't forget to manually edit on file 000 and the .bak file on /etc/apache2/sites-available/%%.conf"
add_option_to_custom_conf() {
    if grep -q "Options +Indexes" /etc/apache2/sites-available/custom.conf; then
        echo "Options +Indexes already present in custom.conf. No action taken."
    else
        echo "Options +Indexes" | sudo tee -a /etc/apache2/sites-available/custom.conf > /dev/null
    fi
}

uninstall_fail2ban() {
    sudo apt purge --autoremove fail2ban -y
}

cd /etc/apache2/sites-available || exit

cp 000-default.conf 000-default.conf.bak || true

add_option_to_custom_conf

cd /var/www/html || exit

mkdir -p asset || true

touch asset/test.py || true

chmod 777 asset || true

cd /etc/apache2 || exit

touch testfile.py || true

chmod 777 testfile.py || true

uninstall_fail2ban

sudo systemctl reload apache2

echo "Configuration changes applied successfully."