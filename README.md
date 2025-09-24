Himawari Wallpaper is a Python-based macOS tool that automatically downloads high-resolution tiles from the [Himawari-9 Real Time Image](https://himawari9.nict.go.jp/), stitches them together, and sets the result as your desktop wallpaper. The project supports multi-monitor setups and runs automatically using a macOS LaunchAgent

---

## Features

- Download **ND×ND tiles** from Himawari satellite images and stitch them into a single high-resolution wallpaper.  
  - `ND` determines the number of tiles per row/column.  
  - Supported values: **1, 2, 4, 8, 16**.  
  - Example: `ND=4` → 4×4 = 16 tiles, higher ND gives higher resolution images.
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
> Make sure save_dir points to a safe, non-protected directory to avoid permission issues with LaunchAgent

## Usage

The CLI supports the following commands:

```bash
python cli.py install    # Install LaunchAgent and run wallpaper update
python cli.py runonce    # Run wallpaper update once
python cli.py stop       # Uninstall LaunchAgent
python cli.py restore    # Restore default system wallpaper
```

## Logs

- Standard output: `~/Library/Logs/com.himawari-live-wallpaper.out`

- Error logs: `~/Library/Logs/com.himawari-live-wallpaper.err`

> Check these logs to see the download progress and errors.

## Notes

- Make sure to use a **non-protected directory** for virtual environment, cache, and logs to avoid `PermissionError` when running via LaunchAgent

- Old wallpapers are automatically cleaned according to `max_pic_count` in `config.json`



