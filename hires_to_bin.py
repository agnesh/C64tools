#! /usr/bin/env python

from PIL import Image
import sys
from collections import Counter
from math import *
import os.path


def main():

    if len(sys.argv) < 3:
        sys.exit('Usage: hires_to_bin.py [IMGFILE] [BINFILE]')
    else:
        infile = sys.argv[1]
        outfile = sys.argv[2]

    imgtochars(infile, outfile)

    return


def imgtochars(infile, outfile):

    # Open image file and convert to C64 bitmap data

    imagefile = Image.open(infile)

    width, height = imagefile.size
     
    if width != 320 or height != 200:
        sys.exit('Image dimensions need to be exactly 320 x 200')

    cols = int(width / 8)
    rows = int(height / 8)

    output = []
    bitmap = []
    colors = []
    error_count = 0

    # Divide image into characters

    for row in range(rows):
        for col in range(cols):
     
            # Calculate char region
            rect = (8 * col, 8 * row, 8 * (col + 1), 8 * (row + 1))

            # Crop char region so we can mess with it
            char = imagefile.crop(rect)
            
            # Get the pixel values
            pixels = char.load()
            
            indices = []

            # Examine the pixels in each character

            for y in range(8):
                for x in range(8):

                    p = pixels[x, y]
                    
                    # List all the palette indices so we can count them later
                    indices.append(p)
            
            # Count colors in character
            c = list(Counter(indices))
            
            # Low nibble (background)
            color_bg = c[0]

            # High nibble (foreground)
            color_fg = 0 if len(list(c)) <= 1 else c[1]

            # Combine the two colors in a single byte
            colors.append((color_fg << 4) | color_bg)
        
            # Convert char pixel data to a line of bits
     
            error = 0

            for y in range(8):

                byte = 0

                for x in range(8):
                    
                    # Background color (0)
                    if pixels[x, y] == c[0]:
                        pixels[x, y] = 0
                         
                    # Foreground color (1)
                    elif len(list(c)) > 1 and pixels[x, y] == c[1]:
                        pixels[x, y] = 1

                    # Character error (2)
                    elif len(list(c)) > 2:
                        pixels[x, y] = 2
                        error = 1

                    b = 0 if pixels[x,y] == 0 else 1
                    
                    # Turn each row of 8 pixels into a byte
                    byte = byte | (b << (7 - x))

                # Char row completed
                bitmap.append(byte)

            # Check if there was an error in the character
            if (error):
                error_count = error_count + 1
                    
            # Update character with new pixel values
            imagefile.paste(char, rect)

    print('Character errors detected: ' + str(error_count))

    # Save 1-bit image (to show any errors)

    outname = 'check_' + infile
    imagefile.save(outname)
    print('Error check: check_' + infile)
    
    # Save binary files
        
    outbin = open('bitmap_' + outfile, 'wb')
    outbin.write(bytes(bitmap))
    outbin.close()
    print('Bitmap data: bitmap_' + outfile)

    outcol = open('colors_' + outfile, 'wb')
    outcol.write(bytes(colors))
    outcol.close()
    print('Color data: colors_' + outfile)

    return


if __name__ == "__main__":
    main()
