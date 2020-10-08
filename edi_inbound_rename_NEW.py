#! python3
# -*- encoding: utf-8 -*-

# Rename EDI files based on ISA and type.

###############################################################################
# Change Log:
#   * 17-Feb-2017: Added a catchall that moves all remaining files.
#   * 27-Jan-2017: Initial release. Husqvarna added.
###############################################################################

import os
import csv

# File Paths are for Windows OS
base_dir = os.path.join("M:", "\EDI")
in_dir = os.path.join(base_dir, "\IN")
staging_dir = os.path.join(base_dir, "IN\STAGING")
staging_dir_test = os.path.join(base_dir, "IN\TEST")


def show_segments(file_name):
    lines = open(file_name).read().split("~")
    for line in lines:
        print("\n\nProcessing line: %s\n" % line)
        cells = line.split("*")
        for i, cell in enumerate(cells):
            print("%d: %s" % (i, cell))


def get_sf_segment(file_name):
    f = open(file_name).read().split("~")
    for line in f:
        cells = line.split("*")
        for i, cell in enumerate(cells):
            if cell == 'sf':
                print(i)
                print(cell)

def get_isa(filename):
    with open(filename) as csvfile:
        csvfile = csvfile.read().split("~")
        readCSV = csv.reader(csvfile, delimiter="*")
        for row in readCSV:
            for idx, cell in enumerate(row):
                isa = row[idx+6].rstrip()
                return isa


def get_file_type(filename):
    # The cell after the 'ST' segment
    with open(filename) as csvfile:
        csvfile = csvfile.read().split('~')
        readCSV = csv.reader(csvfile, delimiter='*')
        for row in readCSV:
            for idx, cell in enumerate(row):
                if cell == "ST":
                    st_cell = row[idx+1]
                    return st_cell


def process_staging_dir():
    print("\nProcessing files in " + staging_dir)
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            rename_file_husq(filename)
        # Move any files left over
        move_remaining_files(filename)
    else:
        print("No files found")


def move_remaining_files(filename):
    # Move any remaing files from STAGING to IN
    print("\nMoving remaining files")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            old_filename = os.path.join(staging_dir, filename)
            new_filename = os.path.join(in_dir, filename)
            os.rename(old_filename, new_filename)
            print(old_filename + '  >  ' + new_filename)


###############################################################################
# Husqvarna Begin
###############################################################################
def get_ship_from_husq(filename):
    filename = os.path.join(staging_dir, filename)
    with open(filename) as csvfile:
        csvfile = csvfile.read().split('~')
        readCSV = csv.reader(csvfile, delimiter='*')
        for row in readCSV:
            for idx, cell in enumerate(row):
                if cell == "SF":
                    sf_cell = row[idx+1]
    try:
        if sf_cell == "THOMSON PLASTICS":
            sf = "THM"
        if sf_cell == "THOMSON PLAS. LEXINGTON":
            sf = "LEX"
    except:
        print("Ship From not found in file")
        sf = "MISSING"
    return sf


def rename_file_husq(filename):
    filename = os.path.join(staging_dir, filename)
    f = filename
    isa = get_isa(f)
    if isa != "HUSQORNGBRG":
        return

    # ECGrid file format: 1027-20201006101520-2e7441af.edi

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split
    f_prefix = "HUSQ"  # Set the customer name
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type(filename)

    # Get Ship From location from 850s and 860s only
    if f_type == "850" or f_type == "860":
        sf = get_ship_from_husq(filename)
        new_filename = f_prefix + sep + sf + sep + f_type + sep + f_date + sep + f_idx + f_ext
    else:
        new_filename = f_prefix + sep + f_type + sep + f_date + sep + f_idx + f_ext

    print(new_filename)
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    # new_filename = os.path.join(staging_dir_test, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# Husqvarna End
###############################################################################


if __name__ == '__main__':
    process_staging_dir()