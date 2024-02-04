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

    A, _ = load_svpchallenge_and_randomize(n, s=challenge_seed, seed=seed)
   A, _ = load_matrix_file(load_matrix)


dsds