#! python3
# -*- encoding: utf-8 -*-

# Rename EDI files based on ISA and type.
# Each customer gets their own section, even though there may be 
#   duplicated functionality.
# This allows for easier future changes.

###############################################################################
# Change Log:
#   * 20-Oct-2021: Added OWT/Ryobi, Auria, GA-Howell, GA-Shelby, GA-SPA, GA-AL,
#                  GATN, GA-Silao, GA-StClair, GA-Marlette
#   * 12-Oct-2020: Added Autoneum and Navistar
#   * 08-Oct-2020: Updated Husqvarna to the ECGrid format.
#   * 17-Feb-2017: Added a catchall that moves all remaining files.
#   * 27-Jan-2017: Initial release. Husqvarna added.
###############################################################################

import os
import re
import csv


# ISA Codes
cci_isa = "7062282688"
autoneum_isa = "GLII006"
husqvarna_isa = "HUSQORNGBRG"
navistar_isa = "781495650"
owt_isa = "827942173"
auria_isa = "ONCBUSUPPU"
ga_alabama_isa = "US080765057LBM"
ga_howell_isa = "609284922"
ga_shelby_isa = "080647135"
ga_spartanburg_isa = "US080950568SPA"
ga_tn_isa = "GA808659114"
ga_silao_isa = "GAS9403186J1"
ga_stclair_isa = "US117778503SCL"
ga_marlette_isa = "GA132713012"

# Ship To Codes
AURIA_THM = "02054852"
AURIA_LEX = "02054851"
AURIA_HOW = "02054850"

# File Paths are for Windows OS
base_dir = os.path.join("M:", "\EDI")
in_dir = os.path.join(base_dir, "IN")
staging_dir = os.path.join(base_dir, "IN\STAGING")
# For testing
# in_dir_test = os.path.join(base_dir, "_TEST_IN")
# staging_dir_test = os.path.join(base_dir, "_TEST_STAGING")
# in_dir = in_dir_test
# staging_dir = staging_dir_test


def get_isa_x12(filename):
    with open(filename) as csvfile:
        csvfile = csvfile.read().split("~")
        readCSV = csv.reader(csvfile, delimiter="*")
        for row in readCSV:
            for idx, cell in enumerate(row):
                isa = row[idx+6].rstrip()
                return isa


def get_file_type_x12(filename):
    # The cell after the 'ST' segment
    with open(filename) as csvfile:
        csvfile = csvfile.read().split('~')
        readCSV = csv.reader(csvfile, delimiter='*')
        for row in readCSV:
            for idx, cell in enumerate(row):
                if cell == "ST":
                    st_cell = row[idx+1]
                    return st_cell


def get_isa_edifact(filename):
    line_idx = None
    with open(filename) as edifile:
        edifile = edifile.read().split("'")
        if edifile[0].startswith("UNB"):
            line_idx = 2
        if edifile[0].startswith("UNA"):
            line_idx = 3
        line = re.split(r'\+', str(edifile))
        cell = re.split(':', str(line[line_idx]))
        isa = cell[0]
        return isa


def get_file_type_edifact(filename):
    line_idx = None
    with open(filename) as edifile:
        edifile = edifile.read().split("'")
        if edifile[0].startswith("UNB"):
            line_idx = 1
        if edifile[0].startswith("UNA"):
            line_idx = 2
        line = re.split(r'\+', str(edifile[line_idx]))
        cell = re.split(r':', str(line[2]))
        file_type = cell[0]
        return file_type


def process_staging_dir():
    # TODO: Pop renamed files off the filenames stack. Make this one loop.
    print("\nProcessing files in " + staging_dir)

    print("\nProcessing Husqvarna")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_husq(filename)
            except:
                continue

    print("\nProcessing Autoneum")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_autoneum(filename)
            except:
                continue

    print("\nProcessing Navistar")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_navistar(filename)
            except:
                continue
    
    print("\nProcessing OWT/Ryobi")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_owt(filename)
            except:
                continue

    print("\nProcessing Auria")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_auria(filename)
            except:
                continue

    print("\nProcessing Grupo-Antolin Howell (X12)")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_gahowell(filename)
            except:
                continue
    
    print("\nProcessing Grupo-Antolin Spartanburg (X12)")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_gaspa(filename)
            except:
                continue

    print("\nProcessing Grupo-Antolin Marlette (X12)")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_gamarlette(filename)
            except:
                continue
    
    print("\nProcessing Grupo-Antolin Spartanburg (EDIFACT)")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_gaspa_edifact(filename)
            except:
                continue
    
    print("\nProcessing Grupo-Antolin Shelby (EDIFACT)")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_gashelby(filename)
            except:
                continue
    
    print("\nProcessing Grupo-Antolin Alabama (EDIFACT)")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_gaalabama(filename)
            except:
                continue
    
    print("\nProcessing Grupo-Antolin TN/KY (EDIFACT)")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_gatn(filename)
            except:
                continue
    
    print("\nProcessing Grupo-Antolin Silao (EDIFACT)")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_gasilao(filename)
            except:
                continue

    print("\nProcessing Grupo-Antolin St. Clair (EDIFACT)")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            # Process each file based on customer functions
            try:
                rename_file_gastclair(filename)
            except:
                continue

    filenames = os.listdir(staging_dir)
    if filenames:
        # Move any files left over
        move_remaining_files(filename)
    else:
        print("No files found")


def move_remaining_files(filename):
    # Move any remaining files from STAGING to IN
    print("\nMoving remaining files")
    filenames = os.listdir(staging_dir)
    if filenames:
        for filename in filenames:
            old_filename = os.path.join(staging_dir, filename)
            new_filename = os.path.join(in_dir, filename)
            # new_filename = os.path.join(staging_dir_test, filename)
            os.rename(old_filename, new_filename)
            print(old_filename + '  >  ' + new_filename)


###############################################################################
###############################################################################
# X12 Format Files
###############################################################################
###############################################################################

###############################################################################
# CCI (X12) Begin
###############################################################################
def rename_file_cci(filename):
    
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in CCI format.
    if not f.startswith("TP"):
        # Not a CCI file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_x12(f_path)


    isa = get_isa_x12(f_path)
    if isa != cci_isa:
        return

    new_filename = "CCI" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# CCI End
###############################################################################

###############################################################################
# Husqvarna (X12) Begin
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
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_x12(f_path)


    isa = get_isa_x12(f_path)
    if isa != husqvarna_isa:
        return

    # Get Ship From location from 850s and 860s only
    if f_type == "850" or f_type == "860":
        sf = get_ship_from_husq(f_path)
        new_filename = "HUSQ" + sep + sf + sep + f_type + sep + f_date + sep + f_idx + f_ext
    else:
        new_filename = "HUSQ" + sep + f_type + sep + f_date + sep + f_idx + f_ext

    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    # new_filename = os.path.join(staging_dir_test, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# Husqvarna End
###############################################################################

###############################################################################
# Autoneum (X12) Begin
###############################################################################
def rename_file_autoneum(filename):
    # Ship From: 140472
    # Ship To Locations
    # THM Only: US03
    # HOW Only: MX02, US02
    # Both THM and HOW use US01

    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_x12(f_path)


    isa = get_isa_x12(f_path)
    if isa != autoneum_isa:
        return

    new_filename = "AUTONEUM" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# Autoneum End
###############################################################################

###############################################################################
# Navistar (X12) Begin
###############################################################################
def rename_file_navistar(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_x12(f_path)


    isa = get_isa_x12(f_path)
    if isa != navistar_isa:
        return

    new_filename = "NAVISTAR" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# Navistar End
###############################################################################

###############################################################################
# OWT/TTI/Ryobi (X12) Begin
###############################################################################
def rename_file_owt(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_x12(f_path)


    isa = get_isa_x12(f_path)
    if isa != owt_isa:
        return

    new_filename = "OWT" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# OWT/TTI/Ryobi End
###############################################################################

###############################################################################
# Auria (X12) Begin
###############################################################################
def get_ship_from_auria(filename):
    filename = os.path.join(staging_dir, filename)
    with open(filename) as csvfile:
        csvfile = csvfile.read().split('~')
        readCSV = csv.reader(csvfile, delimiter='*')
        for row in readCSV:
            for idx, cell in enumerate(row):
                if cell == "SF":
                    sf_cell = row[idx+3]

    try:
        if sf_cell == AURIA_HOW:
            sf = "HOW"
        if sf_cell == AURIA_LEX:
            sf = "LEX"
        if sf_cell == AURIA_THM:
            sf = "THM"
    except:
        print("Ship From not found in file")
        sf = "MISSING"
    return sf


def rename_file_auria(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_x12(f_path)


    isa = get_isa_x12(f_path)
    if isa != auria_isa:
        return
    sf = get_ship_from_auria(f_path)
    new_filename = "AURIA" + sep + sf + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# Auria End
###############################################################################

###############################################################################
# Grupo-Antolin Howell (X12) Begin
###############################################################################
def rename_file_gahowell(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_x12(f_path)


    isa = get_isa_x12(f_path)
    if isa != ga_howell_isa:
        return

    new_filename = "GAHOWELL" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# Grupo-Antolin Howell End
###############################################################################

###############################################################################
# Grupo-Antolin Spartanburg (X12) Begin
###############################################################################
def rename_file_gaspa(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_x12(f_path)


    isa = get_isa_x12(f_path)
    if isa != ga_spartanburg_isa:
        return

    new_filename = "GASPA" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# Grupo-Antolin Spartanburg End
###############################################################################

###############################################################################
# Grupo-Antolin Marlette (X12) Begin
###############################################################################
def rename_file_gamarlette(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_x12(f_path)


    isa = get_isa_x12(f_path)
    if isa != ga_marlette_isa:
        return

    new_filename = "GAMARLETTE" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)
###############################################################################
# Grupo-Antolin Marlette End
###############################################################################


###############################################################################
###############################################################################
# EDIFACT Format Files
###############################################################################
###############################################################################

###############################################################################
# Grupo-Antolin Spartanburg (EDIFACT) Begin
###############################################################################
def rename_file_gaspa_edifact(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_edifact(f_path)


    isa = get_isa_edifact(f_path)
    if isa != ga_spartanburg_isa:
        return

    new_filename = "GASPA" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)


###############################################################################
# Grupo-Antolin Spartanburg End
###############################################################################

###############################################################################
# Grupo-Antolin Shelby (EDIFACT) Begin
###############################################################################
def rename_file_gashelby(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_edifact(f_path)


    isa = get_isa_edifact(f_path)
    if isa != ga_shelby_isa:
        return

    new_filename = "GASHELBY" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)


###############################################################################
# Grupo-Antolin Shelby End
###############################################################################

###############################################################################
# Grupo-Antolin Alabama (EDIFACT) Begin
###############################################################################
def rename_file_gaalabama(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_edifact(f_path)


    isa = get_isa_edifact(f_path)
    if isa != ga_alabama_isa:
        return

    new_filename = "GAALABAMA" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)


###############################################################################
# Grupo-Antolin Alabama End
###############################################################################

###############################################################################
# Grupo-Antolin TN/KY (EDIFACT) Begin
###############################################################################
def rename_file_gatn(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_edifact(f_path)


    isa = get_isa_edifact(f_path)
    if isa != ga_tn_isa:
        return

    new_filename = "GATN" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)


###############################################################################
# Grupo-Antolin TN/KY End
###############################################################################

###############################################################################
# Grupo-Antolin Silao (EDIFACT) Begin
###############################################################################
def rename_file_gasilao(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_edifact(f_path)


    isa = get_isa_edifact(f_path)
    if isa != ga_silao_isa:
        return

    new_filename = "GASILAO" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)


###############################################################################
# Grupo-Antolin Silao End
###############################################################################

###############################################################################
# Grupo-Antolin St. Clair (EDIFACT) Begin
###############################################################################
def rename_file_gastclair(filename):
    f = filename  # Raw file name
    f_path = os.path.join(staging_dir, filename)  # file name with path

    # Check if in ECGrid format.
    # ECGrid file format: 1027-20201006101520-2e7441af.edi
    if not f.startswith("1027"):
        # Not an ECGrid file
        return

    sep = "-" # File separator
    f_ext = ".edi"  # File extension
    f = os.path.splitext(f)[0]  # Strip extension
    f_list = f.split(sep)  # Make a list from the split    
    f_date = f_list[1]  # The second piece is the date code
    f_idx = f_list[2]  # The third piece is the index
    f_type = get_file_type_edifact(f_path)


    isa = get_isa_edifact(f_path)
    if isa != ga_stclair_isa:
        return

    new_filename = "GASTCLAIR" + sep + f_type + sep + f_date + sep + f_idx + f_ext
    old_filename = os.path.join(staging_dir, filename)
    new_filename = os.path.join(in_dir, new_filename)
    os.rename(old_filename, new_filename)
    print(old_filename + '  >  ' + new_filename)


###############################################################################
# Grupo-Antolin St. Clair End
###############################################################################


if __name__ == '__main__':
    process_staging_dir()
