import logging
import os, re
import subprocess


global_fixes = 0
global_scans = 0
alerts = [] 
output_messages = []
fix_performed = []


def check_directory_listing():
    global global_fixes, global_scans, alerts, output_messages, fix_performed
    config_path = '/etc/apache2/sites-available/'
    bannr = "Checking directory listing configuration..."
    output_messages.append(bannr)
    logging.info(bannr)
    cntr = 0
    for root, dir, files in os.walk(config_path):
        for name in files:
            global_scans += 1
            file_path = os.path.join(root, name)
            fix = ""
            with open(file_path, 'r') as file:
                content = file.read()

            if 'Options Indexes' in content:
                alert_message = "ALERT: Directory listing enabled."
                logging.warning(alert_message)
                updated_content = re.sub('Options Indexes', 'Options -Indexes', content)
                with open(file_path, 'w') as file:
                    file.write(updated_content)
                global_fixes += 1
                alerts.append(alert_message)
                bann = "Fixing directory listing: "+file_path
                logging.info(bann)
                output_messages.append(bann)
                fix = "Disable Apache2 Options Indexes: "+file_path
                fix_performed.append(fix)
                cntr += 1
                
            if 'Options +Indexes' in content:
                alert_message = "ALERT: Directory listing enabled."
                logging.warning(alert_message)
                updated_content = re.sub('Options \+Indexes', 'Options -Indexes', content)
                with open(file_path, 'w') as file:
                    file.write(updated_content)
                global_fixes += 1
                alerts.append(alert_message)
                bann = "Fixing directory listing: "+file_path
                logging.info(bann)
                output_messages.append(bann)
                fix = "Disable Apache2 Options Indexes: "+file_path
                fix_performed.append(fix)
                cntr += 1
    
    if cntr == 0:
        msg = "Directory listing configuration is OK."
        output_messages.append(msg)
        logging.info(msg)


def fix_permissions(base_dir):
    global global_fixes, output_messages, fix_performed
    global_fixes +=1
    path_e = '/etc/apache2/'
    path_v = '/var/www/html/'
    bannr = "Fixing Apache2 config files and directory permissions..."
    output_messages.append(bannr)
    logging.info(bannr)
    b_dir = base_dir
    f_file = b_dir+"/fix/fixapache"
    
    if not os.path.exists(f_file):
        c_f = "Compiled fix file does not exist...."
        logging.info(c_f)
        output_messages.append(c_f)
        try:
            gc_c = "Checking GCC existence...."
            logging.info(gc_c)
            output_messages.append(gc_c)
            subprocess.run(["gcc", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError:
            gc_e = "GCC does not exist."
            logging.info(gc_e)
            output_messages.append(gc_e)
            return False
        try:
            com_f = "GCC exist, try to compile fix file...."
            logging.info(com_f)
            output_messages.append(com_f)
            fc_file = f_file+".c"
            subprocess.run(["gcc", "-o", f_file, fc_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError:
            com_e = "Failed to compile fix file, skip fixing permissions."
            logging.error(gc_e)
            output_messages.append(gc_e)
            return False
        com_r = "Fix file compiled successfully."
        logging.info(com_r)
        output_messages.append(com_r)
    
    subprocess.run([f_file])
    fix_e = "Set Default Permissions (644) to: "+path_e
    fix_v = "Set Default Permissions (644) to: "+path_v
    logging.info(fix_e)
    logging.info(fix_v)
    output_messages.append(fix_e)
    output_messages.append(fix_v)


def restart_services():
    global output_messages
    bannr = "Restarting Apache2 and Fail2Ban Services..."
    logging.info(bannr)
    output_messages.append(bannr)
    try:
        ar_s = "Restart Apache2 services."
        logging.info(ar_s)
        output_messages.append(ar_s)
        subprocess.run(["systemctl", "restart", "apache2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        ar_r = "Failed to restart Apache2 services."
        logging.error(ar_r)
        output_messages.append(ar_r)
    try:
        fr_s = "Restart Fail2ban services."
        logging.info(fr_s)
        output_messages.append(fr_s)
        subprocess.run(["systemctl", "restart", "fail2ban"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        fr_r = "Failed to restart Fail2ban services."
        logging.error(fr_r)
        output_messages.append(fr_r)
    msg = "Restart Services Completed."
    logging.info(msg)
    output_messages.append(msg)
    

def scanfix_apache2(base_dir):
    global global_fixes, global_scan, alerts, output_messages, fix_performed
    b_dir = base_dir
    
    conf_sc = ("Starting Apache configuration scan...")
    logging.info(conf_sc)
    output_messages.append(conf_sc)
    
    check_directory_listing()
    dir_sc_comp = ("Directory listing scan completed.")
    logging.info(dir_sc_comp)
    output_messages.append(dir_sc_comp)
    
    fix_permissions(base_dir)
    conf_sc_comp = ("Apache configuration scan completed.")
    logging.info(conf_sc_comp)
    output_messages.append(conf_sc_comp)
    
    restart_services()
    return global_fixes, global_scans, alerts, output_messages, fix_performed

