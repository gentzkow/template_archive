#!/bin/bash   

# separates "./path/to/program.do" into
#   (1) file = program.do
#   (2) extension = do
#   (3) path_to_file = ./path/to/
#   (4) filename = program
unset parse_fp 
parse_fp() {

    # get arguments
    fp="$1"
    opt="$2"
    
    file="${fp##*/}"

    case $opt in
        1)  output="${file}"
            ;;
        2)  output="${file##*.}"
            ;;
        3)  output="${fp%"${file}"}"
            ;;
        4)  output="${file%.*}"
            ;;
        *)  output="ERROR in parse_fp: unmatched option"
            ;;
    esac

    echo "${output}"

}

unset get_abs_filename
get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")"; pwd -P)/$(basename "$1")"
}
