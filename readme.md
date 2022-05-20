# Extract GPS/GPX data from dashcam videos (Innovv K3 2CH)

- Looks for any files in the 'videos' directory (recursively)
- A '.gpx' file will be created next to the file, when it already exists it will be skipped
- Finally all loose '.gpx' files in a folder will be merged to one file (for the whole route)

# Usage

```
git clone git@github.com:rboonzaijer/extract-dashcam-video-gps-to-gpx-Innovv-K3-2CH.git video-extract-gps

cd video-extract-gps
```

- Put your videos in the 'videos' directory, and run the python(3) script

```
python extract.py
```

# Credits
Sergei Franco ( https://sergei.nz/?s=nvtk_mp42gpx.py )
