# video-mosaic

Build a photo mosaic that matches an input image using frames extracted from a video.

## Overview

This tool creates a mosaic by analyzing frames from a video and arranging them to recreate a target image. Each tile in the mosaic is a frame from your video that best matches the corresponding region in your input image.

## Requirements

- Python 3.6+
- ffmpeg (must be installed and available in your PATH)
- Virtual environment (recommended)

## Installation

### 1. Install ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

### 2. Set up Python environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

1. **Prepare your files:**
   - Place your target image as `input.jpg` in the project directory
   - Place your source video as `input.mp4` in the project directory

2. **Run the script:**
   ```bash
   python main.py
   ```

3. **Output:**
   - The mosaic will be saved as `final_collage.jpg`
   - Extracted frames will be stored in the `frames/` folder

### Advanced Usage

If you want to manually curate the frames (remove unwanted frames from the `frames/` folder) and regenerate the mosaic:

```bash
python main2.py
```

This skips the frame extraction step and uses only the frames currently in the `frames/` folder.

## How It Works

1. **Frame Extraction:** ffmpeg extracts frames from the input video
2. **Color Analysis:** Each frame's average color is calculated
3. **Mosaic Generation:** The input image is divided into a grid, and each cell is matched with the most similar video frame
4. **Assembly:** Matched frames are arranged to create the final mosaic

## Examples

### Input Image
![Original Image](https://github.com/Prajith004/video-mosaic/blob/main/input.jpg)

### Resulting Collage
![Collage Result](https://github.com/Prajith004/video-mosaic/blob/main/final_collage.jpg)

### Close-up Detail
![Close-up Detail](https://github.com/Prajith004/video-mosaic/blob/main/closeup.jpg)

## Tips for Best Results

- Use videos with diverse colors and scenes
- Higher resolution input images produce more detailed mosaics
- More frames = better matching, but slower processing

---

**Note:** Processing time depends on video length, frame count, and input image size.
