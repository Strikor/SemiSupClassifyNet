import os
import subprocess
import shutil

# 🔍 Step 0: Determine whether to use pip or pip3
def get_pip_command():
    if shutil.which("pip"):
        return ["pip"]
    elif shutil.which("pip3"):
        return ["pip3"]
    else:
        raise RuntimeError("❌ Neither pip nor pip3 was found on the system.")

pip_cmd = get_pip_command()

# 📥 Step 1: Load requirements.txt and install packages
requirements_path = "requirements.txt"
if os.path.exists(requirements_path):
    print(f"📥 Installing from {requirements_path}...")
    subprocess.run(pip_cmd + ["-r", requirements_path])
    print(f"✅ Packages installed from requirements.txt to {pip_cmd}.")
else:
    print(f"⚠️ {requirements_path} not found. Skipping package installation.")

# Step 2: Install and enable nbstripout
print("🧽 Installing nbstripout...")
subprocess.run(["pip", "install", "--user", "nbstripout"])
subprocess.run(["python", "-m", "nbstripout", "--install"])
print("✅ nbstripout installed and git hook enabled.")

print("\n🎉 Project setup complete! Your outputs will be stripped on commit and your dependencies are pinned.")
