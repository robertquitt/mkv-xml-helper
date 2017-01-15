#mkv-xml-helper
A tool assist in generation of chapter info for long audios in .mkv format from chapter listings on youtube videos.

## An Example
Converting [this soundtrack from YouTube](https://www.youtube.com/watch?v=ca7IELhD_mI) into a navigatable .mkv file.

#### Prerequisites
- (optional) [chocolatey](https://chocolatey.org/) for Windows systems for easy installation of the tools below
- [youtube-dl](https://rg3.github.io/youtube-dl/)
- [ffmpeg](http://ffmpeg.org/)
- mkvpropedit (part of [mkvtoolnix](https://mkvtoolnix.download/))

#### Instructions
1. Find the video you want, then copy the video ID from the URL.
2. Use `youtube-dl -F ca7IELhD_mI` to view the available formats.
3. Download with best audio quality, usually `youtube-dl -f 22 -x ca7IELhD_mI`
	- `-x` to extract audio
4. Convert into Matroska format (.mkv) with `ffmpeg -i "Super Mario Galaxy - Full OST (Complete Soundtrack)-ca7IELhD_mI" -c:a copy "Super Mario Galaxy - Full OST.mkv"`
	- `-i` specifies input
	- `-c:a` specifies audio codec, "copy" to avoid transcoding
5. Copy chapter listing from description into text file `mario_galaxy.txt`, confirm there are no typos.
6. Convert to XML using `python3 chapters_to_xml.py -i 0 1 None -e 2:15:25 mario_galaxy.txt mario_galaxy.xml` 
	- `-i 0 1 None` means `0` is the start time index, and `[1:None]` is the list slice for the chapter title. The line is tokenized by whitespace.
	- `-e ` is the ending time, needed to specify the duration of the last chapter
7. Apply the chapters to the .mkv by using `mkvpropedit "Super Mario Galaxy - Full OST.mkv" --chapters mario_galaxy.xml`
8. Open the file with your favorite media player (I recommend [MPC-HC](https://mpc-hc.org/) for Windows) and enjoy!


## chapters_to_xml.py
### Converts chapter listings into xml data readable by mkvpropedit

#### Requires:
- lxml
  - `pip install lxml`

usage: `chapters_to_xml.py [-h] [-d] [-i timestamp titlestart titleend] [-c config] -e endtime inputfile outputfile`

Converts lines of text containing chapter information into XML readable by
mkvpropedit.

| positional arguments | |
|:--|---|
|`inputfile`  | text file where each line has a chapter name and start time
|`outputfile` | XML file to be written to.

|optional arguments | |
|:---|---|
|`-h`, `--help`          | show this help message and exit
|`-d`, `--debug`         | enable debug printing
|`-i timestamp titlestart titleend` | specifies the indices of the elements on each line (supports negative indices) where timestamp=tokens[timestamp] and title=tokens[titlestart:titleend]. Arguments must be integers or None. If neither -i nor -c are specified, an indexing configuration will be automatically generated.
|`-c config`             | use a premade indexing configuration. Overrides the `-i` option. Valid configs are: super_mario_galaxy, squad_goals, pink_season, minecraft
|`-e endtime`            | specifies the timestamp of the end of the final chapter, usually the length of the entire track.
