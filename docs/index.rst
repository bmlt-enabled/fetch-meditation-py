.. Fetch Meditation documentation master file, created by
   sphinx-quickstart on Tue Apr 22 21:47:32 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Fetch Meditation documentation
==============================

A Python package for fetching daily meditation content from various sources.

Installation
------------

.. code-block:: bash

   pip install fetch-meditation

Usage
-----

.. code-block:: python

   from fetch_meditation import Jft, JftLanguage, JftSettings
   
   # Create settings for English JFT
   settings = JftSettings(language=JftLanguage.English)
   
   # Get the appropriate JFT fetcher
   jft = Jft.get_instance(settings)
   
   # Fetch today's meditation
   entry = jft.fetch()
   
   # Print the meditation title and thought
   print(f"Title: {entry.title}")
   print(f"Thought: {entry.thought}")

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

API Reference
-------------

.. toctree::
   :maxdepth: 3

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

