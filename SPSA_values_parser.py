# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2024 AliceRoselia

While this parser was intended to be used to parse GPL-licensed Stockfish's tune value, this parser is 
a general-purpose parser for any tuning formatted this way. Therefore, this is separately licensed with MIT license.
You can either use this as a part of Stockfish (GPL-licensed) or on its own. 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



"""

#This was used only as a programming aid for inputting values. However, in the spirit of open-source,
#I will make the source available.


SPSA_values = """
example	-3.07	0	-100	100	11.333	10.000	2.91e-03	2.00e-03
"""

def variable_name(x):
    first_bracket = x.find("[")
    if first_bracket == -1:
        return x
    else:
        return x[:first_bracket]

def dimension_inference(x):
    first_bracket = x.find("[")
    if first_bracket == -1:
        return tuple()
    else:
        arr = []
        while first_bracket != -1:
            second_bracket = x.find("]",first_bracket+1)
            
            arr.append(int(x[first_bracket+1:second_bracket]))
            
            first_bracket = x.find("[",second_bracket+1)
        return tuple(arr)
            
            
        
    
    
#Only works for rectangular arrays. Other shapes don't work. The tuning shouldn't work on those arrays either.

info = dict()
dims = dict()

vartype = "Value" #Int, depth, etc.

for i in SPSA_values.strip().split("\n"):
    splitted = i.split()
    var_name = variable_name(splitted[0])
    dimension = dimension_inference(splitted[0])
    value = round(float(splitted[1]))
    dims[var_name] = max(dimension,dims.get(var_name,tuple()))
    if var_name in info:
        info[var_name][dimension] = value
    else:
        info[var_name] = {dimension:value}
    

def formatted_print(info,dimension,idxs = tuple()):
    if len(idxs) == len(dimension):
        return str(info[idxs])
    i = len(idxs)
    x = (formatted_print(info, dimension,idxs+(j,)) for j in range(dimension[i]))
    return "{" + ",".join(x) + "}"


for variable, dimension in dims.items():
    print(vartype,variable,"=")
    print(formatted_print(info[variable], dimension),";",sep="")

