import matplotlib.pyplot as plt
import numpy as np                      
import csv, sys
import TracerLPM_CPP_Library as Solver
import ctypes as c
import datetime
import time
import math


def readInResults():
    try:                                                                    #   Note: saving in excel's UTF-8 csv format will cause weirdness, use plain csv format
        f = open(r'CVAL_LPMsForAgeDistributions_10132022.csv')
    except Exception as e:
        print(e)
        sys.exit()

    with open(r'CVAL_LPMsForAgeDistributions_10132022.csv') as csv_file:
        ResultsDataCSV = csv.reader(csv_file, delimiter = ',')               #   add in timer to check how long each sample takes
        ResultsData = list(ResultsDataCSV)
        #print (ResultsData)
    
    return ResultsData

def writeToCSV(SampleInfo,ArrayList,xArray):
    #print(ArrayList)
    #print(xArray)
    with open("CVAL_LPMsForAgeDistributions_10132022_output9.csv", 'a', newline='') as file:
        writer = csv.writer(file,delimiter = ',')
        writer.writerow(SampleInfo)
        writer.writerow(xArray)        
        writer.writerow(ArrayList)
        
            

def ParseParms(ResultsArray):
    i=0
    print("ResultsArray: ", len(ResultsArray))
    print("i= ",i)
    for row in ResultsArray:
        if i == 0:
            i=i+1
            continue
        t0 = time.time()
        print(str(row[1]),str(row[3]),str(row[5]),str(row[9]),str(row[8]),str(row[4]),str(row[6]),str(row[7]),str(row[10]),str(row[11]))
        AgeDist = GetAgeDist(row[3],            #Model
                             float(row[5]),     #MeanAge1
                             float(row[9]),     #MeanAge2
                             float(row[8]),     #Fraction
                             float(row[4]),     #UZTime
                             float(row[6]),     #ModelParm1_1
                             float(row[7]),     #ModelParm1_2
                             float(row[10]),    #ModelParm2_1
                             float(row[11]))    #ModelParm2_2
        SampleInfo = [row[0],row[1],row[2],row[3],time.time()-t0,"seconds"]
        writeToCSV(SampleInfo,AgeDist[0],AgeDist[1])
        print("Complete row " + str(i))
        i = i+1


def GetAgeDist(Model, MeanAge1, MeanAge2, Fraction, UZTime, MP1_1, MP1_2, MP2_1, MP2_2):                                                                         
        
    isBMM = 0
    DispMult = 1
    numsteps=100
    StartAge1 = 0
    StartAge2 = MeanAge2 / 4
    EndAge1 = 200
    EndAge2 = 50000
    if len(Model)>3:
        isBMM = 1
        print(Model)
        Model = Model.split("-",2)[1]
    if Model == "DM" and MP1_1 > 0.01:
        DispMult = 2    
    if Model == "PEM" and isBMM == 0:
        DispMult = 2
    
    if isBMM == 1:
        EndAge2 = MeanAge2 * 2 * DispMult
    else:
        EndAge1 = (MeanAge1+UZTime) * 2 * DispMult

    if Model == "DM":                                                                      
        AgeDist = Solver.gt_DM(0,int(EndAge1), MeanAge1, MP1_1,UZTime,int(EndAge/numsteps),numsteps)
        print(MeanAge1)
    elif Model == "PEM":
        AgeDist = Solver.gt_PEM(StartAge1,EndAge1, MeanAge1, MP1_1,MP1_2,UZTime,int(EndAge1/numsteps),numsteps)
    if isBMM == 1:
            AgeDist[0]=[val*Fraction for val in AgeDist[0]]
            
    if isBMM == 0:
        return AgeDist
    
    
    
    #print(AgeDist)    
   
    
    
    if isBMM == 1:
        if Model == "DM":                                                                      
            AgeDist2 = Solver.gt_DM(MeanAge1 * 4,int(EndAge), MeanAge2, MP2_1,UZTime,float(EndAge)/numsteps,numsteps)
            print(int(MeanAge2/MeanAge1))
        elif Model == "PEM":
            AgeDist2=Solver.gt_PEM(StartAge2,EndAge2 ,MeanAge2, MP2_1,MP2_2,UZTime,int(EndAge2/numsteps),numsteps)  
        else:
            print("Model type not recognized...")
            # sys.exit()
        
        #print(AgeDist2[0][:100])
        #print(AgeDist2[1][:100])
        
        #print(AgeDist2[1])
        AgeDist2[0]=[val*(1-Fraction) for val in AgeDist2[0]]
        #print(AgeDist2[1])
        BMMAgeDist = np.append(AgeDist[0],AgeDist2[0])
        #AgeDist[1].append(AgeDist2[1])
        Xaxis = np.append(AgeDist[1],AgeDist2[1])

        #print(Xaxis)


        #BMMAgeDist = [a + b for a, b in zip(AgeDist[0],AgeDist2[0])]
        #XArrays = [a + b for a, b in zip(AgeDist[1],AgeDist2[1])]
        
        #BMMAgeDist = AgeDist[0]
        #BMMAgeDist.extend(AgeDist2[0])

        #XArrays = AgeDist[1].tolist()
        #XArrays.extend(AgeDist2[1])
        
         

        ListAgeDist= [BMMAgeDist,Xaxis]
          
        return ListAgeDist
    
    return None

  

ResultsList = readInResults()
#for row in ResultsList:
#    print(row)
#writeToCSV(ResultsList)

ParseParms(ResultsList)

print("Operation Completed!")
