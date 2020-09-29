import argparse
import cv2
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import numpy as np

from src.utilities.reading_images import *
from src.utilities.saving_images import *

def normalize_colorize(image):
    image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F).astype(np.uint8)
    return cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

def print_img_info(name, data):
    print('Variable name: ', name)
    print('Type:', type(data))
    print('Shape:', np.shape(data))
    print('Max', np.max(data))
    print('Min', np.min(data))
    print('Data type', type(data[0][0][0]), '\n')

def visualize_heatmap(image, heatmap, color_map):
    color_heatmap = cv2.applyColorMap(heatmap, color_map)
    vis_heatmap = cv2.addWeighted(image, 0.8, color_heatmap, 0.2, 0)
    return vis_heatmap

def main():
    parser = argparse.ArgumentParser(description="Generate mamogram heatmap")
    parser.add_argument("--image-path",
                        type=str,
                        help="Original or cropped exam image path (png)")
    parser.add_argument("--heatmap-path",
                        type=str,
                        help="Heatmap image path (hdf5)")
    parser.add_argument("--output-path",
                        type=str,
                        help="Output directory for heatmap images")
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_path, exist_ok=True)

    # Get all cropped images
    png_files = []
    for dirpath, subdirs, files in os.walk(args.image_path):
        for x in files:
            if x.endswith(".png"):
                png_files.append(os.path.join(dirpath, x))
    print(png_files)

    # Get all heatmaps
    hdf5_files = []
    for dirpath, subdirs, files in os.walk(args.heatmap_path):
        for x in files:
            if x.endswith(".hdf5"):
                hdf5_files.append(os.path.join(dirpath, x))
    print(hdf5_files)
    
    for hdf5 in hdf5_files:
        hdf5_basename = os.path.splitext(os.path.basename(hdf5))[0]
        for png in png_files:
            png_basename = os.path.splitext(os.path.basename(png))[0]
            if png_basename == hdf5_basename:
                base_image = normalize_colorize(read_image_png(png))
                heatmap = normalize_colorize(read_image_mat(hdf5))
                if 'malignant' in hdf5:
                    image = visualize_heatmap(base_image, heatmap, cv2.COLORMAP_HOT)
                    output_path = os.path.join(args.output_path, hdf5_basename+'_malignant.png')
                elif 'benign' in hdf5:
                    image = visualize_heatmap(base_image, heatmap, cv2.COLORMAP_DEEPGREEN)
                    output_path = os.path.join(args.output_path, hdf5_basename+'_benign.png')
                else: 
                    raise ValueError('Unmatching file error.')
                print('Output path: ', output_path)
                cv2.imwrite(output_path, image)


if __name__ == "__main__":
    main()