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



def query(args:argparse) -> None:
    """
    This Python function loads and queries data from a VCF file based on user input and exports the
    results.
    
    :param args: args is an object that contains the arguments passed to the function. It is likely a
    Namespace object created by parsing command line arguments using argparse
    :type args: argparse
    """

    log.info("Start")

    config = args.config

    param = {}

    vcfdata_obj = Variants(None, args.input, args.output, config, param)

    params = vcfdata_obj.get_param()

    # Explode Infos
    if args.explode_infos:
        params["explode_infos"] = True
    else:
        config["access"] = "RO"

    vcfdata_obj.set_param(params)
    vcfdata_obj.set_config(config)

    # Load
    if args.input:
        vcfdata_obj.load_data()

    # Query
    if args.query or param.get("query", None):
        log.info("Querying...")
        if args.query:
            query = args.query
        print(vcfdata_obj.get_query_to_df(query))

    # Output Query
    if args.output:
        log.info("Exporting Querying...")
        vcfdata_obj.export_output(query=query, export_header=True)


    log.info("End")



