#!/usr/bin/env python

import io
import multiprocessing
import os
import re
import subprocess
from tempfile import NamedTemporaryFile
import tempfile
import duckdb
import json
import argparse
import Bio.bgzf as bgzf
import pandas as pd
import vcf
import logging as log
import sys

from howard.objects.variants import Variants
from howard.objects.database import Database
from howard.commons import *
from howard.tools.databases import *



def stats(args:argparse) -> None:
    """
    The stats() function takes in arguments, loads data from an input file, gets statistics on the data,
    and closes the connection.
    
    :param args: args is a parameter that is passed to the function stats(). It is likely an object or a
    dictionary that contains various arguments or parameters that are needed by the function to perform
    its tasks. Some of the arguments that may be included in args are input file path, configuration
    settings, and other parameters that are
    :type args: argparse
    """

    log.info("Start")

    config = args.config

    param = {}

    # Create VCF object
    if args.input:
        vcfdata_obj = Variants(None, args.input, config=config, param=param)

        # Load data from input file
        vcfdata_obj.load_data()

        # Stats
        vcfdata_obj.get_stats()

        # Close connexion
        vcfdata_obj.close_connexion()

    log.info("End")



