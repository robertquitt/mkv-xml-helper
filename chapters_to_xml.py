'''
chapters_to_xml.py - converts track listing text into xml data for mkvpropedit

ffmpeg -i file.ogg -c:a copy file.mkv
mkvpropedit file.mkv --chapter chapters.xml
'''
from lxml import etree

INPUT_FILENAME = 'super_mario_galaxy.txt'
OUTPUT_FILENAME = 'super_mario_galaxy.xml'
END_TIME = '02:15:24'

def parse_squad_goals(file):
    """From the description of https://www.youtube.com/watch?v=tbWS0j2fulY
    Text is of the form:
    1. Fibre - Supernatural 0:00 - 2:32
    2. Night Tempo - Dreamer 2:33 - 5:05
    ...
    """
    for line in file:
        tokens = line.split()
        yield {
            'time_start': tokens[-3],
            'time_end': tokens[-1],
            'chapter_string': ' '.join(tokens[1:-3])
        }

def parse_pink_season(file):
    """From the description of https://www.youtube.com/watch?v=0c_mhrB7LlQ
    Text is of the form:
    1. Hot Nickel Ball On A P*ssy 0:00
    2. Are You Serious 2:19
    ...
    """
    file_iter = iter(file)
    tokens = next(file_iter).split()
    try:
        while True:
            time_start = tokens[-1]
            chapter_string = ' '.join(tokens[1:-1])
            tokens = next(file_iter).split()
            yield {
                'time_start': time_start,
                'time_end': tokens[-1],
                'chapter_string': chapter_string
            }
    except StopIteration:
        yield {
            'time_start': time_start,
            'time_end': END_TIME,
            'chapter_string': chapter_string
        }

def parse_mario_galaxy(file):
    """From the description of https://www.youtube.com/watch?v=ca7IELhD_mI
    Text is of the form:
    0:00 Wii Menu - Starting The Game (''Super Mario Galaxy'')
    0:04 Star Festival
    ...
    """
    file_iter = iter(file)
    tokens = next(file_iter).split()
    try:
        while True:
            time_start = tokens[0]
            chapter_string = ' '.join(tokens[1:])
            tokens = next(file_iter).split()
            yield {
                'time_start': time_start,
                'time_end': tokens[0],
                'chapter_string': chapter_string
            }
    except StopIteration:
        yield {
            'time_start': time_start,
            'time_end': END_TIME,
            'chapter_string': chapter_string
        }

parse = parse_mario_galaxy

chapters = etree.Element('Chapters')
edition_entry = etree.SubElement(chapters, 'EditionEntry')

for tokens in parse(open(INPUT_FILENAME, encoding='utf-8')):
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

out_str = etree.tostring(chapters, pretty_print=True, xml_declaration=True).decode()

with open(OUTPUT_FILENAME, 'w') as file_out:
    file_out.write(out_str)