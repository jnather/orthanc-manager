#!/bin/bash

# Define the output file
output_file="all_files_concatenated.txt"

# Initialize the output file
echo "Concatenated files from $(pwd)" > $output_file
echo "==============================" >> $output_file

# Recursively find and concatenate all files into the output file
find . -type f -exec echo -e "\n\n===== File: {} =====\n\n" >> $output_file \; -exec cat {} >> $output_file \;

# Notify the user
echo "All files have been concatenated into $output_file"

