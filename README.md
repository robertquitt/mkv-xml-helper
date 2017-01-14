mkv-xml-helper
====
A tool I use to help me generate chapters for long audios in .mkv format from track listings.
## chapters_to_xml.py
### converts track listings into xml data readable by mkvpropedit

Turns

1. Fibre - Supernatural 0:00 - 2:32
2. Night Tempo - Dreamer 2:33 - 5:05
[...]

into
```
<?xml version='1.0' encoding='ASCII'?>
<Chapters>
  <EditionEntry>
    <ChapterAtom>
      <ChapterTimeStart>0:00</ChapterTimeStart>
      <ChapterTimeEnd>2:32</ChapterTimeEnd>
      <ChapterDisplay>
        <ChapterString>Fibre - Supernatural</ChapterString>
        <ChapterLanguage>eng</ChapterLanguage>
      </ChapterDisplay>
    </ChapterAtom>
    <ChapterAtom>
      <ChapterTimeStart>2:33</ChapterTimeStart>
      <ChapterTimeEnd>5:05</ChapterTimeEnd>
      <ChapterDisplay>
        <ChapterString>Night Tempo - Dreamer</ChapterString>
        <ChapterLanguage>eng</ChapterLanguage>
      </ChapterDisplay>
    </ChapterAtom>
    [...]
  </EditionEntry>
</Chapters>
    ```