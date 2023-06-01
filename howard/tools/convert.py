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



def convert(args) -> None:

    log.info("Start")

    config = args.config

    params = {}

    vcfdata_obj = Variants(None, args.input, args.output, config, params)

    params = vcfdata_obj.get_param()

    # Explode Infos
    if args.export_infos:
        params["explode_infos"] = args.export_infos_prefix
        params["export_extra_infos"] = True
    else:
        config["access"] = "RO"

    vcfdata_obj.set_param(params)
    vcfdata_obj.set_config(config)

    # Create VCF object
    if args.input:
        vcfdata_obj = Variants(None, args.input, args.output, config=config, param=params)

        # Load data from input file
        vcfdata_obj.load_data()

        # Load data from input file
        vcfdata_obj.explode_infos()

        # Output
        vcfdata_obj.export_output()

        # Close connexion
        vcfdata_obj.close_connexion()

    log.info("End")



