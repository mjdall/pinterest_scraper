# Pinterest Scraper DNN Practice
## Overview
Welcome to my pinterest scraper DNN practice repository.
The idea is pretty vague at the moment, I've written a pinterest scraper to
scrape images from pinterest. Part of the scraper scrapes the recommended pins,
I intend to use these as labels in order to fine-tune a DNN and eventually extract
embeddings from the fine-tuned DNN.

Once I've got embeddings, running umap
will allow me to visualise the image dataset in 3-dimensions, which could be
pretty cool. I know style transfer is possible but I'll need to look into it a
bit more, but I intend to play around with that also.

Finally, I can package this all up as a pipeline that can produce a
3d-visualisation and image search by providing user-queries for pinterest.
For example you could provide "dogs" and "cats" as labels to the pipeline.
We can then scrape 1000+ images per label to quickly run through and fine-tune
a DNN to finally produce embeddings and enable visualisation.

I'm sure I'll think of more functionality once I've got the initial pipeline
setup. Enjoy!

## Pinterest Scraper TODO
* <del>write the pinterest scraper</del>
* <del>use the scraper to collect labelled data</del>
* <del>refactor the data collection notebook into a python class</del>

## DNN Work
* <del>have a look into popular DNN's for image classification</del>
    * effecientnet - seems to be the most popular currently
* <del>figure out how to use a fine-tuned DNN to perform a semantic search</del>
* look into extracting style from images
* experiment with style transfer
* look into semantic style similarity - semantic similarity but on style-based embedding layer
* <del>run umap/pacmap on the image embeddings</del>

## Embedding Visualisation
* <del>render umap translation in 3d via web app</del>
* visual semantic similarity - KNN or some graph-based visualisation
* HDBSCAN applied to images for visualisation?

## Refinements
* Pull a whole lot of labels from pinterest
* Remove colours from images for training

## Web App
* Create shiny application for interacting with the model and the embeddings
