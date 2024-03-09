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

from g6k.algorithms.workout import workout,workout_modified
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
import time






def usvp():
    """
    svp challenge slover
    """
    dim = 84
    goal_appro_factor = 0.922170     #避免goal_appro_factor达到goal、norm未达到，就在workout阶段终止的情况，所以这里设置很小的值
    goal_norm = 2158**2  #目标长度控制终止程序
    pump_n = 15  #(dim - 40)//2+1+3
    test = False
    control_by_norm = True
    logging.basicConfig(filename=f'pump_n/log_{dim}_pump_{pump_n}.txt', filemode = 'a', level=logging.INFO)


    verbose = True
    trial = 0
    trial_n = 100 #实验次数,python trial_expect.py确定
    if test:
        trial_n = 1


    while(trial < trial_n):
        ##########参数设置###
        trial += 1
        #生成一个1-100000之内的随机数
        seed = random.randint(1, 100000)
        if test:
            seed = 0 
        print("seed: ", seed, "\n")
        #seed = IntegerMatrix.random(1, "uniform", bits=32)[0, 0] #access fplll's rng. 该随机数每次执行code.py都一样的序列
        A, _ = load_svpchallenge_and_randomize(dim, s=seed, seed=seed)
        params = SieverParams(reserved_n=0, reserved_db_size=0, threads=4, sample_by_sums=True, otf_lift=True, lift_radius=1.8, lift_unitary_only=True, saturation_ratio= 0.5, saturation_radius=1.3333333333333333, triplesieve_saturation_radius=1.299, bgj1_improvement_db_ratio=0.65, bgj1_resort_ratio=0.85, bgj1_transaction_bulk_size=0, simhash_codes_basedir=b'/workspaces/lattice/g6k/g6k/spherical_coding', bdgl_improvement_db_ratio=0.8, db_size_base=1.1547005383792515, db_size_factor=3.2, bgj1_bucket_size_expo=0.5, bgj1_bucket_size_factor=3.2, bdgl_bucket_size_factor=0.3, bdgl_blocks=2, bdgl_multi_hash=4, bdgl_min_bucket_size=128, default_sieve='hk3', gauss_crossover=50, dual_mode=False) 
        g6k = Siever(A, params, seed=seed)
        tracer = SieveTreeTracer(g6k, root_label=("svp-challenge", dim), start_clocks=True)
        det = g6k.M.get_log_det(0, -1)  # 2*log(det)
        gh = gaussian_heuristic([g6k.M.get_r(i, i) for i in range(dim)])
        if control_by_norm: 
            goal_r0 = goal_norm
        else:   #control by appro_factor
            goal_r0 = (goal_appro_factor ** 2) * gh #找到的最短向量，的目标长度的平方
        pump_params = {}
        pump_params["verbose"] = True
        pump_params["down_sieve"] = False #默认为false

        ##########主程序###
        # 获取开始的CPU时间和墙壁时间
        start_cpu_time = time.process_time()
        start_wall_time = time.time()

        flast = workout_modified(g6k, tracer, kappa=0, blocksize=dim, goal_r0=goal_r0,dim4free_min=0, pump_n=pump_n,  logfile = f'logging_dim_{dim}_pump_{pump_n}.txt',         # Main parameters
            dim4free_dec=2, start_n=40,                    # Loop control. start_n: Dimension of the first pump (sieving context)
            verbose=verbose, save_prefix=None, pump_params=pump_params)
        tracer.exit()
        # 获取结束的CPU时间和墙壁时间
        end_cpu_time = time.process_time()
        end_wall_time = time.time()

        # 计算运行的CPU时间和墙壁时间
        cpu_time = end_cpu_time - start_cpu_time
        wall_time = end_wall_time - start_wall_time



        ##########输出结果###
        logging.info("trial %d, pump_n %d, sol %d dim, %d seed, %s" % (trial, pump_n, dim, seed, A[0])) #sol,打印sv:...
        norm = sum([x * x for x in A[0]])
        logging.info("norm(|sv|) %.1f, appro_factor %.5f, 2*log(det) %.5f, cpu time %.1f, wall time %.1f" % (norm ** 0.5, (norm / gh) ** 0.5, det, cpu_time, wall_time))
        logging.info("/n")
        if(norm < goal_norm):
            break




if __name__ == "__main__":
    usvp()





#############################################
