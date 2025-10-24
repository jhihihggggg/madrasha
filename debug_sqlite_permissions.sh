#!/bin/bash
# Debug SQLite permission issues

echo "=== Directory Permissions Debug ==="
echo ""

echo "1. /var/www/madrasha ownership:"
ls -ld /var/www/madrasha

echo ""
echo "2. /var/www/madrasha/instance ownership:"
ls -ld /var/www/madrasha/instance 2>/dev/null || echo "instance directory does not exist"

echo ""
echo "3. Can www-data write to instance?"
sudo -u www-data touch /var/www/madrasha/instance/test.txt 2>&1
if [ -f /var/www/madrasha/instance/test.txt ]; then
    echo "✅ www-data CAN write to instance directory"
    ls -l /var/www/madrasha/instance/test.txt
    rm /var/www/madrasha/instance/test.txt
else
    echo "❌ www-data CANNOT write to instance directory"
fi

echo ""
echo "4. Can www-data access venv/bin/python3?"
sudo -u www-data /var/www/madrasha/venv/bin/python3 --version 2>&1

echo ""
echo "5. Working directory test as www-data:"
sudo -u www-data bash -c "cd /var/www/madrasha && pwd" 2>&1

echo ""
echo "6. Test SQLite creation directly:"
sudo -u www-data bash -c "cd /var/www/madrasha && python3 -c 'import sqlite3; conn = sqlite3.connect(\"instance/test.db\"); print(\"✅ SQLite works\"); conn.close()'" 2>&1
if [ -f /var/www/madrasha/instance/test.db ]; then
    echo "Test database created successfully!"
    ls -l /var/www/madrasha/instance/test.db
    rm /var/www/madrasha/instance/test.db
fi

echo ""
echo "7. Check parent directory permissions:"
ls -ld /var/www

echo ""
echo "8. Test with absolute path:"
sudo -u www-data bash -c "cd /var/www/madrasha && python3 -c 'import sqlite3; conn = sqlite3.connect(\"/var/www/madrasha/instance/test2.db\"); print(\"✅ Absolute path works\"); conn.close()'" 2>&1
if [ -f /var/www/madrasha/instance/test2.db ]; then
    echo "Test database with absolute path created!"
    ls -l /var/www/madrasha/instance/test2.db
    rm /var/www/madrasha/instance/test2.db
fi
