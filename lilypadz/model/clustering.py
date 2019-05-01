import numpy as np
import pandas as pd
import plotly.graph_objs as go
from typing import List
from flask import jsonify
from plotly.offline import plot
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from lilypadz.model.data_processor import get_toad_processed_hop


def get_all_clustering_result(n_clusters: int,
                              names: List[str],
                              variable: List[str]):
    """Generate a 3D plot that contains just the dots for K means result.

    :return: A plotly object hat has been converted to HTML format string.
    """
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

    # Get desired toad data.
    toads_hop = [
        get_toad_processed_hop(name=name) for name in names
    ]

    # Get all data.
    all_data = [
        [f"{data_name} {data.sight}"] +
        list(data.kinematic[kinematic_variables].mean(axis="index")) +
        list(data.force_plate[fp_variables].mean(axis="index"))
        for one_toad_hop in toads_hop
        for data_name, data in one_toad_hop.items()
    ]

    data = pd.DataFrame(
        index=[data[0] for data in all_data],
        data=[data[1:] for data in all_data]
    ).dropna(axis="index")

    # Get kMeans analyze result and unpack it.
    k_means = KMeans(n_clusters=n_clusters)
    reduced_data = PCA(n_components=3).fit_transform(data)
    k_means_index = k_means.fit_predict(reduced_data)

    # Get hop names.
    labels = data.index.values

    # Separate x, y, z coordinates from the reduced data set.
    x_value = reduced_data[:, 0]
    y_value = reduced_data[:, 1]
    z_value = reduced_data[:, 2]

    # Create plot for each cluster so the color will differ among clusters.
    data = [
        go.Scatter3d(
            x=x_value[np.where(group_number == k_means_index)],
            y=y_value[np.where(group_number == k_means_index)],
            z=z_value[np.where(group_number == k_means_index)],
            text=labels[np.where(group_number == k_means_index)],
            mode="markers",
            name=f"Cluster {group_number + 1}",
            hoverinfo="text",
            marker=dict(
                size=12,
                line=dict(width=1)
            )
        )
        for group_number in np.unique(k_means_index)
    ]

    # Set the layout of the plot, mainly set the background color to grey.
    layout = go.Layout(
        height=500,
        hovermode="closest",
        title="K-Means Two Dimensional Scatter Plot",
        scene=dict(
            xaxis=dict(
                title="PC1",
                showline=False,
                showbackground=True,
                backgroundcolor="rgb(230,230,230)"),
            yaxis=dict(
                title="PC2",
                showline=False,
                showbackground=True,
                backgroundcolor="rgb(230,230,230)"),
            zaxis=dict(
                title="PC3",
                showline=False,
                showbackground=True,
                backgroundcolor="rgb(230,230,230)"),
        )
    )

    table = pd.DataFrame(data={
        "Cluster #": [index + 1 for index in k_means_index],
        "Document": labels,
        "X-Coordinate": reduced_data[:, 0],
        "Y-Coordinate": reduced_data[:, 1],
        "Z-Coordinate": reduced_data[:, 2]
    }).to_html(
        index=False,
        classes="table table-striped table-bordered text-center"
    )

    # Return the plotly figure and table.
    return jsonify(
        table=table,
        plot=plot(
            go.Figure(data=data, layout=layout),
            show_link=False,
            output_type="div",
            include_plotlyjs=False
        )
    )


def get_one_clustering_result(n_clusters: int,
                              name: str,
                              variable: List[str]):
    """Generate a 3D plot that contains just the dots for K means result.

    :return: A plotly object hat has been converted to HTML format string.
    """
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

    # Get all data.
    all_data = [
        [f"{data_name} {data.sight}"] +
        list(data.kinematic[kinematic_variables].mean(axis="index")) +
        list(data.force_plate[fp_variables].mean(axis="index"))
        for data_name, data in get_toad_processed_hop(name=name).items()
    ]

    data = pd.DataFrame(
        index=[data[0] for data in all_data],
        data=[data[1:] for data in all_data]
    ).dropna(axis="index")

    # Get kMeans analyze result and unpack it.
    k_means = KMeans(n_clusters=n_clusters)
    reduced_data = PCA(n_components=3).fit_transform(data.dropna)
    k_means_index = k_means.fit_predict(reduced_data)

    # Get hop names.
    labels = data.index.values

    # Separate x, y, z coordinates from the reduced data set.
    x_value = reduced_data[:, 0]
    y_value = reduced_data[:, 1]
    z_value = reduced_data[:, 2]

    # Create plot for each cluster so the color will differ among clusters.
    data = [
        go.Scatter3d(
            x=x_value[np.where(group_number == k_means_index)],
            y=y_value[np.where(group_number == k_means_index)],
            z=z_value[np.where(group_number == k_means_index)],
            text=labels[np.where(group_number == k_means_index)],
            mode="markers",
            name=f"Cluster {group_number + 1}",
            hoverinfo="text",
            marker=dict(
                size=12,
                line=dict(width=1)
            )
        )
        for group_number in np.unique(k_means_index)
    ]

    # Set the layout of the plot, mainly set the background color to grey.
    layout = go.Layout(
        height=500,
        hovermode="closest",
        title="K-Means Two Dimensional Scatter Plot",
        scene=dict(
            xaxis=dict(
                title="PC1",
                showline=False,
                showbackground=True,
                backgroundcolor="rgb(230,230,230)"),
            yaxis=dict(
                title="PC2",
                showline=False,
                showbackground=True,
                backgroundcolor="rgb(230,230,230)"),
            zaxis=dict(
                title="PC3",
                showline=False,
                showbackground=True,
                backgroundcolor="rgb(230,230,230)"),
        )
    )

    table = pd.DataFrame(data={
        "Cluster #": [index + 1 for index in k_means_index],
        "Document": labels,
        "X-Coordinate": reduced_data[:, 0],
        "Y-Coordinate": reduced_data[:, 1],
        "Z-Coordinate": reduced_data[:, 2]
    }).to_html(
        index=False,
        classes="table table-striped table-bordered text-center"
    )

    # Return the plotly figure and table.
    return jsonify(
        table=table,
        plot=plot(
            go.Figure(data=data, layout=layout),
            show_link=False,
            output_type="div",
            include_plotlyjs=False
        )
    )
