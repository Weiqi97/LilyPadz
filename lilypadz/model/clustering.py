from typing import List
from lilypadz.model.data_processor import get_all_processed_hop
import pandas as pd 

def get_df_for_clustering():
    """Get clustering plot.

    :param: NA.
    :return: clustering plot.
    """
    All_processed_hop = get_all_processed_hop()
    cluster_df = pd.DataFrame(columns=["Mean elbow flex/ext",
    "Mean humeral protr/retr", "Mean humeral depr/ele",
    "Mean fore-Aft", "Mean lateral", "Mean normal", "Sight"])
    for toad_name, all_hop in All_processed_hop.items:
        for toad_hop, hop_data in all_hop.items:
            kinematic_data = hop_data.kinematic
            mean_elbow_flex_ext = kinematic_data["Elbow flexion/extension"].mean()
            mean_humeral_protr_retr = kinematic_data["Humeral protraction/retraction"].mean()
            mean_humeral_depr_ele = kinematic_data["Humeral depression/elevation"].mean()
            fp_data = hop_data.force_plate
            mean_fore_aft = fp_data["Fore-Aft"].mean()
            mean_lateral = fp_data["Lateral"].mean()
            mean_normal = fp_data["Normal"].mean()
            sight = hop_data.sight
            cluster_df.append({"Mean elbow flex/ext": mean_elbow_flex_ext,
                               "Mean humeral protr/retr": mean_humeral_protr_retr,
                               "Mean humeral depr/ele": mean_humeral_depr_ele,
                               "Mean fore-Aft": mean_fore_aft,
                               "Mean lateral": mean_lateral,
                               "Mean normal": mean_normal,
                               "Sight": sight})
    return cluster_df
            




