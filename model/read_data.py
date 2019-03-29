"""
read_data.py

Creates a dataframe of toad hop data
in order to create visualization of 
comparison of force plate data and kinematic movement data.
"""
import sys
import os
import math
import csv
import pandas as pd
import numpy as np

def create_dataframe():

#if statements to check naming convention to see which data file we are looking at				#ADD LATER

#NAMING CONVENTION
	# FP DATA = EX: Atlas_tn5.csv --> gives frog name _ tn hop #
	# KINEMATIC DATA =  EX: AtlasHop5DLTdv5_data_xyzpts.csv --> gives frog name, Hop, hop #
	# TIMING VARIABLES = 061214_Atlas_Time variables.xlsx --> gives some random #s _frog name _ Time variables

#check if file exists in database 																#ADD LATER
	#if yes: modify
	#if no: save new file to database

#also check to ensure that there are these specific 3 files with same hop #

#for now lets pretend hop number is 5 and we got that from naming convention
	hopNum = 5

#----------Create timing vars data frame-------------------
	#get all data from csv
	timing_data = pd.read_csv("atlas_time.csv")
	kinematic_data = pd.read_csv("try_this.csv")
	fp_data = pd.read_csv("Atlas_tn5.csv", header=None)
#----------------------------------------------------------


#in timing variables, find tn which indicates hop of the files that were input (using hopNum)
	#NOTE: hopNum-1 due to starting at index 0
	firsttouch_hop = timing_data.loc[hopNum-1,'firsttouch']
	firsttouch_hop = firsttouch_hop*.001


#find corresponding starting points in kinematic and FP data files (NOTE: JUST DOING LANDING FOR NOW!!!!)
	
	kinematic_start = firsttouch_hop/.002

	#in order to start with row that can correspond with fp data 
	#(secs (calculate by row*.002 for kinematic data) divisible by .01)
	kinematic_start_secs = kinematic_start * .002
	kinematic_start_secs = kinematic_start_secs * 100
	
	#round up to smallest integer not less than kinematic_start_secs
	kinematic_start_secs = math.ceil(kinematic_start_secs)
	kinematic_start_secs = kinematic_start_secs / 100
	print("seconds now:",kinematic_start_secs)
	
	#calculate new start
	kinematic_start = kinematic_start_secs/.002

	# remove rows that contain ANY NaNs
	kinematic_data = kinematic_data.dropna()

	#NOTE: kinematic_start-2 due to removing header line and then starting at index 0
	#NOTE: ::5 skips 4 rows so that we only get seconds that correspond to FP data (every .01s)
	kinematic_data = kinematic_data.loc[kinematic_start-2::5,['pt1_X','pt1_Y','pt1_Z','pt2_X','pt2_Y','pt2_Z','pt3_X','pt3_Y','pt3_Z','pt4_X','pt4_Y','pt4_Z','pt5_X','pt5_Y','pt5_Z','pt6_X','pt6_Y','pt6_Z']]

	#find how many seconds we are at at the end of this data
	#print(kinematic_data.index[-1] --> being the index of the last row of the dataframe + 2 to make last excel row)
	secs_end = (kinematic_data.index[-1]+2)*.002
	print(secs_end)

	#now lets calculate the end and beginning of fp data based on the previous calculations
	fp_start = kinematic_start_secs/.005
	fp_end = secs_end/.005

	#NOTE: ::2 skips 1 rows so that we only get seconds that correspond to FP data (every .01s)
	fp_data = fp_data.loc[fp_start-2::2] #just gets rows not getting rid of end yet
	fp_data = fp_data.iloc[:, 0:3]
	
	#then ensures we only get the data we want
	fp_data = fp_data.loc[fp_start-2:fp_end] #get rid of end
	
	#RESET THE DATA FRAME INDICES SO THEY MATCH!
	kinematic_data = kinematic_data.reset_index(drop=True)
	print(kinematic_data.head()) 
	print(kinematic_data.tail())

	print("index kin: ",len(kinematic_data.index))

	fp_data = fp_data.reset_index(drop=True)
	print(fp_data.head()) 
	print(fp_data.tail())
	print("index fp: ",len(fp_data.index))

	#concatenate all of these
	frog_final_data = pd.concat([kinematic_data,fp_data], axis=1, ignore_index=True)
	frog_final_data.columns = ['pt1_X','pt1_Y','pt1_Z','pt2_X','pt2_Y','pt2_Z','pt3_X','pt3_Y','pt3_Z','pt4_X','pt4_Y','pt4_Z','pt5_X','pt5_Y','pt5_Z','pt6_X','pt6_Y','pt6_Z','fore-aft','lateral','normal']
	
	# remove rows that contain ANY NaNs
	frog_final_data = frog_final_data.dropna()

	print(frog_final_data.head()) 
	print(frog_final_data.tail())

	#returns final dataframe with all of the necessary data 
	return frog_final_data 

def main():

    create_dataframe()

if __name__ == '__main__':
    main()


