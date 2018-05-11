import os
import re
import sys
import shutil
import argparse

GALLERY_TEMPLATE = os.path.join(os.path.dirname(__file__), './gallery.template')
IMAGE_EXT = ['.png', '.jpg', '.jpeg']
IMAGE_HTML = '<img class="hidden" data-src="{image}" alt="Loading photo..." />'


def main():
    p = argparse.ArgumentParser(description='Generate a simple one-page HTML gallery.')
    p.add_argument('-i', '--input', dest='in_dir', required=True,
                   action='store', help='input directory where images are located')
    p.add_argument('-o', '--output', dest='out_dir',
                   action='store', help='output directory (default: "./gallery")')
    p.add_argument('-t', '--title', dest='title',
                   action='store', help='title to be used in the <title> tag of the HTML (default: Gallery)')
    args = p.parse_args()

    if not args.in_dir:
        p.error('You must specify an input directory!')
        sys.exit(1)

    if not os.path.isdir(args.in_dir):
        p.error('The specified location is not a valid directory')

    # Default title is 'Gallery'
    title = args.title if args.title else 'Gallery'

    # Default output is './gallery'
    out_dir = args.out_dir.rstrip('/') if args.out_dir else './gallery'

    # Overwriting is dangerous, quitting is safer
    if os.path.exists(out_dir):
        print('ERROR: Directory {} already exists. Remove it or specify a different one.'.format(out_dir))
        sys.exit(1)

    file_list = os.listdir(args.in_dir)

    # Filter out non-image files
    img_file_list = []
    for f in file_list:
        _, file_ext = os.path.splitext(f)
        if file_ext.lower() in IMAGE_EXT:
            img_file_list.append(f)
        else:
            print('Skipping {} -- not an image file'.format(f))

    if not img_file_list:
        print('ERROR: Did not locate any image files in {}'.format(args.in_dir))
        sys.exit(1)

    # Open gallery.html template and add images and title
    with open(GALLERY_TEMPLATE) as f:
        template = f.read()

    html = re.sub(r'{{ TITLE }}', title, template)
    photos_html = [IMAGE_HTML.format(image=image) for image in sorted(img_file_list)]
    html = re.sub(r'{{ PHOTOS }}', '\n'.join(photos_html), html)

    # Create output directory
    print('Created directory: {}'.format(out_dir))
    os.makedirs(out_dir)

    # Write out HTML file
    with open(os.path.join(out_dir, 'index.html'), 'w') as f:
        f.write(html)

    # Copy all image files
    for f in img_file_list:
        shutil.copy('{}/{}'.format(args.in_dir.rstrip('/'), f), out_dir)


if __name__ == '__main__':
    main()
