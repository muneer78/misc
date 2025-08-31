import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import tempfile
import os


def create_backup(file_path):
    """Create a backup of the original file"""
    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def is_valid_epub(file_path):
    """Check if the EPUB is a valid ZIP file"""
    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.testzip()
        return True
    except (zipfile.BadZipFile, Exception) as e:
        print(f"Error: '{file_path}' is not a valid EPUB or ZIP file. {e}")
        return False


def find_opf_file(zip_ref):
    """Find the OPF file in the EPUB"""
    # First, check for container.xml to find the OPF file location
    try:
        container_content = zip_ref.read('META-INF/container.xml')
        container_root = ET.fromstring(container_content)

        # Find the rootfile element
        for rootfile in container_root.findall('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile'):
            return rootfile.get('full-path')
    except:
        pass

    # Fallback: look for common OPF file locations
    common_opf_paths = [
        'OEBPS/content.opf',
        'OPS/content.opf',
        'content.opf',
        'EPUB/content.opf'
    ]

    for path in common_opf_paths:
        try:
            zip_ref.getinfo(path)
            return path
        except KeyError:
            continue

    # Last resort: search for any .opf file
    for file_info in zip_ref.filelist:
        if file_info.filename.endswith('.opf'):
            return file_info.filename

    return None


def update_epub_metadata_safe(file_path, new_author=None, new_title=None):
    """Safely update EPUB metadata by working with the ZIP directly"""
    try:
        # Check if the file is valid
        if not is_valid_epub(file_path):
            return False

        # Create backup
        backup_path = create_backup(file_path)

        # Create temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Extract EPUB contents
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_path)

                # Find the OPF file
                opf_file = find_opf_file(zip_ref)
                if not opf_file:
                    print("Error: Could not find OPF file in EPUB")
                    return False

                print(f"Found OPF file: {opf_file}")

            # Work with the OPF file
            opf_path = temp_path / opf_file
            if not opf_path.exists():
                print(f"Error: OPF file not found at {opf_path}")
                return False

            # Parse the OPF XML
            tree = ET.parse(opf_path)
            root = tree.getroot()

            # Define namespaces
            namespaces = {
                'opf': 'http://www.idpf.org/2007/opf',
                'dc': 'http://purl.org/dc/elements/1.1/'
            }

            # Find metadata section
            metadata = root.find('.//opf:metadata', namespaces)
            if metadata is None:
                # Try without namespace
                metadata = root.find('.//metadata')
                if metadata is None:
                    print("Error: Could not find metadata section")
                    return False

            # Get current metadata
            current_title = None
            current_author = None

            for elem in metadata:
                if elem.tag.endswith('}title') or elem.tag == 'title':
                    current_title = elem.text
                elif elem.tag.endswith('}creator') or elem.tag == 'creator':
                    current_author = elem.text

            print("Current Metadata:")
            print(f"Title: {current_title if current_title else 'Not set'}")
            print(f"Author: {current_author if current_author else 'Not set'}")

            # Update metadata
            updated = False

            if new_title:
                # Find and update title
                title_elem = None
                for elem in metadata:
                    if elem.tag.endswith('}title') or elem.tag == 'title':
                        title_elem = elem
                        break

                if title_elem is not None:
                    title_elem.text = new_title
                    updated = True
                else:
                    # Create new title element
                    title_elem = ET.SubElement(metadata, '{http://purl.org/dc/elements/1.1/}title')
                    title_elem.text = new_title
                    updated = True

            if new_author:
                # Find and update creator
                creator_elem = None
                for elem in metadata:
                    if elem.tag.endswith('}creator') or elem.tag == 'creator':
                        creator_elem = elem
                        break

                if creator_elem is not None:
                    creator_elem.text = new_author
                    updated = True
                else:
                    # Create new creator element
                    creator_elem = ET.SubElement(metadata, '{http://purl.org/dc/elements/1.1/}creator')
                    creator_elem.text = new_author
                    updated = True

            if not updated:
                print("No changes made to metadata")
                return True

            # Save the modified OPF file
            tree.write(opf_path, encoding='utf-8', xml_declaration=True)

            # Create new EPUB file
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                for root_dir, dirs, files in os.walk(temp_path):
                    for file in files:
                        file_path_full = Path(root_dir) / file
                        arc_name = file_path_full.relative_to(temp_path)
                        new_zip.write(file_path_full, arc_name)

            print("\nMetadata updated successfully!")
            print("Updated Metadata:")
            print(f"Title: {new_title if new_title else current_title}")
            print(f"Author: {new_author if new_author else current_author}")

            return True

    except Exception as e:
        print(f"Error processing file: {e}")
        import traceback
        traceback.print_exc()

        # Restore from backup if something went wrong
        if 'backup_path' in locals():
            try:
                shutil.copy2(backup_path, file_path)
                print(f"Restored original file from backup")
            except Exception as restore_error:
                print(f"Error restoring backup: {restore_error}")

        return False


# Main execution
if __name__ == "__main__":
    file_path = Path("/Users/muneer78/Downloads/patterson-america-on-the-precipice.epub")
    new_author = "Richard Patterson"
    new_title = "America on the Precipice"

    # Ensure the file exists
    if file_path.exists() and file_path.is_file():
        success = update_epub_metadata_safe(file_path, new_author, new_title)
        if success:
            print("\n✅ EPUB metadata updated successfully!")
        else:
            print("\n❌ Failed to update EPUB metadata.")
    else:
        print(f"Error: The file '{file_path}' does not exist or is not a valid file.")