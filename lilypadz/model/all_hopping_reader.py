"""This file helps to read the all hopping information file."""

import math
import colorlover
import pandas as pd
import plotly.graph_objs as go
from flask import jsonify
from itertools import chain
from typing import Dict, List
from plotly.offline import plot
from lilypadz.helper.constant import useful_parameters

# Type hinting for the toad data structure.
toad_data = Dict[str, pd.DataFrame]


class AllHoppingReader:
    """Class to read and display the data related to all hopping info."""

    def __init__(self, option: dict):
        """Save the input option from flask request."""
        self._option = option

    @property
    def all_data(self) -> pd.DataFrame:
        """Read in the excel file, return it as a pandas DataFrame."""
        # Read in the data from the excel file.
        data = pd.read_csv("data/data.csv")

        # Set the toad name to be the frame index.
        data = data.set_index("ID")

        # Filter the phase selected.
        data = data[data["Hop Phase"] == self._option["phase_selection"]]

        # Filter the toad/toads required.
        data = data.loc[self.selected_toad]

        # First take the useful data and filter user's selection.
        data = data[useful_parameters]
        data = data[self._option["variable_selection"].split("!")]

        # Road all numerical values to 2 digits after decimal.
        data = data.round(2)

        # Calculate the numerical id for toads.
        numerical_id = list(chain.from_iterable([
            [index for _ in range(len(data.loc[toad]))]
            for index, toad in enumerate(set(data.index))
        ]))

        # Append numerical id to the existing pandas DataFrame.
        data["Numerical ID"] = numerical_id

        return data

    @property
    def selected_toad(self) -> List[str]:
        """Return the user selected toad."""
        return self._option["toad_selection"].split("!")

    def toad_data_dict(self) -> toad_data:
        """Get data as a dictionary in format of {toad: data}."""
        return {
            toad: self.all_data.loc[toad]
            for toad in set(self.all_data.index)
        }

    def blind_toad_data(self) -> toad_data:
        """Get data as a dictionary in format of {blind_toad: data}."""
        return {
            f"{toad} Blind": data[data["Sight"] == "Blind"]
            for toad, data in self.toad_data_dict().items()
        }

    def sighted_toad_data(self) -> toad_data:
        """Get data as a dictionary in format of {sighted_toad: data}."""
        return {
            f"{toad} Sighted": data[data["Sight"] == "Sighted"]
            for toad, data in self.toad_data_dict().items()
        }

    def draw_parallel_coordinate(self):
        """Draw the parallel coordinate graph."""
        # Graph the processed data.
        data = self.all_data

        # Create the dimensions for parallel coordinates.
        dimensions = [
            dict(
                label=column,
                values=data[column],
                range=[
                    math.floor(min(data[column]) * 0.95),
                    math.ceil(max(data[column]) * 1.05)
                ]
            )
            for column in data.columns[:-1]
        ]

        # Find the number of toads selected.
        toad_num = len(self.selected_toad)
        # Pick proper color.
        color = colorlover.scales["7"]["qual"]["Dark2"]
        # Find the color scale list.
        color_scale = [
            [1 * index / (toad_num - 1), color[index]]
            for index in range(toad_num)
        ] if toad_num > 1 else [[0, color[0]]]

        # Create the parallel coordinate.
        parallel_coordinate = [
            go.Parcoords(
                line=dict(
                    color=data["Numerical ID"],
                    colorscale=color_scale
                ),
                dimensions=dimensions
            )
        ]

        layout = go.Layout(height=750)

        # Get the color toad matches.
        color_toad = [
            [color[index], toad]
            for index, toad in enumerate(self.selected_toad)
        ]

        # Return the html div to frontend.
        return jsonify(
            plot=plot(
                go.Figure(data=parallel_coordinate, layout=layout),
                show_link=False,
                output_type="div",
                include_plotlyjs=False
            ),
            color_toad=color_toad
        )
