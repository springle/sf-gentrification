""" SF Gentrification Visualization

The data being imported includes the following headers: year, median_rent, housing_units,
                                                        net_new_housing, employment,
                                                        total_wages, CPI
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

#############
# Load Data #
#############

f = open('data.csv', 'r')
reader = csv.reader(f)
headers = next(reader, None);
data = { header: [] for header in headers }
for row in reader:
    for h, v in zip(headers, row):
        data[h].append(v)

################
# Process Data #
################

def filter_trio(x, y, z):
    filtered_x, filtered_y, filtered_z = [], [], []
    for a, b, c in zip(x, y, z):
        if 'NA' not in a and 'NA' not in b and 'NA' not in c:
            filtered_x.append(a)
            filtered_y.append(b)
            filtered_z.append(c)
    return filtered_x, filtered_y, filtered_z

def fill_gaps(years, data_points, cpis):
    filled_years, filled_data_points, filled_cpis = [], [], []
    prev_year, prev_data_point = 0, 0
    for year, data_point, cpi in zip(years, data_points, cpis):
        year = int(year)
        data_point = float(data_point)
        cpi = float(cpi)
        if prev_year:
            while year > prev_year + 1:
                prev_year += 1
                filled_years.append(prev_year)
                filled_data_points.append(prev_data_point)
                filled_cpis.append(0)
        prev_year, prev_data_point = year, data_point
        filled_years.append(year)
        filled_data_points.append(data_point)
        filled_cpis.append(cpi)
    return filled_years, filled_data_points, filled_cpis

def adjust_for_inflation(years, data_points, cpis):
    adjusted_data_points = []
    prev_data_point = 0
    for year, data_point, cpi in zip(years, data_points, cpis):
        if prev_data_point:
            increase = data_point - prev_data_point
            due_to_inflation = prev_data_point * (1 + cpi/100) - prev_data_point
            adjusted_increase = increase - due_to_inflation
            adjusted_data_points.append(prev_data_point + adjusted_increase)
        else:
            adjusted_data_points.append(data_point)
        prev_data_point = data_point
    return adjusted_data_points
                                        

year, median_rent, cpi = filter_trio(data['year'], data['median_rent'], data['CPI'])
filled_year, filled_median_rent, filled_cpi = fill_gaps(year, median_rent, cpi)
adjusted_median_rent = adjust_for_inflation(filled_year, filled_median_rent, filled_cpi)

##################
# Visualize Data #
##################

plt.plot(filled_year, filled_median_rent, label="Unadjusted")
plt.plot(filled_year, adjusted_median_rent, label="Adjusted for Inflation")
plt.xlabel('Year')
plt.ylabel('Average SF Rent in $/month')
plt.title('SF Rent vs. Time')
plt.legend()
plt.show()
