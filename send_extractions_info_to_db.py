# -*- coding: utf-8 -*-
# Send the extractions' path, number of sw under TFSet/train, the date, comments about labeling and the original
# labeled pack to the dbserver in the table table_extractions
#
# Use as followed:
# python send_extractions_info_to_db.py path_to_extraction_folder specie projectId classQuantity side comments original_package

import os
import sys
import mysql.connector
import fnmatch
import time

path = sys.argv[1]
species = sys.argv[2]
projectId = sys.argv[3]
classQuantity = sys.argv[4]
side = sys.argv[5]
comments = sys.argv[6]
package = sys.argv[7]

count_sw = len(fnmatch.filter(os.listdir(path + "/TFSet/train"), '*.tif'))
path = path.split('/mnt/psnas/ps/Extractions/')[1]
dateDatabase = time.strftime('%Y-%m-%d %H:%M:%S')

print(path)
print("{} slidinng windows train folder".format(count_sw))

mydb = mysql.connector.connect(
     host="host",
     user="username",
     passwd="pwd")
mycursor = mydb.cursor()
sql_select_species_id_from_name = "SELECT id from dev.species WHERE name='{}'".format(species)
mycursor.execute(sql_select_species_id_from_name)
species_id = mycursor.fetchall()
if len(species_id) == 0:
     print("Wrong Species name entered")
id_specie_in_species_table = species_id[0][0]

sql_select_project_id_from_name = "SELECT customer_id from dev.customer WHERE customer_name='{}'".format(projectId)
print(sql_select_project_id_from_name)
mycursor.execute(sql_select_project_id_from_name)
project_id = mycursor.fetchall()
if len(project_id) == 0:
     print("Wrong Customer/ProjectId name entered")
id_project_in_customers_table = project_id[0][0]
extractionID = str(path).split('_')[0]


sql = "INSERT INTO dev.table_extractions (Date, SpeciesID, CustomerProjectID, ExtractionNumber, classes, side, name, sw, comments, package) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = (dateDatabase, id_specie_in_species_table, id_project_in_customers_table, extractionID, classQuantity, side, path, count_sw, comments, package)
mycursor.execute(sql, val)
mydb.commit()

print("Complete!")





