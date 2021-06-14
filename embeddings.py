"""
utils for working with embeddings
"""

import umap
import pacmap
import pandas as pd
import numpy as np

import plotly.express as px


def run_umap(embeddings, labels):
    """
    Runs umap on an array of vectors
        and returns a dataframe with the embeddings and class labels.
    """
    umap_model = umap.UMAP(n_components=3)
    umap_comps = umap_model.fit_transform(embeddings)

    return(
        pd.DataFrame({
            "component_1": umap_comps[:, 0],
            "component_2": umap_comps[:, 1],
            "component_3": umap_comps[:, 2],
            "class": labels,
            "row_id": range(len(pacmap_comps)),
        })
    )


def run_pacmap(embeddings, labels,**pacmap_kwargs):
    """
    Runs pacmap algorithm on a vector of embeddings.
    Returns a pandas dataframe with labelled components.
    """
    # get pacmap model
    pacmap_model = pacmap.PaCMAP(
        n_dims=3,
        n_neighbors=None,
        MN_ratio=0.5,
        FP_ratio=2.0)
    if pacmap_kwargs:
        pacmap_model = pacmap.PaCMAP(n_dims=3, **pacmap_kwargs) 

    # create components
    pacmap_comps = pacmap_model.fit_transform(embeddings, init="pca")

    # return labelled components
    return(
        pd.DataFrame({
            "component_1": pacmap_comps[:, 0],
            "component_2": pacmap_comps[:, 1],
            "component_3": pacmap_comps[:, 2],
            "class": labels,
            "row_id": range(len(pacmap_comps)),
        })
    )


def vis_components(
    components_df,
    xcol="component_1",
    ycol="component_2",
    zcol="component_3",
    colour_col="class",
    height=780,
    width=1366):
    """
    Plots a component dataframe in an interactive 3d plotly plot.
    Returns the plotly figure.
    """
    fig = px.scatter_3d(
        components_df,
        x=xcol,
        y=ycol,
        z=zcol,
        color=colour_col)

    fig.update_traces(
        marker=dict(size=3),
        selector=dict(mode="markers"))

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=height, width=width
    )

    return(fig)
