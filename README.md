# GrocerEase Chatbot Repo

Chatbot to accelerate the process of online grocery shopping.

## Overview

-  The application runs using **Streamlit**.
-  The chatbot is based on the [Robby-chatbot](https://github.com/yvann-hub/Robby-chatbot) repository.
-  **Faiss** is used for the vectorDB.

## Data

-  The primary data source is the [Grocery Store Dataset](https://github.com/marcusklasson/GroceryStoreDataset#grocery-store-dataset).
-  The dataset has been processed into a file named `postprocessed data`.
-  Use the `preprocessing.py` script for details on data processing.
-  Each grocery item is delineated with a `;` (semicolon) delimiter.
-  This dataset version excludes images.
