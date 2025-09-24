Himawari Wallpaper is a Python-based macOS tool that automatically downloads high-resolution tiles from the Himawari satellite, stitches them together, and sets the result as your desktop wallpaper. The project supports multi-monitor setups and runs automatically using a macOS LaunchAgent.

---

## Features

- Download ND×ND tiles from Himawari satellite images.
- Stitch tiles into a single high-resolution image.
- Save historical wallpapers and automatically clean old images.
- Automatic updates using macOS LaunchAgent.

---

## Requirements

- macOS 10.15+
- Python 3.9+ (system or Homebrew Python)

---

## Installation

```bash
git clone https://github.com/RubiaPath/himawari-live-wallpaper.git
mv himawari-live-wallpaper ~/Library/Application\ Support/himawari-live-wallpaper
cd ~/Library/Application\ Support/himawari-live-wallpaper
python3 cli.py install
```
config.json

```json
{
  "base_url": ["https://himawari8-dl.nict.go.jp/himawari.asia/img/D531106", "https://anzu.shinshu-u.ac.jp/himawari/img/D531106"],
  "delay_minutes": 15,
  "update_interval_minutes": 10,
  "nd": 2,
  "tile_size": 550,
  "scale_mode": "fit",
  "cover_ratio": 0.8,
  "pic_size": [2560, 1440],
  "max_pic_count": 20,
  "save_dir": "cache"
}     
```
