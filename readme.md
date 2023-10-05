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
