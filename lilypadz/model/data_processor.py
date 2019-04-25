import pandas as pd
from typing import NamedTuple, Dict
from lilypadz.helper.constant import TOAD_HOP
from lilypadz.model.data_reader import get_one_hop


class ProcessedHop(NamedTuple):
    """Data structure of one processed hop of a specific toad."""

    kinematic: pd.DataFrame
    force_plate: pd.DataFrame
    onset_time: float
    first_touch: float
    recovery_time: float

def get_one_processed_hop(name: str, hop: int) -> ProcessedHop:
    """Get processed data for one hop of a specific toad.

    :param name: The toad of interest.
    :param hop: The hop number of interest.
    :return: Desired kinematic and force plate data.
    """
    # Get the hop data from the desired toad.
    hop_data = get_one_hop(name=name, hop=hop)

    # Extract the time data
    onset = hop_data.time["Onset"]
    first_touch = hop_data.time["First Touch"]
    recovery = hop_data.time["Recovery"]

    # Extract the kinematic data.
    hop_kinematic_data = hop_data.angle

    # Process the data.
    processed_kinematic = hop_kinematic_data.iloc[:, 1:].dropna()
    processed_kinematic.columns = [
        "Elbow flexion/extension",
        "Humeral protraction/retraction",
        "Humeral depression/elevation"
    ]
    processed_kinematic = processed_kinematic.iloc[::-1]
    processed_kinematic = processed_kinematic.reset_index(drop=True)

    # Extract the force plate data.
    hop_fp_data = hop_data.force

    # Process the data.
    processed_fp_data = hop_fp_data.iloc[:, :3]
    #Aprocessed_fp_data = processed_fp_data.div(processed_fp_data.loc[0])
    processed_fp_data.columns = ["Fore-Aft", "Lateral", "Normal"]
    processed_fp_data = processed_fp_data.reset_index(drop=True)

    return ProcessedHop(
        kinematic=processed_kinematic,
        force_plate=processed_fp_data,
        onset_time=onset,
        first_touch=first_touch,
        recovery_time=recovery
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
