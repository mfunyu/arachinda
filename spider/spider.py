#!/usr/bin/env python3
import argparse
import requests

exts = [".jpg", ".jpeg", ".png", ",gif", ".bmp"]

def download_images(args, images):

	for i in images:
		if not i.startswith("http"):
			i = args.url + i.strip()
		r = requests.get(i)
		filename = i[len(args.url) + 1:].replace('/', '-')
		print(filename)
		filename = args.p + filename
		with open(filename, 'wb') as f:
			f.write(r.content)

def request(args):

	r = requests.get(args.url)
	c = str(r.content)

	images = []
	for ext in exts:
		i = 0
		while 1:
			filename = i
			i = c.find(ext, i + 1)
			if i == -1:
				break
			start = c.rfind('"', 0, i) + 1
			images.append(c[start:i + len(ext)])

	return images

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", metavar="URL", type=str)
	parser.add_argument("-r", action="store_true")
	parser.add_argument("-l", default=5, type=int)
	parser.add_argument("-p", default="./data/", type=str)
	args = parser.parse_args()

	return args

def main():

	args = parse_args()
	print(args)

	images = request(args)
	print(images)
	download_images(args, images)

main()
