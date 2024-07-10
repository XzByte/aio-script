import logging
import subprocess
import os, sys, io
import time
from datetime import datetime
from scan.scanfixapache import scanfix_apache2


now = datetime.now()
timestamp = now.replace(microsecond=0).strftime("%Y-%m-%d_%H-%M-%S")
base_dir = os.path.dirname(os.path.realpath(__file__))
report_dir = base_dir+"/logs_and_reports/"
if not os.path.exists(report_dir):
    os.makedirs(report_dir)
l_file = report_dir+"logs-"+timestamp+".log"
log_msg = f"Output logged to {l_file}"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(l_file, mode='a')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def check_apache():
    try:
        logger.info("Checking apache2 existence....")
        subprocess.run(["systemctl", "start", "apache2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["systemctl", "status", "apache2"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def check_fail2ban():
    try:
        logger.info("Checking fail2ban existence....")
        subprocess.run(["systemctl", "start", "fail2ban"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        subprocess.run(["systemctl", "status", "fail2ban"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def install_fail2ban():
    try:
        logger.info("Attempting to install fail2ban...")
        subprocess.run(["apt-get", "install", "-y", "fail2ban"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logger.info("Fail2Ban installed successfully.")
        return True
    except subprocess.CalledProcessError:
        logger.error("Failed to install Fail2Ban.")
        return False


def create_config_files():
    num_files_created = 0
    total_lines_added = 0
    configs_performed = []
    j_file = base_dir+"/script/jail.conf"
    fl_file = base_dir+"/script/apache-exploit-attempts.conf"

    logger.info("Reading source files...... (fail2ban config)") 
    with open(j_file, "r") as source_jail_conf_file:
        jail_conf_content = source_jail_conf_file.read()
    with open(fl_file, "r") as source_apache_exploit_attempts_conf_file:
        apache_exploit_attempts_conf_content = source_apache_exploit_attempts_conf_file.read()
    
    logger.info("Writing to destination files...... (fail2ban config)")
    with open("/etc/fail2ban/jail.d/apache_access_jail.conf", "w") as jail_conf_file:
        jail_conf_file.write(jail_conf_content)
        num_files_created += 1
        total_lines_added += len(jail_conf_content.split('\n'))
        configs_performed.append("Updated Fail2Ban Jail: /etc/fail2ban/jail.d/apache_access_jail.conf")
    
    with open("/etc/fail2ban/filter.d/apache-exploit-attempts.conf", "w") as apache_exploit_attempts_conf_file:
        apache_exploit_attempts_conf_file.write(apache_exploit_attempts_conf_content)
        num_files_created += 1
        total_lines_added += len(apache_exploit_attempts_conf_content.split('\n'))
        configs_performed.append("Updated Fail2Ban Filter: /etc/fail2ban/filter.d/apache-exploit-attempts.conf")
    
    logger.info("Fail2ban configuration completed.")
    return num_files_created, total_lines_added, configs_performed


def main():
    apache_installed = check_apache()
    fail2ban_installed = check_fail2ban()

    if apache_installed:
        if not fail2ban_installed:
            logger.info("Fail2Ban does not exist or there is problem starting Fail2Ban services.")
            f2b_ins = install_fail2ban()
            if f2b_ins:
                files_created, lines_added, configs_performed = create_config_files()
            else:
                files_created = 0
                lines_added = 0
                configs_performed = []
                logger.info("Skip Fail2Ban configurations.")
        else:
            logger.info("Fail2Ban is already exist.")
            files_created, lines_added, configs_performed = create_config_files()
    else:
        logger.info("Apache2 does not exist or there is problem starting Apache2 services.")
        logger.info(log_msg)
        return False

    global_fixes, global_scans, alerts, output_messages, fix_performed = scanfix_apache2(base_dir)
    fix_count = global_fixes  
    scan_count = global_scans  
    alert_count = len(alerts) 
    
    print_report(fix_count, scan_count, alert_count, files_created, lines_added, configs_performed, global_fixes, global_scans, alerts, output_messages, fix_performed)
    logger.info(log_msg)


def print_report(fix_count, scan_count, alert_count, files_created, lines_added, configs_performed, global_fixes, global_scans, alerts, output_messages, fix_performed):
    report_text = f"#######################################################################\n"
    report_text += f"\nReport:\n"
    report_text += f"Total Configurations Scanned (Apache2): {scan_count}\n"
    report_text += f"Total Fixes Applied (Apache2): {fix_count}\n"
    report_text += f"Alerts Generated (Vuln/Misconfig detected): {alert_count}\n"
    report_text += f"Config Created (Fail2Ban): {files_created}\n"
    report_text += f"Lines Added (Fail2Ban Config): {lines_added}\n"
    report_text += f"Configurations Performed:\n"
    
    for conf in configs_performed:
            report_text += f"- {conf}\n"

    if alerts:
        report_text += f"\nDetailed Alert Messages:\n"
        for alert in alerts:
            report_text += f"- {alert}\n"
        report_text += f"\nFixing Actions Performed:\n"
        for fixs in fix_performed:
            report_text += f"- {fixs}\n"
    
    if output_messages:
        report_text += "\nOutput Messages:\n"
        for message in output_messages:
            report_text += f"- {message}\n"

    report_text += f"\n#######################################################################\n"
    r_file = report_dir+"report-"+timestamp+".txt"

    logger.info("Creating simple report based on scanning......")
    with open(r_file, 'w') as report_file:
        report_file.write(report_text)

    report_msg = f"Report saved to {r_file}"
    logger.info(report_msg)


if __name__ == "__main__":
    main()
    
    