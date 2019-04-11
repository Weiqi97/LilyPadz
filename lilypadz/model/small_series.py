import numpy as np
import pandas as pd
from plotly import tools
from plotly.offline import plot
from lilypadz.helper.constant import TOAD_HOP


def get_small_series():
    """Draw visualization"""
    """Draw visualization"""
    # create arrays for each variables

    EFE_array = []
    HPR_array = []
    HDE_array = []
    FA_array = []
    LA_array = []
    NO_array = []

    # only choose atlas for now
    toad = 'Atlas'

    # store all hops and length of each hop into an array
    hop_array = []
    length = []
    for hop in TOAD_HOP['Atlas']:
        toad_hop = pd.read_csv(f"lilypadz/data/{toad}/{hop}/frog_data.csv")
        if (toad_hop.shape[0] > 20):
            length.append(toad_hop.shape[0])
            hop_array.append(toad_hop)

    # find the minimum length among all hop length
    min_length = min(length)

    # align the hop into same length and store in each variable
    for hop in hop_array:
        EFE_array.append(np.array(hop["Elbow_Flex_Ext"])[:min_length])
        HPR_array.append(np.array(hop["Humeral_Pro_Ret"])[:min_length])
        HDE_array.append(np.array(hop["Humeral_Dep_Ele"])[:min_length])
        FA_array.append(np.array(hop["fore-aft"])[:min_length])
        LA_array.append(np.array(hop["lateral"])[:min_length])
        NO_array.append(np.array(hop["normal"])[:min_length])

    var_array = [np.array(EFE_array), np.array(HPR_array), np.array(HDE_array),
                 np.array(FA_array), np.array(LA_array), np.array(NO_array)]

    # build dataframe for each variables (Krissa, you may want to  change the column name into something easy for the vis label)
    var_df = []
    for var in var_array:
        df = pd.DataFrame(np.column_stack(var),
                          columns=[x for x in range(len(var))])
        var_df.append(df)

    # draw visualization
    fig = tools.make_subplots(rows=6, cols=1, shared_xaxes=True,
                              subplot_titles=(
                                  'Elbow_Flex_Ext', 'Humeral_Pro_Ret',
                                  'Humeral_Dep_Ele', 'fore-aft', 'lateral',
                                  'normal'))
    fig_row = 1
    for df in var_df:
        if (fig_row == 1):
            legend_display = True
        else:
            legend_display = False

        for col in df.columns:
            fig.append_trace(
                {'x': df.index, 'y': df[col], 'type': 'scatter', 'name': col,
                 'legendgroup': col, 'showlegend': legend_display}, fig_row, 1)
        fig_row += 1

    fig['layout'].update(height=820)
    fig['layout']['xaxis'].update(title='time(ms)',
                                  tickmode='linear',
                                  ticks='outside',
                                  tick0=0,
                                  dtick=1,
                                  ticklen=4,
                                  tickwidth=2,
                                  tickcolor='#000'
                                  )

    return plot(
        fig,
        show_link=False,
        output_type="div",
        include_plotlyjs=False
    )
