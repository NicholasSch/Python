from threading import Thread
import time

maxA = [[0,1,0,1,0],
          [0,0,1,0,1],
          [1,0,0,1,1],
          [0,1,0,0,1],
          [1,0,1,0,0]]

size = len(maxA)

maxC = [[0 for i in range(size)] for j in range(size)]

influencer1ColunmTotal = 0
influencer2ColunmTotal = 0
influencer1Colunm = -1
influencer2Colunm = -1

influencerrow1total = 0
influencerrow2total = 0
influencer1row = -1
influencer2row = -1

influencertotal = 0 
influencerRO = -1 
influencerCO = -1 

def printMatrix(mat):
  for row in mat:
    print(row)

def mult():
  global step_i, maxC ,totaltime1
  starttime = time.time()
  i = step_i
  step_i = step_i + 1
  for j in range(size):
    for k in range(size):
      maxC[i][j] = maxC[i][j] + maxA[i][k] * maxA[k][j]

  time.sleep(0.1)
  totaltime1 += time.time() - starttime


def biggestnumbs():
  global influencertotal,influencerRO,influencerCO,step_i,totaltime4
  starttime = time.time()
  i = step_i
  step_i = step_i + 1

  current = 0
  for k in range(size):
    current = maxC[i][k]

    if influencertotal <= current:
      influencertotal = current 
      influencerRO = i
      influencerCO = k

  time.sleep(0.1)
  totaltime4 += time.time() - starttime

def biggestrows():
  global influencerrow1total,influencerrow2total,influencer1row,influencer2row,step_i,totaltime2
  starttime = time.time()
  i = step_i
  step_i = step_i + 1

  current = 0
  for k in range(size):
    current += maxC[i][k]

  if influencerrow1total <= current:
    influencerrow2total = influencerrow1total
    influencerrow1total = current 
    influencer2row= influencer1row
    influencer1row = i
  elif influencerrow2total <= current:
    influencerrow2total = current
    influencer2row= i

  time.sleep(0.1)
  totaltime2 += time.time() - starttime

def biggestcolunms():
  global influencer1ColunmTotal,influencer2ColunmTotal,influencer1Colunm,influencer2Colunm,step_i,totaltime3
  starttime = time.time()

  i = step_i
  step_i = step_i + 1

  current = 0
  for k in range(size):
    current+= maxC[k][i]

  if influencer1ColunmTotal <= current:
    influencer2ColunmTotal = influencer1ColunmTotal
    influencer1ColunmTotal = current 
    influencer2Colunm = influencer1Colunm
    influencer1Colunm = i
  elif influencer2ColunmTotal <= current:
    influencer2ColunmTotal = current
    influencer2Colunm = i
    
  time.sleep(0.1)
  totaltime3 += time.time() - starttime

  


thread = list(range(size))

# Multiplicação de matrizes
step_i = 0
totaltime1 = 0

for i in range(size):
    thread[i] = Thread(target=mult)
    thread[i].start()
    
for i in range(size):
    thread[i].join()

# Maior número
step_i = 0
totaltime4 = 0

for i in range(size):
    thread[i] = Thread(target=biggestnumbs)
    thread[i].start()
    
for i in range(size):
    thread[i].join()


# Maiores linhas
step_i = 0
totaltime2 = 0

for i in range(size):
    thread[i] = Thread(target=biggestrows)
    thread[i].start()
    
for i in range(size):
    thread[i].join()



# Maiores colunas
step_i = 0
totaltime3 = 0

for i in range(size):
    thread[i] = Thread(target=biggestcolunms)
    thread[i].start()
    
for i in range(size):
    thread[i].join()


printMatrix(maxC)

print("linha "+str(influencerRO) + " e " + "coluna "+str(influencerCO) + " são os com mais amigos em comum")

print("coluna "+str(influencer1Colunm) + " é o mais popular")

print("EXTRA: linha "+str(influencer1row) + " e " + "linha "+str(influencer2row) + " são as maiores linhas")

print(str(totaltime1 - 0.1*size) + " tempo de multiplicação de matriz")

print(str(totaltime4 - 0.1*size) + " tempo de procura do maior número")

print(str(totaltime3 - 0.1*size) + " tempo de soma das colunas")

print("EXTRA: " + str(totaltime2 - 0.1*size) + " tempo de soma das linhas")
