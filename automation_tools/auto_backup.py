"""
Automatically back up folders to a chosen directory.
Usage:
    python auto_backup.py "C:/Users/Akai/Documents" "D:/Backups"
"""
import os, shutil, sys, datetime

if len(sys.argv) != 3:
    print("Usage: python auto_backup.py <source> <destination>")
    sys.exit(1)

src, dst = sys.argv[1], sys.argv[2]
backup_name = f"backup_{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}"
backup_path = os.path.join(dst, backup_name)
shutil.copytree(src, backup_path)
print(f"✅ Backup created at: {backup_path}")
