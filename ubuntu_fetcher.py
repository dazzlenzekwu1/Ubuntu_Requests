import os
import requests

def download_images(urls, folder="images", max_size_mb=5):
    """
    Downloads images from one or multiple URLs with safety checks:
    - Skips non-image URLs
    - Skips if file already exists
    - Skips if file is larger than max_size_mb
    """

    if not os.path.exists(folder):
        os.makedirs(folder)

    for url in urls:
        url = url.strip()  # clean spaces
        if not url:
            continue

        try:
            # HEAD request to check metadata
            head = requests.head(url, allow_redirects=True, timeout=10)

            # ✅ Check content type
            content_type = head.headers.get("Content-Type", "")
            if not content_type.startswith("image/"):
                print(f"Skipping {url} (not an image)")
                continue

            # ✅ Check file size
            size_bytes = int(head.headers.get("Content-Length", 0))
            size_mb = size_bytes / (1024 * 1024)
            if size_mb > max_size_mb:
                print(f"Skipping {url} (too large: {size_mb:.2f} MB)")
                continue

            # ✅ Extract filename
            filename = os.path.basename(url.split("?")[0])
            filepath = os.path.join(folder, filename)

            # ✅ Prevent duplicates
            if os.path.exists(filepath):
                print(f"Skipping {url} (already downloaded)")
                continue

            # ✅ Download image
            print(f"Downloading {url} → {filepath}")
            response = requests.get(url, stream=True, timeout=10)
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            print(f"Saved: {filepath}")

        except Exception as e:
            print(f"Failed to download {url}: {e}")


# === Main Program (Interactive Mode) ===
print("Welcome to the Ubuntu Image Fetcher 🚀")
user_input = input("Enter image URL(s) (separate multiple with commas): ")

# split input into list of URLs
urls = user_input.split(",")

download_images(urls)
