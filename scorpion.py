#!/usr/bin/env python3
import sys
from PIL import Image, ExifTags
import os
import time

#The program correctly displays basic metadata such as the date
# of creation and modification.
# The program shows the EXIF data of images of these extensions:
# jpg, png, bmp and gif.

def print_exif_data(exif_data):
	if not exif_data:
		print(" No EXIF Data")
		return

	print(" [EXIF Data]")
	for key, val in exif_data.items():
		if key in ExifTags.TAGS:
			print(f' - {ExifTags.TAGS[key]}: {val}')
		else:
			print(f' - {key}: {val}')

def print_basic_metadata(img_filename, img):
	print(" [Basic Data]")
	try:
		img_type = img.format
		creation_time = os.path.getctime(img_filename)
		modification_time = os.path.getmtime(img_filename)
		creation_datetime = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(creation_time))
		modification_datetime = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(modification_time))


		print(f" - Type: {img_type}")
		print(f" - Size: {img_type}")
		print(f" - Width: {img_type}")
		print(f" - Height: {img_type}")
		print(f" - Modified: {modification_datetime}")
		print(f" - Created: {creation_datetime}")

	except Exception as e:
		print("ERROR:", e)

def display_metadata(img_filename):
	try:
		print(f'[{img_filename}]')
		with Image.open(img_filename) as img:
			exif_data = img._getexif()

			print_basic_metadata(img_filename, img)
			print_exif_data(exif_data)

	except Exception as e:
		print("ERROR:", e)

def main():
	args = sys.argv

	if len(args) <= 1:
		print("Error: Requires arguments")
		return

	for i in range(1, len(args)):
		display_metadata(args[i])
		print()

main()
