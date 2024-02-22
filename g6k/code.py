#!/usr/bin/env python  
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
import copy
import logging
import pickle as pickler
from collections import OrderedDict

from fpylll.util import gaussian_heuristic
from fpylll import IntegerMatrix, GSO

from g6k.algorithms.workout import workout
from g6k.siever import Siever
from g6k import SieverParams
from g6k.utils.cli import parse_args, run_all, pop_prefixed_params
from g6k.utils.stats import SieveTreeTracer
from g6k.utils.util import load_svpchallenge_and_randomize, load_matrix_file, db_stats
from g6k.utils.util import sanitize_params_names, print_stats, output_profiles

import six
from six.moves import range
import logging
import random

# Set up logging
dim = 67
logging.basicConfig(filename=f'log_{dim}.txt', filemode = 'a', level=logging.INFO)




def usvp():
    """
    svp challenge slover
    """
    goal_appro_factor = 0.89846
    verbose = True
    trial_n = 575 #实验次数 
    trial = 0
    while(trial < trial_n):
        trial += 1
        #生成一个1-100000之内的随机数
        seed = random.randint(1, 100000)
        print("seed: ", seed, "\n")
        #seed = IntegerMatrix.random(1, "uniform", bits=32)[0, 0] #access fplll's rng. 该随机数每次执行code.py都一样的序列
        A, _ = load_svpchallenge_and_randomize(dim, s=seed, seed=seed)
        params = SieverParams(reserved_n=0, reserved_db_size=0, threads=4, sample_by_sums=True, otf_lift=True, lift_radius=1.8, lift_unitary_only=True, saturation_ratio= 0.5  #0.5
                                , saturation_radius=1.3333333333333333, triplesieve_saturation_radius=1.299, bgj1_improvement_db_ratio=0.65, bgj1_resort_ratio=0.85, bgj1_transaction_bulk_size=0, simhash_codes_basedir=b'/workspaces/lattice/g6k/g6k/spherical_coding', bdgl_improvement_db_ratio=0.8, db_size_base=1.1547005383792515, db_size_factor=3.2, bgj1_bucket_size_expo=0.5, bgj1_bucket_size_factor=3.2, bdgl_bucket_size_factor=0.3, bdgl_blocks=2, bdgl_multi_hash=4, bdgl_min_bucket_size=128, default_sieve='hk3', gauss_crossover=50, dual_mode=False) 
        g6k = Siever(A, params, seed=seed)
        tracer = SieveTreeTracer(g6k, root_label=("svp-challenge", dim), start_clocks=True)
        gh = gaussian_heuristic([g6k.M.get_r(i, i) for i in range(dim)])
        goal_r0 = (goal_appro_factor ** 2) * gh #找到的最短向量，的目标长度的平方
        pump_params = {}
        pump_params["verbose"] = True
        pump_params["down_sieve"] = False #默认为false

        flast = workout(g6k, tracer, kappa=0, blocksize=dim, goal_r0=goal_r0,dim4free_min=0,              # Main parameters
            dim4free_dec=2, start_n=40,                    # Loop control. start_n: Dimension of the first pump (sieving context)
            verbose=verbose, save_prefix=None, pump_params=pump_params)
        tracer.exit()
        logging.info("trial %d, sol %d dim, %d seed, %s" % (trial, dim, seed, A[0])) #sol,打印sv:...
        norm = sum([x * x for x in A[0]])
        logging.info("norm(|sv|) %.1f ,appro_factor %.5f" % (norm ** 0.5, (norm / gh) ** 0.5))
        logging.info("\n")
        if(norm < goal_r0):
            break












if __name__ == "__main__":
    usvp()