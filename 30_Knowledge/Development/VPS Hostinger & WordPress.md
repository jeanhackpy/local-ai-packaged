# ☁️ VPS Hostinger & WordPress Management

**Part of:** [[README]]  
**Related:** [[SystemPolicy]], [[Scripts]]

## 🔌 Remote Connection Setup

### Prerequisites
1. Install Remote - SSH extension in VS Code/Cursor
2. Configure SSH keys:
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
ssh-copy-id user@hostinger-vps-ip
```

### SSH Config (`~/.ssh/config`)
```
Host hostinger-vps
    HostName YOUR_VPS_IP
    User YOUR_USERNAME
    Port 22
    IdentityFile ~/.ssh/id_rsa
```

### Connect via VS Code/Cursor
1. Open Command Palette (Cmd+Shift+P)
2. Select "Remote-SSH: Connect to Host"
3. Choose "hostinger-vps"

## 🐧 VPS Management Commands

### System Information
```bash
# Check system info
uname -a
cat /etc/os-release

# Check disk usage
df -h

# Check memory usage
free -h

# Check running processes
top
```

### Security Management
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Enable firewall
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https

# Check firewall status
sudo ufw status
```

## 🌐 WordPress Management with WP-CLI

### WP-CLI Installation
```bash
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp
```

### Common WP-CLI Commands
```bash
# Navigate to WordPress directory
cd /var/www/html/your-wordpress-site

# Update WordPress core
wp core update

# Update plugins
wp plugin update --all

# Update themes
wp theme update --all

# Backup database
wp db export backup-$(date +"%Y%m%d-%H%M%S").sql

# List users
wp user list

# Create admin user
wp user create admin admin@example.com --role=administrator --user_pass=securepassword
```

## 🔄 File Sync with rsync

### Basic rsync Syntax
```bash
# Sync local to remote
rsync -avz --progress /local/path/ user@host:/remote/path/

# Sync remote to local
rsync -avz --progress user@host:/remote/path/ /local/path/

# Exclude files
rsync -avz --exclude '*.log' --exclude 'cache/' /local/path/ user@host:/remote/path/
```

### WordPress Deployment Example
```bash
# Deploy theme updates
rsync -avz --progress ./wp-content/themes/your-theme/ user@hostinger-vps:/var/www/html/wp-content/themes/your-theme/

# Deploy plugin updates
rsync -avz --progress ./wp-content/plugins/your-plugin/ user@hostinger-vps:/var/www/html/wp-content/plugins/your-plugin/

# Sync uploads (be careful!)
rsync -avz --progress ./wp-content/uploads/ user@hostinger-vps:/var/www/html/wp-content/uploads/
```

## 🔐 Security Best Practices

### SSH Hardening
1. Disable password authentication:
```bash
sudo nano /etc/ssh/sshd_config
# Set PasswordAuthentication no
sudo systemctl restart ssh
```

2. Change default SSH port (optional)
3. Use SSH keys only
4. Implement fail2ban

### WordPress Security
```bash
# Set proper file permissions
find /var/www/html -type d -exec chmod 755 {} \;
find /var/www/html -type f -exec chmod 644 {} \;
chmod 600 wp-config.php
```

### SSL Certificate with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
```

## 📊 Monitoring & Maintenance

### Log Locations
- Apache: `/var/log/apache2/`
- MySQL: `/var/log/mysql/`
- WordPress: `wp-content/debug.log` (enable in wp-config.php)

### Automated Backups
Create a backup script:
```bash
#!/bin/bash
DATE=$(date +"%Y%m%d-%H%M%S")
# Database backup
mysqldump -u username -p database_name > backup-$DATE.sql
# Files backup
tar -czf files-backup-$DATE.tar.gz /var/www/html/
```

### Scheduled Tasks (cron)
```bash
# Edit crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /path/to/backup-script.sh

# Weekly update
0 3 * * 0 apt update && apt upgrade -y
```

## 🔗 Related Documentation
- System Setup: [[SystemPolicy/01_BaseSetup]]
- Security Guidelines: [[SystemPolicy/03_Security]]
- Maintenance Procedures: [[SystemPolicy/05_Maintenance]]
- Scripts: [[Scripts/crawl_test.py]] (example of automation)
