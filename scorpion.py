#!/usr/bin/env python3
import sys
from PIL import Image, ExifTags

#The program correctly displays basic metadata such as the date
# of creation and modification.
# The program shows the EXIF data of images of these extensions:
# jpg, png, bmp and gif.

def parse_exif(img_filename):

	img = Image.open(img_filename)
	exif_data = img._getexif()
	print(img_filename)
	if not exif_data:
		print("No Data")
		return

	for key, val in exif_data.items():
		if key in ExifTags.TAGS:
			print(f'{ExifTags.TAGS[key]}:{val}')
		else:
			print(f'{key}:{val}')

def main():
	args = sys.argv

	if len(args) <= 1:
		print("Error: Requires arguments")
		return

	for i in range(1, len(args)):
		parse_exif(args[i])

main()
