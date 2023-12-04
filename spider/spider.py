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

	print(len(images))

def search_from_tag(tag, arg, c):

	idx = 0
	tag = "<" + tag
	arg = arg + '="'
	results = []
	while 1:
		idx = c.find(tag, idx)
		if idx == -1:
			break
		r_start = c.find(arg, idx)
		if r_start == -1:
			print("ERROR")
			return
		r_start = r_start + len(arg)
		r_end = c.find('"', r_start)
		if r_end == -1:
			print("ERROR")
			return
		result = c[r_start:r_end]
		results.append(result)
		idx = r_end

	return results

def get_images_from_url(url):

	r = requests.get(url)
	if r.status_code != 200:
		print(r)
		return

	c = str(r.content)

	return search_from_tag("img", "src", c)

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

	images = get_images_from_url(args.url)
	print(images)
	download_images(args, images)

main()
