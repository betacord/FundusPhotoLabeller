# Fundus Photo Labeller

A simple GUI in **Jupyter Notebook** tool that allows you to assign labels to fundus photographs (and not only) such as:
- side (left/right),
- quality (good/acceptable/bad),
- centering (disc/fovea/no),
- optic artifacts (no/non-obscuring/obscuring),
- field of view (fov).

To create the tool, [Python](https://www.python.org) version [3.10](https://www.python.org/downloads/release/python-31011/) was used to ensure compatibility with the [Google Colab](https://colab.research.google.com) platform.

## How to run?
There are 2 ways to use the tool: local and remote on the Google Colab platform.

### Local run
Local run is the simplest way to work with Fundus Image Labeller. A method useful for people who do not use Google services and prefer to control the launch on the side of their own computer. To do this, follow the list of steps below.
1. Install the [Python](https://www.python.org) interpreter in version [3.10](https://www.python.org/downloads/release/python-31011/).
2. Create a directory for a project (the name doesn't matter).
3. [Install](https://jupyter.org/install) the Jupyter Notebook and run the server.
4. Copy the *app_local.ipynb* and *utils.py* to the main directory of your project.
5. Open the *app_local.ipynb* notebook on the Jupyter server side.
6. Follow the instructions inside the notebook.

### Running on the side of the Google Colab service
Starting on the side of the [Google Colab](https://colab.research.google.com) service is useful when the size of the photo collection is large and you don't have enough space on your local computer. To do this, follow the list of steps below.
1. Go to [Google Drive](https://drive.google.com) service and create a new empty folder there (name doesn't matter).
2. Upload the *app_colab.ipynb* and *utils.py* files.
3. Open the *app_colab.ipynb* notebook.
4. Follow the instructions inside the notebook.
