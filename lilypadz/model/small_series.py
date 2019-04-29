import colorlover
from typing import List
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.tools import make_subplots
from lilypadz.model.data_processor import get_toad_processed_hop


def get_small_series_for_one_toad(name: str, variable: List[str]):
    """Get small series plot for one specific toad.

    :param name: The name of the desired toad.
    :param variable: Variable of interest.
    :return: Two plots, the kinematic and force plate small series.
    """
    # Get the processed hop data.
    all_processed_hop = get_toad_processed_hop(name=name)

    # Set the global color to use.
    color = colorlover.scales["12"]["qual"]["Paired"]

    # Get the force plate column names.
    fp_variables = list(
        {"Fore-Aft", "Lateral", "Normal"}.intersection(variable)
    )

    # Get the kinematic column names.
    kinematic_variables = list(
        {"Elbow flexion/extension",
         "Humeral protraction/retraction",
         "Humeral depression/elevation"}.intersection(variable)
    )

    # Create the subplot for force plate plot.
    small_series = make_subplots(
        cols=1,
        shared_xaxes=True,
        rows=len(variable),
        subplot_titles=variable
    )

    # Iterate over processed data for each hop.
    for index, (toad_hop, hop_data) in enumerate(all_processed_hop.items()):
        # Iterate over each column within the hop data.
        for col_index, col_name in enumerate(fp_variables):
            # Append trace to the subplot.
            small_series.append_trace(
                col=1, row=col_index + 1,
                trace=go.Scatter(
                    x=hop_data.force_plate.index,
                    y=hop_data.force_plate[col_name],
                    mode="lines",
                    name=toad_hop,
                    legendgroup=toad_hop,
                    line=dict(color=color[index % len(color)]),
                    # Show the legend only for first trace.
                    showlegend=True if col_index == 0 else False
                )
            )

        # Iterate over each column within the hop data.
        for col_index, col_name in enumerate(kinematic_variables):
            # Append trace to the subplot.
            small_series.append_trace(
                col=1, row=col_index + 4,
                trace=go.Scatter(
                    x=hop_data.kinematic.index,
                    y=hop_data.kinematic[col_name],
                    mode='lines',
                    name=toad_hop,
                    showlegend=False,
                    legendgroup=toad_hop,
                    line=dict(color=color[index % len(color)])
                )
            )

    # Adjust the settings of the plot.
    small_series["layout"].update(
        height=850, margin={"l": 40, "r": 40, "b": 30, "t": 40}
    )

    return plot(
        small_series,
        show_link=False,
        output_type="div",
        include_plotlyjs=False
    )
