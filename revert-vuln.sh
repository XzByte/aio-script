#!/bin/bash

# Function to remove or revert changes in Apache configuration files
revert_apache_config() {
    local file=$1
    local backup_file=$2
    if [ -f "$backup_file" ]; then
        cp "$backup_file" "$file"
    else
        echo "No backup found for $file. Manual intervention required."
    fi
}

# Revert changes in Apache configuration files
revert_apache_config "/etc/apache2/sites-available/custom.conf" "/etc/apache2/sites-available/custom.conf.bak"

# Remove or revert the asset directory and its contents
if [ -d "/var/www/html/asset" ]; then
    rm -rf "/var/www/html/asset"
else
    echo "Asset directory does not exist. No action taken."
fi

# Remove or revert the testfile.py
if [ -f "/etc/apache2/testfile.py" ]; then
    rm "/etc/apache2/testfile.py"
else
    echo "testfile.py does not exist. No action taken."
fi

# Reset permissions of parent directories
chown -R www-data:www-data /var/www/html
chmod -R 644 /var/www/html

# Reload Apache to apply changes
sudo systemctl reload apache2

echo "Reverted changes successfully."