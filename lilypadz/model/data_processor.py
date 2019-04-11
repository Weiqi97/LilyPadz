import math
import pandas as pd
from lilypadz.helper.constant import TOAD_HOP
from lilypadz.model.data_reader import get_all_hop


def align_data_for_each_hop():
    """Align kinematic data, force plate data and time """

    all_hop = get_all_hop()

    for toad, hops in TOAD_HOP.items():
        for hop in hops:
            hop_kinematic = all_hop[toad][hop].angle
            hop_fp = all_hop[toad][hop].force
            hop_time = all_hop[toad][hop].time
            # find corresponding starting points in kinematic and FP data files (NOTE: JUST DOING LANDING FOR NOW!!!!)
            firsttouch_hop = hop_time * .001

            # kinematic data
            kinematic_start_row = math.ceil(firsttouch_hop / .002)

            # remove the rows that is before the first touch
            new_kinematic_data = hop_kinematic[-kinematic_start_row:]

            # reset the index
            new_kinematic_data = new_kinematic_data.reset_index(drop=True)

            # select every 5 rows in data to make it aligned within 0.01s
            new_kinematic_data = new_kinematic_data.iloc[::5, 1:].reset_index(
                drop=True)

            # get number of rows
            nrow_kinematic = new_kinematic_data.shape[0]

            # fp data
            # fp starts at the first touch, assume the first row starts the same as the first touch time

            # select every 5 rows in data to make it aligned within 0.01s
            new_fp_data = hop_fp.iloc[::2, :3]
            # align with kinematic data
            new_fp_data = new_fp_data[:nrow_kinematic]
            # assign columns
            new_fp_data.columns = ['fore-aft', 'lateral', 'normal']
            # reset index
            new_fp_data = new_fp_data.reset_index(drop=True)

            # concatenate two data
            frog_final_data = pd.concat([new_kinematic_data, new_fp_data],
                                        axis=1, ignore_index=True)
            # drop NA
            frog_final_data = frog_final_data.dropna()
            # reset index
            frog_final_data = frog_final_data.reset_index(drop=True)
            # assign columns
            frog_final_data.columns = ['Elbow_Flex_Ext', 'Humeral_Pro_Ret',
                                       'Humeral_Dep_Ele', 'fore-aft',
                                       'lateral', 'normal']

            frog_final_data.to_csv(f"../data/{toad}/{hop}/frog_data.csv")