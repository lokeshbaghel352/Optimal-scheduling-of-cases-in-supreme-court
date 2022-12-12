# -*- coding: utf-8 -*-
"""optimal scheduling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fqUhRX7U6PWQa0nk76KyJf4MEArPucYM
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install gurobipy

# This command imports the Gurobi functions and classes.
import numpy as np
import gurobipy as gp
from gurobipy import GRB
# other necessary libraries
import pandas as pd
from pylab import *
import matplotlib
import matplotlib.pyplot as plt

# # Amount each worker is paid to work one shift.
workers, pay = gp.multidict({
  "Judge-1":   10,
  "Judge-2": 10,
  "Judge-3":   10,
  "Judge-4":   10,
  "Judge-5":    10,
  })

# number of days in Jan 2022, it can be  changed to any other (29/31)
x = range(1,31)
Shifts  = []
Shifts = [str(i) for i in x]
print(Shifts)

# Assume everyone is available give one for avaliability 
availability = pd.DataFrame(np.ones((len(workers), len(Shifts))), index=workers, columns=Shifts)

# Here is the days and workers whose are unavaliable the day that given
availability.at['Judge-1','1'] = 0
availability.at['Judge-2','1'] = 0
availability.at['Judge-2','9'] = 0
availability.at['Judge-2','4'] = 0
availability.at['Judge-4','14'] = 0
availability.at['Judge-3','1'] = 0
availability.at['Judge-3','2'] = 0
availability.at['Judge-3','3'] = 0
availability.at['Judge-3','4'] = 0
availability.at['Judge-1','23'] = 0
availability.at['Judge-1','24'] = 0
availability.at['Judge-1','22'] = 0
availability.at['Judge-1','7'] = 0
availability.at['Judge-1','5'] = 0
availability.at['Judge-1','6'] = 0

temp = availability
# Create availability dictionary to be used in decision variable bounding
column=list(temp)
avail = {(w,s) : availability.loc[w,s] for w in workers for s in Shifts}

# print(avail)
print(availability)

# Create initial model.
m = gp.Model("workforce5")

# Assuming that a case will finish in 8 hearings
# You can input number of gap for hearings
# In this example maximum number of cases completed are 4 with each hearing scheduled with 3 days gap
# Output array shows index number as date and index value as case number ( [1,1,2] => On 1st and 2nd day Case-1 is scheduled and on 3rd day Case-2 is scheduled )
gap=3
case=temp.iloc[0,:].tolist()
cases_completed=0
print(case)
def fun(case,c,gap):
  i=0
  sum=0 
  global cases_completed
  while(i<30):
    if(case[i]!=0 and case[i]==1):
      case[i]=c
    else:
      while(case[i]!=1):
        i+=1
      case[i]=c
    i+=gap
  return case
(fun(case,2,gap))
(fun(case,3,gap))
data = fun(case,4,gap)
print(data)
df = pd.DataFrame(data, columns=['Case Number'])

df = df.rename_axis('Date')
print(df,"\n")

# Schedule a high priority case as soon as possible

def high_priority(data,case_num,case_len,gap_required):
  i=0
  global cases_completed
  while(i<30):
    if(data[i]!=0 and case_len!=0):
      data[i]=case_num
      case_len-=1
      i+=gap_required
    else:
      i+=1
  if(case_len==0):
    cases_completed+=1

      
  return data

print(high_priority(data,6,3,4))

import collections

# If a case gets completed before the scheduled date

def early_completion(data,case_number,index):
  global cases_completed
  for i in range (index, len(data)):
    if(data[i]==case_number):
      data[i]=1
  cases_completed+=1
  return data
print(early_completion(data,2,10))
print()
print(fun(case,5,gap))
print()

# Get the status of number of hearings completed as of now
def CountFrequency(arr):
    return collections.Counter(arr)

def get_status(data):
  global cases_completed
  freq = CountFrequency(data)
  for (key, value) in freq.items():
      if(value>=8):
        cases_completed+=1
      if(key!=0.0):
        print("Case",key, " -> ", value, "hearings completed")

get_status(data)
print()

df = pd.DataFrame(data, columns=['Case Number'])
df.index = np.arange(1, len(df) + 1)
df = df.rename_axis('Date')
print(df,"\n")
print("Total cases completed:", cases_completed )

# Implemented Shortest Remaining Time First (SRTF) algorithm
# Case with less remaining hearings are scheduled first
# Cases disposed are 5

import heapq as hq
import numpy as np
import random
import matplotlib.pyplot as plt

def CountFrequency(my_list):
 
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
 
    for key, value in freq.items():
        print ("% d :% d"%(key, value))
def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

def givP(at,t):  # for list of values in dictionary at that match  t
    l = []
    for i in at:
        if i[0]==t:
            l.append(i[1])
    return l

def isEnd(remainingTime):
    return sum(remainingTime)==0

def column(matrix, i):
    return [row[i] for row in matrix]

def fun(case,c,gap,freq):
  i=0
  sum=0 
  while(i<30):
    if(case[i]==0 and freq!=0):
      case[i]=c
      freq-=1
    else:
      while(case[i]!=0):
        i+=1
      if(freq!=0):
        case[i]=c
        freq-=1
    i+=gap
  return case
def rindex(lst, value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1

def getCT(at,rt):
    at = [[value,key] for key,value in at.items()] #at, pid
    hq.heapify(at)
    rtt = [[value,key] for key,value in rt.items()] #at, pid
    hq.heapify(rtt)
    print('rt_original:=',rt)
    print('rtt:=',rtt)
    t = 0
    Q = []
    ct={}
    myplot=[]
    cases=[]
    hq.heapify(Q)
    #rt,pid
    while True:
        P_at_t = givP(rtt,t) #gives pid which comes at time t
        print('givP(rtt,t):=',givP(rtt,t))
        for p in P_at_t:
            hq.heappush(Q,[rt[p],p])
        print("Q_before",Q) 
        if Q:
            now = hq.heappop(Q) #1st priority  
            cases.append(now[1])
            ct[now[1]] = t+1 #completion time last starting at t and end at t+1
            rt[now[1]] = now[0]-1
            if rt[now[1]]>0:
                hq.heappush(Q,[rt[now[1]],now[1]])
        print("Q_after",Q) 
        print('cases',cases)
        print('ct',ct)
        print('rt_changed',rt)
        if isEnd(list(rt.values())):
            break
        t+=1
    
    case=zerolistmaker(40)
    freq = {}
    gap=3 # fixing gap
    for item in cases:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
 
    for key, value in freq.items():
        case= fun(case,key,gap,value)

    for i in range(len(case)):
      myplot.append([i,case[i]])
    case_comp = {}
    num_days=22
    for i in range(num_days):
        if (case[i] in case_comp):
            case_comp[case[i]] += 1
        else:
            case_comp[case[i]] = 1
    res=0
    shared_items = {k: case_comp[k] for k in case_comp if k in freq and case_comp[k] == freq[k]}
    print("For",num_days,"days","Number of cases completed are", len(shared_items))
    duration = []
    for i in range(len(at)+1):
        duration.append([])
    for mp in myplot:
        duration[mp[1]-1].append((mp[0],1))
    
    
#     return t,ct,myplot

    return ct,myplot,case


def Plotit(myplot):
    endTime = myplot[-1][0] +1
    def getColor(n):
        myCol = ['blue','brown','cyan',
         'green','olive',
        'orange','pink','red']
        s = set()
        while(len(s)!=n):
            s.add('tab:'+myCol[random.randint(0,len(myCol)-1)])
        return list(s)
    print("Gant Chart:-")
    fig, gnt = plt.subplots(figsize =(10,5),dpi=300)
    gnt.set_ylim(0, 10)
    gnt.set_xlabel('Date')
    gnt.set_ylabel('Case')
    gnt.grid(True)

    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('None')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',5))

    My = []
    for i in range(len(at)+1):
        My.append([])
    for mp in myplot:
        My[mp[1]-1].append((mp[0],1))
    randomColor=getColor(len(My)-1)
    gnt.set_xlim(0,40)
    gnt.set_yticks([5])
    gnt.set_yticklabels(['C'])
    gnt.set_xticks([i+1 for i in range(endTime+2)])
    

    for i in range(len(My)-1):
        gnt.broken_barh(My[i], (4, 2), facecolors =(randomColor[i]))

    gnt.legend(['Case '+str(i) for i in range(1,len(at)+1)],loc='upper left')
#     plt.savefig("MyGantChart.png")
    plt.show()
    
def Print(at,rt,ct,res):
    process = list(at.keys())
    tat = {}
    wt = {}
    for p in process:
        tat[p] = ct[p] - at[p]
        wt[p] = tat[p] - rt[p]
    gap={1:2,2:3,3:4,4:"-",5:"-"}
    print("*"+("-"*18+"*")*4)
    print("|{:^18}|{:^18}|{:^18}|{:^18}|{:^18}|".format("Case","Hearing Arrival","Total Hearings","Hearing Required","Gap"))
    print("*"+("-"*18+"*")*4)
    for p in process:
        print("|{:^18}|{:^18}|{:^18}|{:^18}|{:^18}|".format("Case {}".format(p),at[p],res[p],res[p]-at[p],gap[p]))
    print("*"+("-"*18+"*")*4)
    tat_value = list(tat.values())
    wt_value = list(wt.values())
    ct,myplot,cases=getCT(at,rt)
    

    # print("Average Turn Around Time is : {}".format(sum(tat_value)/len(tat_value)))
    # print("Average Waiting Time is     : {}".format(sum(wt_value)/len(wt_value)))

def solve(at,rt,res):
    rt_copy = rt.copy()
    ct,myplot,case=getCT(at,rt)

    s=set(case)
    s.remove(0)
    case_dict={}
    lol=len(s)-1
    for cases in s:
      case_dict[cases]=abs(case.index(cases)-rindex(case,cases))+1
    avg_dur=0
    for key in case_dict:
        avg_dur+=case_dict[key]
    print("Average Case duration is", avg_dur/len(case_dict))
    Plotit(myplot)
    Print(at,rt_copy,ct,res)
def userInput():
    n = int(input("Enter Number of Cases:- "))
    at={};res={};rt={};
    for p in range(1,n+1):
        at[p] = int(input("Arrival Time  @{} : ".format(p)))
        res[p] = int(input("Hearings Required   @{} : ".format(p)))
    rt = {key: res[key] - at.get(key, 0) for key in res.keys()}
    return at,rt,res

# Example UserInput
import heapq as hq
# at,rt=userInput()
# solve(at,rt,res)

#Example2
at = {1:5,2:3,3:4,4:2,5:3}
res = {1:10,2:9,3:8,4:10,5:5}
rt= {1:8, 2:12, 3:9, 4:7, 5:11} #duration
#rt = {key: res[key] - at.get(key, 0) for key in res.keys()}
# print(rt)
# pt = [[value,key] for key,value in at.items()]
# hq.heapify(pt)
# print(pt)
solve(at,rt,res)

!pip install heapq_max
!pip3 install maxheapq

# Implemented Shortest Remaining Time First (SRTF) algorithm
# Case with maximuim duration are scheduled first
# Cases disposed are 5

from heapq_max import *
import numpy as np
import random
import heapq as h
import matplotlib.pyplot as plt
from maxheap import maxheap

def CountFrequency(my_list):
 
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
 
    for key, value in freq.items():
        print ("% d :% d"%(key, value))
def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros

def givP(at,t):  # for list of values in dictionary at that match  t
    l = []
    for i in (at):
        if i[0]==t:
            l.append(i[1])
    return l

def isEnd(remainingTime):
    return sum(remainingTime)==0

def column(matrix, i):
    return [row[i] for row in matrix]

def fun(case,c,gap,freq):
  i=0
  sum=0 
  while(i<30):
    if(case[i]==0 and freq!=0):
      case[i]=c
      freq-=1
    else:
      while(case[i]!=0):
        i+=1
      if(freq!=0):
        case[i]=c
        freq-=1
    i+=gap
  return case
def rindex(lst, value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1
def _heappush_max(heap, item):
    heap.append(item)
    h._siftdown_max(heap, 0, len(heap)-1)
def _heappop_max(heap):
    lastelt = heap.pop()  # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        h._siftup_max(heap, 0)
        return returnitem
    return lastelt

    return [_heappop_max(h) for i in range(len(h))]
def getCT(at,rt):
    at = [[value,key] for key,value in at.items()] #at, pid
    maxheap.heapify(at)
    rtt = [[value,key] for key,value in rt.items()] #at, pid
    maxheap.heapify(rtt)
    t = 30
    Q = []
    ct={}
    myplot=[]
    cases=[]
    maxheap.heapify(Q)
    while True :
        P_at_t = givP(rtt,t) #gives pid which comes at time t
        for p in P_at_t:
            maxheap.heappush(Q,[rt[p],p]) 
        if Q:
            now = maxheap.heappop(Q) #1st priority  
            cases.append(now[1])
            ct[now[1]] = t+1 #completion time last starting at t and end at t+1
            rt[now[1]] = now[0]-1
            if rt[now[1]]>0:
                maxheap.heappush(Q,[rt[now[1]],now[1]])
        if isEnd(list(rt.values())):
            break
        t-=1
    
    case=zerolistmaker(40)
    freq = {}
    gap=2
    for item in cases:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
 
    for key, value in freq.items():
        case= fun(case,key,gap,value)

    for i in range(len(case)):
      myplot.append([i,case[i]])
    case_comp = {}
    num_days=10
    for i in range(num_days):
        if (case[i] in case_comp):
            case_comp[case[i]] += 1
        else:
            case_comp[case[i]] = 1
    res=0
    shared_items = {k: case_comp[k] for k in case_comp if k in freq and case_comp[k] == freq[k]}
    print("For",num_days,"days","Number of cases completed are", len(shared_items))
    duration = []
    for i in range(len(at)+1):
        duration.append([])
    for mp in myplot:
        duration[mp[1]-1].append((mp[0],1))
    
    
#     return t,ct,myplot

    return ct,myplot,case


def Plotit(myplot):
    endTime = myplot[-1][0] +1
    def getColor(n):
        myCol = ['blue','brown','cyan',
         'green','olive',
        'orange','pink','red']
        s = set()
        while(len(s)!=n):
            s.add('tab:'+myCol[random.randint(0,len(myCol)-1)])
        return list(s)
    print("Gant Chart:-")
    fig, gnt = plt.subplots(figsize =(10,5),dpi=300)
    gnt.set_ylim(0, 10)
    gnt.set_xlabel('Date')
    gnt.set_ylabel('Case')
    gnt.grid(True)

    ax = plt.gca()  # gca stands for 'get current axis'
    ax.spines['right'].set_color('None')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',5))

    My = []
    for i in range(len(at)+1):
        My.append([])
    for mp in myplot:
        My[mp[1]-1].append((mp[0],1))
    randomColor=getColor(len(My)-1)
    gnt.set_xlim(0,40)
    gnt.set_yticks([5])
    gnt.set_yticklabels(['C'])
    gnt.set_xticks([i+1 for i in range(endTime+2)])
    

    for i in range(len(My)-1):
        gnt.broken_barh(My[i], (4, 2), facecolors =(randomColor[i]))

    gnt.legend(['Case '+str(i) for i in range(1,len(at)+1)],loc='upper left')
#     plt.savefig("MyGantChart.png")
    plt.show()
    
def Print(at,rt,ct,res):
    process = list(at.keys())
    tat = {}
    wt = {}
    for p in process:
        tat[p] = ct[p] - at[p]
        wt[p] = tat[p] - rt[p]
    gap={1:2,2:3,3:4,4:"-",5:"-"}
    print("*"+("-"*18+"*")*4)
    print("|{:^18}|{:^18}|{:^18}|{:^18}|{:^18}|".format("Case","Hearing Arrival","Total Hearings","Hearing Required","Gap"))
    print("*"+("-"*18+"*")*4)
    for p in process:
        print("|{:^18}|{:^18}|{:^18}|{:^18}|{:^18}|".format("Case {}".format(p),at[p],res[p],res[p]-at[p],gap[p]))
    print("*"+("-"*18+"*")*4)
    tat_value = list(tat.values())
    wt_value = list(wt.values())
    ct,myplot,cases=getCT(at,rt)
    

    # print("Average Turn Around Time is : {}".format(sum(tat_value)/len(tat_value)))
    # print("Average Waiting Time is     : {}".format(sum(wt_value)/len(wt_value)))

def solve(at,rt,res):
    rt_copy = rt.copy()
    ct,myplot,case=getCT(at,rt)

    s=set(case)
    s.remove(0)
    case_dict={}
    lol=len(s)-1
    for cases in s:
      case_dict[cases]=abs(case.index(cases)-rindex(case,cases))+1
    avg_dur=0
    for key in case_dict:
        avg_dur+=case_dict[key]
    print("Average Case duration is", avg_dur/len(case_dict))
    Plotit(myplot)
    Print(at,rt_copy,ct,res)
def userInput():
    n = int(input("Enter Number of Cases:- "))
    at={};res={};rt={};
    for p in range(1,n+1):
        at[p] = int(input("Arrival Time  @{} : ".format(p)))
        res[p] = int(input("Hearings Required   @{} : ".format(p)))
    rt = {key: res[key] - at.get(key, 0) for key in res.keys()}
    return at,rt,res

# Example UserInput
import heapq as hq
# at,rt=userInput()
# solve(at,rt,res)

at = {1:5,2:3,3:4,4:2,5:3}
res = {1:10,2:9,3:8,4:10,5:5}
rt= {1:8, 2:12, 3:9, 4:7, 5:11}
#rt = {key: res[key] - at.get(key, 0) for key in res.keys()}

solve(at,rt,res)

