#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>

void fix_permissions() {
    system("chmod 644 /etc/apache2/*");
    system("chmod 644 /var/www/html/*");
}

int main() {
    fix_permissions();
    return 0;
}

