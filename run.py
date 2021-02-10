# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This program merge different NEB tables for different apertures of the same target and files to
generate the new report with the best of all
"""
from os import listdir
from os import mkdir
from os.path import isfile, join
from shutil import copy2
from typing import List, Dict

# Parameters needed for the process, the first one will be used for header and footer :
from src.model.check import Check
from src.model.star import Star

SOURCE_PATH: List[str] = [
    '/home/fgh/Astronomia/procesant/procesant/analisis/FINAL',
    '/home/fgh/Astronomia/procesant/procesant/analisis/FINAL/NEB_5',
    '/home/fgh/Astronomia/procesant/procesant/analisis/FINAL/NEB_5_NEW',
    '/home/fgh/Astronomia/procesant/procesant/analisis/FINAL/NEB_11',
    '/home/fgh/Astronomia/procesant/procesant/analisis/FINAL/NEB_13',
    '/home/fgh/Astronomia/procesant/procesant/analisis/FINAL/NEB_15'
]

DESTINATION_PATH: str = 'result'


# Global Variables
TABLE_FILE_END: str = 'NEB-table.txt'
FOLDER_NEB_CHECK_END: str = 'NEBcheck'
PLOT_END: str = '-NEBdepth-plot.png'
END_HEATHER: str = 'Star  from target  PA (deg.)  dmag   RMS(ppt)  NEBdepth(ppt)  NEBdepth/RMS    ' \
                   'Disposition\n'
START_FOOTER: str = '\n'

heather: str = None
footer: str = None
result_file_name: str = None
result_folder_name: str = None
result_base_files_name: str = None

all_information: List[Check] = []

# get all the information:
for path in SOURCE_PATH:
    file: str = None
    directory: str = None
    base_file_name: str = None
    header: str = ''
    footer: str = ''
    stars: Dict[str, Star] = dict()
    header_is_finished: bool = False
    footer_has_start: bool = False
    for f in listdir(path):
        if isfile(join(path, f)) and f.endswith(TABLE_FILE_END):
            base_file_name = f.replace(TABLE_FILE_END, '')
            if not result_base_files_name:
                result_base_files_name = base_file_name
            file = join(path, f)
        elif not isfile(join(path, f)) and f.endswith(FOLDER_NEB_CHECK_END):
            directory = join(path, f)

    if not file or not directory:
        raise Exception('[EXCEPTION] {} not contain any NEB check'.format(path))

    # loop file
    with open(file) as fp:
        for line in fp:
            if not header_is_finished:
                header += line
                if line == END_HEATHER:
                    header_is_finished = True
            elif footer_has_start:
                footer += line
            else:
                if line == START_FOOTER:
                    footer += line
                    footer_has_start = True
                else:
                    cleaned_line = [x.strip() for x in line.split()]
                    stars[cleaned_line[0]] = Star(
                        name=cleaned_line[0],
                        neb_depth_vs_rms=float(cleaned_line[6]) if cleaned_line[6] != 'N/A' else 0.0,
                        line=line
                    )

    all_information.append(Check(
        table_path=file,
        directory_path=directory,
        base_file_name=base_file_name,
        header=header,
        footer=footer,
        stars=stars
    ))

# Generate Result
# ##################################################################################################
not_cleared: List[str] = []
likely_cleared: List[str] = []
cleared: List[str] = []
total: int = 0


# create result directory
directory_pah: str = join(DESTINATION_PATH, '{}{}'.format(result_base_files_name, FOLDER_NEB_CHECK_END))
try:
    if not isfile(directory_pah):
        mkdir(directory_pah)
except OSError:
    print ('[Exception] creating directory {}'.format(directory_pah))

output_table: str = ''
base_check: Check = all_information.pop(0)

output_table += base_check.header

star_name: str
for star_name in base_check.stars:
    final_star: Star = base_check.stars[star_name]
    final_check: Check = base_check

    check: Check
    for check in all_information:
        if check.stars[star_name].neb_depth_vs_rms > final_star.neb_depth_vs_rms:
            final_star = check.stars[star_name]
            final_check = check

    total += 1
    if final_star.neb_depth_vs_rms < 3.0:
        not_cleared.append(final_star.name)
    elif final_star.neb_depth_vs_rms < 5.0:
        likely_cleared.append(final_star.name)
    else:
        cleared.append(final_star.name)

    # add line in table:
    output_table += final_star.line
    # copy image to result
    copy2(join(final_check.directory_path, '{}{}{}'.format(final_check.base_file_name, final_star.name, PLOT_END)),
          join(directory_pah, '{}{}{}'.format(result_base_files_name, final_star.name, PLOT_END)))

output_table += base_check.footer

# Write file
text_file = open(join(DESTINATION_PATH, '{}{}'.format(result_base_files_name, TABLE_FILE_END)), "w")
text_file.write(output_table)
text_file.close()


print('From {}/{} was cleared'.format(len(cleared), total))
print('{} not cleared'.format(not_cleared))
print('{} Likely cleared'.format(likely_cleared))









