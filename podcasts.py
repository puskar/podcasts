import os
import time
import xml.etree.ElementTree as ET
import argparse

def scan_directory_for_mp3_files(directory):
    mp3_files = []
    for root, dirs, files in os.walk(directory):
        dirs.sort()
        files.sort()
        for file in files:
            if file.endswith(".mp3"):
                mp3_files.append(os.path.join(root, file))
    return mp3_files

def create_podcast_feed(mp3_files, feed_title, feed_description, feed_link, output_file):
    rss = ET.Element("rss", {
        "xmlns:atom":"http://www.w3.org/2005/Atom",
        "xmlns:content": "http://purl.org/rss/1.0/modules/content/",
        "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "xmlns:podcast": "https://podcastindex.org/namespace/1.0",
        "version": "2.0"
    })
    channel = ET.SubElement(rss, "channel")

    title = ET.SubElement(channel, "title")
    title.text = feed_title

    language = ET.SubElement(channel, "language")
    language.text = "en-us"

    description = ET.SubElement(channel, "description")
    description.text = feed_description

    link = ET.SubElement(channel, "link")
    link.text = feed_link

    atom_link = ET.SubElement(channel, "atom:link", {"href": "https://api.puskar.net/podcasts/eara/indes.xml", "rel": "self", "type": "application/rss+xml"})

    # iTunes-specific elements
    itunes_author = ET.SubElement(channel, "itunes:author")
    itunes_author.text = "Cecilia and Helen"

    itunes_category = ET.SubElement(channel, "itunes:category", {"text": "Music Commentary"})

    itunes_image = ET.SubElement(channel, "itunes:image", {"href": "https://api.puskar.net/podcasts/"+ os.path.basename(args.directory_to_scan) +"/image.jpg"})

    itunes_explicit = ET.SubElement(channel, "itunes:explicit")
    itunes_explicit.text = "true"

    itunes_owner = ET.SubElement(channel, "itunes:owner")
    itunes_owner_name = ET.SubElement(itunes_owner, "itunes:name")
    itunes_owner_name.text = "Helen and Cecilia"
    itunes_owner_email = ET.SubElement(itunes_owner, "itunes:email")
    itunes_owner_email.text = "hpuskar@oberlin.edu"

    itunes_subtitle = ET.SubElement(channel, "itunes:subtitle")
    itunes_subtitle.text = "Helen and Cecilia's Radio Show"

    itunes_summary = ET.SubElement(channel, "itunes:summary")
    itunes_summary.text = feed_description

    for index, mp3_file in enumerate(mp3_files, start=1):
        item = ET.SubElement(channel, "item")

        item_title = ET.SubElement(item, "title")
        item_title.text = description.text + time.strftime(" %B %d, %Y ", time.gmtime(os.path.getmtime(mp3_file)))

        item_description = ET.SubElement(item, "description")
        item_description.text = description.text + time.strftime(" %B %d, %Y ", time.gmtime(os.path.getmtime(mp3_file)))

        item_xunes_image = ET.SubElement(item, "itunes:image", {"href": "https://api.puskar.net/podcasts/"+ os.path.basename(args.directory_to_scan) +"/image.jpg"})

        item_link = ET.SubElement(item, "link")
        item_link.text = "https://api.puskar.net/podcasts/" + os.path.dirname(os.path.relpath(mp3_file, args.podcast_root))

        item_pubDate = ET.SubElement(item, "pubDate")
        item_pubDate.text = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(os.path.getmtime(mp3_file)))

        # iTunes-specific elements for each item
        itunes_duration = ET.SubElement(item, "itunes:duration")
        itunes_duration.text = "00:00:00"  # Replace with actual duration

        itunes_episode = ET.SubElement(item, "itunes:episode")
        itunes_episode.text = str(index)

        itunes_explicit = ET.SubElement(item, "itunes:explicit")
        itunes_explicit.text = "true"

        itunes_summary = ET.SubElement(item, "itunes:summary")
        itunes_summary.text = "Podcast episode: " + os.path.basename(mp3_file)

        enclosure = ET.SubElement(item, "enclosure", {
            "url": "https://api.puskar.net/podcasts/" + os.path.relpath(mp3_file, args.podcast_root),
            "length": str(os.path.getsize(mp3_file)),
            "type": "audio/mpeg"
        })

    tree = ET.ElementTree(rss)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a podcast feed from MP3 files.")
    parser.add_argument("podcast_root", help="Base directory for podcast")
    parser.add_argument("directory_to_scan", help="Podcast directory to scan for MP3 files")
    parser.add_argument("feed_title", help="Title of the podcast feed")
    parser.add_argument("feed_description", help="Description of the podcast feed")
    parser.add_argument("output_file", help="Output file for the podcast feed")

    args = parser.parse_args()

    mp3_files = scan_directory_for_mp3_files(args.podcast_root+"/"+args.directory_to_scan)
    create_podcast_feed(mp3_files, args.feed_title, args.feed_description, "https://api.puskar.net/podcasts/", args.output_file)
    print(f"Podcast feed generated: {args.output_file}")
