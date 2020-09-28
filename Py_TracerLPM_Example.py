
from LPM_Library import *

        
############################################################
#                                                          #
#                  SAMPLE INPUT EXAMPLE                    #
#                                                          #
############################################################




SampleInput1 = SampleInput("SampleInput.csv")                       #   1. Set sample input
PSW1 = Model(PEM_PEM)                                               #   2. Create Model object for a given sample
SetOutput('Ar39_dataset.csv','Ar39 in Modesto, CA')                 #   3. Set output csv file, 1: filename, 2: descriptive name




                                                                    

PSW1.SetSample(SampleInput1,1)                                      #   4.  Set sample to be modeled using ID (col A) from sample input sheet. See example sheet for format requirements.                                
                                                                    #   Note: When setting up sample input sheet, make sure to have measured concentration correct precision visible! (e.g. 0.670758 vs 0.67)
PSW1.SetTracers(["3H","3He(trit)","14C", "39Ar"])                   #   5.  Select which tracers to model. Note: Tracer names require quotes.
PSW1.ChangeTimeStep(0.5)                                            #   6.  Change time step if desired, 0.083 is default. Must set this after choosing tracers or you'll receive error.

PSW1.SetParm(FRACTION,0.5)                            
PSW1.SetParm(UZ_TIME, 0)                                            #   7.  Optional: Change initial values of parameters associated with model.
PSW1.SetParm(MEAN_AGE,80)                                           #                 Parameters are global variables and do not require quotes.
PSW1.SetParm(MEAN_AGE_2,8000)                                       #                 See Model -> ModelParm block for default values.
                            

PSW1.SetFitParms([MEAN_AGE,FRACTION])                               #   8.  Select which parameter(s) to solve for. If multiple parameters, it must be in [list] format.


PSW1_1_Result = PSW1.RunModel()                                     #   9.  Create object to store results array (if desired) -- solution values are automatically stored in Model object (eg. PSW1.Solution.___, see below).
WriteOut(PSW1)                                                      #   10. Write the output to chosen output file, appending to the bottom. Calling SetOutput will overwrite, rather than append, so be careful.

print(PSW1.Solution.ChiSqr)                                         #   Example of #9 above
print(PSW1.Solution.SolvedModelParms)                         

PSW1.SetFitParms([MEAN_AGE,FRACTION,MEAN_AGE_2])                    #   The same Model object (eg. PSW1) can be run again with different fitting parameters.
PSW1_Result = PSW1.RunModel() 
WriteOut(PSW1)

PSW1 = Model(DM_DM)                                                 #   The same Model object (eg. PSW1) can be switched to a different model type.
PSW1.SetSample(SampleInput1,1)              
PSW1.SetTracers(["3H","3He(trit)","14C", "39Ar"])

PSW1.ChangeTimeStep(0.083)
PSW1.SetParm(FRACTION,0.5)
PSW1.SetParm(UZ_TIME, 0)
PSW1.SetParm(MEAN_AGE,80)
PSW1.SetParm(MEAN_AGE_2,8000)
PSW1.SetParm(DISP_PARM, 0.1)
PSW1.SetParm(DISP_PARM_2, 0.01)

PSW1.SetFitParms([MEAN_AGE,DISP_PARM,FRACTION])

PSW1_2_Result = PSW1.RunModel()                                     #   If the new solution values are not saved to a different object, they will be overwritten!
WriteOut(PSW1)

PSW1.SetFitParms([MEAN_AGE,FRACTION])                       
for x in range(0,10):                                               #   11. Parameters can be changed incrementally using for loops.
    PSW1.SetParm(DISP_PARM, float(x/10))                            #   Here the dispersion parameter of the young fraction is incremented from 0 to 0.9 by 0.1 increments.
    PSW1.RunModel()                                                 #   The solution values are not saved internally but are written to the output file for each loop event.
    WriteOut(PSW1)



MER11 = Model(PEM_PEM)                                              

MER11.SetSample(SampleInput1,2)
MER11.SetTracers(["3H","14C","39Ar"])
MER11.ChangeTimeStep(0.5)
MER11.SetParm(FRACTION,0.5)
MER11.SetParm(UZ_TIME,0)
MER11.SetParm(MEAN_AGE,10)
MER11.SetParm(MEAN_AGE_2,6500)

MER11.SetFitParms([MEAN_AGE,FRACTION])

MER11_1_Result = MER11.RunModel()
WriteOut(MER11)


MER10 = Model(PEM)

MER10.SetSample(SampleInput1,3)
MER10.SetTracers(["3H","3He(trit)","14C","39Ar"])
MER10.ChangeTimeStep(0.5)
MER10.SetParm(MEAN_AGE, 50)
MER10.SetFitParms([MEAN_AGE])

MER10_1_Result = MER10.RunModel()
WriteOut(MER10)

TRLK05 = Model(PEM_PEM)
TRLK05.SetSample(SampleInput1,4)
TRLK05.SetTracers(["3H","14C","39Ar"])
TRLK05.ChangeTimeStep(0.5)
TRLK05.SetParm(MEAN_AGE, 10)
TRLK05.SetParm(FRACTION, 0.5)
TRLK05.SetParm(MEAN_AGE_2, 18000)

TRLK05.SetFitParms([MEAN_AGE,FRACTION])

TRLK05_1_Result = TRLK05.RunModel()                         
WriteOut(TRLK05)                                       


MER11_Age_Dist = MER11.GetAgeDist(MER11.Solution.SolvedModelParms[0])       #  Create age distribution for selected model, one argument = mean age.
                                                                            #  This argument can be set by the solution value (as shown), or manually.
                                                                            #  Currently this function assumes the other parameters are the initial values
                                                                            #  If you want to use a solved parameter, such as dispersion parameter for DM, it would need to be manually
                                                                            #  changed in the GetAgeDist function. This will likely be updated in the future.
                                                                            #  The plotting is for example purposes, and contained in "TracerLPM_CPP_Library.py"

                                                                            #  Populate tracer-tracer arrays and years-array for use in plotting. Arguments are:
MER11.PopulateTracerTracerArrays("3H",                                      #  Tracer 1
                                "39Ar",                                      #  Tracer 2
                                MER11.InitialVals[MEAN_AGE_2],              #  2nd Mean Age (if BMM, otherwise 0)
                                    MER11.InitialVals[PEM_U_RATIO],         #  Model Parm 1
                                    MER11.InitialVals[PEM_L_RATIO],         #  Model Parm 2 (if applicable, otherwise 0)
                                    MER11.Solution.SolvedModelParms[1],     #  Fraction (if BMM, otherwise 0)          
                                    MER11.InitialVals[PEM_U_RATIO_2],       #  2nd Model Parm 1 (if BMM, otherwise 0)
                                    MER11.InitialVals[PEM_L_RATIO_2])       #  2nd Model Parm 2 (if BMM and applicable, otherwise 0) 
                                                                            #  TracerTracerArrays[0] = tracer 1 concs eg. x-axis, [1] = tracer 2 concs eg. y-axis, [2] = years eg. z-axis

print(MER11.TracerTracerArray[0])
print(MER11.TracerTracerArray[1])                                           #  These arrays can be used to do plotting in R, or excel, etc.
print(MER11.TracerTracerArray[2])

TracerTracerWrite(MER11,"MER11_tta.csv")                                    #  This is a basic function to write the three arrays to a csv file, arg1 = Model object, arg2 = filename.



###########################################################
#                                                         #             This shows how to implement tracer-tracer plotting in order to aid in finding good solutions,
#                   PLOTTING EXAMPLE                      #             but there are likely more efficient ways to set this up. By default TracerOutput and GetAgeDist
#                   (w/ matplotlib)                       #             populate arrays which can be plotted in python (as seen here) or output to plot in R.
#                                                         #
###########################################################




    


fig, ax = plt.subplots()
ax.plot(MER11.TracerTracerArray[0][1:],MER11.TracerTracerArray[1][1:], label='3H vs 39Ar')
BMM_line_start = []
BMM_line_end = []
for x,y,z in zip(MER11.TracerTracerArray[0],MER11.TracerTracerArray[1],MER11.TracerTracerArray[2]):
    label = MER11.TracerTracerArray[2][z]
    if (z < 50 and z%5==0) or (z >= 50 and z <200 and z%10==0) or z == 500 or z==1000 or z==10000:
        ax.annotate(label, (x,y), textcoords = "offset points", xytext=(0,10), ha='center')
    if (z ==  int(MER11.Solution.SolvedModelParms[0])):
        BMM_line_start = [x,y]
    if (z == int(MEAN_AGE_2) or z > int(MEAN_AGE_2)):
        BMM_line_end = [x,y]
        
ax.plot(MER11.ModelTracerConcs[0],MER11.ModelTracerConcs[2],'ro')
#ax.plot(BMM_line_start,BMM_line_end,'r-') #??????
#ax.set_ylim(0,140)
#ax.set_xlim(0,5)
fig.suptitle("".join(('Tracer-Tracer Plot, ',str(MER11.Name),', ',str(MER11.ModelParms[2].NameAlias),' = ',str(MER11.InitialVals[2]))))
ax.set_xlabel(MER11.TracerAlphas[0])
ax.set_ylabel(MER11.TracerAlphas[2])
ax.legend()
    
plt.show()

