from PIL import Image
import cv2
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from sklearn.neighbors import KDTree
import glob
from functools import lru_cache
import random

def resize(input_path="input.jpg", output_path="resized_image.jpg", max_size=256):
    img = Image.open(input_path)
    h, w = img.size
    ratio = max_size / max(h, w)
    img = img.resize((int(h * ratio), int(w * ratio)), Image.LANCZOS)
    img.save(output_path)

def extract(input_path="input.mp4", output_dir="frames", frame_rate="1/2", size=64):
    os.makedirs(output_dir, exist_ok=True)
    comm = f"""ffmpeg -i {input_path} -vf "fps={frame_rate},scale='if(gte(iw,ih),{size},-1)':'if(gte(iw,ih),-1,{size})':force_original_aspect_ratio=decrease" {output_dir}/frame_%06d.jpg"""
    os.system(comm)

def process_image(img_path):
    """Extract average color from image"""
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Get average RGB color
    avg_color = img.mean(axis=(0, 1))
    return (os.path.basename(img_path), avg_color)

def map_colors(frames_dir="frames"):
    frame_paths = glob.glob(os.path.join(frames_dir, "*.jpg"))
    print(f"Found {len(frame_paths)} frames in {frames_dir}")
    
    if len(frame_paths) == 0:
        raise ValueError(f"No frames found in {frames_dir}. Please check the directory.")
    
    print("Processing frames to build color mapping...")
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_image, frame_paths))
    
    mapping = dict(results)
    filenames = np.array(list(mapping.keys()))
    colors = np.array(list(mapping.values()))
    tree = KDTree(colors)
    
    print(f"Color mapping complete. Using {len(filenames)} frames.")
    return mapping, filenames, colors, tree

@lru_cache(maxsize=1024)
def get_tile(fname, frames_dir="frames", tile_size=64):
    """Cached function to load and resize tiles"""
    path = os.path.join(frames_dir, fname)
    return Image.open(path).resize((tile_size, tile_size), Image.LANCZOS)

def build_collage(pixel_data, filenames, color_tree, frames_dir="frames", tile_size=64, k_neighbors=5):
    # Reshape to get individual pixel colors
    height, width = pixel_data.shape[:2]
    pixel_colors = pixel_data.reshape(-1, 3)
    
    print(f"Finding best matches for {len(pixel_colors)} pixels...")
    _, indices = color_tree.query(pixel_colors, k=k_neighbors)
    
    collage = Image.new("RGB", (width * tile_size, height * tile_size))
    
    print(f"Building {width}x{height} collage (output: {width*tile_size}x{height*tile_size})...")
    
    for y in range(height):
        for x in range(width):
            pixel_idx = y * width + x
            closest_indices = indices[pixel_idx]
            selected_idx = random.choice(closest_indices)
            fname = filenames[selected_idx]
            tile = get_tile(fname, frames_dir, tile_size)
            collage.paste(tile, (x * tile_size, y * tile_size))
        
        if (y + 1) % 10 == 0:
            print(f"Progress: {y + 1}/{height} rows complete")
    
    print("Saving collage...")
    collage.save("final_collage.jpg")
    print("Collage saved as final_collage.jpg")

def main():
    # Check if input image exists
    if not os.path.exists("resized_image.jpg"):
        if os.path.exists("input.jpg"):
            print("Resizing input image...")
            resize()
        else:
            print("ERROR: No input image found. Please ensure 'input.jpeg' exists.")
            return
    
    # Rebuild color mapping from existing frames
    print("\n=== Rebuilding color mapping from frames folder ===")
    _, filenames, _, color_tree = map_colors()
    
    # Load the resized image
    print("\nLoading resized image...")
    img = np.array(Image.open("resized_image.jpg").convert("RGB"))
    
    # Build the collage
    print("\n=== Building collage ===")
    build_collage(img, filenames, color_tree, k_neighbors=5)

if __name__ == "__main__":
    main()