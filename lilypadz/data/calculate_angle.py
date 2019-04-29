"""Run the file manually to find all angle data."""

import math
import numpy as np
import pandas as pd
from lilypadz.helper.constant import TOAD_HOP


def convert_xyz_to_kinematic(xyz_data: pd.DataFrame) -> pd.DataFrame:
    """Calculate three kinematic variables from the XYZ data.

    :param xyz_data: xyz data of a hop of a specific toad.
    :return: a pandas DataFrame that holds the kinematic variables.
    """

    # Create a data frame for kinematic data.
    angle_data = pd.DataFrame(
        columns=['Elbow_Flex_Ext', 'Humeral_Pro_Ret', 'Humeral_Dep_Ele']
    )

    # Iterate over rows to find the angle data for each row.
    for index, row in xyz_data.iterrows():
        # If the row contains any empty data, make the entire angle row empty.
        if row.isnull().values.any():
            elbow_flex_ext = np.NaN
            humeral_pro_ret = np.NaN
            humeral_dep_ele = np.NaN

        # Do the proper calculations.
        else:
            # Calculate Elbow Flexion/Extraction
            seg_a = math.sqrt(
                (row['pt4_X'] - row['pt5_X']) ** 2 +
                (row['pt4_Y'] - row['pt5_Y']) ** 2 +
                (row['pt4_Z'] - row['pt5_Z']) ** 2
            )
            seg_b = math.sqrt(
                (row['pt5_X'] - row['pt6_X']) ** 2 +
                (row['pt5_Y'] - row['pt6_Y']) ** 2 +
                (row['pt5_Z'] - row['pt6_Z']) ** 2
            )
            seg_c = math.sqrt(
                (row['pt4_X'] - row['pt6_X']) ** 2 +
                (row['pt4_Y'] - row['pt6_Y']) ** 2 +
                (row['pt4_Z'] - row['pt6_Z']) ** 2
            )
            try:
                elbow_flex_ext = math.degrees(
                    math.acos(
                        (seg_c ** 2 - seg_a ** 2 - seg_b ** 2) /
                        (-2 * seg_a * seg_b)
                    )
                )
            except ZeroDivisionError:
                elbow_flex_ext = 0

            # Calculate Humeral Protraction/Retraction
            pt5_x2 = row['pt5_X'] + (row['pt2_X'] - row['pt4_X'])
            pt5_y2 = row['pt5_Y'] + (row['pt2_Y'] - row['pt4_Y'])
            pt5_z2 = row['pt5_Z'] + (row['pt2_Z'] - row['pt4_Z'])
            seg_d = math.sqrt(
                (row['pt1_X'] - row['pt2_X']) ** 2 +
                (row['pt1_Y'] - row['pt2_Y']) ** 2 +
                (row['pt1_Z'] - row['pt2_Z']) ** 2
            )
            seg_e = math.sqrt(
                (row['pt2_X'] - pt5_x2) ** 2 +
                (row['pt2_Y'] - pt5_y2) ** 2 +
                (row['pt2_Z'] - pt5_z2) ** 2
            )
            seg_f = math.sqrt(
                (pt5_x2 - row['pt1_X']) ** 2 +
                (pt5_y2 - row['pt1_Y']) ** 2 +
                (pt5_z2 - row['pt1_Z']) ** 2
            )
            try:
                humeral_pro_ret = 180 - math.degrees(
                    math.acos(
                        (seg_f ** 2 - seg_d ** 2 - seg_e ** 2) /
                        (-2 * seg_d * seg_e)
                    )
                )
            except ZeroDivisionError:
                humeral_pro_ret = 0

            # Calculate Humeral Depression/Elevation
            pt5_x3 = row['pt5_X'] + (row['pt3_X'] - row['pt4_X'])
            pt5_y3 = row['pt5_Y'] + (row['pt3_Y'] - row['pt4_Y'])
            pt5_z3 = row['pt5_Z'] + (row['pt3_Z'] - row['pt4_Z'])
            seg_g = math.sqrt(
                (row['pt3_X'] - row['pt2_X']) ** 2 +
                (row['pt3_Y'] - row['pt2_Y']) ** 2 +
                (row['pt3_Z'] - row['pt2_Z']) ** 2
            )
            seg_h = math.sqrt(
                (row['pt3_X'] - pt5_x3) ** 2 +
                (row['pt3_Y'] - pt5_y3) ** 2 +
                (row['pt3_Z'] - pt5_z3) ** 2
            )
            seg_i = math.sqrt(
                (pt5_x3 - row['pt2_X']) ** 2 +
                (pt5_y3 - row['pt2_Y']) ** 2 +
                (pt5_z3 - row['pt2_Z']) ** 2
            )
            try:
                humeral_dep_ele = 180 - math.degrees(
                    math.acos(
                        (seg_i ** 2 - seg_h ** 2 - seg_g ** 2) /
                        (-2 * seg_g * seg_h)
                    )
                )
            except ZeroDivisionError:
                humeral_dep_ele = 0

        angle_data = angle_data.append(
            {'Elbow_Flex_Ext': elbow_flex_ext,
             'Humeral_Pro_Ret': humeral_pro_ret,
             'Humeral_Dep_Ele': humeral_dep_ele},
            ignore_index=True
        )

    return angle_data


def save_all_kinematic_data():
    for name, hops in TOAD_HOP.items():
        for hop in hops:
            xyz_data = pd.read_csv(f"{name}/{hop}/xyz.csv")
            angle_data = convert_xyz_to_kinematic(xyz_data=xyz_data)
            angle_data.to_csv(f"{name}/{hop}/angle.csv")


save_all_kinematic_data()
