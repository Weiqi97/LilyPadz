"""This file helps reading in the data."""

import pandas as pd
from typing import NamedTuple


class HopData(NamedTuple):
    """Data structure of one hop of a specific toad."""

    xyz: pd.DataFrame
    force: pd.DataFrame
    time: float


def get_one_hop(name: str, hop: int) -> HopData:
    """Get data for one hop of a specific toad.

    :param name: The toad of interest.
    :param hop: The hop number of interest.
    :return: Desired hop data contains xyz data, force data and a time value.
    """
    # Read in the xyz data.
    xyz_frame = pd.read_csv(f"../data/{name}/{hop}/xyz.csv")

    # Read in the force plate data.
    force_frame = pd.read_csv(f"../data/{name}/{hop}/force.csv")

    # Read in the time data and pick the corresponding time.
    time_frame = pd.read_csv(f"../data/{name}/time.csv", index_col="Hop")
    time = time_frame.at[hop, "First Touch"]

    # Pack all information and return the NamedTuple.
    return HopData(xyz=xyz_frame, force=force_frame, time=time)
