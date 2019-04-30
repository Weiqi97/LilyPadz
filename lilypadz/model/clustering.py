import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA, SparsePCA
from lilypadz.model.data_processor import get_all_processed_hop


def get_data_for_clustering():
    """Find the DataFrame that contains all data from hops for clustering."""
    all_data = [
        [f"{data_name} {data.sight}"] +
        list(data.kinematic.mean(axis="index")) +
        list(data.force_plate.mean(axis="index"))
        for one_toad_hop in get_all_processed_hop().values()
        for data_name, data in one_toad_hop.items()
    ]

    # all_data = [
    #     [f"{data_name} {data.sight}"] +
    #     list(data.kinematic.mean(axis="index")) +
    #     list(data.force_plate.mean(axis="index"))
    #     for data_name, data in get_toad_processed_hop(name="Atlas").items()
    # ]

    return pd.DataFrame(
        index=[data[0] for data in all_data],
        data=[data[1:] for data in all_data]
    )


def get_clustering_result(n_clusters: int):
    """Generate a 2D plot that contains just the dots for K means result.

    :return: A plotly object hat has been converted to HTML format string.
    """
    # Get kMeans analyze result and unpack it.
    data = get_data_for_clustering()
    print(data.shape)
    data = data.dropna(axis="index")
    print(data.shape)
    k_means = KMeans(n_clusters=n_clusters)
    reduced_data = PCA(n_components=2).fit_transform(data)
    print(reduced_data)
    print(reduced_data[:, 0])
    k_means_index = k_means.fit_predict(reduced_data)

    # Get hop names.
    labels = data.index.values

    # Separate x, y coordinates from the reduced data set.
    x_value = reduced_data[:, 0]
    y_value = reduced_data[:, 1]

    # Create plot for each cluster so the color will differ among clusters.
    data = [
        go.Scatter(
            x=x_value[np.where(group_number == k_means_index)],
            y=y_value[np.where(group_number == k_means_index)],
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

    # Set the layout of the plot.
    layout = go.Layout(
        title="K-Means Two Dimensional Scatter Plot",
        xaxis=go.layout.XAxis(title='x-axis', showline=False),
        yaxis=go.layout.YAxis(title='y-axis', showline=False),
        hovermode="closest")

    # Return the plotly figure and table.
    plot(go.Figure(data=data, layout=layout))
