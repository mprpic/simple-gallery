import os
import sys
import shutil
import optparse
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: missing jinja2 module")
    sys.exit(1)

GALLERY_TEMPLATE = './gallery.html'
IMAGE_EXT = ['.png', '.jpg', '.jpeg']


def main():

    p = optparse.OptionParser(description='Generate a simple one-page HTML gallery.',
                              usage='%prog [-h|--help] -i DIR [-o OUTDIR]')
    p.add_option('-i', '--input', dest='in_dir',
                 action='store', help='Input directory where images are located')
    p.add_option('-o', '--output', dest='out_dir',
                 action='store', help='Output directory (default: "./gallery")')
    p.add_option('-t', '--title', dest='title',
                 action='store', help="Title to be used in the gallery's HTML (default: Gallery)")
    (opts, args) = p.parse_args()

    if not opts.in_dir:
        p.error('You must specify an input directory!')
        sys.exit(1)

    if not os.path.isdir(opts.in_dir):
        p.error('The specified location is not a valid directory')

    # Default title is 'Gallery'
    title = opts.title if opts.title else 'Gallery'

    # Default output is './gallery'
    out_dir = opts.out_dir.rstrip('/') if opts.out_dir else './gallery'

    # Overwriting is dangerous, quitting is safer
    if os.path.exists(out_dir):
        print('ERROR: Directory %s already exists. Remove it or specify a different one.' % out_dir)
        sys.exit(1)

    file_list = os.listdir(opts.in_dir)

    # Filter out non-image files
    img_file_list = []
    for f in file_list:
        if os.path.splitext(f)[1].lower() in IMAGE_EXT:
            img_file_list.append(f)
        else:
            print('Skipping %s -- not an image file' % f)

    if not img_file_list:
        print('ERROR: Did not locate any images files the specified directory')
        sys.exit(1)

    # Load up Jinja template and pass sorted data
    jinja_env = Environment(loader=FileSystemLoader('./'))
    template = jinja_env.get_template(GALLERY_TEMPLATE)
    rendered_html = template.render(title=title, images=sorted(img_file_list))

    # Create output directory
    print('Creating directory: %s' % out_dir)
    os.makedirs(out_dir)

    # Write out HTML file
    with open(os.path.join(out_dir, 'index.html'), 'w') as f:
        f.write(rendered_html)

    # Copy all image files
    for f in img_file_list:
        shutil.copy('%s/%s' % (opts.in_dir.rstrip('/'), f), out_dir)


if __name__ == '__main__':
    main()
