########################################################
########################################################
# Author: Lionel Butry (lionel.butry@ruhr-uni-bochum.de)
# Purpose: Reformats the PHILIPS DWI gradient vectors file to the SIEMENS required .dvs-format; 
#          (integrates b-value into vector length)
# Requirements:
#   - PHILIPS gradient vector .txt file ('dti_vector_input.txt')
########################################################
########################################################

# User input
path_input_txt = input("Enter path to PHILIPS .txt file: ")
path_output = input("Enter path to .dvs output file: ")
highest_b = input("Enter highest b-value of PHILIPS gradient scheme: ")
add_comment = input("Do you want to add a comment to the .dvs header? (y/n): ").lower().strip() == "y"
if add_comment:
    comment_dvs = input("Enter comment: ")

# Import modules
from math import sqrt
import numpy as np

# Read the PHILIPS gradient scheme
with open(path_input_txt, 'r') as file:
    next(file) # ignore 1st line
    lines = file.readlines()

# Define dummy variables
output_lines = []
b_phil = []
list_mag_siemens = []
list_mag_philips = []

# Iterate through all lines to reformat gradient scheme
for i, line in enumerate(lines):
    # get variables from lines
    values = line.split()
    x_philips, y_philips, z_philips, b_philips = float(values[0]), float(values[1]), float(values[2]), float(values[3])

    # calculate scaling-factor (magnitude of vec which corresponds to specific b-value)
    magnitude_philips = sqrt(x_philips**2 + y_philips**2 + z_philips**2)
    scalefactor = sqrt(b_philips / highest_b * magnitude_philips**2) # b_ist = b_ui^2 * Betrag_ist^2 / Betrag_max^2 | scalefactor = Betrag_ist

    # transform xyz with scalefactor
    x = x_philips * scalefactor
    y = y_philips * scalefactor
    z = z_philips * scalefactor

    # reformat for SIEMENS .dvs 
    formatted_vector = f'Vector[{i}] = ( {x:.4f}, {y:.4f}, {z:.4f} )'
    output_lines.append(formatted_vector)

# Save the gradient scheme as a .dvs file & add header
with open(path_output, 'w') as file:
    file.write(f"[directions={len(lines)}]\n")
    file.write("Normalisation = none\n")
    file.write("CoordinateSystem = xyz\n")
    if comment_dvs:
        file.write(f"Comment = {comment_dvs}\n")
    file.write('\n'.join(output_lines))

print("The SIEMENS gradient vector file (.dvs) is stored in:", path_output)
print("Please validate the .dvs file manually.")
