+++
title =  "Configuring Rocky Linux 8 for Quantitative Analysis in Julia"
date = "2022-05-24T00:30:32.169Z"
description = "Configure Rocky Linux 8 for Julia development and quantitative analysis."
author = "Justin Napolitano"
categories = ['Julia','Tutorials', 'Legal Research', 'Data Wrangling']
tags = ['julia', 'dataframes', 'SCOTUS','data-wrangling' ]
images = ['featured-julia.png']
series = ['Quantitative Analysis in Julia']
+++

## Install Jupyter

Start with installing jupyter.  It will serve as our server for development.  

### Install Dependencies

```bash
sudo dnf install gcc python3-devel kernel-headers-$(uname -r)
```

### Install Jupyter Via Pip

```bash
pip3 install --user jupyter
```

## Install Julia

We will be installing from the official binaries.  

Make a directory in user profile.  i simply ran `mkdir julia` in the `home` folder.  The `cd` to `julia`.  

When in the folder run 

### Wget 

```bash
wget https://julialang-s3.julialang.org/bin/linux/x64/1.7/julia-1.7.2-linux-x86_64.tar.gz

```

### Unpack
Then unpack 

``` bash
tar zxvf julia-1.7.2-linux-x86_64.tar.gz
```


### Add to Path

In my case I added the following to my shell profile.  

```bash

export PATH="$PATH:/home/jnapolitano/julia/julia-1.7.2/bin/"

```

##  Downloading the QuantEcon Project

I will be working through the QuantEcon textbook provided at [https://julia.quantecon.org/](https://julia.quantecon.org/).

### Clone the repository 

``` bash

git clone https://github.com/quantecon/lecture-julia.notebooks

```

## Activate the Project.

Run a julia repl by typing `julia` into your terminal... if you added it to the path.  Otherwise navigate to the bin and activate julia.  



### Install the Dependencies

Next run the following commands from the Julia REPL.  



````julia

using Pkg

Pkg.activate(".")

Pkg.instantiate()

```

IT will take some time to download and extract all of the packages give it time.  


