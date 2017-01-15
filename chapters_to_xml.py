#!/usr/bin/env python
'''
chapters_to_xml.py - converts track listing text into xml data for mkvpropedit

python chapters_to_xml.py chapters.txt chapters.xml
ffmpeg -i file. -c:a copy file.mkv
mkvpropedit file.mkv --chapter chapters.xml
'''
import sys
import argparse
import time
from lxml import etree

CONFIG_PRESETS = {
    'super_mario_galaxy': (0, 1, None),
    # "0:00 Wii Menu - Starting The Game (''Super Mario Galaxy'')" https://www.youtube.com/watch?v=ca7IELhD_mI
    'squad_goals': (-3, 1, -3),
    # "1. Fibre - Supernatural 0:00 - 2:32" https://www.youtube.com/watch?v=tbWS0j2fulY
    'pink_season': (-1, 1, -1),
    # "1. Hot Nickel Ball On A P*ssy 0:00" https://www.youtube.com/watch?v=0c_mhrB7LlQ
    'minecraft': (0, 2, None)
    # "0:00 - Key" https://www.youtube.com/watch?v=Dg0IjOzopYU
}

def time_string(s):
    try:
        return time.strptime(s, "%M:%S")
    except ValueError:
        pass
    try:
        return time.strptime(s, "%H:%M:%S")
    except ValueError:
        pass
    return None

def parse(file, time_i, title_i_start, title_i_end, final_time_end):
    """Parse lines using given arguments.

    file: An iterable where each iteration yields a line.
    time_i: The index of the timestamp. Supports negative indices.
    title_i_start: The index of the first word of the chapter's title.
    title_i_end: The index of the end of the chapter's title.
    final_time_end: The ending time of the final chapter, which is the length of the track.
    """
    file_iter = iter(file)
    tokens = next(file_iter).split()
    try:
        while True:
            time_start = tokens[time_i]
            if not time_string(time_start):
                print('error: could not interpret \'{}\' as time'
                      ''.format(time_start))
                sys.exit(1)
            chapter_string = ' '.join(tokens[title_i_start:title_i_end])
            tokens = next(file_iter).split()
            yield {
                'time_start': time_start,
                'time_end': tokens[time_i],
                'chapter_string': chapter_string
            }
    except StopIteration:
        yield {
            'time_start': time_start,
            'time_end': final_time_end,
            'chapter_string': chapter_string
        }

def main():
    # Configure argparse
    parser = argparse.ArgumentParser(
            description="Converts lines of text containing chapter information "
                        "into XML readable by mkvpropedit.")
    parser.add_argument('-d', '--debug', action='store_true', help="enable "
                        "debug printing")
    parser.add_argument('inputfile', help="text file where each line has a "
                        "chapter name and start time")
    parser.add_argument('outputfile', help="XML file to be written to")
    parser.add_argument('-i', dest='indices', metavar=('timestamp', 'titlestart',
                        'titleend'), nargs=3, help="specifies the indices of the "
                        " elements on each line (supports negative indices) "
                        "where timestamp=tokens[timestamp] and title=tokens"
                        "[titlestart:titleend]. Arguments must be integers or "
                        "None. If neither -i nor -c are specified, an indexing "
                        "configuration will be automatically generated.")
    parser.add_argument('-c', dest='config', help="Use a premade indexing "
                        "configuration. Overrides the -i option. Valid "
                        "configs are: {}".format(', '.join(CONFIG_PRESETS)), 
                        choices=CONFIG_PRESETS, metavar='config', default=None)
    parser.add_argument('-e', help="specifies the timestamp of the end of the "
                        "final chapter, usually the length of the entire track.",
                        dest='endtime', required=True, metavar='endtime')
    # Parse args
    args = parser.parse_args()
    INPUT_FILENAME = args.inputfile
    OUTPUT_FILENAME = args.outputfile
    debug = args.debug
    if args.config is not None:
        try:
            parse_config = CONFIG_PRESETS[args.config]
        except KeyError:
            # Should theoretically never get here
            print('config not recognized: {}'.format(args.config))
            sys.exit(1)
    elif args.indices is not None:
        try:
            parse_config = [None if i.lower() == 'none' else int(i) for i in args.indices]
        except ValueError as ve:
            print('error: could not interpret {} as index'.format(ve.args[0].split()[-1]))
            sys.exit(1)
    else:
        if debug:
            print('no configuration specified, generating...')
        print('automatic configuration generation not yet implemented, please '
              ' use -i or -c')
        sys.exit(1)
    if time_string(args.endtime):
        END_TIME = args.endtime
    else:
        print('error: could not interpret \'{}\' as time'.format(args.endtime))
        sys.exit(1)
    # Create elementTree
    chapters = etree.Element('Chapters')
    edition_entry = etree.SubElement(chapters, 'EditionEntry')
    for tokens in parse(open(INPUT_FILENAME, encoding='utf-8'), *parse_config, END_TIME):
        # Iterate through each chapter
        if debug:
            print('processing chapter {0[chapter_string]}, start={0[time_start]}, '
                  'end={0[time_end]}'.format(tokens))
        chapter = etree.SubElement(edition_entry, 'ChapterAtom')
        time_start = etree.SubElement(chapter, 'ChapterTimeStart')
        time_start.text = tokens['time_start']
        time_end = etree.SubElement(chapter, 'ChapterTimeEnd')
        time_end.text = tokens['time_end']
        chapter_display = etree.SubElement(chapter, 'ChapterDisplay')
        chapter_string = etree.SubElement(chapter_display, 'ChapterString')
        chapter_string.text =  tokens['chapter_string']
        chapter_language = etree.SubElement(chapter_display, 'ChapterLanguage')
        chapter_language.text = 'eng'
    # Output XML
    xml_bytes = etree.tostring(chapters, pretty_print=True, xml_declaration=True)
    if debug:
        print('opening file {}'.format(OUTPUT_FILENAME))
    with open(OUTPUT_FILENAME, 'w') as file_out:
        file_out.write(xml_bytes.decode())
    if debug:
       print('wrote to {} succesfully'.format(OUTPUT_FILENAME))
    sys.exit(0)

if __name__ == '__main__':
    main()