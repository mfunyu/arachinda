#!/usr/bin/env python3
import argparse
import requests

exts = [".jpg", ".jpeg", ".png", ",gif", ".bmp"]

def download_images(url, directory, images):

	for i in images:
		
		if not i.startswith("http"):
			i = url + i.strip()
		r = requests.get(i)
		filename = i[len(url) + 1:].replace('/', '-')
		filename = directory + filename
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
			break
		r_start = r_start + len(arg)
		r_end = c.find('"', r_start)
		if r_end == -1:
			print("ERROR")
			break
		result = c[r_start:r_end]
		results.append(result)
		idx = r_end

	return results

def validate_urls(url, urls):
	valids = []
	second_slash = url.find('/', url.find("://") + 3)
	if second_slash != -1:
		url = url[:second_slash]
	print("base", url)
	for u in urls:
		if not u.startswith("http"):
			if u == "/":
				continue
			u = url + u
		valids.append(u)

	return valids

def spider(args, l, url):
	r = requests.get(url)
	if r.status_code != 200:
		print("ERROR", url, r)
		return
	c = str(r.content)

	print(url, l)
	images = search_from_tag("img", "src", c)
	download_images(url, args.p, images)

	if l:
		urls = search_from_tag("a", "href", c)
		urls = validate_urls(url, urls)
		for url in urls:
			spider(args, l - 1, url)

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", metavar="URL", type=str)
	parser.add_argument("-r", action="store_true")
	parser.add_argument("-l", default=5, type=int)
	parser.add_argument("-p", default="./data/", type=str)
	args = parser.parse_args()
	if not args.r:
		args.l = 0

	return args

def main():

	args = parse_args()
	print(args)

	spider(args, args.l, args.url)

main()
