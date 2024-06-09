#!/usr/bin/env python3
import re
import argparse

def print_banner():
    banner="""   
___________________________________________________________________________
  ____  _______     _______ ____  ____  _____   _____ ____  _____ _____ 
 |  _ \| ____\ \   / / ____|  _ \/ ___|| ____| |_   _|  _ \| ____| ____|
 | |_) |  _|  \ \ / /|  _| | |_) \___ \|  _|     | | | |_) |  _| |  _|  
 |  _ <| |___  \ V / | |___|  _ < ___) | |___    | | |  _ <| |___| |___ 
 |_| \_\_____|  \_/  |_____|_| \_\____/|_____|   |_| |_| \_\_____|_____|
___________________________________________________________________________
                        @Deividgdt - Version 1.0.0
    """
    print(banner)                                                           

# If the tree output color codes, we remove them
def remove_color_codes(line):
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', line)

# Four blank spaces are replaced by [b], this way
# we calculate the current depth of the tree
def replace_blank_spaces(line):
    return line.replace('    ', '[b]')

# Process the current line to remove color codes
# and blank spaces
def process_line(line):
    line = remove_color_codes(line)
    line = replace_blank_spaces(line)

    return line

# We calculate the current depth
def calculate_depth(line):             
    return line.count("│") + line.count("└──") + line.count("├──") + line.count('[b]')

# In order to build the paths, we need to know the changes
# between the differents depths, with this function
# we handle the depth change
def handle_depth_change(stack, current_depth, last_depth, lastchar):
    # Check if the last depth level is lesser
    if last_depth > current_depth:
        depth_difference=last_depth-current_depth               
        pop_out_n_times=depth_difference+1

        for i in range(0, pop_out_n_times):
            # print("popping out: "+str(pop_out_n_times)+" times")
            stack.pop()

    if last_depth == current_depth and len(stack) > 0 and lastchar != '└──':
        stack.pop()

# Build the paths, and print the path with the search term
def build_paths(filename, search_term, verbose=False):
    paths = []
    stack = []
    node = ""
    lastchar = ""
    currentchar = ""
    last_depth = 0

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            total_lines = len(lines)

            print("Reading "+str(total_lines)+" lines from the file: "+filename)

            for line_number, current_line in enumerate(lines, start=1):
                line = process_line(current_line)

                if "├──" in line:
                    currentchar="├──"

                if "└──" in line:
                    currentchar="└──"
                
                # Save the current depth level
                current_depth = calculate_depth(line)

                # We handle the depth change in this loop
                handle_depth_change(stack, current_depth, last_depth, lastchar)

                # Depending on the current char, we split the string in order to get the node name
                if currentchar == '└──':
                    node = line.split('└──')[-1].strip()
                elif currentchar == '├──':
                    node = line.split('├──')[-1].strip()
                else:
                    node = line.strip()

                stack.append(node)
                path = '/'.join(stack)

                if verbose:
                    print(stack)

                if search_term.lower() in path.lower():
                    paths.append(path)

                last_depth=current_depth
                lastchar=currentchar

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

    return paths

# We parse the arguments using argparse module 
def parse_arguments():
    parser = argparse.ArgumentParser(description="Search for paths in a file tree structure.")
    parser.add_argument('--filename', type=str, help='The file to search within.')
    parser.add_argument('--search_term', type=str, help='The term to search for in the paths.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output.')
    return parser.parse_args()

# Main function
def main():
    print_banner()
    args = parse_arguments()

    paths = build_paths(args.filename, args.search_term, args.verbose)

    if paths:
        print(f"\nFound {len(paths)} instances of '{args.search_term}':")
        for path in paths:
            print(path)
    else:
        print(f"No instances of '{args.search_term}' found.")

if __name__ == "__main__":
    main()