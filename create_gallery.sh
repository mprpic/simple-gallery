#!/bin/bash

usage(){
    echo "Usage: ./$0 dir_name main_file_name"
    exit 1
}

if [ "$#" -ne 2 ]; then
    echo "ERROR: Illegal number of arguments"
    usage
    exit 1
fi

/usr/bin/mkdir "$1"
/usr/bin/cp right.svg left.svg "$1"

sed '/<!-- images start -->/q' ./gallery.html > "$1/$2"

for image in $(ls | grep -i "\.jpe\?g"); do
    printf '    <img src="%s" class="hidden" />\n' "$image" >> "$1/$2"
    /usr/bin/cp "$image" "$1"
done

sed -n '/<!-- images end -->/,$p' ./gallery.html >> "$1/$2"
