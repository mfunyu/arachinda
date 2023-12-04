#!/usr/bin/env python3
import argparse
import requests

def request_images(args, images):

	for i in images:
		r = requests.get(args.url + i)
		filename = i
		filename = filename.replace('/', '-')
		filename = args.p + filename
		with open(filename, 'wb') as f:
			f.write(r.content)

def request(args):

	r = requests.get(args.url)
	c = str(r.content)

	i = 0
	images = []
	while 1:
		ext = ".png"
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

	request_images(args, images)

main()
