## 安装必要软件

- cmake
- 编译器
- 自动化构建工具
- python

### cmake
```shell script
apt-get install cmake
```

### 编译器
gnu/linux上，gnu编译器
```shell script
apt-get install g++ gcc gfortran
```

### 自动化构建工具

- make工具
- ninja [https://github.com/ninja-build/ninja/releases](https://github.com/ninja-build/ninja/releases)
```shell script
# 下载后，移动到/usr/local/bin目录下，重启shell即可使用
```
- python

```shell script
apt-get install python3-dev

pip install --user pip pipenv --upgrade
pipenv install --python python3
# pinenv shell，进入命令行中，exit退出当前环境

# 使用隔离环境中直接执行命令
pipenv run
```
- conda
```shell script
# https://repo.anaconda.com/miniconda/下找对应平台下的安装包的shell文件，如
curl -Ls https://repo.anaconda.com/miniconda/Miniconda3-4.7.12.1-Linux-x86_64.sh > miniconda.sh
bash miniconda.sh -b -p "$HOME"/Deps/conda
touch "$HOME"/Deps/conda/conda-meta/pinned
# 设置环境变量
export PATH=$HOME/Deps/conda/bin${PATH:+:$PATH}
conda config --set show_channel_urls True
conda config --set changeps1 no
conda update --all
conda clean -tipy
# 安装conda之后，可以执行如下命令安装python模块
conda create -n cmake-cookbook python=3
conda activate cmake-cookbook
conda install --file requirements.txt
# 执行conda deactivate退出conda环境
```

### 依赖软件

- blas和lapack
```shell script
apt-get install libatlas-base-dev liblapack-dev liblapacke-dev
```

- openmpi
```shell script
apt-get install openmpi-bin libopenmpi-dev
```

- 线性代数模板库eigen(http://eigen.tuxfamily.org/index.php?title=Main_Page)
```shell script
$ eigen_version="3.3.9"
$ mkdir -p eigen
$ curl -Ls http://bitbucket.org/eigen/eigen/get/${eigen_version}.tar.gz | tar -xz -C eigen --strip-components=1
$ cd eigen
$ cmake -H. -Bbuild_eigen -DCMAKE_INSTALL_PREFIX="$HOME/Deps/eigen" &> /dev/null
$ cmake --build build_eigen -- install &> /dev/null
# 将eigen安装到$HOME/Deps/Eigen目录
```

- boost库
```shell script
apt-get install libboost-filesystem-dev libboost-python-dev libboost-test-dev
```

- 交叉编译器
```shell script
apt-get install gcc-mingw-w64 g++-mingw-w64 gfortran-mingw-w64
```

- zeroMQ,pkg-config,uuid,doxygen
```shell script
apt-get install pkg-config libzmq3-dev doxygen graphviz-dev uuid-dev
```

- conda的构建和部署
```shell script
# 想要使用conda打包，需要使用miniconda和conda构建和部署工具，安装其构建和部署工具，请运行以下命令
conda install --yes --quiet conda-build anaconda-client jinja2 setuptools
conda clean -tipsy
conda info -a
```

- 测试环境
    - travis(https://travis-ci.org)用于gnu/linux和maxos，其配置文件travis.yml
    - appveyor(https://www.appveyor.com)用于windows，其配置文件.appveyor.yml
    - circleci(https://circleci.com)用于附加的gnu/linux测试和商业编译器，其配置文件.circleci/config.yml
    
