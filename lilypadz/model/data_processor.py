import pandas as pd
import numpy as np
import math
from typing import NamedTuple, Dict
from sklearn import preprocessing
from lilypadz.helper.constant import TOAD_HOP
from lilypadz.model.data_reader import get_one_hop


class ProcessedHop(NamedTuple):
    """Data structure of one processed hop of a specific toad."""

    kinematic: pd.DataFrame
    force_plate: pd.DataFrame
    sight: str

def get_one_processed_hop(name: str, hop: int) -> ProcessedHop:
    """Get processed data for one hop of a specific toad.

    :param name: The toad of interest.
    :param hop: The hop number of interest.
    :return: Desired kinematic and force plate data.
    """
    

    # Get the hop data from the desired toad.
    hop_data = get_one_hop(name=name, hop=hop)

    # Get sighted or blinded
    all_hop_info = hop_data.all_hop_info
    hop_list = np.array(all_hop_info[all_hop_info['ID'] == name]['Hop Number'])
    if hop in hop_list:
        sightedness = all_hop_info[(all_hop_info['ID'] == name) & 
        (all_hop_info['Hop Number'] == hop) & 
        (all_hop_info['Hop Phase'] == 'Landing')]['Sight']
        sighted = sightedness.iloc[0]
    else:
        sighted = 'unknown'

    # Extract the time data
    time = hop_data.time
    onset = time.loc[time['Hop']==hop]['Onset'].iloc[0]
    first_touch = time.loc[time['Hop']==hop]['First Touch'].iloc[0]
    recovery = time.loc[time['Hop']==hop]['Recovery'].iloc[0]

    # Round the time data 
    first_touch = round(first_touch) 
    recovery = round(recovery) 
    onset = round(onset) 

    # Extract the kinematic data
    hop_kinematic_data = hop_data.angle

    # Calculate the start row for kinematic data
    kinematic_start = first_touch - onset
    kinematic_start = abs(kinematic_start/2)

    # Calculate the end row for kinematic data
    kinematic_end = recovery - onset
    kinematic_end = abs(kinematic_end/2)

    # Select data from landing to recovery
    hop_kinematic_data = hop_kinematic_data.loc[kinematic_start-1:kinematic_end-1] 

    # """
    # #find whether the frog is blinded or sighted (finds the first row to match this criteria)
    # hop_row = all_hopping_data.loc[(all_hopping_data['ID']==frogName) & (all_hopping_data['Hop Number'] == hopNum)].index[0]
    # sighted_blinded = all_hopping_data.loc[hop_row,'Sight']

    # # add attribute to tell whether frog is blind/sighted
    # hop_kinematic_data.sighted = sighted_blinded
    # """

    # Process the data.
    processed_kinematic = hop_kinematic_data.iloc[:, 1:].dropna() #all rows, all columns from 2nd column & remove NaNs

    # normalize each column in kinematic data
    scaler = preprocessing.StandardScaler()
    if(processed_kinematic.shape[0] != 0):
        scaled_kinematic_data = scaler.fit_transform(processed_kinematic)
        processed_kinematic = pd.DataFrame(scaled_kinematic_data)
        
    processed_kinematic.columns=["Elbow flexion/extension",
    "Humeral protraction/retraction", "Humeral depression/elevation"]
    processed_kinematic = processed_kinematic.reset_index(drop=True)


    # Extract the force plate data.
    hop_fp_data = hop_data.force

    # Find where normal force (col 3) data begins to increase
    normal_df = hop_fp_data.iloc[:,2] # third column of data frame (normal force)
    # Get the size of the dataframe 
    nrows_fp = len(hop_fp_data.index)
    index = 1
    while (index < nrows_fp):
        if ((normal_df.iloc[index] - normal_df.iloc[index-1]) > 0):
            #if we found it increases for one check if it increases for next 10!
            totalIncrease = 0
            if (index + 10 < nrows_fp):
                for i in range(1,10):
                    totalIncrease = totalIncrease + (normal_df.iloc[index+i] - normal_df.iloc[index+i-1])
                    if (totalIncrease > 1):
                        increasing = True
                    else:
                        increasing = False
                if (increasing == True):
                    #WE FOUND WHERE FIRSTOUCH OF FP DATA IS (since this is where normal force starts going up)
                    fp_start = index
                    print("index",index)
                    index = nrows_fp #TO STOP THIS LOOP
            else:
                fp_start = 100
        else:
            fp_start = 100
                
        index = index + 1

    # # Select data from landing to recovery
    hop_fp_data = hop_fp_data.loc[fp_start-100:fp_start+100]

    # Process the data.
    processed_fp_data = hop_fp_data.iloc[:, :3] #only want 1st 3 columns

    # normalize each column in fp data
    scaler = preprocessing.StandardScaler()
    scaled_fp_data = scaler.fit_transform(processed_fp_data)
    processed_fp_data = pd.DataFrame(scaled_fp_data, columns=["Fore-Aft", "Lateral", "Normal"])
    processed_fp_data = processed_fp_data.reset_index(drop=True)

    return ProcessedHop(
        kinematic=processed_kinematic,
        force_plate=processed_fp_data,
        sight=sighted
    )

def get_toad_processed_hop(name: str) -> Dict[str, ProcessedHop]:
    """Get all processed hop data from one specific toad.

    :param name: The toad of interest.
    :return: A dictionary where the key is hop number and the item is data.
    """
    return {
        f"{name} hop {hop}": get_one_processed_hop(name=name, hop=hop)
        for hop in TOAD_HOP[name]
    }


def get_all_processed_hop() -> Dict[str, Dict[str, ProcessedHop]]:
    """Get all processed hop data from all toads.

    :param name: NA
    :return：A dictionary of a dictionary 
    """
    return {
        toad: get_toad_processed_hop(name=toad)
        for toad in TOAD_HOP
    }
