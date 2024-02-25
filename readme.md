# 安装必要的包

## fplll

sudo apt update
sudo apt install aptitude
sudo aptitude install fplll-tools

查看是否安装成功：
conda list

## NTL

教程：https://libntl.org/doc/tour-unix.html
   % gunzip ntl-xxx.tar.gz
   % tar xf ntl-xxx.tar   # Extract all files from archive.tar.
   % cd ntl-xxx/src
   % ./configure 
   % make
   % make check
   % sudo make install


## progressive BKZ library

https://www2.nict.go.jp/security/pbkzcode/install.html
unzip unzip pbkzlib-202205.zip -d pbkzlib-202205

特别注意，

### 

Please ensure that you have already installed the following libraries. GCC, NTL, boost, GMP, GSL, and MPFR.
sudo apt-get install libboost-all-dev  # 对于Ubuntu/Debian
sudo apt-get install libgmp-dev
sudo apt-get install libgsl-dev
sudo apt-get install libmpfr-dev

###

chmod +x install_files.sh  授予脚本可执行权限
./install_files.sh


/usr/bin/g++ -fdiagnostics-color=always -g /workspaces/lattice/pbkzlib-202205/1code.cpp -o /workspaces/lattice/pbkzlib-202205/1code -I. -I../boost_1_75_0 -lgmp -lmpfr -lgsl -lntl -fopenmp
./code1



## g6k

千万不要！！git clone https://github.com/fplll/g6k.git 从源代码来编译。
当你在一个 Git 仓库中克隆另一个仓库时，克隆的仓库会成为一个独立的 Git 仓库，它有自己的历史记录和提交。这就是为什么你无法将 g6k 文件夹提交到你的原始仓库的原因。

如果你想要将 g6k 的代码作为你的原始仓库的一部分进行版本控制，copy一下就行。



1. python -m pip install virtualenv

2. 如果你的系统包管理器中没有较新版本的 MPFR，你可以尝试手动下载和安装较新版本的 MPFR。
sudo apt-get update
sudo apt-get install libmpfr-dev

3.  
./bootstrap.sh
source ./activate （deactivate

4. 
python code1.py  (不用直接点击run


other qs：
1. 不能debug。调整编译器为./fpylll-env/bin/python
2. python文件pylint报错，但能编译。https://blog.csdn.net/zj010206/article/details/92806700




### g6k 用法

            seed = IntegerMatrix.random(1, "uniform", bits=32)[0, 0] #access fplll's rng. 生成一个随机数


```python
# class siever 
from fpylll import IntegerMatrix, GSO
from g6k import Siever

#从integerMatrix生成一个siever对象
A = IntegerMatrix.random(50, "qary", k=25, bits=10)
siever = Siever(A, seed=0x1337) #A is a matGSO object or an integerMatrix.若是integerMatrix，在siever中会自动转换为matGSO，float_type由matrix的A.nrows决定

#从matGSO生成一个siever对象
_ = Siever(GSO.Mat(A)) #error: Siever requires UinvT enabled
M = GSO.Mat(A, U=IntegerMatrix.identity(50), UinvT=IntegerMatrix.identity(50))
siever = Siever(M)


# siever.params
siever.params 
siever.params = siever.params.new(reserved_n=10) # create a new copy of the parameters with reserved_n set to 10
siever.params.attr1 = 10 #报错


# siever.update_gso. 
siever.update_gso(0, 50) #Update the Gram-Schmidt vectors (from the left bound 0 up to the right bound 50
# siever.M.update_gso(0, 50) !禁止这么做！


#初始化sieving context and lifting context
siever.initialize_local(0, 5, 10) #ll, l, r
siever.ll  
siever.l
siever.r
siever.n # r-l, sieving dimension
siever()
len(siever)
db = list(siever.itervalues()) #all entries in the database (in the order determined by the compressed database). We get coordinates wrt the basis B


# property
siever.max_sieving_dim #You can simply change the ``MAX_SIEVING_DIM`` macro in siever.h and then recompile.
siever.full_n #Full dimension of the lattice.
len(siever) #the number of vectors in the (compressed) database.



#SieverParams class
known_attributes = [
        # C++
        "reserved_n",
        "reserved_db_size",
        "threads",
        "sample_by_sums",
        "otf_lift",
        "lift_radius",
        "lift_unitary_only",
        "saturation_ratio",
        "saturation_radius",
        "triplesieve_saturation_radius",
        "bgj1_improvement_db_ratio",
        "bgj1_resort_ratio",
        "bgj1_transaction_bulk_size",
        "simhash_codes_basedir",
        "bdgl_improvement_db_ratio",
        # Python
        "db_size_base",
        "db_size_factor",
        "bgj1_bucket_size_expo",
        "bgj1_bucket_size_factor",
        "bdgl_bucket_size_factor",
        "bdgl_blocks",
        "bdgl_multi_hash",
        "bdgl_min_bucket_size",
        "default_sieve",
        "gauss_crossover",
        "dual_mode"
    ]

from g6k import SieverParams
_ = SieverParams() 
print(_.get("attr1")) #若attr1存在，返回其值；否则返回None
print(_.get("attr1", 42)) #若attr1存在，返回其值；否则返回42
_.pop("attr1") #和get类似，但是会删除attr1
_.attr1  #若attr1存在，返回其值；否则返回报错
_.attr1 = 42 #设置attr1的值
_['attr'] #支持中括号访问
_['attr'] = 42 #支持中括号赋值
_.dict() #返回所有值
_.dict(True)  #只返回和默认结果不同的值

```



```python
# svp challenge
python ./svp_challenge.py --help 
python ./svp_challenge.py 70  #lower bound is 70
python ./svp_challenge.py 70 --show-defaults #显示默认参数

#以下参数可以在svp_challenge.py中修改
load_matrix=None
verbose = True
challenge_seed = 0
workout__dim4free_dec=3

```


to do：
* SieverParams中各个参数的含义
* workout可以进一步优化吗
* summer的pro-pnj-bkz算法, g6k的GPU版本
* 更好的服务器？



 比原先更短的向量（different seed) means, 长度更短，而非appro_factor更小。
 INFO:root:trial 1, sol 67 dim, 70193 seed, (403, 272, -267, 419, -144, 74, -493, 250, 178, -423, 42, 224, -182, 246, 143, 64, 362, 237, 134, 35, -34, -57, -317, 25, 317, 293, 112, -177, -125, -36, 599, -214, -395, -163, 158, -176, 93, -262, 12, -299, 301, -102, -194, -166, 145, -119, 112, -199, -111, 168, 51, 354, -305, 55, -151, -350, 382, 318, 67, 61, 140, -163, 172, 56, -69, -149, -13)
INFO:root:norm(|sv|) 1894.6 ,appro_factor 0.89803
INFO:root:








