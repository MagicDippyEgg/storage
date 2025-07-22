import os
import shutil

# Set your actual source folder here
source_dir = r"C:\path\to\your\starting\folder"
destination_dir = r"C:\Users\kai_w\OneDrive\Pictures\wallpaper"

# Common image file extensions
image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff"}

# Ensure the destination exists
os.makedirs(destination_dir, exist_ok=True)

# Check if source folder actually exists
if not os.path.exists(source_dir):
    print(f"❌ Source folder does not exist: {source_dir}")
else:
    print(f"🔍 Searching in: {source_dir}")

    found_any = False

    # Walk through all subdirectories
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in image_extensions:
                found_any = True
                src_file = os.path.join(root, file)
                dest_file = os.path.join(destination_dir, file)

                # Avoid overwriting
                counter = 1
                while os.path.exists(dest_file):
                    name, ext = os.path.splitext(file)
                    dest_file = os.path.join(destination_dir, f"{name}_{counter}{ext}")
                    counter += 1

                # Move the file
                shutil.move(src_file, dest_file)
                print(f"✅ Moved: {src_file} → {dest_file}")

    if not found_any:
        print("⚠️ No image files found.")
