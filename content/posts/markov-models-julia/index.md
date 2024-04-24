+++
title =  "Markov Chains in Julia"
date = "2022-05-26T01:30:32.169Z"
description = "Writing a Markov Simulation Problem the hard way."
author = "Justin Napolitano"
categories = ['Julia','Tutorials', 'Quantitative Analysis']
tags = ['julia', 'dataframes', 'mathematics','statistics','markov' ]
images = ['featured-julia.png']
series = ['Quantitative Analysis in Julia']
+++



## Introduction

I am currently working on a [legal research series](https://blog.jnapolitano.io/series/legal-research-with-ai/) where I perform statistical analysis and ml models to legal datasets.  My intention is to model the behavior of courts, determine the outcome of cases, and build a pipeline capable of identifying relevant case law by issue area.  

That data set is nearly complete, but I have not decided which models to apply to it.  This is where Julia comes into play.  

I plan to perform the statistical analysis and possible the ml workload with Julia.  

In this post, I share an Algorithm to compute Markov Chains.  




## Markov Chains

I don't understand them completely.  I am grateful to [the text](https://julia.quantecon.org/tools_and_techniques/finite_markov.html) for helping me to bettter grasp how they operate.  

As far as my understanding goes they permit modeling the transition of states, possibly in infinite time, according to a probability distribution.  I recommend reading [this source](https://julia.quantecon.org/tools_and_techniques/finite_markov.html#markov-chains) for authority.  


## My Translation of Markov Chains

Lets start with a finite set of of elements that we call S.  In Cs terms think of this is as an array in the C Language.  It must be defined prior to an operation. `I think markov chains can be performed on unbounded sets as well but I'm not at that level yet`.

The set is called the set space.  Each value within it considered an individual state. 

Markov Chains are sets that contain the Markov Property.  A markov property considers the probability of the model having a state within the space at a point in time.  

Thus, the probability of going from x to y in one step of unit time can be computed.  If we consider the state changes within a stochastic matrix we can then determine the overall probabily of arriving at states within a system.

Review the [formal defition](https://julia.quantecon.org/tools_and_techniques/finite_markov.html#equation-mpp).

## Application to My Work

I will be using this model to determine the probability of a justice transitioning from emotional states.  The central thesis of my understanding of judicial behavior is that the justices develop attitudinal states towards issue areas, legal provisions, states, religions, objects in general.  I will compute those states by first determining them.  I will then calculate the bayesian probability of state transition across time.  Finally, those distribution will be inputted in Markov Chain models.  

## Markov Simulation the Hard Way

The work below is not my own.  I attribute it to [julia.quantecon.org/](https://julia.quantecon.org/tools_and_techniques/finite_markov.html#equation-mpp). 

The alogorithm takes a stochastic probability matrix(square in this case) and create a random distribution according to those probabilities.  

The simulation then randomly selects values from the random distibution.  That discrete value is stored in the output.  As I understand it currently, the output is the Markov Chain.  


The comments in the code are mine.  


``` Julia 

using LinearAlgebra, Statistics
using Distributions, Plots, Printf, QuantEcon, Random

function mc_sample_path(P; init = 1, sample_size = 1000)


    @assert size(P)[1] == size(P)[2] # square required
    N = size(P)[1] # should be square # well it's been asserted

    # create vector of discrete RVs for each row
    # In human terminology. Create a Categorical distribution of length = the size of the row of the matrix.  
    #IF that makes sense
    dists = [Categorical(P[i, :]) for i in 1:N]

    # setup the simulation
    X = fill(0, sample_size) # allocate memory, or zeros(Int64, sample_size) # I love Julia.  Readable syntax and low level contro
    X[1] = init # set the initial state Equal to 1 in this case.  

    for t in 2:sample_size # start at position 2.  Work from t-1# This is a common technique.  Couldn't figure this out once in a technical interview.  I wrote an if else for the zero condition.... Not so smart
        dist = dists[X[t-1]] # get discrete RV from last state's transition distribution
        X[t] = rand(dist) # draw new value
    end
    return X
end
```


## Markov Simulation the Easier Way

Given a stochastic probability matrix, the Markov Chain function will produce a chain.  

The simulate method will then simulate the chain across a n steps.  

We can then take the mean of the output to determine the average amount of time spent in a state.  In this case the average amount of time spent in state 1 which should correlate to unemployment.  


```Julia
using LinearAlgebra, Statistics
using Distributions, Plots, Printf, QuantEcon, Random


function easy_way()
    P = [0.4 0.6; 0.2 0.8];
    mc = MarkovChain(P)
    X = simulate(mc, 100_000);
    μ_2 = count(X .== 1)/length(X) # or mean(x -> x == 1, X)
end

```julia