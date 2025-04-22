import os
import subprocess

# Step 1: Generate requirements.txt
print("📦 Generating requirements.txt...")
subprocess.run(["pip", "freeze"], stdout=open("requirements.txt", "w"))
print("✅ requirements.txt created.")

# Step 2: Install and enable nbstripout
print("🧽 Installing nbstripout...")
subprocess.run(["pip", "install", "--user", "nbstripout"])
subprocess.run(["python", "-m", "nbstripout", "--install"])
print("✅ nbstripout installed and git hook enabled.")

print("\n🎉 Project setup complete! Your outputs will be stripped on commit and your dependencies are pinned.")
