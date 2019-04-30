import pandas as pd
from sklearn import preprocessing
from typing import NamedTuple, Dict
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
    global increasing
    hop_data = get_one_hop(name=name, hop=hop)

    # Get sighted or blinded for the input toad.
    sightedness = hop_data.all_hop_info[
        (hop_data.all_hop_info["ID"] == name) &
        (hop_data.all_hop_info["Hop Number"] == hop) &
        (hop_data.all_hop_info["Hop Phase"] == "Landing")]["Sight"]

    sight = sightedness.iloc[0] if not sightedness.empty else "Unknown"

    # Extract and round the time data.
    time = hop_data.time
    onset = round(time.loc[time['Hop'] == hop]['Onset'].iloc[0])
    recovery = round(time.loc[time['Hop'] == hop]['Recovery'].iloc[0])
    first_touch = round(time.loc[time['Hop'] == hop]['First Touch'].iloc[0])

    # Extract the kinematic data.
    hop_kinematic_data = hop_data.angle

    # Calculate the start row for kinematic data.
    kinematic_start = abs((first_touch - onset) / 2)

    # Calculate the end row for kinematic data.
    kinematic_end = abs((recovery - onset) / 2)

    # Select data from landing to recovery.
    hop_kinematic_data = \
        hop_kinematic_data.loc[kinematic_start - 1: kinematic_end - 1]

    # Process the data.
    processed_kinematic = hop_kinematic_data.iloc[:, 1:].dropna(axis="index")

    # Normalize each column in kinematic data
    scalar = preprocessing.StandardScaler()
    if processed_kinematic.shape[0] != 0:
        scaled_kinematic_data = scalar.fit_transform(processed_kinematic)
        processed_kinematic = pd.DataFrame(scaled_kinematic_data)

    processed_kinematic.columns = ["Elbow flexion/extension",
                                   "Humeral protraction/retraction",
                                   "Humeral depression/elevation"]
    processed_kinematic = processed_kinematic.reset_index(drop=True)

    if len(processed_kinematic.index) > 60:
        processed_kinematic = processed_kinematic.iloc[:61]

    # Extract the force plate data.
    hop_fp_data = hop_data.force

    # Find where normal force (col 3) data begins to increase
    normal_df = hop_fp_data.iloc[:, 2]

    # Get the size of the DataFrame.
    index = 1
    fp_start = 0
    increasing = False
    frame_size = len(hop_fp_data.index)

    while index < frame_size:
        if (normal_df.iloc[index] - normal_df.iloc[index - 1]) > 0:
            # if it increases for one check if it increases for next 10.
            total_increase = 0
            if index + 10 < frame_size:
                for i in range(1, 10):
                    total_increase = \
                        total_increase + \
                        (normal_df.iloc[index + i] -
                         normal_df.iloc[index + i - 1])
                    if total_increase > 1:
                        increasing = True
                    else:
                        increasing = False
                if increasing:
                    fp_start = index
                    # Stop the loop.
                    index = frame_size
            else:
                fp_start = 100
        else:
            fp_start = 100

        index = index + 1

    # Select data from landing to recovery
    hop_fp_data = hop_fp_data.loc[fp_start - 10: fp_start + 50]

    # Process the data.
    processed_fp_data = hop_fp_data.iloc[:, :3]  # only want 1st 3 columns

    # Normalize each column in fp data
    scalar = preprocessing.StandardScaler()
    scaled_fp_data = scalar.fit_transform(processed_fp_data)
    processed_fp_data = pd.DataFrame(
        scaled_fp_data,
        columns=["Fore-Aft", "Lateral", "Normal"]
    )
    processed_fp_data = processed_fp_data.reset_index(drop=True)

    return ProcessedHop(
        kinematic=processed_kinematic,
        force_plate=processed_fp_data,
        sight=sight
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
    """Get all processed hop data from all toads."""
    return {
        toad: get_toad_processed_hop(name=toad)
        for toad in TOAD_HOP.keys()
    }
