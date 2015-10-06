#! /usr/bin/env python3


from .util.io import *


import os
import sys
import re


root = './'
if len(sys.argv) >= 2:
	root = sys.argv[1]

get_allhist_tdx_day_source(root)

