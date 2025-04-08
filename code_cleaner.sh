#!/bin/bash

# Function to process files
process_file() {
    local input_file="$1"
    local output_file="$2"
    local extension="${input_file##*.}"

    # Define comment patterns for supported languages
    declare -A comment_patterns=(
        ["py"]="#.*|\"\"\".*?\"\"\"|'''.*?'''"
        ["js"]="\/\/.*|\/\*.*?\*\/"
        ["java"]="\/\/.*|\/\*.*?\*\/"
        ["c"]="\/\/.*|\/\*.*?\*\/"
        ["cpp"]="\/\/.*|\/\*.*?\*\/"
        ["sh"]="#.*"
        ["html"]="<!--.*?-->"
        ["css"]="\/\*.*?\*\/"
    )

    # Define log patterns for supported languages
    declare -A log_patterns=(
        ["py"]="print\(.*?\)|logging\.\w+\(.*?\)"
        ["js"]="console\.\w+\(.*?\)"
        ["java"]="System\.out\.\w+\(.*?\)|System\.err\.\w+\(.*?\)"
        ["c"]="printf\(.*?\)|fprintf\(.*?\)"
        ["cpp"]="std::cout.*?<<|std::cerr.*?<<"
        ["sh"]="echo .*"
    )

    # Get the comment and log patterns for the file extension
    comment_pattern="${comment_patterns[$extension]}"
    log_pattern="${log_patterns[$extension]}"

    # If patterns are defined, process the file
    if [[ -n "$comment_pattern" || -n "$log_pattern" ]]; then
        # Remove comments and log statements
        sed -E "s/$comment_pattern//g; s/$log_pattern//g" "$input_file" > "$output_file"
    else
        # Copy the file as is if no patterns are defined
        cp "$input_file" "$output_file"
    fi
}

# Main script
main() {
    local current_dir=$(pwd)
    local output_dir="$current_dir/copy"

    # Create the output directory
    mkdir -p "$output_dir"

    # Process each file in the current directory recursively
    find "$current_dir" -type f ! -path "$output_dir/*" | while read -r file; do
        # Determine the relative path for the output file
        relative_path="${file#$current_dir/}"
        output_file="$output_dir/$relative_path"

        # Create the necessary directories in the output folder
        mkdir -p "$(dirname "$output_file")"

        # Process the file
        process_file "$file" "$output_file"
    done

    echo "Processing complete. Processed files are saved in the 'copy' folder."
}

# Run the main function
main
