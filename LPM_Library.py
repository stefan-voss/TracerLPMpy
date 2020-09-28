
import matplotlib.pyplot as plt
import numpy as np                      
import csv, sys
import TracerLPM_CPP_Library as Solver
import ctypes as c
import datetime
import time
import math

#########################
#   GLOBAL VARIABLES    #
#########################


SampleDataLoaded = 0
TracerDataLoaded = 0
SampleData = np.array(object)
TracerParms = np.array(object)
TracerParmsLoaded = 0
AllTracerData = []
outfile = ''

UZ_TIME = 0
MEAN_AGE = 1
EPM_RATIO = 2
PEM_U_RATIO = 2
SHAPE = 2
MODEL_PARM_1 = 2
DISP_PARM = 2
MODEL_PARM_2 = 3
PEM_L_RATIO = 3
ALPHA = 3
FRACTION = 4
MEAN_AGE_2 = 5
EPM_RATIO_2 = 6
PEM_U_RATIO_2 = 6
SHAPE_2 = 6
MODEL_PARM_1_2 = 6
DISP_PARM_2 = 6
MODEL_PARM_2_2 = 7
PEM_L_RATIO_2 = 7
ALPHA_2 = 7

DM  = 'DM'
PFM = 'PFM'
EMM = 'EMM'
EPM = 'EPM'
GAM = 'GAM'
PEM = 'PEM'
FDM = 'FDM'

DM_DM  = 'DM_DM'
DM_PFM = 'DM_PFM'
DM_EMM = 'DM_EMM'
DM_EPM = 'DM_EPM'
DM_GAM = 'DM_GAM'
DM_PEM = 'DM_PEM'
DM_FDM = 'DM_FDM'

PFM_DM  = 'PFM_DM'
PFM_PFM = 'PFM_PFM'
PFM_EMM = 'PFM_EMM'
PFM_EPM = 'PFM_EPM'
PFM_GAM = 'PFM_GAM'
PFM_PEM = 'PFM_PEM'
PFM_FDM = 'PFM_FDM'

EMM_DM  = 'EMM_DM'
EMM_PFM = 'EMM_PFM'
EMM_EMM = 'EMM_EMM'
EMM_EPM = 'EMM_EPM'
EMM_GAM = 'EMM_GAM'
EMM_PEM = 'EMM_PEM'
EMM_FDM = 'EMM_FDM'

EPM_DM  = 'EPM_DM'
EPM_PFM = 'EPM_PFM'
EPM_EMM = 'EPM_EMM'
EPM_EPM = 'EPM_EPM'
EPM_GAM = 'EPM_GAM'
EPM_PEM = 'EPM_PEM'
EPM_FDM = 'EPM_FDM'

GAM_DM  = 'GAM_DM'
GAM_PFM = 'GAM_PFM'
GAM_EMM = 'GAM_EMM'
GAM_EPM = 'GAM_EPM'
GAM_GAM = 'GAM_GAM'
GAM_PEM = 'GAM_PEM'
GAM_FDM = 'GAM_FDM'

PEM_DM  = 'PEM_DM'
PEM_PFM = 'PEM_PFM'
PEM_EMM = 'PEM_EMM'
PEM_EPM = 'PEM_EPM'
PEM_GAM = 'PEM_GAM'
PEM_PEM = 'PEM_PEM'
PEM_FDM = 'PEM_FDM'

FDM_DM  = 'FDM_DM'
FDM_PFM = 'FDM_PFM'
FDM_EMM = 'FDM_EMM'
FDM_EPM = 'FDM_EPM'
FDM_GAM = 'FDM_GAM'
FDM_PEM = 'FDM_PEM'
FDM_FDM = 'FDM_FDM'



#########################
#                       #
#       LPM Class       #
#                       #
#########################


class SampleInput:
    
    def __init__(self, FileName):                              
        global SampleDataLoaded
        global SampleData                                      
        try:                                                   
            f = open(FileName)
        except Exception as e:
            print(e)
            sys.exit()

        with open(FileName) as csv_file:
            SampleDataCSV = csv.reader(csv_file, delimiter = ',')       #   Indexing is SampleData[Sample Id/row][column]
            SampleDataList = list(SampleDataCSV)
        SampleData = np.array(SampleDataList,object)
        SampleDataLoaded = 1

        self.Samples = []

        for x in range(len(SampleData)):
            if x > 0:
                self.Samples.append(Sample(x))
        
    def __getitem__(self, index):
        return self.Samples[index]

class Sample:
    global SampleDataLoaded
    global SampleData
    global AllTracerData
    
   
    
     
    def __init__(self, SampleIndex):                                    #   SampleIndex = ID of sample (1st sample = 1), 
                                                                        #   See sample input example form for correct formatting of columns
        if SampleDataLoaded == 0:
            print("Load sample input csv first")
            sys.exit()
        self.Index = SampleData[SampleIndex][0]
        self.Study = SampleData[SampleIndex][1]                         #   Study name, optional
        self.Area = SampleData[SampleIndex][2]                          #   Study area name, optional
        self.SampleID = SampleData[SampleIndex][3]                      #   Sample name, alphanumeric
                                                                        #   Sample date in decimal format, eg: 2005.79452054795
        self.SampleDatFrac = str(SampleData[SampleIndex][4])
        self.SampleDate = self.toYearFraction(self.SampleDatFrac)
        self.TracerName = []
        self.TracerLoc = []
        self.TracerConc = []
        self.TracerErr = []
        self.lSampleRow = SampleIndex
        self.SelectedTracerData = np.array(object)
        self.SampleTracerInput = self.TracerInput()

        Loop = 0
        for x in SampleData[SampleIndex]:
           
            if x == '':
                Loop += 1
                continue
            if Loop < 5:
                Loop += 1
                continue
            if Loop > 44:
                if Loop == 49:
                   self.PEM_Upper = float(x)
                elif Loop == 50:
                    self.PEM_Lower = float(x)
                else: 
                    Loop += 1
                    continue
            elif (3+Loop) % 4 == 0:
                self.TracerName.append(x)
            elif (3+Loop) % 4 == 1:
                self.TracerLoc.append(x)
            elif (3+Loop) % 4 == 2:
                self.TracerConc.append(float(x))
            elif (3+Loop) % 4 == 3:
                self.TracerErr.append(float(x))
            Loop += 1

        
        self.GetTracerData()
    
    def toYearFraction(self,dateStr):                                               #   Converts mm/dd/yyyy into decimal year format
        try:
            date = datetime.datetime.strptime(dateStr,"%m/%d/%Y")
        except:
            print("Sample date [",dateStr,"] should be in mm/dd/yyyy format")
            sys.exit()
        start = datetime.date(date.year, 1, 1).toordinal()
        
        year_length = datetime.date(date.year+1, 1, 1).toordinal() - start
        return date.year + float(date.toordinal() - start) / year_length

    def LoadTracerData(self):                                                       #   Load tracer data from storedtracerdata.csv. This file should be ~~READ ONLY~~
        global TracerDataLoaded                                                     #   Be very careful editing this file, excel will save whatever precision is visible
        global AllTracerData                                                        #   It may truncate/round values!
        AllTracerData = LoadStoredTracerData()                                      
        TracerDataLoaded = 1                                                                   
                                                                                               
    def GetTracerData(self):                                               
        
        self.LoadTracerData()
        if TracerDataLoaded == 0:
            print("Tracer data not yet loaded, call LoadTracerData(FileName) first")
            sys.exit()
        StartDate = -48050                                                          #   The start date can be changed to a younger value, like 1850, if desired
        EndDate = 2030                                                              #   -48050 is the end of the paleo 14C tracer data
        RowStartFound = 0
        RowEndFound = 0
        TracerData = []
        NumOfTracers = len(self.TracerName)
            

        if NumOfTracers == 1:                                                                      
            TracerColIndex = -99
        elif NumOfTracers > 1:
            TracerColIndex = np.zeros(NumOfTracers)
        else:
            print("Tracer Input function failed: Tracer input list is empty or weird")
            sys.exit()
            

        NPAllTracerData = np.array(AllTracerData, object)
        
                      
        for x in range(3,np.size(NPAllTracerData,0)):                              
            if StartDate == float(NPAllTracerData[x,0]):
                RowStartIndex = x+1
                RowStartFound = 1
            elif EndDate == float(NPAllTracerData[x,0]):
                RowEndIndex = x
                RowEndFound = 1
        if RowStartFound == 0:
            print("Date Start not found in loaded tracer data")
        if RowEndFound == 0:
            print("Date end not found in loaded tracer data")
        if RowStartFound == 0 or RowEndFound == 0:
            sys.exit()
        
        for x in range(np.size(NPAllTracerData,1)):                                                             
            if NumOfTracers == 1:                                                                                  
                if self.TracerName[0] == "3He(trit)":                                                           
                    self.TracerName[0] = "3H"
                    if self.TracerName[0] == NPAllTracerData[0,x] and self.TracerLoc[0] == NPAllTracerData[2,x]:
                        TracerColIndex = x
                    self.TracerName[0] = "3He(trit)"
                elif self.TracerName[0] == "3Ho":
                    self.TracerName[0] = "3H"
                    if self.TracerName[0] == NPAllTracerData[0,x] and self.TracerLoc[0] == NPAllTracerData[2,x]:
                        TracerColIndex = x
                    self.TracerName[0] = "3Ho"
                elif self.TracerName[0] == NPAllTracerData[0,x] and self.TracerLoc[0] == NPAllTracerData[2,x]:
                    TracerColIndex = x
                        
            else:
                for i in range(NumOfTracers):
                   
                    if self.TracerName[i] == "3He(trit)":
                        self.TracerName[i] = "3H"
                        if self.TracerName[i] == NPAllTracerData[0,x] and self.TracerLoc[i] == NPAllTracerData[2,x] and TracerColIndex[i] == 0:
                            TracerColIndex[i] = x
                        self.TracerName[i] = "3He(trit)"
                    elif self.TracerName[i] == "3Ho":
                        self.TracerName[i] = "3H"
                        if self.TracerName[i] == NPAllTracerData[0,x] and self.TracerLoc[i] == NPAllTracerData[2,x] and TracerColIndex[i] == 0:
                            TracerColIndex[i] = x
                        self.TracerName[i] = "3Ho"
                    elif self.TracerName[i] == NPAllTracerData[0,x] and self.TracerLoc[i] == NPAllTracerData[2,x] and TracerColIndex[i] == 0:
                        TracerColIndex[i] = x
        if (isinstance(TracerColIndex,int)):
            if int(TracerColIndex) == -99:
                print("Tracer data column not found, check TracerData input array ... are tracer name and location correct?")
                sys.exit()
        else:
            NotFound = 0
            for i in range(NumOfTracers):
                if TracerColIndex[i] == 0:
                    print("Tracer number ", i,"(",self.TracerName[i],") not found.")
                    NotFound = 1
            if NotFound == 1:
                sys.exit()
                            
                
        SelectedTracerData = np.zeros((RowStartIndex - RowEndIndex + 3, NumOfTracers+1), object)
        SelectedTracerData[0:3,0] = NPAllTracerData[0:3,0]
        SelectedTracerData[3:RowStartIndex - RowEndIndex+3,0] = NPAllTracerData[RowEndIndex:RowStartIndex,0]
            

        if NumOfTracers == 1:
            SelectedTracerData[0:3, 1] = NPAllTracerData[0:3,TracerColIndex]
            SelectedTracerData[3:RowStartIndex - RowEndIndex + 3, 1] = [float(i) for i in NPAllTracerData[RowEndIndex:RowStartIndex,TracerColIndex]]

        else:
            for x in range(NumOfTracers):
                SelectedTracerData[0:3,x+1] = NPAllTracerData[0:3,int(TracerColIndex[x])]
                SelectedTracerData[3:RowStartIndex - RowEndIndex + 3, x + 1] = [float(i) for i in NPAllTracerData[RowEndIndex:RowStartIndex,int(TracerColIndex[x])]]

            
            
            
        self.SelectedTracerData=SelectedTracerData
        
        #populate tracer input fields

        for x in self.TracerName:
            self.SampleTracerInput.Tracers.append(Tracer(x))

        self.SampleTracerInput.DateRange = SelectedTracerData[3:,0]
        self.SampleTracerInput.InputRange = SelectedTracerData[3:,1:len(SelectedTracerData)-1]
        self.SampleTracerInput.Location = SelectedTracerData[2,1:len(SelectedTracerData)-1]
        self.SampleTracerInput.TracerNum = NumOfTracers
        
    class TracerInput:

        def __init__(self):
            self.StoredTracerColumn = 0
            self.Location = np.array(object)
            self.Uppm = 2.75031                                             #   Default values for these parameters can be changed here if desired
            self.THppm = 9.7476                                             #   They can also be changed on the fly by accessing the Model object: Model.Sample.SampleTracerInput.Uppm, eg.
            self.Porosity = 0.2
            self.BulkDensity = 2.2
            self.HeSolnRate = 1.33764e-10
            self.DIC1 = 100.0
            self.DIC2 = 100.0
            self.TimeIncr = 0.0833333
            self.DateRange = np.array(object)
            self.InputRange = np.array(object)
            self.TracerNum = 0
            self.ScaleFact = 0.0
            self.Tracers = []
    

    

        

                
class Tracer:                                                   #   This is the class for each individual tracer found in the sample input
    global TracerParms                                          #   Lambda and tracer ID (for C++) are set here

    def __init__(self, Name):
        global TracerParmsLoaded

        self.Name = Name
        self.TracerNumber = 0
        self.MeasVal = -99.
        self.MeasValErr = -99.
        self.ParmCode = ''
        self.IsFitTracer = 0
        self.HalfLife = 0.0
        self.DecayConst = 0.0
        self.TracerType = 0             
        self.Order = 0
        self.Units = ''
        self.IsHe3 = 0
        self.Is3Ho = 0
        self.Is3H3Ho = 0
        self.UZTimeCond = 1
        self.UZTime = 0.0
        self.Ref = ''
        self.Descrip = ''
        self.TracerParmRow = -99
        

        if TracerParmsLoaded == 0:
            LoadTracerParms()
            TracerParmsLoaded = 1


        for x in range(len(TracerParms)):
            if self.Name == TracerParms[x][1]:
                self.TracerParmRow = x
        if self.TracerParmRow == -99:
            print("Could not find tracer in TracerParms.csv")
            sys.exit()


        self.HalfLife = TracerParms[self.TracerParmRow][3]

                                        

        if self.Name == '3H':
            self.TracerType = 1
        elif self.Name == '3He(trit)':
            self.TracerType = 2
            self.IsHe3 = 1
            self.Is3Ho = 0
            self.Is3H3Ho = 0
        elif self.Name == '3Ho':
            self.TracerType = 3
            self.IsHe3 = 0
            self.Is3Ho = 1
            self.Is3H3Ho = 0
        elif self.Name == '3H/3Ho':
            self.TracerType = 4
            self.IsHe3 = 0
            self.Is3Ho = 0
            self.Is3H3Ho = 1
        elif self.Name == '4He':
            self.TracerType = 5
        elif self.Name == '14C':
            self.TracerType = 6
        else:
            self.TracerType = 0
            self.IsHe3 = 0
            self.Is3Ho = 0
            self.Is3H3Ho = 0

        #   Set decay constant based on Half Life

        if float(self.HalfLife) > 0:
            #self.DecayConst = float(0.693/float(self.HalfLife))
            self.DecayConst = math.log(2)/float(self.HalfLife)
            
        else:
            self.DecayConst = 0

        
        if self.Name == ('3He(trit)' or '3Ho' or '3H/3Ho'):
            self.Name = '3H'
            self.Units = 'in TU'
    
    
    
    
            
             
 

 
class Model:                                                        #   All of the parameters and settings for the Model object, which is the primary functional unit of the class

    class ModelTracerInput:
        def __init__(self, TracerDateArray):
            self.TracerInputRange = [] 
            self.TracerInputRange = TracerDateArray
            

        def __getitem__(self, index):
            return self.TracerInputRange[index]

        def __iter__(self):
            self.x = 0
            return self

        def __next__(self):
            index = self.x
            self.x += 1

            return self.TracerInputRange[index]

    def __init__(self, Type):
        self.Name = Type                  
        self.NameShort = ''
        self.ID = 0                     
        self.NameComp1 = ''             
        self.IDComp1 = 0
        self.NameComp2 = '0'              
        self.IDComp2 = 0
        self.isBMM = 0
        self.isPEM = 0
        self.Index = 0
        self.IsMonteCarlo = 0
        self.IsMonteCarloDet = 0
        self.MonteCarloSims = 1
        self.IsTracerTracer = 0
        self.ModelParms = []
        self.ModelFits = []
        self.InitialVals = [0,0,0,0,0,0,0,0]
        self.LowBounds = [0,0,0,0,0,0,0,0]
        self.HiBounds = [0,0,0,0,0,0,0,0]
        self.Tracers = []
        self.ModelTracerConcs = []
        self.ModelTracerErrs = []
        self.Sample = None
        self.Solution = None
        self.TracerInputRange = []
        self.Index4He = 0
        self.IsTimeSeries = 0
        self.IsSolveSuccess = 0
        self.MonteCarloPath = ''
        self.AgeDist = np.array(float)
        self.TracerTracerArray = np.array([0,0,0],object)
        self.TracerArray = []
        self.origTracerArray = []
        self.origDateArray = []
        self.TracerArrayColID = []
        self.DateArray = []
        self.Lambda = []
        self.UZTime = []
        self.UZCond = []
        self.TimeStep = 0.083333
        self.TracerSetBool = 0
        self.TracerAlphas = []
        self.FitParmNames = []
        
        if len(self.Name) < 4:
            self.NameComp1 = self.Name
        elif len(self.Name) > 4:
            if self.Name.find('_') == -1:
                print("Binary mixture syntax missing underscore")
                sys.exit()
            self.NameComp1 = self.Name.split('_')[0]
            self.NameComp2 = self.Name.split('_')[1]
           

        #   Set Model ID based on Model Name
        
        if self.NameComp1 == 'PFM':
            self.ID = 1
            self.AddParm("UZ_TIME")
            self.AddParm("MEAN_AGE")
        elif self.NameComp1 == 'EMM':
            self.ID = 2
            self.AddParm("UZ_TIME")
            self.AddParm("MEAN_AGE")
        elif self.NameComp1 == 'EPM':
            self.ID = 3
            self.AddParm("UZ_TIME")
            self.AddParm("MEAN_AGE")
            self.AddParm("EPM_RATIO")
        elif self.NameComp1 == 'GAM':
            self.ID = 4
            self.AddParm("UZ_TIME")
            self.AddParm("MEAN_AGE")
            self.AddParm("SHAPE")
        elif self.NameComp1 == 'DM':
            self.ID = 5
            self.AddParm("UZ_TIME")
            self.AddParm("MEAN_AGE")
            self.AddParm("DISP_PARM")
        elif self.NameComp1 == 'PEM':
            self.ID = 6
            self.AddParm("UZ_TIME")
            self.AddParm("MEAN_AGE")
            self.AddParm("PEM_U_RATIO")
            self.AddParm("PEM_L_RATIO")
        elif self.NameComp1 == 'FDM':
            self.ID = 7
            self.AddParm("UZ_TIME")
            self.AddParm("MEAN_AGE")
            self.AddParm("ALPHA")
            self.AddParm("DISP_PARM")
        else: 
            self.ID = -99
            print("Error with model name")
            sys.exit()

        if self.NameComp2 != '0':                               # FOR BMMs
            self.isBMM = 1
            if self.NameComp2 == 'PFM':
                self.ID = self.ID * 10 + 1
                self.AddParm("MEAN_AGE_2")
                self.AddParm("FRACTION")
            elif self.NameComp2 == 'EMM':
                self.AddParm("MEAN_AGE_2")
                self.AddParm("FRACTION")
                self.ID = self.ID * 10 + 2
            elif self.NameComp1 == 'EPM':
                self.ID = self.ID * 10 + 3
                self.AddParm("MEAN_AGE_2")
                self.AddParm("EPM_RATIO_2")
                self.AddParm("FRACTION")
            elif self.NameComp1 == 'GAM':
                self.ID = self.ID * 10 + 4
                self.AddParm("MEAN_AGE_2")
                self.AddParm("ALPHA")
                self.AddParm("FRACTION")
            elif self.NameComp1 == 'DM':
                self.ID = self.ID * 10 + 5
                self.AddParm("MEAN_AGE_2")
                self.AddParm("DISP_PARM_2")
                self.AddParm("FRACTION")
            elif self.NameComp1 == 'PEM':                               
                self.ID = self.ID * 10 + 6
                self.AddParm("MEAN_AGE_2")
                self.AddParm("PEM_U_RATIO_2")
                self.AddParm("PEM_L_RATIO_2")
                self.AddParm("FRACTION")
            elif self.NameComp1 == 'FDM':
                self.ID = self.ID * 10 + 7
                self.AddParm("MEAN_AGE_2")
                self.AddParm("ALPHA_2")
                self.AddParm("DISP_PARM_2")
                self.AddParm("FRACTION")
            else: 
                self.ID = -99
                print("Error with second model name")
                sys.exit()

    def SetSample(self, SampleInputObj, SampleIndex):                               #   Function to choose which sample from sample input sheet will be associated with the model
        if not SampleIndex >=0:
            print("".join(['Sample ID (', SampleIndex ,') is not valid.']))
            sys.exit()
        else: self.Sample = SampleInputObj[SampleIndex-1]
        self.Index = SampleIndex-1
        if self.NameComp1 == "PEM":
            self.InitialVals[2] = self.Sample.PEM_Upper
            self.InitialVals[3] = self.Sample.PEM_Lower
        if self.NameComp2 == "PEM":
            self.InitialVals[6] = self.Sample.PEM_Upper
            self.InitialVals[7] = self.Sample.PEM_Lower

        
    def ChangeTimeStep(self, interval):                                             #   Change time step, options are 0.083 (actually will be set to 0.083333), 0.5, 0.25 or 1
        if self.TracerSetBool == 0:
            print("Select tracers before changing timestep")
            sys.exit(0)
        if interval == 0.25 or interval == 0.5 or interval == 1 or interval == 0.083:
            self.TimeStep = interval
            NewDateArray = []
            NewTracerArray = []
        else:
            print("Invalid time step. Options are 0.083, 0.25, 0.5 and 1")
            sys.exit()
        
        if self.TimeStep == 0.083:
            NewTracerArray = self.origTracerArray
            NewDateArray = self.origDateArray
        elif self.TimeStep == 0.25:
            count = 0
           
            for val in self.DateArray:
                if count % 3 == 0:
                    NewDateArray.append(val)
                count += 1
            for tracer in self.TracerArray:
                count = 1
                NewTracerArray.append([])
                TraceGlom = 0
                for val in tracer:
                    TraceGlom += val
                    if count % 3 == 0:
                        NewTracerArray[-1].append(TraceGlom/3)
                        TraceGlom = 0
                    count += 1
        
                ArrayLenDiff = len(NewDateArray) - len(NewTracerArray[-1])
                if ArrayLenDiff > 0:
                    for x in range (ArrayLenDiff):
                        NewTracerArray[-1].append(NewTracerArray[-1][-1])
                elif ArrayLenDiff < 0:
                    NewTracerArray[-1] = NewTracerArray[-1][:len(NewDateArray)]
            

        elif self.TimeStep == 0.5:
            count = 0
            for val in self.DateArray:
                if count % 6 == 0:
                    NewDateArray.append(val)
                count += 1
            for tracer in self.TracerArray:
                count = 1
                NewTracerArray.append([])
                TraceGlom = 0
                for val in tracer:
                    TraceGlom += val
                    if count % 6 == 0:
                        NewTracerArray[-1].append(TraceGlom/6)
                        TraceGlom = 0
                    count += 1
        
                ArrayLenDiff = len(NewDateArray) - len(NewTracerArray[-1])
                if ArrayLenDiff > 0:
                    for x in range (ArrayLenDiff):
                        NewTracerArray[-1].append(NewTracerArray[-1][-1])
                elif ArrayLenDiff < 0:
                    NewTracerArray[-1] = NewTracerArray[-1][:len(NewDateArray)]
                                
        elif self.TimeStep ==1:
            count = 0
            for val in self.DateArray:
                if count % 12 == 0:
                    NewDateArray.append(val)
                count += 1
            for tracer in self.TracerArray:
                count = 1
                NewTracerArray.append([])
                TraceGlom = 0
                for val in tracer:
                    TraceGlom += val
                    if count % 12 == 0:
                        NewTracerArray[-1].append(TraceGlom/12)
                        TraceGlom = 0
                    count += 1
        
                ArrayLenDiff = len(NewDateArray) - len(NewTracerArray[-1])
                if ArrayLenDiff > 0:
                    for x in range (ArrayLenDiff):
                        NewTracerArray[-1].append(NewTracerArray[-1][-1])
                elif ArrayLenDiff < 0:
                    NewTracerArray[-1] = NewTracerArray[-1][:len(NewDateArray)]

        self.DateArray = NewDateArray
        self.TracerArray = NewTracerArray
        
        print("".join(('Time step = ',str(self.TimeStep))))
        
    
    def TracerID(self, Name):                                               #   Lookup table to convert tracer name to tracer ID
        if Name == '3H':
            return 1
        elif Name == '3He(trit)':
            return 2
            
        elif Name == '3Ho':
            return 3
            
        elif Name == '3H/3Ho':
            return 4
            
        elif Name == '4He':
            return 5
        elif Name == '14C':
            return 6
        else:
            return 0

    def SetTracers(self, Tracers):                                                  #   Determine which tracers will be used in the model. If a chosen tracer doesn't have a measured concentration,
                                                                                    #   an error will be displayed.
        TracerInputHold = []
        
        TracerFound = 0
        valid = 0
        for sel in Tracers:
            tracerindex = 0
            for t in self.Sample.TracerName:
                if sel == t:
                    valid +=1
                    self.ModelTracerConcs.append(self.Sample.TracerConc[tracerindex])
                    self.ModelTracerErrs.append(self.Sample.TracerErr[tracerindex])
                    self.Lambda.append(self.Sample.SampleTracerInput.Tracers[tracerindex].DecayConst)
                    self.UZCond.append(self.Sample.SampleTracerInput.Tracers[tracerindex].UZTimeCond)
                    self.UZTime.append(self.Sample.SampleTracerInput.Tracers[tracerindex].UZTime)

                tracerindex += 1
        if valid < len(Tracers):
            print("One or more tracers not found in sample data -- check sample input file against tracers being set")
            sys.exit()

        
               
        TracerInputHold.append(0)
        if isinstance(Tracers,list):


            for ChosenTracer in Tracers:
                self.TracerAlphas.append(ChosenTracer)
                if TracerFound < len(Tracers):
                    for i in range(1,len(self.Sample.SelectedTracerData[0])):    
                        if ChosenTracer == "3He(trit)":
                            if "3H" == self.Sample.SelectedTracerData[0][i]:
                                self.Tracers.append(self.TracerID(ChosenTracer))
                                TracerInputHold.append(i)
                                TracerFound += 1
                                #print("i: ",i,"TracerFound: ",TracerFound,"ChosenTracer: ",ChosenTracer,self.TracerID(ChosenTracer), "Comp: ", self.Sample.SelectedTracerData[0][i])
                                break
                                       
                                
                        elif ChosenTracer == self.Sample.SelectedTracerData[0][i]:
                            self.Tracers.append(self.TracerID(ChosenTracer))
                            TracerInputHold.append(i)
                            TracerFound += 1
                            #print("i: ",i,"TracerFound: ",TracerFound,"ChosenTracer: ",ChosenTracer,self.TracerID(ChosenTracer), "Comp: ", self.Sample.SelectedTracerData[0][i])
                            break
                                
          
        elif isinstance(Tracers,str):
            self.TracerAlphas.append(Tracers)
            for i in range(1,len(self.Sample.SelectedTracerData[0])):
                if Tracers == "3He(trit)":
                        Tracers = "3H"
                        if Tracers == self.Sample.SelectedTracerData[0][i]:
                            self.Tracers.append(self.TracerID(Tracers))
                            TracerInputHold.append(i)
                            TracerFound += 1
                        Tracers = "3He(trit)"
                elif Tracers == self.Sample.SelectedTracerData[0][i]:
                        self.Tracers.append(self.TracerID(Tracers))
                        TracerInputHold.append(i)
                        TracerFound += 1
                    
        if (isinstance(Tracers,str) and TracerFound == 0) or (isinstance(Tracers,list) and TracerFound < len(Tracers)):
            print("".join(("Could not find selected tracers in sample.")))
            sys.exit()

        
        
            
        for j in TracerInputHold:
                
                
            self.TracerInputRange.append(self.Sample.SelectedTracerData[:,j])
                 
             
        self.TracerArray = []

        
        
        self.DateArray = [float(i) for i in self.TracerInputRange[0][3:]]
        for col in range(len(Tracers)):
            
            self.TracerArray.append([])
            self.TracerArrayColID.append(self.TracerID(self.TracerInputRange[col+1][0]))
            self.TracerArray[col]= [float(i) for i in self.TracerInputRange[col+1][3:]]
            
            

        
        self.TracerArray = np.asarray(self.TracerArray)
        self.origDateArray = self.DateArray
        self.origTracerArray = self.TracerArray
        self.TracerSetBool = 1
        
        
        
        


    class ModelParm:                                                            #   The Model object makes use of ModelParm to set initial value, lower and upper bounds,
                                                                                #   and identify which parameters will be fitted.
        def __init__(self, Name):
            self.Parm = Name
            self.ParmIndex = 0
            self.FittedVal = 0.0
            self.FittedErr = 0.0
            self.InitialVal = 0.0
            self.LowerBound = 0.0
            self.UpperBound = 0.0
            self.IsRange = 0
            self.RangeStep = 0.0
            self.IsFitParm = 0
            self.NameAlias = ''
            
            if self.Parm.upper() == ('UZ_TIME'):
                self.NameAlias = 'UZ Time'
                self.ParmIndex = 1
                self.UpperBound = 50
            elif self.Parm.upper() == 'MEAN_AGE' or self.Parm.upper() == 'MEAN AGE':
                self.NameAlias = 'Mean Age'
                self.ParmIndex = 2
                self.InitialVal = 50
                self.LowerBound = 0.1
                self.UpperBound = 100000
            elif self.Parm.upper() == 'EPM_RATIO' or self.Parm.upper() == 'MODEL_PARM_1' or self.Parm.upper() == 'PEM_U_RATIO' or self.Parm.upper() == 'SHAPE':
                self.NameAlias = 'Model Parm 1'
                self.ParmIndex = 3
                self.InitialVal = 0.5
                self.LowerBound = 0.001
                self.UpperBound = 10000
            elif self.Parm.upper() == ('DISP_PARM'):
                self.NameAlias = 'Model Parm 1'                                                         
                self.ParmIndex = 3
                self.InitialVal = 0.01
                self.LowerBound = 0.001
                self.UpperBound = 3
            elif self.Parm.upper() == 'MODEL_PARM_2' or self.Parm.upper() == 'PEM_L_RATIO':
                self.NameAlias = 'Model Parm 2'
                self.ParmIndex = 4
                self.InitialVal = 1
                self.UpperBound = 10000
            elif self.Parm.upper() == ('ALPHA'):
                self.NameAlias = 'Model Parm 2'
                self.ParmIndex = 4
                self.InitialVal = 1.5
                self.LowerBound = 1
                self.UpperBound = 2
            elif self.Parm.upper() == ('FRACTION'):
                self.NameAlias = 'Fraction'
                self.ParmIndex = 5
                self.InitialVal = 0.5
                self.UpperBound = 1
            elif self.Parm.upper() == '2ND_MEAN_AGE' or self.Parm.upper() == 'MEAN_AGE_2':
                self.NameAlias = '2nd Mean Age'
                self.ParmIndex = 6
                self.InitialVal = 500
                self.UpperBound = 100000
            elif self.Parm.upper() == '2ND_MODEL_PARM_1' or self.Parm.upper() == 'EPM_RATIO_2' or self.Parm.upper() == 'PEM_U_RATIO_2' or self.Parm.upper() == 'SHAPE_2':
                self.NameAlias = '2nd Model Parm 1'
                self.ParmIndex = 7
                self.InitialVal = 0.5
                self.LowerBound = 0.001
                self.UpperBound = 10000
            elif self.Parm.upper() == ('DISP_PARM_2'):
                self.NameAlias = '2nd Model Parm 1'
                self.ParmIndex = 7
                self.InitialVal = 0.01
                self.LowerBound = 0.001
                self.UpperBound = 3
            elif self.Parm.upper() == '2ND_MODEL_PARM_2' or self.Parm.upper() == 'PEM_L_RATIO_2' or self.Parm.upper() == 'ALPHA_2':
                self.NameAlias = '2nd Model Parm 2'
                self.ParmIndex = 8
                self.InitialVal = 1
                self.UpperBound = 10000
            elif self.Parm.upper() == ('ALPHA_2'):
                self.NameAlias = '2nd Model Parm 2'
                self.ParmIndex = 8
                self.InitialVal = 1.5
                self.LowerBound = 1
                self.UpperBound = 2
            else: 
                raise Exception("Model parm initialization error")

    def AddParm(self, Name):
        
        self.ModelParms.append(Model.ModelParm(Name))
        self.InitialVals[self.ModelParms[-1].ParmIndex-1] = self.ModelParms[-1].InitialVal
        self.LowBounds[self.ModelParms[-1].ParmIndex-1] = self.ModelParms[-1].LowerBound
        self.HiBounds[self.ModelParms[-1].ParmIndex-1] = self.ModelParms[-1].UpperBound
        
        
    def ParmLookup(self, IDs):                                                      #   Lookup table to convert between parameter ID and parameter name, primarily for output purposes
        
        ret_list = []
        for ID in IDs:
            if ID <1 or ID >8:
                print("Invalid Parm Index")
                sys.exit()
            elif ID == 1:
                ret_list.append("UZ TIME")
            elif ID == 2:
                ret_list.append("MEAN AGE")
            elif ID == 3:
                ret_list.append("MODEL PARM 1")
            elif ID == 4:
                ret_list.append("MODEL PARM 2")
            elif ID == 5:
                ret_list.append("FRACTION")
            elif ID == 6:
                ret_list.append("MEAN AGE 2")
            elif ID == 7:
                ret_list.append("2ND MODEL PARM 1")
            elif ID == 8:
                ret_list.append("2ND MODEL PARM 2")
        return ret_list

    def SetFitParms(self, ParmIndexes):
        self.ModelFits = []
        if isinstance(ParmIndexes, int):
            self.ModelFits.append(ParmIndexes+1)
        elif isinstance(ParmIndexes,list):
            for index in ParmIndexes:
                if index < 0 or index > 8:
                    print("Invalid Parm Index")
                    sys.exit()
                else:
                    self.ModelFits.append(index+1)
        else:
            print("Invalid fit parm index")
            sys.exit()
                

    
    def RunModel(self):
        
        
       
        
        print("".join(("Running sample ", self.Sample.SampleID, ", ", str(self.Sample.SampleDatFrac)," with model ",str(self.Name), " solving for: ", str([x for x in self.ParmLookup([y for y in self.ModelFits])]))))

        
        
        

        res = Solver.SolveNewtonMethodPy(self.ModelTracerConcs,                     #   This will call the solver (SolveNewtonMethod) from the TracerLPM_CPP_Library
                                  self.ModelTracerErrs,                             #   There are other solver options (GNLM, LevenbergMarquardt), but they haven't been
                                  self.Sample.SampleDate,                           #   rigorously tested. This functionality could be added in the future.
                                  self.ID,
                                  self.ModelFits,
                                  self.InitialVals,
                                  self.LowBounds,
                                  self.HiBounds,
                                  self.Tracers,                                       
                                  self.DateArray,
                                  self.TracerArray,
                                  self.Lambda,
                                  self.UZTime,
                                  self.UZCond,
                                  np.array([0,0,0,0],c.c_double),
                                  self.Sample.SampleTracerInput.DIC1,
                                  self.Sample.SampleTracerInput.DIC2,
                                  self.Sample.SampleTracerInput.Uppm,
                                  self.Sample.SampleTracerInput.THppm,
                                  self.Sample.SampleTracerInput.Porosity,
                                  self.Sample.SampleTracerInput.BulkDensity,
                                  self.Sample.SampleTracerInput.HeSolnRate,
                                  self.IsMonteCarlo,
                                  self.MonteCarloSims,
                                  0,
                                  '')
        
        self.Solution = ModelFits()
        ModParmCount = 0
        for i in self.ModelFits:
            if i > 0:
                self.Solution.SolvedModelParms.append(res[ModParmCount])
                self.Solution.SolvedModelParmsErr.append(res[ModParmCount+1])
                ModParmCount +=2
        self.Solution.ChiSqr = res[ModParmCount]
        self.Solution.ChiSqrProb = res[ModParmCount+1]
        self.Solution.HiTracer = res[ModParmCount+2]
        self.Solution.HiTracerErr = res[ModParmCount+3]
        self.Solution.NumOfIters = res[ModParmCount+4]
        self.Solution.SolveTime = res[ModParmCount+5]
        self.Solution.DateTime = datetime.datetime.now()
        
        print("".join(('Calculation completed at ',str(self.Solution.DateTime))))
        return res

    def GetAgeDist(self,  Tau):                                                                         #   This function may need some modification for full utility.
        if self.NameComp1 == "DM":                                                                      #   Currently it uses default initial values for the various parameters for each model,
            self.AgeDist = Solver.gt_DM(0,int(Tau+100), Tau, self.InitialVals[2],DMTest.InitialVals[0]) #   but manually editing the function here would allow for changing parameters, e.g. PEM ratios,
        elif self.NameComp1 == "EMM":                                                                   #   dispersion parameters, gamma alphas, etc.
            self.AgeDist = Solver.gt_EMM(0,int(Tau+100), Tau, self.InitialVals[0])                      #   Tau is mean age.
        elif self.NameComp1 == "EPM":
            self.AgeDist = Solver.gt_EPM(0,int(Tau+100), Tau, self.InitialVals[3],self.InitialVals[0])
        elif self.NameComp1 == "PFM":
            self.AgeDist = Solver.gt_PFM(0,int(Tau+100), Tau, self.InitialVals[0])
        elif self.NameComp1 == "PEM":
            self.AgeDist = Solver.gt_PEM(0,int(Tau+100), Tau, self.InitialVals[3],self.InitialVals[4],self.InitialVals[0])
        elif self.NameComp1 == "GAM":
            self.AgeDist = Solver.gt_GAM(0,int(Tau+100), Tau, self.InitialVals[4],self.InitialVals[0])
        elif self.NameComp1 == "FDM":
            self.AgeDist = Solver.gt_FDM(0,int(Tau+100), self.InitialVals[4], Tau, self.InitialVals[3],self.InitialVals[0])
        else:
            print("Model type not recognized...")
            sys.exit()
        return self.AgeDist

    def TracerOutput(self, tracer, MeanAge,MeanAge2, ModelParm1, ModelParm2, Fraction, ModelParm1_2, ModelParm2_2):
 
                                                                                                                    #   This function returns a tracer concentration array, given the tracer and relevant parameters.
                                                                                                                    #   It could be used as a standalone function, but is also called from the PopulateTracerTracerArrays
        col = -99                                                                                                   #   function to produce three arrays for plotting.

        for i in range(len(self.TracerAlphas)):
           
            if tracer == self.TracerAlphas[i] and col == -99:
               
                col = i
                if tracer == "3He(trit)":
                    decay = 0
                else:
                    decay = self.Lambda[col]
                break
        
        if col == -99:
            print("TracerOutput: Couldn't find chosen tracer in tracer input ")
            sys.exit()
        
        res = Solver.TracerOutput(float(self.Sample.SampleDate),(self.ID%10),self.TracerID(tracer),self.DateArray,self.TracerArray[col],decay,
                            self.Sample.SampleTracerInput.Tracers[col].UZTime,self.Sample.SampleTracerInput.Tracers[col].UZTimeCond,0,#tracer_comp_2
                            self.Sample.SampleTracerInput.DIC1,self.Sample.SampleTracerInput.DIC2,self.Sample.SampleTracerInput.Uppm, self.Sample.SampleTracerInput.THppm,
                            self.Sample.SampleTracerInput.Porosity,self.Sample.SampleTracerInput.BulkDensity,self.Sample.SampleTracerInput.HeSolnRate,
                            MeanAge, MeanAge2, ModelParm1, ModelParm2, Fraction, ModelParm1_2, ModelParm2_2)
        
        return res     

    def PopulateTracerTracerArrays(self,tracer1,tracer2,MeanAge2,ModelParm1, ModelParm2, Fraction, ModelParm1_2, ModelParm2_2):             #   Populates three arrays, [0] = tracer 1, [1] = tracer 2, [2] = age in  years
        xArray = []
        yArray = []
        zArray = []
        TracerOutputReturn = []
        for i in range(1,10001):
            if i<100 or i == 500 or i==1000 or i==10000:
                
                TracerOutputReturn = self.TracerOutput(tracer1,i,MeanAge2,ModelParm1, ModelParm2, Fraction, ModelParm1_2, ModelParm2_2)
                
                xArray.append(TracerOutputReturn[0])
                TracerOutputReturn = self.TracerOutput(tracer2,i,MeanAge2,ModelParm1, ModelParm2, Fraction, ModelParm1_2, ModelParm2_2)
                
                yArray.append(TracerOutputReturn[0])
        
            zArray.append(i)             
        self.TracerTracerArray[0] = xArray
        self.TracerTracerArray[1] = yArray
        self.TracerTracerArray[2] = zArray

    

    def SetParm(self,index, val):                                                       #   This function will change the initial value of a parameter
        if index >= 0:
            self.InitialVals[index] = val
        else:
            print("Invalid index (<0)")
            sys.exit()
        
class ModelFits:                                                                        #   This class contains the solution values after the model is run



    def __init__(self):
        self.SolvedModelParms = []
        self.SolvedModelParmsErr = []
        self.ChiSqr = 0.0
        self.ChiSqrProb = 0.0
        self.SolveTime = 0.0
        self.NumOfIters = 0
        self.DateTime = 0.0
        self.HiTracer = ''
        self.HiTracerErr = 0.0
        
        
        
        
        



def LoadStoredTracerData():                                                 #   Function to load stored tracer data
                                                                            #   Tracer Data must be in csv format,  -- see file (StoredTracerData.csv) 
    try:                                                                    #   This is not meant to be changed often, but filename can be changed here if needed.
        f = open('StoredTracerData.csv')                                    #   Note: saving in excel's UTF-8 csv format will cause weirdness, use plain csv format
    except Exception as e:
        print(e)
        sys.exit()

    with open('StoredTracerData.csv') as csv_file:
        TracerDataCSV = csv.reader(csv_file, delimiter = ',')               #   Indexing is TracerData[row][column]
        TracerData = list(TracerDataCSV)

    
    return TracerData
    
def LoadTracerParms():                                                      #   Loads half life data and units for tracers
    global TracerParms
    try:                                                   
        f = open('TracerParms.csv')
    except Exception as e:
        print(e)
        sys.exit()

    with open('TracerParms.csv') as csv_file:
        TracerParmsCSV = csv.reader(csv_file, delimiter = ',')              
        TracerParms = list(TracerParmsCSV)


def SetOutput(filename, outputname):                                        #   Sets up solution output file. Call this only to create a new output file, and must be called before WriteOut works.
    global outfile                                                          #   !!! It will overwrite existing file of the same name !!!
    
    with open(filename, 'w') as csvfile:
        filewriter = csv.writer(csvfile,delimiter=',')
        filewriter.writerow([outputname])
        filewriter.writerow(["ID","ID","ID","ID","ID","Initial","Initial","Initial","Initial","Initial","Initial","Initial","Initial","Solution", "Solution","Solution","Solution","Solution","Solution","Solution","Solution"])
        filewriter.writerow(["Model Name","Date/Time Model Run","Sample ID","Sample Date","Tracers Modeled", "UZ Time","Mean Age", "Model Parm 1", "Model Parm 2", "Fraction", "2nd Mean Age", 
                             "2nd Model Parm 1", "2nd Model Parm 2","Chi Sqr", "Chi Sqr Probability", "Hi Tracer", "Hi Tracer Err","Solved Model Parms","Solved Model Parms","Solved Model Parm Errs","Num iterations","Solve Time"])

    outfile = filename

def WriteOut(modelout):                                                     #   Write a solution to the output file. This is not necessary, but useful for batch processing.
    global outfile                                                          #   Solution data is also stored in array format in the Solution object of the Model object.
    try:
        f = open(outfile)
    except Exception as e:
        print(e)
        sys.exit()
    with open(outfile, 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile,delimiter=',')
        
        filewriter.writerow([modelout.Name,modelout.Solution.DateTime,modelout.Sample.SampleID,modelout.Sample.SampleDatFrac,modelout.TracerAlphas,modelout.InitialVals[0],modelout.InitialVals[1],modelout.InitialVals[2],modelout.InitialVals[3],
                             modelout.InitialVals[4],modelout.InitialVals[5],modelout.InitialVals[6],modelout.InitialVals[7],modelout.Solution.ChiSqr,modelout.Solution.ChiSqrProb,modelout.TracerAlphas[int(modelout.Solution.HiTracer)],modelout.Solution.HiTracerErr,
                             [x for x in modelout.ParmLookup([y for y in modelout.ModelFits])],[x for x in modelout.Solution.SolvedModelParms],[x for x in modelout.Solution.SolvedModelParmsErr],modelout.Solution.NumOfIters,modelout.Solution.SolveTime])

    
def TracerTracerWrite(mod, filename):                                       #   This function creates a csv file with row 1 = tracer 1 concentration array, row 2 = tracer 2 concentration array, row 3 = age in year array
    
    with open(filename, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile,delimiter=',')
        filewriter.writerow(mod.TracerTracerArray[0])
        filewriter.writerow(mod.TracerTracerArray[1])
        filewriter.writerow(mod.TracerTracerArray[2])

