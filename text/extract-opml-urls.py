from pathlib import Path
import xml.etree.ElementTree as ET


def extract_and_prefix_rss_urls(opml_path, output_dir):
    try:
        # Ensure the OPML file exists
        opml_file = Path(opml_path)
        if not opml_file.is_file():
            raise FileNotFoundError(f"The file {opml_file} does not exist.")

        # Parse the OPML file
        tree = ET.parse(opml_file)
        root = tree.getroot()

        # Find all outline elements
        outlines = root.findall(".//outline")

        # Collect and prefix RSS URLs
        rss_urls = []
        for outline in outlines:
            url = outline.attrib.get("xmlUrl")
            if url:  # Only append if `xmlUrl` exists
                rss_urls.append(f"  - href: {url}")

        # Set output file path
        output_dir = Path(output_dir)
        output_dir.mkdir(
            parents=True, exist_ok=True
        )  # Create directory if it doesn't exist
        output_file = output_dir / "rss_urls.txt"

        # Write prefixed RSS URLs to the text file
        with output_file.open("w") as f:
            f.write("\n".join(rss_urls))

        print(f"Extracted and prefixed {len(rss_urls)} RSS URLs to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
opml_path = "/Users/muneer78/Downloads/fraidycat.opml"  # Replace with the actual path to your OPML file
output_dir = "/Users/muneer78/Downloads"  # Replace with the desired output directory

extract_and_prefix_rss_urls(opml_path, output_dir)
