#!/usr/bin/env python3
"""
Himawari Wallpaper Downloader and Setter

This script downloads Himawari satellite tiles, stitches them into a full image,
resizes it to fit the screen, and sets it as the desktop wallpaper.
"""

import os
import subprocess
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
from PIL import Image

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH) as f:
    cfg = json.load(f)

# https://anzu.shinshu-u.ac.jp/himawari/img/D531106 or https://himawari8-dl.nict.go.jp/himawari.asia/img/D531106
BASE_URL = cfg["base_url"]
if isinstance(BASE_URL, str):
    BASE_URL = [BASE_URL]
DELAY_MINUTES = cfg["delay_minutes"]
UPDATE_INTERVAL_MINUTES = cfg["update_interval_minutes"]
ND = cfg["nd"]
TILE_SIZE = cfg["tile_size"]
SCALE_MODE = cfg["scale_mode"]
COVER_RATIO = cfg["cover_ratio"]
SAVE_DIR = Path(__file__).parent / cfg["save_dir"]
PIC_SIZE = cfg["pic_size"]
MAX_PIC = cfg["max_pic_count"]

os.makedirs(SAVE_DIR, exist_ok=True)


def get_aligned_time():
    """Return the target time aligned to UPDATE_INTERVAL_MINUTES."""
    now = datetime.utcnow()
    target = now - timedelta(minutes=DELAY_MINUTES)
    minute = (target.minute // UPDATE_INTERVAL_MINUTES) * UPDATE_INTERVAL_MINUTES
    return target.replace(minute=minute, second=0, microsecond=0)


def convert_time(time_str: str):
    """Convert '/' in time string to '__' for filename."""
    return time_str.replace("/", "__")


def list_png(dir_path_str: str):
    """List all PNG files in a directory."""
    dir_path = Path(dir_path_str)
    return list(dir_path.glob("*.png"))


def get_timestamp(file_path):
    """Extract timestamp from filename for sorting."""
    name = file_path.stem
    parts = name.split("_")
    return parts[2] if len(parts) >= 3 else "0"


def clean_old_images(dir_path, max_images):
    """Remove old images exceeding max_images count."""
    images = list_png(dir_path)
    if len(images) <= max_images:
        return
    images.sort(key=get_timestamp)
    for img in images[:len(images)-max_images]:
        print(f"Deleting old image {img}")
        img.unlink()


def get_screen_size():
    """Return primary screen width and height."""
    script = 'tell application "Finder" to get bounds of window of desktop'
    out = subprocess.check_output(["osascript", "-e", script]).decode()
    nums = [int(x.strip()) for x in out.replace("{","").replace("}","").split(",")]
    width = nums[2] - nums[0]
    height = nums[3] - nums[1]
    return width, height


def download_tiles(time_str):
    """
    Download ND x ND tiles and return as PIL Image matrix.
    Try multiple base URLs in order if a download fails.
    """
    tiles = []
    for row in range(ND):
        row_tiles = []
        for col in range(ND):
            success = False
            last_exception = None
            for base_url in BASE_URL:
                url = f"{base_url}/{ND}d/{TILE_SIZE}/{time_str}_{col}_{row}.png"
                try:
                    print(f"Downloading {url}")
                    resp = requests.get(url, timeout=10)
                    resp.raise_for_status()
                    img_path = os.path.join(SAVE_DIR, f"tile_{row}_{col}.png")
                    with open(img_path, "wb") as f:
                        f.write(resp.content)
                    row_tiles.append(Image.open(img_path))
                    success = True
                    break  # stop trying other URLs
                except Exception as e:
                    print(f"⚠️ Failed to download from {url}: {e}")
                    last_exception = e
            if not success:
                raise RuntimeError(f"Failed to download tile ({col},{row}) from all URLs") from last_exception
        tiles.append(row_tiles)
    return tiles



def stitch_tiles(tiles):
    """Stitch ND x ND tiles into one large image."""
    tile_w, tile_h = tiles[0][0].size
    big_w, big_h = tile_w * ND, tile_h * ND
    big_img = Image.new("RGB", (big_w, big_h))
    for row in range(ND):
        for col in range(ND):
            big_img.paste(tiles[row][col], (col * tile_w, row * tile_h))
    return big_img


def resize_and_center(big_img, screen_size, cover_ratio):
    """Resize big image and paste onto black background to fit screen."""
    W, H = screen_size
    short_edge = min(W, H)
    target_size = int(short_edge * cover_ratio)

    bg = Image.new("RGB", (W, H), (0, 0, 0))
    big_resized = big_img.resize((target_size, target_size), Image.LANCZOS)
    offset_x = (W - target_size) // 2
    offset_y = (H - target_size) // 2
    bg.paste(big_resized, (offset_x, offset_y))
    return bg


def save_wallpaper(img, filename=None):
    """Save image to SAVE_DIR with optional filename."""
    if not filename:
        time_str = get_aligned_time().strftime("%Y/%m/%d/%H%M%S")
        filename = f"{ND}d_{TILE_SIZE}_{convert_time(time_str)}.png"
    out_path = os.path.join(SAVE_DIR, filename)
    img.save(out_path)
    return out_path


def set_wallpaper(path):
    """Set the image at 'path' as desktop wallpaper."""
    script = f'''
    tell application "System Events"
        tell every desktop
            set picture to "{path}"
        end tell
    end tell
    '''
    subprocess.call(["osascript", "-e", script])
    print(f"Wallpaper updated: {path}")


def main():
    """Main function to download, stitch, resize, save, and set wallpaper."""
    clean_old_images(SAVE_DIR, MAX_PIC)

    aligned_time = get_aligned_time()
    time_str = aligned_time.strftime("%Y/%m/%d/%H%M%S")

    tiles = download_tiles(time_str)
    big_img = stitch_tiles(tiles)
    screen_size = PIC_SIZE  # or get_screen_size()
    final_img = resize_and_center(big_img, screen_size, COVER_RATIO)
    out_path = save_wallpaper(final_img)
    set_wallpaper(out_path)


if __name__ == "__main__":
    main()
