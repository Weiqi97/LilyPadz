import colorlover
from typing import List
import plotly.graph_objs as go
from flask import jsonify
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
    fp_column_name = list(
        {"Fore-Aft", "Lateral", "Normal"}.intersection(variable)
    )

    # Create the subplot for force plate plot.
    fp_plot = make_subplots(
        rows=len(fp_column_name), cols=1,
        shared_xaxes=True, subplot_titles=fp_column_name
    )

    # Iterate over processed data for each hop.
    for index, (toad_hop, hop_data) in enumerate(all_processed_hop.items()):
        # Iterate over each column within the hop data.
        for col_index, col_name in enumerate(fp_column_name):
            # Append trace to the subplot.
            fp_plot.append_trace(
                col=1, row=col_index + 1,
                trace=go.Scatter(
                    x=hop_data.force_plate.index,
                    y=hop_data.force_plate[col_name],
                    mode='lines',
                    name=toad_hop,
                    legendgroup=toad_hop,
                    line=dict(color=color[index % len(color)]),
                    # Show the legend only for first trace.
                    showlegend=True if col_index == 0 else False
                )
            )

    # Adjust the settings of the plot.
    fp_plot["layout"].update(
        height=400, margin={"l": 40, "r": 40, "b": 30, "t": 40}
    )

    # Get the kinematic column names.
    kinematic_column_name = list({
        "Elbow flexion/extension",
        "Humeral protraction/retraction",
        "Humeral depression/elevation"
    }.intersection(variable))

    # Create the subplot for force plate plot.
    kinematic_plot = make_subplots(
        rows=len(kinematic_column_name), cols=1,
        shared_xaxes=True, subplot_titles=kinematic_column_name
    )

    # Iterate over processed data for each hop.
    for index, (toad_hop, hop_data) in enumerate(all_processed_hop.items()):
        # Iterate over each column within the hop data.
        for col_index, col_name in enumerate(kinematic_column_name):
            # Append trace to the subplot.
            kinematic_plot.append_trace(
                col=1, row=col_index + 1,
                trace=go.Scatter(
                    x=hop_data.kinematic.index,
                    y=hop_data.kinematic[col_name],
                    mode='lines',
                    name=toad_hop,
                    legendgroup=toad_hop,
                    line=dict(color=color[index % len(color)]),
                    # Show the legend only for first trace.
                    showlegend=True if col_index == 0 else False
                )
            )

    # Adjust the settings of the plot.
    kinematic_plot["layout"].update(
        height=400, margin={'l': 40, 'r': 40, 'b': 30, 't': 40}
    )

    return jsonify(
        fp_plot=plot(
            fp_plot,
            show_link=False,
            output_type="div",
            include_plotlyjs=False
        ),
        kinematic_plot=plot(
            kinematic_plot,
            show_link=False,
            output_type="div",
            include_plotlyjs=False
        )
    )
