+++
title =  "Spearman Rank in Standard Julia"
date = "2022-05-30T20:20:32.169Z"
description = "Numerical Recipes in Julia.  Spearman Rank Correlation adapted to nearly standard Julia."
author = "Justin Napolitano"
categories = ['Julia','Tutorials', 'Quantitative Analysis','Numerical Computing']
tags = ['julia','numerical-computing','spearman-rank-correlation','statistics']
images = ['featured-julia.png']
series = ['Quantitative Analysis in Julia']
+++

## Spearman Rank in Standard Julia

Well nearly, I did import the erfc function from the SpecialFunctions package.  I don't like it either.  I'll write my own soon to make up for it. 


## Special Thanks

I came across the text Numerical Recipes in C.  It was first published in 1988, by the Cambridge University Press.  The authors are William H. Press, Brian P. Flannery, Saul. A. Teukolsky, and William T. Veterling.  

The book is beautiful.  You should try to find a copy.  It comes in Pascal and Fortran too!!! 

I'm having fun with it and will translate some of the recipes from my first love C to Julia.  


I'll write up a review on the functions below in an upcoming edit.  I'm so excited that it works that I had to publish.  

## Update: There is a Website!!!

[numerical.recipes](http://numerical.recipes/) is a website with all of the code and the ebook.  I thought it was open source at first, but they want some money.  I guess it's okay, but still.  Check it out there.  

[The amazon book link is here](https://www.amazon.com/Numerical-Recipes-Scientific-Computing-Second/dp/0521431085#:~:text=The%20product%20of%20a%20unique,to%20actual%20practical%20computer%20routines)


## Update Again:

I found the PDF!  It is available via penn state university. Here's the [download link](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.129.5354&rep=rep1&type=pdf)


## Using SpecialFunctions:erfc

I had to import the complementary error function.  I wanted to use just the standard library, but I had to test the code below first.  I'll write the compelemntary error function in pure julia next.


```julia

using SpecialFunctions:erfc
```

## Spearman Correlation Function.

It takes:
* two distributions
* the sample size

It returns a t score  The original, used pointers to return multiple variables.  I'll probably rewrite the function to calculate the copmlimentary variables in seperate methods.  Might as well take advantage of the multiple dispatch capability of the language.  





```julia
function spearman(data1,data2,n)

    j =1 
    
    wksp1m= Vector{Float64}(0:n)
    wksp2m = Vector{Float64}(0:n)
    
    for j in 1:(n)
        wksp1m[j]=data1[j]
        wksp2m[j]=data2[j]
    end

    sort!(wksp1m)
    sort!(wksp2m)

    sf = crank(n,wksp1m)
    sg = crank(n,wksp2m)

    d = 0 

    for j in 1:n
        d += sqrt((Complex(wksp1m[j]-wksp2m[j])))
    end
    
    en=n
    en3n = (en*en*en)-en
    aved=(en3n/6.0)-((sf+sg)/12)
    fac=(1.0-sf/en3n)*(1.0-(sg/en3n))
    vard =((en-1.0)*en*en*sqrt(en+1.0)/36.0)*fac
    zd = (d-aved/sqrt(vard))
    probd=erfc((abs(zd)/1.4142136))
    rs = (1.0-(6.0/en3n)*(d+0.5*(sf+sg)))/fac
    t=(rs)*sqrt((en-2.0)/((rs+1.0)*(1.0-rs)))
    return t
    
end
    
```




    spearman (generic function with 2 methods)



### Crank

It ranks the distributions by modifying the original sorted array.  So very C.  I may play with this to return a new value, but I like that it modifies in place.  


```julia
function crank(n,w)
    
    #w= Vector{Float64}(1:n)
    c = 0
    j = 0
    s = 0
    for j in 1:(n-1)
        if w[j+1] != w[j]
            w[j] = j
        else
            for jt in 1:(n)
                if (w[jt] != w[j])
                    break
                end
            end
            rank = .5*(j+jt-1)
            for ji in j:(jt-1)
                w[ji] = rank
            end
            t = jt-j
            s += t*t*t-1
        end
        c = j
        j=j
    end
    if c == n 
        w[n]=n
    end
    return s
end
```




    crank (generic function with 1 method)



## Main()

Creates two random distributions and ranks tests them for correlation.. 


```julia
function main()
    d1 = [5rand()+2 for i=1:50]
    d2 = [3rand()+2 for i=1:50]

    t =spearman(d1,d2,50,0,0,0,0,0)
    display(t)
end
```




    main (generic function with 1 method)




```julia
main()
```


    619.0719816953838 - 0.0im

