+++
title =  "Legal Research with AI Part 7: Wrangling Data with Julia"
date = "2022-05-22T16:30:32.169Z"
description = "File management with Julia in preperation for data merge."
author = "Justin Napolitano"
image = "thumbnail.*"
categories = ['Julia','Tutorials', 'Legal Research', 'Data Wrangling']
tags = ['julia', 'dataframes', 'SCOTUS','data-wrangling' ]
images = ['featured-julia.png']
series = ['Legal Research with AI']
+++

## Intro
In a [previous post](https://blog.jnapolitano.io/posts/legal-research-part-5/), I seperated all of the results returned from the Library of Congress API into individual JSON documents to be imported as nodes into a neo4j graph.  

In this post, I filter the `LOC` data against another data set from Oyez that will be integrated in the next post.  

## Filtering Data

Both data sets have been seperated into individual case nodes stored in the json format as a file with the format : <citation>.json.

The Library of Congress data contains indices, admonitions, briefs, and other data that I will not yet be incorporating into my data set.  

In order to find only the case data I will be creating a dataframe containing the paths of json files with matching citations.  

## Using Julia Instead of Python

I love Python, but I want to try something new.  Julia's [multiple dispatch](https://docs.julialang.org/en/v1/manual/methods/) design tempted me to try it out.  This is my first Julia program.  I will be documenting the work more so than usual. 

### Julia "import" Functions

Coming from Python, I typically import libraries/packages with an `import` call.  Something like:

``` python

import numpy

```

In Julia, we use the `using` call to import the package. Like: 

```julia

using DataFrames
using CSV

```

A package can also be imported, but this does not instantiate the methods and functions within it (As far as I understand it). 

For instance `import CSV` would only load the package but I would have to call CSV.method to actually do something.  Something like `from pandas import to_csv` in Python.  


```julia

import DataFrames
import CSV

```


## The Main Function

Just like in C -and like we should in Python-, I declared a main function to run the program.  I call it with main().  I do not know if there is a similar convention to Python's `if __name__ == "__main__"`.  I will find out soon.  

The main difference in function declaration between Python and Julia is the inclusion of the `end` keyword and the end of the function.

For instance review the main function below :

```julia
function main()
    
    # outpath fo the current file
    outpath = joinpath(pwd(),"case_files.csv")

    #Glob files from directory
    oyez_dataframe = get_files("oyez_cited")
    
    #Glob files from directory
    loc_dataframe = get_files("loc_cited")

    
    # Join on File excluding extraneous data not in the oyez dataset
    master_df = innerjoin(oyez_dataframe, loc_dataframe, on = :File, validate=(true, true), makeunique = true)

    #Select every file but the .DS_Store from the dataframe.  
    master_df = filter(row -> !(row.File == ".DS_Store"), master_df)

    #Write to file
    outpath = df_to_file(master_df,outpath)
    

end

main()


```
### Creating an outpath

The main function creates an outpath to write the resultant master df to file by calling `joinpath(pwd(), "case_files.csv")`. 

  

### The Get Files Function


Next, the get_files function is called to create two data frames:  the loc_df and the oyez_df.  

#### Declaring empty string arrays

Each file name is appended to a file_name array declared with `<array_name> = String[]`


#### Reading Files with readdir()

File names are from from a directory passed to the built in `readdir()` function. 

#### Appending Files to file_name Array

Each file name is appended to a file_name array declared with `file_name = String[]` and appended to with the push!(file_name,f) call.  Note the `!` following push.  This typically means that the function is operating on the data in memory and will not return a new value. 

#### Appending File Paths to file_path Array

I also include the file path by appending what is returned by `path = joinpath(working_path, f)` to the file_path list.

I love the built in `joinpath` function.  Pythons `os.sep.join()` works well, but I really like Julia's implementation.

#### Sorting the Arrays with Merge Sort

Arrays are soreted by call `sort_array(<array>)`.  It returns a sorted array using the merge sort alogorithm.  

```julia
function sort_array(array)
    
    return sort(array; alg=MergeSort)

end
```
#### Crating a Dataframe with the Arrays

Finally a dataframe containing the sorted file_name and file_path lists as the columns file and path is created and then returned. 


#### A note on refactoring

This function should be refactored into seperate ones, but it works well enough with this workflow that I am going to leave it.  


```julia
function get_files(directory)
    file_name = String[]
    file_path = String[]

    working_path = joinpath(pwd(), directory)
    # context management.  Cd and then go back to the orignal pwd
    cd(working_path) do 
        #print("Current directory: ", working_path)
        foreach(readdir()) do f
            path = joinpath(working_path, f)
            push!(file_name,f)
            push!(file_path, path)
            #dump(stat(f.desc)) # you can customize what you want to print
        end
    end
    #println('\n', pwd())
    #display(file_paths)
    file_name = sort_array(file_name)
    file_path = sort_array(file_path)
    df = DataFrame(File = file_name, Path = file_path)
    return df

end


```
### Joining Data Frames by Citation

Julia's DataFrames package can easily join dataframes on a column.  In this workflow the file which is titled after a case citation is used.  

```julia
# Join on File excluding extraneous data not in the oyez dataset
master_df = innerjoin(oyez_dataframe, loc_dataframe, on = :File, validate=(true, true), makeunique = true)

```




    

### Filtering the DF for Extraneous Files

The master_df  is filtered to remove `.DS_Store` from the list of files to be processed.  Below notice the `!` in this case it will return all a data frame of values that are not equal to .DS_Store in the File column.  

```julia
#Select every file but the .DS_Store from the dataframe.  
master_df = filter(row -> !(row.File == ".DS_Store"), master_df)
```




### The df_to_file Function

Finally the df is written to file.  


``` julia
#Write to file
outpath = df_to_file(master_df,outpath)


function df_to_file(df,outpath)
    CSV.write(outpath, df)
    return outpath

end

```



## The Complete Program

``` julia
using DataFrames
using CSV

function get_files(directory)
    file_name = String[]
    file_path = String[]

    working_path = joinpath(pwd(), directory)
    # context management.  Cd and then go back to the orignal pwd
    cd(working_path) do 
        #print("Current directory: ", working_path)
        foreach(readdir()) do f
            path = joinpath(working_path, f)
            push!(file_name,f)
            push!(file_path, path)
            #dump(stat(f.desc)) # you can customize what you want to print
        end
    end
    #println('\n', pwd())
    #display(file_paths)
    file_name = sort_array(file_name)
    file_path = sort_array(file_path)
    df = DataFrame(File = file_name, Path = file_path)
    return df

end



function sort_array(array)
    
    return sort(array; alg=MergeSort)

end



function df_to_file(df,outpath)
    CSV.write(outpath, df)
    return outpath

end


function main()
    
    # outpath fo the current file
    outpath = joinpath(pwd(),"case_files.csv")

    #Glob files from directory
    oyez_dataframe = get_files("oyez_cited")
    
    #Glob files from directory
    loc_dataframe = get_files("loc_cited")

    
    # Join on File excluding extraneous data not in the oyez dataset
    master_df = innerjoin(oyez_dataframe, loc_dataframe, on = :File, validate=(true, true), makeunique = true)

    #Select every file but the .DS_Store from the dataframe.  
    master_df = filter(row -> !(row.File == ".DS_Store"), master_df)

    #Write to file
    outpath = df_to_file(master_df,outpath)
    

end

main()

```