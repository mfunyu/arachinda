#!/usr/bin/python3
import argparse
import requests
import re
import os

exts = [".jpg", ".jpeg", ".png", ",gif", ".bmp"]
links_visited = set()
total = 0

def form_url(url, base):
	if url.startswith("http"):
		return url
	if base.startswith('//'):
		return base + url[:1]
	if not url.startswith('/'):
		return base + '/' + url
	return base + url

def download_images(url, directory, images):
	init = False

	pattern = re.compile(fr'.*({"|".join(re.escape(ext) for ext in exts)})$')
	cnt = 0
	for img_link in images:
		if not pattern.match(img_link):
			continue
		img_link = form_url(img_link, url)
		#print(url, "|", img_link, "|")
		content = request(img_link)
		if not content:
			continue
		filename = directory + img_link[len(url) + 1:].replace('/', '-')
		if not init and not os.path.exists(directory):
			os.makedirs(directory)
			init = True
		with open(filename, 'wb') as f:
			f.write(content)
		cnt = cnt + 1
	return cnt

def request(url):
	try:
		links_visited.add(url)
		r = requests.get(url)
	except requests.exceptions.ConnectionError:
		print("ERROR: connection refused - ", url)
		return
	except:
		print("ERROR: invalid URL -", url)
		exit(1)

	if r.status_code != 200:
		print("ERROR:", url, r)
		return
	return r.content

def is_valid_link(href):
	if href.startswith('#'):
		return False
	if href.startswith("ftp:"):
		return False
	if href.startswith("tel:"):
		return False
	if href.startswith("javascript:"):
		return False
	if href.startswith("mailto:"):
		return False
	return True

def log(url, loop, num_imgs):
	print(' ' * (total - loop), '-', url, end =" ")
	print('->', num_imgs)

def spider(url, loop, dir, space):
	c = str(request(url))
	images = re.findall(r'<img[^>]+src="(.*?)"', c)
	base = re.search(r'^(https?://[^/]+)', url).group()
	num_imgs = download_images(base, dir, images)
	log(url, loop, num_imgs)

	if not loop:
		return

	hrefs = re.findall(r'<a[^>]+href="(.*?)"', c)
	for href in hrefs:
		if not is_valid_link(href):
			continue
		if href in links_visited:
			continue
		href = form_url(href, base)
		spider(href, loop - 1, dir, ' ' + space)

def validate_args(args):
	if not args.r:
		args.l = 0
	global total
	total = args.l

	if '.' not in args.url :
		print("ERROR: not a valid URL -", args.url)
		exit(1)
	if not args.url.startswith('https://') and\
		not args.url.startswith('http://'):
		args.url = 'https://' + args.url
	if not args.url.endswith('/'):
		args.url = args.url + '/'

	if not args.p.endswith('/'):
		args.p = args.p + '/'

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("url", metavar="URL", type=str)
	parser.add_argument("-r", action="store_true")
	parser.add_argument("-l", default=5, type=int)
	parser.add_argument("-p", default="./data/", type=str)
	return parser.parse_args()

def main():
	args = parse_args()
	validate_args(args)
	spider(args.url, args.l, args.p, "-")

main()
