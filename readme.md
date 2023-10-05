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

