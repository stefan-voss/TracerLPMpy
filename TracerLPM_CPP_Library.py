import math, ctypes, csv
from ctypes import *
import numpy as np
from numpy.ctypeslib import ndpointer
import matplotlib.pyplot as plt


_doublepp = ndpointer(dtype=np.uintp,ndim=1,flags='C')
libc = CDLL('Py_TracerLPM.dll')


Call_TracerOutput = libc.LPM_TracerOutput
Call_TracerOutput.argtypes      = [c_double, c_int, c_int, ndpointer(c_double), c_int, #nDateRange
                                ndpointer(c_double), c_int, c_double, c_double, c_double, #lxUZtimeCond
                                c_double, c_double, c_double, c_double, c_double,         #THppm
                                c_double, c_double, c_double, c_double, c_double,         #MeanAge_2
                                c_double, c_double, c_double, c_double, c_double]
Call_TracerOutput.restype = POINTER(c_double)


Call_SolveNewtonMethod = libc.SolveNewtonMethod
Call_SolveNewtonMethod.argtypes = [ndpointer(c_double),ndpointer(c_double),c_int,ndpointer(c_double),c_int, c_int, ndpointer(c_double), c_int,#nFitParmIndexes
                              ndpointer(c_double),c_int,ndpointer(c_double),c_int,ndpointer(c_double),c_int,ndpointer(c_double),c_int,#nTracers
                              ndpointer(c_double),c_int,_doublepp,c_int,c_int,ndpointer(c_double),c_int,ndpointer(c_double),c_int,#nUzTime
                              ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double,c_double,#THppm
                              c_double,c_double,c_double,c_int,c_int,c_int,c_char_p, POINTER(c_int)]
Call_SolveNewtonMethod.restype = POINTER(c_double)

Call_Levenberg = libc.SolveLevenbergMarquardt
Call_Levenberg.argtypes = [ndpointer(c_double),ndpointer(c_double),c_int,ndpointer(c_double),c_int, c_int, ndpointer(c_double), c_int,#nFitParmIndexes
                              ndpointer(c_double),c_int,ndpointer(c_double),c_int,ndpointer(c_double),c_int,ndpointer(c_double),c_int,#nTracers
                              ndpointer(c_double),c_int,_doublepp,c_int,c_int,ndpointer(c_double),c_int,ndpointer(c_double),c_int,#nUzTime
                              ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double,c_double,#THppm
                              c_double,c_double,c_double,c_int,c_int,c_int,c_char_p, POINTER(c_int)]
Call_Levenberg.restype = POINTER(c_double)

Call_GNLM = libc.SolveGNLM
Call_GNLM.argtypes = [ndpointer(c_double),ndpointer(c_double),c_int,ndpointer(c_double),c_int, c_int, ndpointer(c_double), c_int,#nFitParmIndexes
                              ndpointer(c_double),c_int,ndpointer(c_double),c_int,ndpointer(c_double),c_int,ndpointer(c_double),c_int,#nTracers
                              ndpointer(c_double),c_int,_doublepp,c_int,c_int,ndpointer(c_double),c_int,ndpointer(c_double),c_int,#nUzTime
                              ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double,c_double,#THppm
                              c_double,c_double,c_double,c_int,c_int,c_int,c_char_p, POINTER(c_int)]
Call_GNLM.restype = POINTER(c_double)




Call_gt_EMM = libc.gt_EMM
Call_gt_EMM.argtypes = [c_double, c_double, c_double, c_double]
Call_gt_EMM.restype = c_double

Call_gt_DM = libc.gt_DM
Call_gt_DM.argtypes = [c_double, c_double, c_double, c_double, c_double]
Call_gt_DM.restype = c_double

Call_gt_EPM = libc.gt_EPM
Call_gt_EPM.argtypes = [c_double, c_double, c_double, c_double, c_double]
Call_gt_EPM.restype = c_double

Call_gt_FDM = libc.gt_FDM
Call_gt_FDM.argtypes = [c_double, c_double, c_double, c_double, c_double]
Call_gt_FDM.restype = c_double

Call_gt_GAM = libc.gt_GAM
Call_gt_GAM.argtypes = [c_double, c_double, c_double, c_double, c_double]
Call_gt_GAM.restype = c_double

Call_gt_PEM = libc.gt_PEM
Call_gt_PEM.argtypes = [c_double, c_double, c_double, c_double, c_double, c_double]
Call_gt_PEM.restype = c_double

Call_gt_PFM = libc.gt_PFM
Call_gt_PFM.argtypes = [c_double, c_double, c_double, c_double]
Call_gt_PFM.restype = c_double

Call_DM = libc.DM
Call_DM.argtypes = [ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double,c_double, c_double, c_int,c_int,c_int]
Call_DM.restype = c_double

Call_DM_He4 = libc.DM_He4
Call_DM_He4.argtypes = [c_double,c_double,c_double,c_double,c_double,c_double,c_double]
Call_DM_He4.restype = c_double

Call_EMM = libc.EMM
Call_EMM.argtypes = [ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double, c_double, c_int,c_int,c_int]
Call_EMM.restype = c_double

Call_EMM_He4 = libc.EMM_He4
Call_EMM_He4.argtypes = [c_double,c_double,c_double,c_double,c_double,c_double]
Call_EMM_He4.restype = c_double

Call_EPM = libc.EPM
Call_EPM.argtypes = [ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double,c_double, c_double, c_int,c_int,c_int]
Call_EPM.restype = c_double

Call_EPM_He4 = libc.EPM_He4
Call_EPM_He4.argtypes = [c_double,c_double,c_double,c_double,c_double,c_double,c_double]
Call_EPM_He4.restype = c_double

Call_FDM = libc.FDM
Call_FDM.argtypes = [ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double,c_double,c_double, c_double, c_int,c_int,c_int]
Call_FDM.restype = c_double

Call_GAM = libc.GAM
Call_GAM.argtypes = [ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double,c_double, c_double, c_int,c_int,c_int]
Call_GAM.restype = c_double

Call_GAM_He4 = libc.GAM_He4
Call_GAM_He4.argtypes = [c_double,c_double,c_double,c_double,c_double,c_double,c_double]
Call_GAM_He4.restype = c_double

Call_PEM = libc.PEM
Call_PEM.argtypes = [ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double,c_double,c_double, c_double, c_int,c_int,c_int]
Call_PEM.restype = c_double

Call_PEM_He4 = libc.PEM_He4
Call_PEM_He4.argtypes = [c_double,c_double,c_double,c_double,c_double, c_double,c_double,c_double]
Call_PEM_He4.restype = c_double

Call_PFM = libc.PFM
Call_PFM.argtypes = [ndpointer(c_double),c_int,ndpointer(c_double),c_int,c_double,c_double,c_double, c_double, c_int,c_int,c_int]
Call_PFM.restype = c_double

Call_PFM_He4 = libc.PFM_He4
Call_PFM_He4.argtypes = [c_double,c_double,c_double,c_double,c_double,c_double]
Call_PFM_He4.restype = c_double

def gt_EMM(MinAge, MaxAge, Tau, UZtime):
    #double MinAge, double MaxAge, double Tau, double UZtime
    result_array = np.array(np.zeros(int(MaxAge-MinAge)),c_double)
    
    x_array = np.array(np.zeros(MaxAge-MinAge),c_double)

    for i in range(MinAge, MaxAge):
        result_array[i-MinAge] = Call_gt_EMM(c_double(i-MinAge),c_double(i+1-MinAge),c_double(Tau),c_double(UZtime))
        x_array[i] = i+0.5
    
    plt.plot(x_array,result_array)
    plt.suptitle("".join(('Exponential Model, ',str(MinAge),' - ', str(MaxAge),' Years, Mean Age = ',str(np.around(Tau,2)),' years')))
    plt.xlabel('Years')
    plt.ylabel('Fraction')
    plt.legend()
    
    plt.show()
    
    return result_array

def gt_DM(MinAge, MaxAge, Tau, DP, UZtime):
    #double MinAge, double MaxAge, double Tau, double DP, double UZtime
    result_array = np.array(np.zeros(MaxAge-MinAge),c_double)
    
    x_array = np.array(np.zeros(MaxAge-MinAge),c_double)

    for i in range(MinAge, MaxAge):
        result_array[i-MinAge] = Call_gt_DM(c_double(i-MinAge),c_double(i+1-MinAge),c_double(Tau),c_double(DP),c_double(UZtime))
        x_array[i] = i+0.5
    
    plt.plot(x_array,result_array, label="".join(('DP = ',str(DP))))
    plt.suptitle("".join(('Dispersion Model, ',str(MinAge),' - ', str(MaxAge),' Years, Mean Age = ',str(np.around(Tau,2)),' years')))
    plt.xlabel('Years')
    plt.ylabel('Fraction')
    plt.legend()
    
    plt.show()
    
    return result_array

def gt_EPM(MinAge, MaxAge, Tau, EPM, UZtime):
    #double MinAge, double MaxAge,	double Tau, double EPMratio, double UZtime)
    result_array = np.array(np.zeros(MaxAge-MinAge),c_double)
    
    x_array = np.array(np.zeros(MaxAge-MinAge),c_double)

    for i in range(MinAge, MaxAge):
        result_array[i-MinAge] = Call_gt_EPM(c_double(i-MinAge),c_double(i+1-MinAge),c_double(Tau),c_double(EPM),c_double(UZtime))
        x_array[i] = i+0.5
    
    plt.plot(x_array,result_array, label="".join(('EPM ratio = ',str(EPM))))
    plt.suptitle("".join(('Exponential-Piston Flow Model, ',str(MinAge),' - ', str(MaxAge),' Years, Mean Age = ',str(np.around(Tau)),' years')))
    plt.xlabel('Years')
    plt.ylabel('Fraction')
    plt.legend()
    
    plt.show()
    
    return result_array
    


    

def gt_FDM(MinAge, MaxAge, Alpha, Tau, DP , UZtime):
    #double MinAge, double MaxAge, double Alpha, double Tau, double DP, double UZtime)
    result_array = np.array(np.zeros(MaxAge-MinAge),c_double)
    
    x_array = np.array(np.zeros(MaxAge-MinAge),c_double)

    for i in range(MinAge, MaxAge):
        result_array[i-MinAge] = Call_gt_FDM(c_double(i-MinAge),c_double(i+1-MinAge),c_double(Alpha),c_double(Tau),c_double(DP),c_double(UZtime))
        x_array[i] = i+0.5
    
    plt.plot(x_array,result_array, label="".join(('Alpha = ',str(Alpha),'; DP = ',str(DP))))
    plt.suptitle("".join(('FD Model, ',str(MinAge),' - ', str(MaxAge),' Years, Mean Age = ',str(np.around(Tau,2)),' years')))
    plt.xlabel('Years')
    plt.ylabel('Fraction')
    plt.legend()
    
    plt.show()
    
    return result_array

    

def gt_GAM(MinAge, MaxAge, Tau, Alpha, UZtime):
    #double MinAge, double MaxAge, double Tau, double Alpha, double UZtime
    result_array = np.array(np.zeros(MaxAge-MinAge),c_double)
    
    x_array = np.array(np.zeros(MaxAge-MinAge),c_double)

    for i in range(MinAge, MaxAge):
        result_array[i-MinAge] = Call_gt_GAM(c_double(i-MinAge),c_double(i+1-MinAge),c_double(Tau),c_double(Alpha),c_double(UZtime))
        x_array[i] = i+0.5
    
    plt.plot(x_array,result_array, label="".join(('Alpha = ',str(Alpha))))
    plt.suptitle("".join(('Gamma Model, ',str(MinAge),' - ', str(MaxAge),' Years, Mean Age = ',str(np.around(Tau,2)),' years')))
    plt.xlabel('Years')
    plt.ylabel('Fraction')
    plt.legend()
    
    plt.show()
    
    return result_array

    


    
def gt_PEM(MinAge, MaxAge, Tau, Urat, Lrat, UZtime):
    #double MinAge, double MaxAge, double Tau, double PEM_Uratio, double PEM_Lratio, double UZtime
    result_array = np.array(np.zeros(MaxAge-MinAge),c_double)
    
    x_array = np.array(np.zeros(MaxAge-MinAge),c_double)

    for i in range(MinAge, MaxAge):
        result_array[i-MinAge] = Call_gt_DM(c_double(i-MinAge),c_double(i+1-MinAge),c_double(Tau),c_double(Urat),c_double(Lrat),c_double(UZtime))
        x_array[i] = i+0.5
    
    plt.plot(x_array,result_array, label="".join(('Upper = ',str(Urat),'; Lower = ',str(Lrat))))
    plt.suptitle("".join(('Partial Exponential Model, ',str(MinAge),' - ', str(MaxAge),' Years, Mean Age = ',str(np.around(Tau,2)),' years')))
    plt.xlabel('Years')
    plt.ylabel('Fraction')
    plt.legend()
    
    plt.show()
    
    return result_array

#TracerTracer Plot 3H He3

def gt_PFM(MinAge, MaxAge, Tau, UZtime):
    #double MinAge, double MaxAge, double Tau, double UZtime
    result_array = np.array(np.zeros(int(MaxAge-MinAge)),c_double)
    
    x_array = np.array(np.zeros(MaxAge-MinAge),c_double)

    for i in range(MinAge, MaxAge):
        result_array[i-MinAge] = Call_gt_PFM(c_double(i-MinAge),c_double(i+1-MinAge),c_double(Tau),c_double(UZtime))
        x_array[i] = i+0.5
    
    plt.plot(x_array,result_array)
    plt.suptitle("".join(('Piston Flow Model, ',str(MinAge),' - ', str(MaxAge),' Years, Mean Age = ',str(np.around(Tau)),' years')))
    plt.xlabel('Years')
    plt.ylabel('Fraction')
    plt.legend()
    
    plt.show()
    
    return result_array

def DM():
    #double* DateRange, int lenDateRange, double* TracerRange, int lenTracerRange, double Tau, double SampleDate,
	#double Lambda, double DP, double UZtime, int HeliumThree, int InitialTrit, int TritInitialTritRatio

    lxTracerInputRange = np.array(Get2DTracerLPMInput("dTracerInputData.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)

    lxtracershape = lxTracerInputRange.shape
    TracerRange = np.array(np.zeros(lxtracershape[0]),c_double)
    nTracers = TracerRange.size
    nSampleDates = lxSampleDates.size

    for x in range(nTracers):
        TracerRange[x] = lxTracerInputRange[x,0]

    MeanAge = 30
    SampleDate = 1985.79726027397
    Lambda = 1.62E-02
    DP = 0.01
    UZtime = 0
    HeliumThree = 0
    InitialTrit = 0
    TritInitialTritRatio = 0

    Result = Call_DM(lxSampleDates,
                        c_int(nSampleDates),
                        TracerRange,
                        c_int(nTracers),
                        c_double(MeanAge),
                        c_double(SampleDate),
                        c_double(Lambda),
                        c_double(DP),
                        c_double(UZtime),
                        c_int(HeliumThree),
                        c_int(InitialTrit),
                        c_int(TritInitialTritRatio))

    print (Result)


def DM_He4():
    #(double Uppm, double THppm, double Porosity, double SedDensity, double Tau, double DP, double HeSolnRate

    Uppm = 0.1
    THppm = 0.9
    Porosity = 0.01
    SedDensity = 0.001
    MeanAge = 30
    DP = 0.01
    HeSolnRate = 0
    Result = -99
    Result = Call_DM_He4(Uppm,
                THppm,
                Porosity,
                SedDensity,
                MeanAge,
                DP,
                HeSolnRate)

    print (Result)

def EMM():
    #double* DateRange, int lenDateRange, double* TracerRange, int lenTracerRange, double Tau, double SampleDate,
	#double Lambda, double UZtime, int HeliumThree, int InitialTrit, int TritInitialTritRatio

    lxTracerInputRange = np.array(Get2DTracerLPMInput("dTracerInputData.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)

    lxtracershape = lxTracerInputRange.shape
    TracerRange = np.array(np.zeros(lxtracershape[0]),c_double)
    nTracers = TracerRange.size
    nSampleDates = lxSampleDates.size

    for x in range(nTracers):
        TracerRange[x] = lxTracerInputRange[x,0]

    MeanAge = 30
    SampleDate = 1985.79726027397
    Lambda = 1.62E-02
    UZtime = 0
    HeliumThree = 0
    InitialTrit = 0
    TritInitialTritRatio = 0

    Result = Call_EMM(lxSampleDates,
                        c_int(nSampleDates),
                        TracerRange,
                        c_int(nTracers),
                        c_double(MeanAge),
                        c_double(SampleDate),
                        c_double(Lambda),
                        c_double(UZtime),
                        c_int(HeliumThree),
                        c_int(InitialTrit),
                        c_int(TritInitialTritRatio))

    print (Result)


def EMM_He4():
    #double Uppm, double THppm, double Porosity, double SedDensity, double Tau, double HeSolnRate
    Uppm = 0.1
    THppm = 0.9
    Porosity = 0.01
    SedDensity = 0.001
    MeanAge = 30
    HeSolnRate = 0
    Result = -99
    Result = Call_EMM_He4(Uppm,
                THppm,
                Porosity,
                SedDensity,
                MeanAge,
                HeSolnRate)

    print (Result)



def EPM():
    #double* DateRange, int lenDateRange, double* TracerRange, int lenTracerRange, double Tau, double SampleDate,
	#double Lambda, double EPMratio, double UZtime, int HeliumThree, int InitialTrit, int TritInitialTritRatio)


    lxTracerInputRange = np.array(Get2DTracerLPMInput("dTracerInputData.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)

    lxtracershape = lxTracerInputRange.shape
    TracerRange = np.array(np.zeros(lxtracershape[0]),c_double)
    nTracers = TracerRange.size
    nSampleDates = lxSampleDates.size

    for x in range(nTracers):
        TracerRange[x] = lxTracerInputRange[x,0]

    MeanAge = 30
    SampleDate = 1985.79726027397
    Lambda = 1.62E-02
    EPMratio = 0.3
    UZtime = 0
    HeliumThree = 0
    InitialTrit = 0
    TritInitialTritRatio = 0

    Result = Call_EPM(lxSampleDates,
                        c_int(nSampleDates),
                        TracerRange,
                        c_int(nTracers),
                        c_double(MeanAge),
                        c_double(SampleDate),
                        c_double(Lambda),
                        c_double(EPMratio),
                        c_double(UZtime),
                        c_int(HeliumThree),
                        c_int(InitialTrit),
                        c_int(TritInitialTritRatio))

    print (Result)


def EPM_He4():
    #	double Uppm, double THppm, double Porosity, double SedDensity, double Tau, double EPMratio, double HeSolnRate
    Uppm = 0.1
    THppm = 0.9
    Porosity = 0.01
    SedDensity = 0.001
    MeanAge = 30
    EPMratio = 0.3
    HeSolnRate = 0
    Result = -99
    Result = Call_EMM_He4(Uppm,
                THppm,
                Porosity,
                SedDensity,
                MeanAge,
                EPMratio,
                HeSolnRate)

    print (Result)




def FDM():
    #double* DateRange, int lenDateRange, double* TracerRange, int lenTracerRange, double Tau, double SampleDate, double Lambda,
	#double Alpha, double DP, double UZtime, int HeliumThree, int InitialTrit, int TritInitialTritRatio

    lxTracerInputRange = np.array(Get2DTracerLPMInput("dTracerInputData.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)

    lxtracershape = lxTracerInputRange.shape
    TracerRange = np.array(np.zeros(lxtracershape[0]),c_double)
    nTracers = TracerRange.size
    nSampleDates = lxSampleDates.size

    for x in range(nTracers):
        TracerRange[x] = lxTracerInputRange[x,0]

    MeanAge = 30
    SampleDate = 1985.79726027397
    Lambda = 1.62E-02
    Alpha = 0.3
    DP = 0.01
    UZtime = 0
    HeliumThree = 0
    InitialTrit = 0
    TritInitialTritRatio = 0

    Result = Call_FDM(lxSampleDates,
                        c_int(nSampleDates),
                        TracerRange,
                        c_int(nTracers),
                        c_double(MeanAge),
                        c_double(SampleDate),
                        c_double(Lambda),
                        c_double(Alpha),
                        c_double(DP),
                        c_double(UZtime),
                        c_int(HeliumThree),
                        c_int(InitialTrit),
                        c_int(TritInitialTritRatio))

    print (Result)



def GAM():
    #double* DateRange, int lenDateRange, double* TracerRange, int lenTracerRange, double Tau, double SampleDate, 
	#double Lambda, double Alpha, double UZtime, bool HeliumThree, bool InitialTrit, bool TritInitialTritRatio

    lxTracerInputRange = np.array(Get2DTracerLPMInput("dTracerInputData.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)

    lxtracershape = lxTracerInputRange.shape
    TracerRange = np.array(np.zeros(lxtracershape[0]),c_double)
    nTracers = TracerRange.size
    nSampleDates = lxSampleDates.size

    for x in range(nTracers):
        TracerRange[x] = lxTracerInputRange[x,0]

    MeanAge = 30
    SampleDate = 1985.79726027397
    Lambda = 1.62E-02
    Alpha = 0.3
    UZtime = 0
    HeliumThree = 0
    InitialTrit = 0
    TritInitialTritRatio = 0

    Result = Call_GAM(lxSampleDates,
                        c_int(nSampleDates),
                        TracerRange,
                        c_int(nTracers),
                        c_double(MeanAge),
                        c_double(SampleDate),
                        c_double(Lambda),
                        c_double(Alpha),
                        c_double(UZtime),
                        c_int(HeliumThree),
                        c_int(InitialTrit),
                        c_int(TritInitialTritRatio))

    print (Result)



def GAM_He4():
    #double Uppm, double THppm, double Porosity, double SedDensity, double Tau, double Alpha, double HeSolnRate

    Uppm = 0.1
    THppm = 0.9
    Porosity = 0.01
    SedDensity = 0.001
    MeanAge = 30
    Alpha = 0.3
    HeSolnRate = 0
    Result = -99
    Result = Call_GAM_He4(Uppm,
                THppm,
                Porosity,
                SedDensity,
                MeanAge,
                Alpha,
                HeSolnRate)

    print (Result)


def PEM():
    #double* DateRange, int lenDateRange, double* TracerRange, int lenTracerRange, double Tau, double SampleDate,	
	#double Lambda, double PEM_Uratio, double PEM_Lratio, double UZtime, int HeliumThree, int InitialTrit, int TritInitialTritRatio)

    lxTracerInputRange = np.array(Get2DTracerLPMInput("dTracerInputData.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)

    lxtracershape = lxTracerInputRange.shape
    TracerRange = np.array(np.zeros(lxtracershape[0]),c_double)
    nTracers = TracerRange.size
    nSampleDates = lxSampleDates.size

    for x in range(nTracers):
        TracerRange[x] = lxTracerInputRange[x,0]

    MeanAge = 30
    SampleDate = 1985.79726027397
    Lambda = 1.62E-02
    URatio = 0.3
    LRatio = 0.2
    UZtime = 0
    HeliumThree = 0
    InitialTrit = 0
    TritInitialTritRatio = 0

    Result = Call_PEM(lxSampleDates,
                        c_int(nSampleDates),
                        TracerRange,
                        c_int(nTracers),
                        c_double(MeanAge),
                        c_double(SampleDate),
                        c_double(Lambda),
                        c_double(URatio),
                        c_double(LRatio),
                        c_double(UZtime),
                        c_int(HeliumThree),
                        c_int(InitialTrit),
                        c_int(TritInitialTritRatio))

    print (Result)



def PEM_He4():
    #double Uppm, double THppm, double Porosity, double SedDensity, double Tau, double PEM_Uratio, 
	#double PEM_Lratio, double HeSolnRate

    Uppm = 0.1
    THppm = 0.9
    Porosity = 0.01
    SedDensity = 0.001
    MeanAge = 30
    URatio = 0.3
    LRatio = 0.2
    HeSolnRate = 0
    Result = -99
    Result = Call_PEM_He4(Uppm,
                THppm,
                Porosity,
                SedDensity,
                MeanAge,
                URatio,
                LRatio,
                HeSolnRate)

    print (Result)



def PFM():
    #double* DateRange, int lenDateRange, double* TracerRange, int lenTracerRange, double Tau, double SampleDate,
	#double Lambda, double UZtime, int HeliumThree, int InitialTrit, int TritInitialTritRatio

    lxTracerInputRange = np.array(Get2DTracerLPMInput("dTracerInputData.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)

    lxtracershape = lxTracerInputRange.shape
    TracerRange = np.array(np.zeros(lxtracershape[0]),c_double)
    nTracers = TracerRange.size
    nSampleDates = lxSampleDates.size

    for x in range(nTracers):
        TracerRange[x] = lxTracerInputRange[x,0]

    MeanAge = 30
    SampleDate = 1985.79726027397
    Lambda = 1.62E-02
    UZtime = 0
    HeliumThree = 0
    InitialTrit = 0
    TritInitialTritRatio = 0

    Result = Call_PFM(lxSampleDates,
                        c_int(nSampleDates),
                        TracerRange,
                        c_int(nTracers),
                        c_double(MeanAge),
                        c_double(SampleDate),
                        c_double(Lambda),
                        c_double(UZtime),
                        c_int(HeliumThree),
                        c_int(InitialTrit),
                        c_int(TritInitialTritRatio))

    print (Result)


def PFM_He4():

    #double Uppm, double THppm, double Porosity, double SedDensity, double Tau, double HeSolnRate

    Uppm = 0.1
    THppm = 0.9
    Porosity = 0.01
    SedDensity = 0.001
    MeanAge = 30
    HeSolnRate = 0
    Result = -99
    Result = Call_PFM_He4(Uppm,
                THppm,
                Porosity,
                SedDensity,
                MeanAge,
                HeSolnRate)

    print (Result)




def TracerOutput(lxSampleDate,
                            modelNum,
                            lxTracer,
                            lxdateRange,
                            lxTracerInputRange,
                            lxLambda,
                            lxuzTime,
                            lxUZtimeCond,
                            lxTracerComp_2,
                            lxDIC_1,
                            lxDIC_2,
                            Uppm,
                            THppm,
                            Porosity,
                            SedDensity,
                            He4SolnRate,
                            MeanAge,
                            MeanAge_2,
                            modelParm1,
                            modelParm2,
                            Fraction,
                            modelParm1_2,
                            modelParm2_2):
    

    
    lxTracerInputRange = np.asarray(lxTracerInputRange, c_double)
    lxdateRange = np.asarray(lxdateRange,c_double)   
    nTracerInput = lxTracerInputRange.size
    numDateRange = lxdateRange.size
    

    RE_SIZE = c_int(10)
    res = []

    res = Call_TracerOutput(c_double(lxSampleDate),
                            c_int(modelNum),
                            c_int(lxTracer),
                            lxdateRange,
                            c_int(numDateRange),
                            lxTracerInputRange,
                            c_int(nTracerInput),
                            c_double(lxLambda),
                            c_double(lxuzTime),
                            c_double(lxUZtimeCond),
                            c_double(lxTracerComp_2),
                            c_double(lxDIC_1),
                            c_double(lxDIC_2),
                            c_double(Uppm),
                            c_double(THppm),
                            c_double(Porosity),
                            c_double(SedDensity),
                            c_double(He4SolnRate),
                            c_double(MeanAge),
                            c_double(MeanAge_2),
                            c_double(modelParm1),
                            c_double(modelParm2),
                            c_double(Fraction),
                            c_double(modelParm1_2),
                            c_double(modelParm2_2),
                            byref(RE_SIZE))

    
    ResRet = []

   
    for i in range(RE_SIZE.value):
        ResRet.append(res[i])
   
    return ResRet




def SolveNewtonMethod():
    
    
    lxMeasTracerConcs = np.array(GetTracerLPMInput("MeasuredTracerConc.txt"),c_double) 
    lxMeasSigmas = np.array(GetTracerLPMInput("MeasuredSigmaConc.txt"),c_double)       
    lxTracerInputRange = np.array(Get2DTracerLPMInput("ReStoredTracer.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)
    #print(lxSampleDates)
    lxFitParmIndexes = np.array(GetTracerLPMInput("FitParmIndexes.txt"),c_double)
    lxInitModVals = np.array(GetTracerLPMInput("InitModelValues.txt"),c_double)
    lxLowBounds = np.array(GetTracerLPMInput("LowerBounds.txt"),c_double)
    lxHiBounds = np.array(GetTracerLPMInput("UpperBounds.txt"),c_double)
    lxTracers = np.array(GetTracerLPMInput("TracerIntegers.txt"),c_double)
    lxdateRange = np.array(GetTracerLPMInput("ReDates.txt"),c_double)
    lxLambda = np.array(GetTracerLPMInput("dLambdas.txt"),c_double)
    lxuzTime = np.array(GetTracerLPMInput("dUZtime.txt"),c_double)
    lxUZtimeCond = np.array(GetTracerLPMInput("UZtimeCond.txt"),c_double)


    _lxTracerInputRange = (lxTracerInputRange.__array_interface__['data'][0] + np.arange(lxTracerInputRange.shape[0])*lxTracerInputRange.strides[0]).astype(np.uintp)
    
    
    lxTracerComp_2 = np.array([0,0,0,0],c_double)

    
    TracerInputShape = lxTracerInputRange.shape
    numMeasTracers = lxMeasTracerConcs.size
    
    numMeasSigmas = lxMeasSigmas.size
   
    lenDates = lxSampleDates.size
    rowsTracerInputRange = TracerInputShape[0]
    colsTracerInputRange = TracerInputShape[1]
    print(rowsTracerInputRange)
    print(colsTracerInputRange)
    s
    modelNumAr = GetTracerLPMInput("ModNum.txt")
    modelNum = int(modelNumAr[0])
    lxDIC_1 = 100.0
    lxDIC_2 = 100.0
    Uppm = 1.0
    THppm = 1.0
    Porosity = 0.2
    SedDensity = 1.0
    He4SolnRate = 1.0
    lxIsMonteCarlo = 0
    iTotalSims = 1
    lxIsWriteOut = 0
    FileName = ""
    lxOutFile = FileName.encode('utf-8')
    
    numFitParms = lxFitParmIndexes.size
    numInitModVals = lxInitModVals.size
    numLowBounds = lxLowBounds.size
    numHiBounds = lxHiBounds.size
    numTracers = lxTracers.size
    numDateRange = lxdateRange.size
    numLambda = lxLambda.size
    numUZtime = lxuzTime.size
    numUZtimeCond  = lxUZtimeCond.size
    numTracerComp_2 = lxTracerComp_2.size

    RE_SIZE = c_int(10)
    res = []
    
    with open("SolverArgsOld.csv", mode='w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([lxMeasTracerConcs,
                            lxMeasSigmas,
                            c_int(numMeasTracers),
                            lxSampleDates,
                            c_int(lenDates), 
                            c_int(modelNum),
                            lxFitParmIndexes,
                            c_int(numFitParms),
                            lxInitModVals,
                            c_int(numInitModVals),
                            lxLowBounds,
                            c_int(numLowBounds),
                            lxHiBounds,
                            c_int(numHiBounds),
                            lxTracers,
                            c_int(numTracers),
                            lxdateRange,
                            c_int(numDateRange),
                            lxTracerInputRange,
                            c_int(rowsTracerInputRange),
                            c_int(colsTracerInputRange),
                            lxLambda,
                            c_int(numLambda),
                            lxuzTime,
                            c_int(numUZtime),
                            lxUZtimeCond,
                            c_int(numUZtimeCond),
                            lxTracerComp_2,
                            c_int(numTracerComp_2),
                            c_double(lxDIC_1),
                            c_double(lxDIC_2),
                            c_double(Uppm),
                            c_double(THppm),
                            c_double(Porosity),
                            c_double(SedDensity),
                            c_double(He4SolnRate),
                            c_int(lxIsMonteCarlo),
                            c_int(iTotalSims),
                            c_int(lxIsWriteOut),
                            lxOutFile])
    with open("SolverArgsOldTracer.csv", mode='w') as f:
        writer = csv.writer(f)
        for i in _lxTracerInputRange:
            writer.writerow(str(i))
                
    res = Call_SolveNewtonMethod(lxMeasTracerConcs,
                            lxMeasSigmas,
                            c_int(numMeasTracers),
                            lxSampleDates,
                            c_int(lenDates), 
                            c_int(modelNum),
                            lxFitParmIndexes,
                            c_int(numFitParms),
                            lxInitModVals,
                            c_int(numInitModVals),
                            lxLowBounds,
                            c_int(numLowBounds),
                            lxHiBounds,
                            c_int(numHiBounds),
                            lxTracers,
                            c_int(numTracers),
                            lxdateRange,
                            c_int(numDateRange),
                            _lxTracerInputRange,
                            c_int(rowsTracerInputRange),
                            c_int(colsTracerInputRange),
                            lxLambda,
                            c_int(numLambda),
                            lxuzTime,
                            c_int(numUZtime),
                            lxUZtimeCond,
                            c_int(numUZtimeCond),
                            lxTracerComp_2,
                            c_int(numTracerComp_2),
                            c_double(lxDIC_1),
                            c_double(lxDIC_2),
                            c_double(Uppm),
                            c_double(THppm),
                            c_double(Porosity),
                            c_double(SedDensity),
                            c_double(He4SolnRate),
                            c_int(lxIsMonteCarlo),
                            c_int(iTotalSims),
                            c_int(lxIsWriteOut),
                            lxOutFile,
                            byref(RE_SIZE)
                            )


    ResRet = []

    #print (RE_SIZE.value)
    for i in range(RE_SIZE.value):
        ResRet.append(res[i])
    return ResRet

def SolveNewtonMethodPy(lxMeasTracerConcs,
                            lxMeasSigmas,
                            lxSampleDates,
                            modelNum,
                            lxFitParmIndexes,
                            lxInitModVals,
                            lxLowBounds,
                            lxHiBounds,
                            lxTracers,
                            lxdateRange,
                            lxTracerInputRange,
                            lxLambda,
                            lxuzTime,
                            lxUZtimeCond,
                            lxTracerComp_2,
                            lxDIC_1,
                            lxDIC_2,
                            Uppm,
                            THppm,
                            Porosity,
                            SedDensity,
                            He4SolnRate,
                            lxIsMonteCarlo,
                            iTotalSims,
                            lxIsWriteOut,
                            FileName):
    
    

    
    #lxTracerInputRange =  np.transpose(lxTracerInputRange)
    lxTracerInputRange = np.asarray(lxTracerInputRange, c_double)

 
    
    _lxTracerInputRange = (lxTracerInputRange.__array_interface__['data'][0] + np.arange(lxTracerInputRange.shape[0])*lxTracerInputRange.strides[0]).astype(np.uintp)
    
    
    
    
    lxdateRange = np.asarray(lxdateRange,c_double)   
    TracerInputShape = lxTracerInputRange.shape

    lxMeasTracerConcs = np.array(lxMeasTracerConcs,c_double)
    
    numMeasTracers = lxMeasTracerConcs.size
    
    lxMeasSigmas = np.asarray(lxMeasSigmas,c_double)
    numMeasSigmas = lxMeasSigmas.size


    
    if isinstance(lxSampleDates,list):
        lxSampleDates = np.asarray(lxSampleDates,c_double)
    else:
        lxSampleDates = np.array([lxSampleDates],c_double)
    
    #print(lxSampleDates)
    lenDates = lxSampleDates.size
    rowsTracerInputRange = TracerInputShape[0]
    colsTracerInputRange = TracerInputShape[1]
    
    
    lxFitParmIndexes = np.asarray(lxFitParmIndexes,c_double)
    numFitParms = lxFitParmIndexes.size
    lxInitModVals = np.asarray(lxInitModVals,c_double)
    numInitModVals = lxInitModVals.size
    lxLowBounds = np.asarray(lxLowBounds,c_double)
    numLowBounds = lxLowBounds.size
    lxHiBounds = np.asarray(lxHiBounds, c_double)
    numHiBounds = lxHiBounds.size
    lxTracers = np.asarray(lxTracers,c_double)
    numTracers = lxTracers.size
    numDateRange = lxdateRange.size
    lxLambda = np.asarray(lxLambda,c_double)
    numLambda = lxLambda.size
    lxuzTime = np.asarray(lxuzTime,c_double)
    numUZtime = lxuzTime.size
    lxUZtimeCond = np.asarray(lxUZtimeCond,c_double)
    numUZtimeCond  = lxUZtimeCond.size
    numTracerComp_2 = lxTracerComp_2.size
    lxOutFile = FileName.encode('utf-8')
    RE_SIZE = c_int(10)
    res = []
    
    
    with open("SolverArgsNew.csv", mode='w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([lxMeasTracerConcs,
                            lxMeasSigmas,
                            c_int(numMeasTracers),
                            lxSampleDates,
                            c_int(lenDates), 
                            c_int(modelNum),
                            lxFitParmIndexes,
                            c_int(numFitParms),
                            lxInitModVals,
                            c_int(numInitModVals),
                            lxLowBounds,
                            c_int(numLowBounds),
                            lxHiBounds,
                            c_int(numHiBounds),
                            lxTracers,
                            c_int(numTracers),
                            lxdateRange,
                            c_int(numDateRange),
                            lxTracerInputRange,
                            c_int(rowsTracerInputRange),
                            c_int(colsTracerInputRange),
                            lxLambda,
                            c_int(numLambda),
                            lxuzTime,
                            c_int(numUZtime),
                            lxUZtimeCond,
                            c_int(numUZtimeCond),
                            lxTracerComp_2,
                            c_int(numTracerComp_2),
                            c_double(lxDIC_1),
                            c_double(lxDIC_2),
                            c_double(Uppm),
                            c_double(THppm),
                            c_double(Porosity),
                            c_double(SedDensity),
                            c_double(He4SolnRate),
                            c_int(lxIsMonteCarlo),
                            c_int(iTotalSims),
                            c_int(lxIsWriteOut),
                            lxOutFile])
    

    
    res = Call_SolveNewtonMethod(lxMeasTracerConcs,
                            lxMeasSigmas,
                            c_int(numMeasTracers),
                            lxSampleDates,
                            c_int(lenDates), 
                            c_int(modelNum),
                            lxFitParmIndexes,
                            c_int(numFitParms),
                            lxInitModVals,
                            c_int(numInitModVals),
                            lxLowBounds,
                            c_int(numLowBounds),
                            lxHiBounds,
                            c_int(numHiBounds),
                            lxTracers,
                            c_int(numTracers),
                            lxdateRange,
                            c_int(numDateRange),
                            _lxTracerInputRange,
                            c_int(rowsTracerInputRange),
                            c_int(colsTracerInputRange),
                            lxLambda,
                            c_int(numLambda),
                            lxuzTime,
                            c_int(numUZtime),
                            lxUZtimeCond,
                            c_int(numUZtimeCond),
                            lxTracerComp_2,
                            c_int(numTracerComp_2),
                            c_double(lxDIC_1),
                            c_double(lxDIC_2),
                            c_double(Uppm),
                            c_double(THppm),
                            c_double(Porosity),
                            c_double(SedDensity),
                            c_double(He4SolnRate),
                            c_int(lxIsMonteCarlo),
                            c_int(iTotalSims),
                            c_int(lxIsWriteOut),
                            lxOutFile,
                            byref(RE_SIZE)
                            )

    
    ResRet = []

    #print (RE_SIZE.value)
    for i in range(RE_SIZE.value):
        ResRet.append(res[i])
    
    print (ResRet)
    return ResRet

def SolveLevenberg():
    
    
    lxMeasTracerConcs = np.array(GetTracerLPMInput("MeasuredTracerConc.txt"),c_double) 
    lxMeasSigmas = np.array(GetTracerLPMInput("MeasuredSigmaConc.txt"),c_double)       
    lxTracerInputRange = np.array(Get2DTracerLPMInput("dTracerInputData.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)
    lxFitParmIndexes = np.array(GetTracerLPMInput("FitParmIndexes.txt"),c_double)
    lxInitModVals = np.array(GetTracerLPMInput("InitModelValues.txt"),c_double)
    lxLowBounds = np.array(GetTracerLPMInput("LowerBounds.txt"),c_double)
    lxHiBounds = np.array(GetTracerLPMInput("UpperBounds.txt"),c_double)
    lxTracers = np.array(GetTracerLPMInput("TracerIntegers.txt"),c_double)
    lxdateRange = np.array(GetTracerLPMInput("rDateRange.txt"),c_double)
    lxLambda = np.array(GetTracerLPMInput("dLambdas.txt"),c_double)
    lxuzTime = np.array(GetTracerLPMInput("dUZtime.txt"),c_double)
    lxUZtimeCond = np.array(GetTracerLPMInput("UZtimeCond.txt"),c_double)


    _lxTracerInputRange = (lxTracerInputRange.__array_interface__['data'][0] + np.arange(lxTracerInputRange.shape[0])*lxTracerInputRange.strides[0]).astype(np.uintp)

    
    lxTracerComp_2 = np.array([0,0,0,0],c_double)

    
    TracerInputShape = lxTracerInputRange.shape
    numMeasTracers = lxMeasTracerConcs.size
    
    numMeasSigmas = lxMeasSigmas.size
   
    lenDates = lxSampleDates.size
    rowsTracerInputRange = TracerInputShape[0]
    colsTracerInputRange = TracerInputShape[1]
    

    modelNumAr = GetTracerLPMInput("ModNum.txt")
    modelNum = int(modelNumAr[0])
    lxDIC_1 = 1.0
    lxDIC_2 = 1.0
    Uppm = 1.0
    THppm = 1.0
    Porosity = 1.0
    SedDensity = 1.0
    He4SolnRate = 1.0
    lxIsMonteCarlo = 0
    iTotalSims = 1
    lxIsWriteOut = 0
    FileName = "a"
    lxOutFile = FileName.encode('utf-8')
    
    numFitParms = lxFitParmIndexes.size
    numInitModVals = lxInitModVals.size
    numLowBounds = lxLowBounds.size
    numHiBounds = lxHiBounds.size
    numTracers = lxTracers.size
    numDateRange = lxdateRange.size
    numLambda = lxLambda.size
    numUZtime = lxuzTime.size
    numUZtimeCond  = lxUZtimeCond.size
    numTracerComp_2 = lxTracerComp_2.size

    RE_SIZE = c_int(10)
    res = []
    
    res = Call_Levenberg(lxMeasTracerConcs,
                            lxMeasSigmas,
                            c_int(numMeasTracers),
                            lxSampleDates,
                            c_int(lenDates), 
                            c_int(modelNum),
                            lxFitParmIndexes,
                            c_int(numFitParms),
                            lxInitModVals,
                            c_int(numInitModVals),
                            lxLowBounds,
                            c_int(numLowBounds),
                            lxHiBounds,
                            c_int(numHiBounds),
                            lxTracers,
                            c_int(numTracers),
                            lxdateRange,
                            c_int(numDateRange),
                            _lxTracerInputRange,
                            c_int(rowsTracerInputRange),
                            c_int(colsTracerInputRange),
                            lxLambda,
                            c_int(numLambda),
                            lxuzTime,
                            c_int(numUZtime),
                            lxUZtimeCond,
                            c_int(numUZtimeCond),
                            lxTracerComp_2,
                            c_int(numTracerComp_2),
                            c_double(lxDIC_1),
                            c_double(lxDIC_2)
                            ,c_double(Uppm),
                            c_double(THppm),
                            c_double(Porosity),
                            c_double(SedDensity),
                            c_double(He4SolnRate),
                            c_int(lxIsMonteCarlo),
                            c_int(iTotalSims),
                            c_int(lxIsWriteOut),
                            lxOutFile,
                            byref(RE_SIZE))


    ResRet = []

    #print (RE_SIZE.value)
    for i in range(RE_SIZE.value):
        ResRet.append(res[i])
    print (ResRet)
    return ResRet


def SolveGNLM():
    
    
    lxMeasTracerConcs = np.array(GetTracerLPMInput("MeasuredTracerConc.txt"),c_double) 
    lxMeasSigmas = np.array(GetTracerLPMInput("MeasuredSigmaConc.txt"),c_double)       
    lxTracerInputRange = np.array(Get2DTracerLPMInput("dTracerInputData.txt"),c_double)  
    lxSampleDates = np.array(GetTracerLPMInput("dSampleDates.txt"),c_double)
    lxFitParmIndexes = np.array(GetTracerLPMInput("FitParmIndexes.txt"),c_double)
    lxInitModVals = np.array(GetTracerLPMInput("InitModelValues.txt"),c_double)
    lxLowBounds = np.array(GetTracerLPMInput("LowerBounds.txt"),c_double)
    lxHiBounds = np.array(GetTracerLPMInput("UpperBounds.txt"),c_double)
    lxTracers = np.array(GetTracerLPMInput("TracerIntegers.txt"),c_double)
    lxdateRange = np.array(GetTracerLPMInput("rDateRange.txt"),c_double)
    lxLambda = np.array(GetTracerLPMInput("dLambdas.txt"),c_double)
    lxuzTime = np.array(GetTracerLPMInput("dUZtime.txt"),c_double)
    lxUZtimeCond = np.array(GetTracerLPMInput("UZtimeCond.txt"),c_double)


    _lxTracerInputRange = (lxTracerInputRange.__array_interface__['data'][0] + np.arange(lxTracerInputRange.shape[0])*lxTracerInputRange.strides[0]).astype(np.uintp)

    
    lxTracerComp_2 = np.array([0,0,0,0],c_double)

    
    TracerInputShape = lxTracerInputRange.shape
    numMeasTracers = lxMeasTracerConcs.size
    
    numMeasSigmas = lxMeasSigmas.size
   
    lenDates = lxSampleDates.size
    rowsTracerInputRange = TracerInputShape[0]
    colsTracerInputRange = TracerInputShape[1]
    

    modelNumAr = GetTracerLPMInput("ModNum.txt")
    modelNum = int(modelNumAr[0])
    lxDIC_1 = 1.0
    lxDIC_2 = 1.0
    Uppm = 1.0
    THppm = 1.0
    Porosity = 1.0
    SedDensity = 1.0
    He4SolnRate = 1.0
    lxIsMonteCarlo = 0
    iTotalSims = 1
    lxIsWriteOut = 0
    FileName = "a"
    lxOutFile = FileName.encode('utf-8')
    
    numFitParms = lxFitParmIndexes.size
    numInitModVals = lxInitModVals.size
    numLowBounds = lxLowBounds.size
    numHiBounds = lxHiBounds.size
    numTracers = lxTracers.size
    numDateRange = lxdateRange.size
    numLambda = lxLambda.size
    numUZtime = lxuzTime.size
    numUZtimeCond  = lxUZtimeCond.size
    numTracerComp_2 = lxTracerComp_2.size

    RE_SIZE = c_int(10)
    res = []
    
    res = Call_GNLM(lxMeasTracerConcs,
                            lxMeasSigmas,
                            c_int(numMeasTracers),
                            lxSampleDates,
                            c_int(lenDates), 
                            c_int(modelNum),
                            lxFitParmIndexes,
                            c_int(numFitParms),
                            lxInitModVals,
                            c_int(numInitModVals),
                            lxLowBounds,
                            c_int(numLowBounds),
                            lxHiBounds,
                            c_int(numHiBounds),
                            lxTracers,
                            c_int(numTracers),
                            lxdateRange,
                            c_int(numDateRange),
                            _lxTracerInputRange,
                            c_int(rowsTracerInputRange),
                            c_int(colsTracerInputRange),
                            lxLambda,
                            c_int(numLambda),
                            lxuzTime,
                            c_int(numUZtime),
                            lxUZtimeCond,
                            c_int(numUZtimeCond),
                            lxTracerComp_2,
                            c_int(numTracerComp_2),
                            c_double(lxDIC_1),
                            c_double(lxDIC_2)
                            ,c_double(Uppm),
                            c_double(THppm),
                            c_double(Porosity),
                            c_double(SedDensity),
                            c_double(He4SolnRate),
                            c_int(lxIsMonteCarlo),
                            c_int(iTotalSims),
                            c_int(lxIsWriteOut),
                            lxOutFile,
                            byref(RE_SIZE))


    ResRet = []

    #print (RE_SIZE.value)
    for i in range(RE_SIZE.value):
        ResRet.append(res[i])
    print (ResRet)
    return ResRet

    
    
        
    
def GetTracerLPMInput2(filename):
    inputFile = open(filename,"r")
    values = inputFile.read().splitlines()
    print (values)
    contents = []
    for val in values:
        contents.append([float(v) for v in val.split()])
    return contents

def GetTracerLPMInput(filename):
    contents = []
    with open(filename) as f:
        for line in f:
            data = line.split()
            contents.append(float(data[0]))
    #print (filename)
    #print (contents)
    return contents
            

def Get2DTracerLPMInput(filename):
    inputFile = open(filename,"r")
    values = inputFile.read().splitlines()
    contents = []
    for val in values:
        contents.append([float(v) for v in val.split(' ')])
    #print(contents)
    return contents    
    
    
def TracerTracerPlot():                                                     #   Incomplete function for plotting tracer-tracer plots. Needs work.
    
    TracerOutputArray = []
    TracerOutputReturn = []
    
    meanyears = []
    for i in range(10001):
        if i<100 or i == 500 or i==1000 or i==10000:
            TracerOutputReturn = TracerOutput(i)
            TracerOutputArray.append(TracerOutputReturn)
            print(i)
        meanyears.append(i)
        

    print("Loop complete")
    #print (TracerOutputArray)
    PlotArray = np.array(TracerOutputArray)
    
    
    xArray = np.array(PlotArray[:,0])
    yArray = np.array(PlotArray[:,1])
    zArray = np.array(meanyears)
    #print (zArray)
    #print (xArray)
    #print (yArray)
    
    plt.plot(xArray,yArray, label='3H vs He3')
    for x,y,z in zip(xArray,yArray,zArray):
        label = zArray[z]
        if (z < 50 and z%5==0) or (z >= 50 and z <100 and z%10==0) or z == 500 or z==1000 or z==10000:
            plt.annotate(label, (x,y), textcoords = "offset points", xytext=(0,10), ha='center') 
        
    
    plt.suptitle('Tracer-TracerPlot, 0 - 100 Years, 3H vs He3')
    plt.xlabel('3H')
    plt.ylabel('He3')
    plt.legend()
    
    plt.show()


    
