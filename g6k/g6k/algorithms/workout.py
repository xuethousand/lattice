# -*- coding: utf-8 -*-
####
#
#   Copyright (C) 2018-2021 Team G6K
#
#   This file is part of G6K. G6K is free software:
#   you can redistribute it and/or modify it under the terms of the
#   GNU General Public License as published by the Free Software Foundation,
#   either version 2 of the License, or (at your option) any later version.
#
#   G6K is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with G6K. If not, see <http://www.gnu.org/licenses/>.
#
####


"""

"""
from __future__ import absolute_import
from __future__ import print_function
import sys
from .pump import pump
from fpylll.util import gaussian_heuristic
import time
from six.moves import range
import logging


def workout(g6k, tracer, kappa, blocksize, dim4free_min=0,              # Main parameters
            dim4free_dec=1, start_n=40, goal_r0=0.,                     # Loop control
            verbose=False, save_prefix=None, pump_params=None           # Misc
            ): 
    """
    :param g6k: The g6k object to work with
    :param tracer: A tracer for g6k
    :param kappa: beginning of the block
    :param blocksize: dimension of the block
    :param dim4free_min: Minimal number of dimension for free ``dimension for free'' [Ducas,
        Eurcrypt 2018] (may stop before reaching that if goal_r0)
    :param dim4free_dec: By how much do we decreaseee dim4free at each iteration
    :param start_n: Dimension of the first pump (sieving context)
    :param goal_r0: an extra hook to always insert at position kappa if this goal length can be met
        by a lift.  Quit when this is reached.
    :param verbose: Print workout steps (with timing and quality) information on the standard
        output.  Enforce verbosity of pump as well.
    :param save_prefix: If not None, save intermediate basis at a file-name with this prefix.
        Allows to resume computation.
    :param pump_params: Parameters to forward to the pump.

    """
    if pump_params is None:
        pump_params = {}

    f_start = max(blocksize - start_n, 0, dim4free_min)
    fs = list(range(dim4free_min, f_start+1, dim4free_dec))[::-1]

    if goal_r0:
        #fs += 9999*[dim4free_min] #若goal_r0不为0，则一直循环最后一个pump
        fs += 3*[dim4free_min] 

    gh = gaussian_heuristic([g6k.M.get_r(i, i) for i in range(kappa, kappa+blocksize)])
    runtimestart = time.time()

    if "verbose" not in pump_params:
        pump_params["verbose"] = verbose #若pump_params中没有verbose，默认为false

    with tracer.context(("workout", "beta:%d f:%d" % (blocksize, dim4free_min))):
        for f in fs:
            flast = f
            timestart = time.time()

            sys.stdout.flush()
            pump(g6k, tracer, kappa, blocksize, f, goal_r0=goal_r0, **pump_params)

            if verbose:
                gh2 = gaussian_heuristic([g6k.M.get_r(i, i) for i in range(kappa+f, kappa+blocksize)])
                quality = (gh * (blocksize - f)) / (gh2 * blocksize) #有啥用？
                print("T:%10.5fs, TT:%10.5fs, quality:%10.5f (r0/gh)**2:%10.5f" %
                      (time.time() - timestart,
                       time.time() - runtimestart, quality, g6k.M.get_r(kappa, kappa) / gh))

            if g6k.M.get_r(kappa, kappa) < goal_r0:
                break

            if save_prefix is not None: #保存g6k.M.B,实时格基
                fn = open("%s_%d_%d.mat" % (save_prefix.rstrip(), g6k.M.d - f, g6k.M.d), "w")
                fn.write(str(g6k.M.B))
                fn.close()

    return flast

#####################

def workout_modified(g6k, tracer, kappa, blocksize, dim4free_min=0, pump_n=1,  logfile = 'logging_pump.txt' ,         # Main parameters
            dim4free_dec=1, start_n=40, goal_r0=0.,                     # Loop control
            verbose=False, save_prefix=None, pump_params=None           # Misc
            ): 
    """
    :param pump_n: 运行多少个pump
    :param logfile: 将中间数据保存在logfile文件中
    """
    if pump_params is None:
        pump_params = {}

    f_start = max(blocksize - start_n, 0, dim4free_min)
    fs = list(range(dim4free_min, f_start+1, dim4free_dec))[::-1]

    # 如果fs的长度大于pump_n，去掉末尾的数
    if len(fs) > pump_n:
        fs = fs[:pump_n]
    # 如果fs的长度小于pump_n， 在末尾增加0
    elif len(fs) < pump_n:
        fs.extend([0] * (pump_n - len(fs)))
        

    gh = gaussian_heuristic([g6k.M.get_r(i, i) for i in range(kappa, kappa+blocksize)])
    runtimestart = time.process_time()

    if "verbose" not in pump_params:
        pump_params["verbose"] = verbose #若pump_params中没有verbose，默认为false

    with tracer.context(("workout", "beta:%d f:%d" % (blocksize, dim4free_min))):
        logging.basicConfig(filename=logfile, filemode = 'a', level=logging.INFO)
        _ = 0
        for f in fs:
            _= _+1
            flast = f
            timestart = time.process_time()

            sys.stdout.flush()
            pump(g6k, tracer, kappa, blocksize, f, goal_r0=goal_r0, **pump_params)

            if verbose:
                gh2 = gaussian_heuristic([g6k.M.get_r(i, i) for i in range(kappa+f, kappa+blocksize)])
                quality = (gh * (blocksize - f)) / (gh2 * blocksize) 
                T = time.process_time() - timestart #cpu time
                TT = time.process_time() - runtimestart #cpu time
                appro_factor= (g6k.M.get_r(kappa, kappa) / gh)**(1/2)
                print("T(cpu):%10.5fs, TT(cpu):%10.5fs, r0/gh:%10.5f" %
                      (T,
                       TT, appro_factor))
                logging.info("pump:%d, dim:%d, f:%d, T(单个pump):%10.5fs, TT(截止所有pump):%10.5fs, quality:%10.5f, (r0/gh):%10.5f" % (_,blocksize,f,T,TT,quality, appro_factor))



            if g6k.M.get_r(kappa, kappa) < goal_r0:
                break

            if save_prefix is not None: #保存g6k.M.B,实时格基
                fn = open("%s_%d_%d.mat" % (save_prefix.rstrip(), g6k.M.d - f, g6k.M.d), "w")
                fn.write(str(g6k.M.B))
                fn.close()

    return flast
