+++
title =  "Quantitative Julia Problems"
date = "2022-05-24T01:30:32.169Z"
description = "Testing your Julia Configuration with some numerical computing."
author = "Justin Napolitano"
categories = ['Julia','Tutorials', 'Quantitative Analysis']
tags = ['julia', 'dataframes', 'mathematics' ]
images = ['featured-julia.png']
series = ['Quantitative Analysis in Julia']
+++
## Introduction


In my [previous post](https://blog.jnapolitano.io/posts/rocky-linux-8-julia/), I demonstrated how to configure Rocky Linux and RHEL distributions for quantitative analysis. 

In this post, I include a few sample programs to test your installation.  

## How to run the programs

I saved them to a folder within the project directory.

### Activate the Project

```julia

using Pkg
Pkg.activate(".")

#cd("<sub-directory-containing-files>) optional

```


### Run a program 

```Julia

include("path/to/script-name.jl")

```


## Estimate the Value of Pi

Use the Monte Carlo method to estimate the value of pi.  

### Solution

We estimate the area by sampling bivariate uniforms and looking at the fraction that fall into the unit circle.


``` Julia

# Number of iterations
n = 1000000
#counter variable
count = 0
for i in 1:n # for i in the range of 1 to n
    
    global count  # make count global to reference within the loop.  Otherwise the the variable will be understood to be a local within the for loop
    #rand(2) Returns a two element vector.  
    #Can be read as let u be equal to the first index of the vector and let v be equal to the second
    u, v = rand(2)
    
    d = sqrt((u - 0.5)^2 + (v - 0.5)^2)  # distance from middle of square
    if d < 0.5
        count += 1
    end
end

area_estimate = count / n

print(area_estimate * 4)  # dividing by radius**2

```


## Use QuadGk to Aproximate an integral

The trapezoidal rule can be used to aproximate an integral. 


``` Julia

using QuadGK

f(x) = x^8 # The Function

value, accuracy = quadgk(f, 0.0, 1.0) # pass the function, the lower bound and the upper bound

```