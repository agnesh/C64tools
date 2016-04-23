
## `hires_to_bin.py`

This script assumes the input is an 8-bit indexed image 320 x 200 pixels in size and converts the image into Commodore 64 bitmap data and color data. The first 16 colors are assumed to be in the same order as the C64 palette.

The included image `example_image_hires.png` contains an example palette.

# Color order:

```
   0x0 Black    0x8 Orange
   0x1 White    0x9 Brown
   0x2 Red      0xA Light red
   0x3 Cyan     0xB Dark gray
   0x4 Purple   0xC Mid gray
   0x5 Green    0xD Light green
   0x6 Blue     0xE Light blue
   0x7 Yellow   0xF Light gray
```

The output error indicator image will use the first three colors in the palette (assumed to be black, white, red).

Example usage (Linux):

```
python hires_to_bin.py example_image_hires.png test.bin
acme viewer_hires.a
```
