#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 10:39:31 2023

@author: calkinsh
"""


import pandas
from kf_utils.dataservice.patch import send_patches


sequencing_experiments_to_update = pandas.read_csv(
    "/Users/calkinsh/Documents/Github/kf_ingests/project_hope/seq_exp_strat_updates.csv"
)


patches = sequencing_experiments_to_update.set_index("kf_id").to_dict(orient="index")


host = "https://kf-api-dataservice.kidsfirstdrc.org"

send_patches(host, patches)
