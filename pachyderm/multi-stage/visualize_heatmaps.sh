#!/bin/bash

# ID=$(ls /pfs/crop/ | head -n 1)

CROPPED_IMAGE_PATH="/pfs/crop/${ID}/cropped_images"
HEATMAP_PATH="/pfs/generate_heatmaps/${ID}/heatmaps/"
OUTPUT_PATH="/pfs/out/${ID}/"

# ID=$(ls ./tmp2/ | head -n 1)

# CROPPED_IMAGE_PATH="./tmp2/${ID}/cropped_images/"
# HEATMAP_PATH="./tmp/${ID}/heatmaps/"
# OUTPUT_PATH="./tmp_output/${ID}/"

export PYTHONPATH=$(pwd):$PYTHONPATH

echo 'Stage 5: Visualize Heatmaps'
python3 src/heatmaps/visualize_heatmaps.py \
    --image-path $CROPPED_IMAGE_PATH \
    --heatmap-path $HEATMAP_PATH \
    --output-path $OUTPUT_PATH 
