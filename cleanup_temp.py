"""
Deletes temporary files safely (Windows/Linux).
"""
import os, shutil, tempfile

def cleanup_temp():
    temp_dir = tempfile.gettempdir()
    print(f"🧹 Cleaning temp directory: {temp_dir}")
    count = 0
    for root, dirs, files in os.walk(temp_dir):
        for name in files:
            try:
                os.remove(os.path.join(root, name))
                count += 1
            except Exception:
                pass
    print(f"✅ {count} temporary files deleted!")

if __name__ == "__main__":
    cleanup_temp()
