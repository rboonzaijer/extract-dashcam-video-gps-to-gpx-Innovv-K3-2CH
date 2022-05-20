# Extract GPS/GPX data from dashcam videos (Innovv K3 2CH)

- Looks for any files in the 'videos' directory (recursively)
- A '.gpx' file will be created next to the file, when it already exists it will be skipped
- Finally all loose '.gpx' files in a folder will be merged to one file (for the whole route)

# Usage

1. Put your videos in the 'videos' directory
2. Run:

```
python extract.py
```
