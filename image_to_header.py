#!/usr/bin/env python3
"""
Script to convert grayscale image to C header file.
Generates image data in header format for STM32 project.
"""

import numpy as np
from PIL import Image
import os


def create_sample_image(width=64, height=64, output_path="sample_image.png"):
    """
    Creates a sample grayscale image.
    Contains gradient and some patterns.
    """
    # Create gradient image
    img_array = np.zeros((height, width), dtype=np.uint8)

    # Horizontal gradient
    for y in range(height):
        for x in range(width):
            # Gradient + some patterns
            value = int((x / width) * 255)
            # Add vertical lines
            if x % 16 < 4:
                value = min(255, value + 50)
            # Add horizontal lines
            if y % 16 < 4:
                value = min(255, value + 30)
            img_array[y, x] = value

    # Convert to PIL Image and save
    img = Image.fromarray(img_array, mode="L")
    img.save(output_path)
    print(f"Sample image created: {output_path}")
    return img_array


def image_to_header(image_path, header_path="image_data.h", array_name="image_data"):
    """
    Converts image file to C header file.
    """
    # Load image and convert to grayscale
    img = Image.open(image_path)
    if img.mode != "L":
        img = img.convert("L")

    # Convert to NumPy array
    img_array = np.array(img, dtype=np.uint8)
    height, width = img_array.shape

    # Create header file
    with open(header_path, "w") as f:
        f.write(f"/*\n")
        f.write(f" * Image Data Header File\n")
        f.write(f" * Generated from: {image_path}\n")
        f.write(f" * Image Size: {width}x{height}\n")
        f.write(f" */\n\n")
        f.write(f"#ifndef IMAGE_DATA_H\n")
        f.write(f"#define IMAGE_DATA_H\n\n")
        f.write(f"#define IMAGE_WIDTH  {width}\n")
        f.write(f"#define IMAGE_HEIGHT {height}\n")
        f.write(f"#define IMAGE_SIZE   ({width} * {height})\n\n")
        f.write(f"// Grayscale image data (8-bit per pixel)\n")
        f.write(f"const unsigned char {array_name}[IMAGE_SIZE] = {{\n")

        # Write data (16 values per line)
        for i in range(0, len(img_array.flatten()), 16):
            row = img_array.flatten()[i : i + 16]
            values = ", ".join(f"{val:3d}" for val in row)
            if i + 16 < len(img_array.flatten()):
                f.write(f"    {values},\n")
            else:
                f.write(f"    {values}\n")

        f.write(f"}};\n\n")
        f.write(f"#endif // IMAGE_DATA_H\n")

    print(f"Header file created: {header_path}")
    print(f"Image size: {width}x{height} = {width*height} pixels")
    return width, height


if __name__ == "__main__":
    # Create sample image
    sample_img = create_sample_image(64, 64, "sample_image.png")

    # Convert to header file
    width, height = image_to_header("sample_image.png", "image_data.h", "image_data")

    print("\nProcess completed!")
    print(f"  - Image: sample_image.png ({width}x{height})")
    print(f"  - Header: image_data.h")
