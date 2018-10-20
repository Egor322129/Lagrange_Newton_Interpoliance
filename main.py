import numpy as np
import matplotlib.pyplot as plt
import math

#constant
global a, b, checkDotsNum
a,b = np.array([-1, 1])+0.2
checkDotsNum = 100


#test function
def f(x):
    try:
        #return x**2 - np.sin(10*x)
        #return np.sin(x)+np.cos(x)
        #return x**3 - np.exp(x) + 1
        #return np.cos(x)/np.sin(x) - x
        return x**2 - np.arcsin(x-0.2)
    except:
        print("ha" , x)
#Init
def Init1(n):
    xData = np.linspace(a,b,n)
    yData = f(xData) 
    return xData, yData

#Chebyshev Init
def Init2(n):
    ChebDots = lambda i: 0.5*((b-a)*np.cos(np.pi*(2*i+1)/(2*(n+1)))+b+a)
    preData = np.linspace(0,n,n)
    xData = ChebDots(preData)
    yData = f(xData) 
    return xData, yData

#Lagrange Method
def Lagr(x, f, n, par=None): 
    if par == None:
        xData, yData = Init1(n)
    if par == 1:
        xData, yData = Init2(n)
    result = 0
    for i in range (0, len(xData)):
        curDot = xData[i]
        coef = np.linspace(1,1,len(x))
        for j in range (0, len(xData)):
            if (i != j):
                coef *= (x-xData[j])/(curDot-xData[j]) 
        result += f(curDot)*coef
        
    return result

#Newton metgod
def New(x,f,n, par=None):
    if par == None:
        xData, yData = Init1(n)
    if par == 1:
        xData, yData = Init2(n)
    result = 0
    for i in range (0, len(xData)):
        coef = 1
        for j in range(0, i):
            coef *= x-xData[j]
            
        dd = 0
        for j in range(0, i+1):
            g = 1
            for k in range(0, i+1):
                if k != j:
                    g *= 1/(xData[j]-xData[k])
            dd += yData[j]*g
        result += coef*dd
    
    return result

#init
x = np.linspace(a,b,checkDotsNum)
n = 15
y = f(x)
yL = Lagr(x, f, n)
yN = New(x, f, n)
yLCh = Lagr(x, f, n, 1)
yNCh = New(x, f, n, 1)

fig, ax = plt.subplots()
ax.plot(x,y, 'k', label = 'test function', linewidth=1.5)
#ax.plot(x,yL, 'r', label = 'Lagrange polynomial', linewidth=1.5)
ax.plot(x,yN, 'b', label = 'Newton polynomial', linewidth=1.5)
#ax.plot(x,yLCh, 'm', label = 'Lagrange polynomial Chebyshev', linewidth=1.5)
ax.plot(x,yNCh, 'c', label = 'Newton polynomial Chebyshev', linewidth=1.5)
ax.legend(loc='upper center', shadow=True, fontsize=15)
fig.set_size_inches(12, 10)

RLagr = {}
RNew = {}
RLagrCh = {}
RNewCh = {}
start = 2
finish = 42
step = 2

#computing digression
y = f(x)
for i in range(start,finish,step):
    yL = Lagr(x, f, i)
    yN = New(x, f, i)
    yLCh = Lagr(x, f, i, 1)
    yNCh = New(x, f, i, 1)
    RLagr[i] = max(abs(y-yL))
    RNew[i] = max(abs(y-yN))
    RLagrCh[i] = max(abs(y-yLCh)) 
    RNewCh[i] = max(abs(y-yNCh))  

#plots digression    
fig1, ax1 = plt.subplots()
ax1.plot(RLagr.keys(),RLagr.values(), label = 'Lagrange digression ', linewidth=2)
ax1.plot(RNew.keys(),RNew.values(), '-.', label = 'Newton digression ', linewidth=2)
ax1.plot(RLagrCh.keys(),RLagrCh.values(), label = 'Lagrange-Chebyshev digression ', linewidth=2)
ax1.plot(RNewCh.keys(),RNewCh.values(),'-.', label = 'Newton-Chebyshev digression ', linewidth=2)
ax1.legend(loc='upper center', shadow=True, fontsize=15)
fig1.set_size_inches(12, 10)

#export to table
s="number of nodes---number of checking dots---Lagrange digression---Newton digression"
for i in range(start,finish,step):
    s += "\n" + str(i) + "---" + str(checkDotsNum) + "---" + str(RLagr[i]) + "---" + str(RNew[i])

table=['<htm><body><table border="1">']
for line in s.splitlines():
    if not line.strip():
        continue
    table.append(r'<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(*line.split('---')))

table.append('</table></body></html>') 
html_str = ''.join(table)
f = open("yourpage.html","w")
f.write(html_str)
f.close()



