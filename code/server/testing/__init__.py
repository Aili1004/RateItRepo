#!/usr/bin/env python

"""The __init__.py file makes Python treat directories containing it as modules.
So for example, this allows us to call the home module from home.py (which itself is contained in the pages folder) as such:

	pages.home.home
	

Furthermore, this is the first file to be loaded in a module, so you can use it to execute code that you want to run each time a module is loaded, or specify the submodules to be exported.
"""