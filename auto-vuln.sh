#!/bin/bash

# Function to safely edit apache configuration files
add_option_to_custom_conf() {
    # Check if the line already exists
    if grep -q "Options +Indexes" /etc/apache2/sites-available/custom.conf; then
        echo "Options +Indexes already present in custom.conf. No action taken."
    else
        echo "Options +Indexes" | sudo tee -a /etc/apache2/sites-available/custom.conf > /dev/null
    fi
}

uninstall_fail2ban() {
    sudo apt purge --autoremove fail2ban -y
}

# Navigate to the sites-available directory
cd /etc/apache2/sites-available || exit

# Backup the original 000-default.conf file
cp 000-default.conf 000-default.conf.bak || true

# Append "Options +Indexes" to custom.conf
add_option_to_custom_conf

# Navigate to the html directory
cd /var/www/html || exit

# Create the asset directory if it doesn't exist
mkdir -p asset || true

# Create test.py in the asset directory
touch asset/test.py || true

# Change permissions of the asset directory to 777
chmod 777 asset || true

# Navigate to the apache2 directory
cd /etc/apache2 || exit

# Create testfile.py
touch testfile.py || true

# Change permissions of testfile.py to 777
chmod 777 testfile.py || true

uninstall_fail2ban

# Reload Apache to apply changes
sudo systemctl reload apache2

echo "Configuration changes applied successfully."