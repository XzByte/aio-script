# Re-ABAC

mkdir /var/www/html/asset
touch /var/www/html/asset/file.txt
chmod 777 /var/www/html/asset/
ls –l /var/www/html/asset/

touch /etc/apache2/testfile.txt
chmod 777 /etc/apache2/testfile.txt
ls –l /etc/apache2/
tail -n 15 /var/log/apache2/access.log