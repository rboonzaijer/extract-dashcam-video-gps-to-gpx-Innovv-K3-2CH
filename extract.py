import os
import time
import gpxpy
import gpxpy.gpx as gpx
from typing import Optional
import datetime
import multiprocessing
from collections import defaultdict
from pathlib import Path

def getVideos():
	files = []
	for dirpath, dirnames, filenames in os.walk("videos"):
		for filename in [f for f in filenames if not f.endswith('.gpx') and not f.endswith('.gitkeep') and not f.lower().endswith('_r.ts')]:
			path = os.path.join(dirpath, filename)
			pathWithoutExtension = os.path.splitext(path)[0]
			
			files.append({
				"path": path,
				"pathWithoutExtension": pathWithoutExtension
			})
	return files

def process(video):
	#print(video)
	os.system('python lib/nvtk_mp42gpx.py -e -i "' + video['path'] + '" -o "' + video['pathWithoutExtension'] + '.gpx"')

def getGpxFiles():
	files = []
	for dirpath, dirnames, filenames in os.walk("videos"):
		for filename in [f for f in filenames if f.endswith('.gpx') and not f.endswith(' DIR.gpx')]:
			path = os.path.join(dirpath, filename)
			pathWithoutExtension = os.path.splitext(path)[0]
			files.append({
				"dir": dirpath,
				"path": path,
				"pathWithoutExtension": pathWithoutExtension,
			})
	return files

def get_time(g: gpx.GPX) -> Optional[datetime.datetime]:
    for t in g.tracks:
        for s in t.segments:
            for pt in s.points:
                if pt.time:
                    return pt.time
    return None

def merge_gpx():
	start_time = time.time()
	files = getGpxFiles()
	groups = defaultdict(list)
	for obj in files:
		groups[obj['dir']].append(obj)
	dir_list = groups.values()
	for dir_files in dir_list:
		dir_basename = os.path.basename(dir_files[0]['dir'])
		out_file = os.path.join(dir_files[0]['dir'], '_' + dir_basename + ' DIR.gpx')
		gpxs: List[gpx.GPX] = []
		for gpx_file in dir_files:
			gpxs.append(gpxpy.parse(open(gpx_file['path'])))
		gpxs = sorted(gpxs, key=get_time)
		base_gpx: Optional[gpx.GPX] = None
		for g in gpxs:
			if base_gpx:
				if len(g.nsmap) != len(base_gpx.nsmap):
					keep_extensions = False
				else:
					for key in base_gpx.nsmap:
						if not key in g.nsmap or g.nsmap[key] != base_gpx.nsmap[key]:
							keep_extensions = False
			else:
				base_gpx = g.clone()
				base_gpx.tracks = []
				base_gpx.routes = []
			for track in g.tracks:
				base_gpx.tracks.append(track)
			for route in g.routes:
				base_gpx.routes.append(route)
		if base_gpx:
			with open(out_file, "w") as f:
				f.write(base_gpx.to_xml())
	print("Merged GPX in %s seconds" % (round(time.time() - start_time, 1)))

def extract_gpx():
	start_time = time.time()
	videos = getVideos()
	pool = multiprocessing.Pool()
	processed_amount = 0
	for video in videos:
		if not os.path.isfile(video['pathWithoutExtension'] + '.gpx'):
			processed_amount += 1
			pool.apply_async(process, args = (video, ))
	pool.close()
	pool.join()
	print("Extracted GPX for %d videos (of %d total videos) in %s seconds" % (processed_amount, len(videos), round(time.time() - start_time, 1)))

def main():
	extract_gpx()
	merge_gpx()

if __name__ == "__main__":
	main()
