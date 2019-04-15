"""This file helps reading in the data."""

import pandas as pd
from typing import Dict, List, NamedTuple
from lilypadz.helper.constant import TOAD_HOP


class HopData(NamedTuple):
    """Data structure of one hop of a specific toad."""

    xyz: pd.DataFrame
    angle: pd.DataFrame
    force: pd.DataFrame


def get_one_hop(name: str, hop: int) -> HopData:
    """Get data for one hop of a specific toad.

    :param name: The toad of interest.
    :param hop: The hop number of interest.
    :return: Desired hop data contains xyz data, force data and a time value.
    """
    # Read in the xyz data.
    xyz_frame = pd.read_csv(f"lilypadz/data/{name}/{hop}/xyz.csv")

    # Read in the angle data time.
    angle_frame = pd.read_csv(f"lilypadz/data/{name}/{hop}/angle.csv")

    # Read in the force plate data.
    force_frame = pd.read_csv(f"lilypadz/data/{name}/{hop}/force.csv")

    # Pack all information and return the NamedTuple.
    return HopData(xyz=xyz_frame, angle=angle_frame, force=force_frame)


def get_toad_hop(name: str, hops: List[int]) -> Dict[str, HopData]:
    """Get all hop data from one specific toad.

    :param name: The toad of interest.
    :param hops: A list of existing hop numbers.
    :return: A dictionary where the key is hop number and the item is data.
    """
    return {hop: get_one_hop(name=name, hop=hop) for hop in hops}


def get_all_hop() -> Dict[str, Dict[str, HopData]]:
    """Get all hop data from all toads."""
    return {
        toad: get_toad_hop(name=toad, hops=hops)
        for toad, hops in TOAD_HOP.items()
    }
