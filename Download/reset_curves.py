# Tool: Reset Curves
# Author: RIST JIANWEN CHENG
# Python Version: 3.10.8
# System: Linux
# Support: Updated as MAYA versions
# Creation Date: May 21, 2016
# Updated Date: Aug 01, 2025
# Version: 1.6




def ui_resetCurves(position='default'):  
    """
    Create the main UI window for the 'Reset Curves' tool.
    
    Args:
        position (str or list): Position as a list, e.g., [400, 700]; Default positions relative to the parent main window.

    Returns:
        dict:
            A dictionary named 'uiSearchAndBlendShapeForCurvesOutputDic', containing references to the created UI elements.
    """
        
    import maya.cmds as cmds
    import os
    import importlib
    
    global uiResetCurvesOutputDic 
    
    # Variable definitions.
    variateInheritedList = ['TOOL_PARENT_MAIN_WINDOW', 'resetCurves_image_0_0.png']    
    variateNameList = ['Reset_Curves', 'ui_resetCurves_preset.py'] 
    variateValueDic = {1:['Segment Length On Shortest Curve :', 'Segment Length On Longest Curve :', 3], 2:['Amount Of CV On Shortest Curve :', 'Amount Of CV On Longest Curve :', 0]}
    uiDefaultValueDic = {'om1':{'value':'Rebuild Curve(s)'}, 'rbg1':{'select':1}, 'ff1':{'v':[[0.001, 0.23], [4, 18]], 'bgc':[0.1,0.2,0.1]}, 'ff2':{'v':[[0.001, 0.23], [4, 18]], 'bgc':[0.1,0.2,0.1]}, 'b1':{'bgc':[0.1,0.2,0.1]}, 'rbg2':{'select':2}, 'cb1':{'value':False}}
    
    # Search the preset file directory.
    scriptPathStr = os.environ['MAYA_SCRIPT_PATH']
    scriptPathList = scriptPathStr.split(':')
    string = 'maya/scripts'
    for scriptPath in scriptPathList:
        if string in scriptPath:
            presetFile = variateNameList[1]
            presetFileName = presetFile.split(".")[0]
            presetFilePath = scriptPath+'/'+presetFile
            break
        else:
            presetFilePath = False
    # Detecting if the preset file exists.
    if os.access(presetFilePath, os.F_OK):        
        uiPreset = __import__(presetFileName)
        importlib.reload(uiPreset)
        uiValueDic = uiPreset.resetCurvesPresetValueDic 
        pathResult = "The UI settings have been retrieved from the presets file: " + presetFilePath
        print(pathResult)     
    else:                       
        uiValueDic = uiDefaultValueDic

    # Determine window position.
    if position == 'default':   
        if cmds.window(variateInheritedList[0], exists=True) == True:  
            # Retrieve the position of the parent main window.
            parentMainWindowPosition = cmds.window(variateInheritedList[0], q=True, topLeftCorner=True) 
            # Set window postion of 'Reset Curves'.
            position = [parentMainWindowPosition[0]+114, parentMainWindowPosition[1]-261]
        else:
            position = [400,700]
    else:  
        position = position 
        
    # Ensure the 'Reset Curves' window does not already exist.
    windowName = variateNameList[0]                       
    if cmds.window(windowName, exists=True) == True:        
        cmds.deleteUI(windowName)
    if cmds.windowPref(windowName, exists=True):
        cmds.windowPref(windowName, remove=True) 
                
    # Create window.    
    windowTitle = windowName.replace('_', ' ')      
    #cmds.window(windowName, q=True, widthHeight=True)
    #cmds.window(windowName, q=True, topLeftCorner=True)  
    #cmds.window(variateInheritedList[0], q=True, topLeftCorner=True)
    cmds.window(windowTitle, widthHeight=[252, 218], topLeftCorner=position, sizeable=False)
         
    cl1=cmds.columnLayout(adjustableColumn=True)
    mb1=cmds.menuBarLayout()
    m1=cmds.menu(label='Edit', helpMenu=False)
    mi1=cmds.menuItem(label='Save Settings', command="reset_curves.CM_ResetCurves.cm_uiControl(controlName='Save Settings')")
    mi2=cmds.menuItem(label='Reset Settings', command="reset_curves.CM_ResetCurves.cm_uiControl(controlName='Reset Settings')") 
    m2=cmds.menu(label='Help', helpMenu=True )
    mi3=cmds.menuItem(label="Help on 'Reset Curves'", command="reset_curves.CM_ResetCurves.cm_uiControl(controlName='Reset Curves PDF')")
    mi4=cmds.menuItem(label='Information', command="reset_curves.CM_ResetCurves.cm_uiControl(controlName='Reset Curves Information')")  
    
    cl2=cmds.columnLayout(columnAttach=('both', 2), adjustableColumn=True)
    
    cmds.separator(style='in',width=1)
    
    rl1=cmds.rowLayout(p=cl2, numberOfColumns=2) 
    cbg1=cmds.checkBoxGrp(p=rl1, numberOfCheckBoxes=2, label='Display :', labelArray2=['EP', 'CV'], columnWidth3=[50,40,40], columnAlign3=['left','left','left'], valueArray2=[False,False], changeCommand="reset_curves.CM_ResetCurves.cm_uiControl(controlName='cbg1')")     
    image1=cmds.image(p=rl1, image=variateInheritedList[-1])

    cmds.separator(p=cl2)   

    rl2=cmds.rowLayout(p=cl2, numberOfColumns=1)
    om1=cmds.optionMenu(label="Reset Method", width=237)
    mi5=cmds.menuItem(label='Rebuild Curve(s)', p=om1)
    mi6=cmds.menuItem(label='Recreate Curve(s)', p=om1)
    cmds.optionMenu(om1, e=True, value=uiValueDic['om1']['value'])
    
    cmds.separator(p=cl2)
    
    rbg1=cmds.radioButtonGrp(p=cl2, label='Specify : ', columnAlign=[1,'left'], labelArray2=['Segment Length', 'CV Amount'], numberOfRadioButtons=2, columnWidth3=[44,112,60], select=uiValueDic['rbg1']['select'], changeCommand="reset_curves.CM_ResetCurves.cm_uiControl(controlName='rbg1')")

    cmds.separator(p=cl2)

    rl3=cmds.rowLayout(p=cl2, numberOfColumns=3, columnAttach=[(1, 'left', 1), (2, 'right', 1)])
    t1=cmds.text(label=variateValueDic[uiValueDic['rbg1']['select']][0], align='left', width=181)
    ff1= cmds.floatField(bgc=uiValueDic['ff1']['bgc'], minValue=uiValueDic['ff1']['v'][(uiValueDic['rbg1']['select']-1)][0], value=uiValueDic['ff1']['v'][(uiValueDic['rbg1']['select']-1)][1], precision=variateValueDic[uiValueDic['rbg1']['select']][2], height=16, width=55, visible=True, changeCommand="reset_curves.CM_ResetCurves.cm_uiControl(controlName='ff1')")

    rl4=cmds.rowLayout(p=cl2, numberOfColumns=2, columnAttach=[(1, 'left', 1), (2, 'right', 1)])
    cmds.separator(width=204, visible=False ) 
    b1=cmds.button("i||i", bgc=uiValueDic['b1']['bgc'], height=8, width=8, command="reset_curves.CM_ResetCurves.cm_uiControl(controlName='b1')" )
    
    rl5=cmds.rowLayout(p=cl2, numberOfColumns=3, columnAttach=[(1, 'left', 1), (2, 'right', 1)])
    t2=cmds.text(label=variateValueDic[uiValueDic['rbg1']['select']][1], align='left', width=181)
    ff2= cmds.floatField(bgc=uiValueDic['ff2']['bgc'], minValue=uiValueDic['ff2']['v'][(uiValueDic['rbg1']['select']-1)][0], value=uiValueDic['ff2']['v'][(uiValueDic['rbg1']['select']-1)][1], precision=variateValueDic[uiValueDic['rbg1']['select']][2], height=16, width=54, visible=True, changeCommand="reset_curves.CM_ResetCurves.cm_uiControl(controlName='ff2')")
    
    cmds.separator(p=cl2) 

    rbg2=cmds.radioButtonGrp(p=cl2, label='Degree :', columnAlign=[1,'left'], labelArray4=['1 Linear', '3 Cubic','5','7'], numberOfRadioButtons=4, columnWidth5=[45,60,60,30,30], select=uiValueDic['rbg2']['select'], changeCommand="reset_curves.CM_ResetCurves.cm_uiControl(controlName='rbg2')")
    cb1=cmds.checkBox(p=cl2, label='Keep original curve(s) in a group', width=50, value=uiValueDic['cb1']['value'])
     
    cmds.separator(p=cl2, style='single', horizontal=False, height=5)  
                                       
    rl6=cmds.rowLayout(p=cl2, numberOfColumns=2)
    b2=cmds.button("Apply", width=119, command="reset_curves.CM_ResetCurves.cm_resetCurves('selected', 'valueOnUi', 'valueOnUi', 'valueOnUi', 'valueOnUi', 'valueOnUi', 'valueOnUi')")
    b3=cmds.button("Cancel", width=119, command="reset_curves.CM_ResetCurves.cm_uiControl(controlName='cancel')")
    
    cmds.showWindow(windowName)

    uiResetCurvesOutputDic = {0:windowName, 1:cbg1, 2:image1, 3:om1, 4:rbg1, 5:t1, 6:ff1, 7:b1, 8:t2, 9:ff2, 10:rbg2, 11:cb1, 12:uiDefaultValueDic, 13:uiValueDic, 14:presetFilePath, 15:presetFile, 16:variateValueDic}
    
    return uiResetCurvesOutputDic
    
    
class CM_ResetCurves:
    """
    A class for rebuilding or recreating curves using a specified segment length or number of CVs.
    """
    
    @classmethod
    def cm_resetCurves(cls, curveTransformList, resetMethod, specify, valueOnShortestCurve, valueOnLongestCurve, degree, keepOriginalCurve):        
        """ 
        This function allows precise customization for rebuilding or recreating the segment length or CV number on curves. It will return a 'curveTransformList'.
                
        Args:
            curveTransformList (list): Selected transforms of the curves. Defaults to 'selected'.
            resetMethod (str): Method to reset the curves. Valid arguments are 'rebuild Curve(s)' or 'recreate Curve(s)'. Defaults to 'valueOnUi'.
            specify (int): Specifies whether the operation is based on 'Segment Length' or 'CV Number'. Defaults to 'valueOnUi'. 
                - 1 represents 'Segment Length'
                - 2 represents 'CV Number'
            valueOnShortestCurve (float/int). Defaults to 'valueOnUi': 
                - If 'specify' is 'Segment Length', this must be a float.
                - If 'specify' is 'CV Number', this must be an integer.
            valueOnLongestCurve (float/int). Defaults to 'valueOnUi': 
                - If 'specify' is 'Segment Length', this must be a float.
                - If 'specify' is 'CV Number', this must be an integer.
            degree (int): Degree of the curve. Defaults to 'valueOnUi'. Valid values are:
                - 1 indicates '1 Linear'
                - 2 indicates '3 Cubic'
                - 3 indicates '5'
                - 4 indicates '7'
            keepOriginalCurve (int): Indicates whether to keep the original curve(s) in a group. Valid values are 0 (no) or 1 (yes). Defaults to 'valueOnUi'.
    
            Returns:
                list: The transformed curve list ('curveTransformList').
    
            Formula:
                (L3-L1)/(S3-S1) = coefficient = (LN-L1)/(SN-S1)
                SN = L1 + (LN-L1)/coefficient
    
            Explanation:
                This formula relates the segment lengths and calculates the value for the new segment ('SN').
                The method applies the transformation based on the input parameters and returns the updated curve data.
        """
        
        import maya.cmds as cmds
        
        # Get user-defined or UI values.
        cbg1 = uiResetCurvesOutputDic[1]
        cbg1valueArray = cmds.checkBoxGrp(cbg1, q=True, valueArray2=True)     
        # Check if we are retrieving parameters from the UI or by specifying them.
        if resetMethod == 'valueOnUi':  
            om1 = uiResetCurvesOutputDic[3]
            resetMethod = cmds.optionMenu(om1, q=True, value=True)
        else:
            resetMethod = resetMethod
            
        if specify == 'valueOnUi':  
            rbg1 = uiResetCurvesOutputDic[4] 
            specify = cmds.radioButtonGrp(rbg1, q=True, select=True)
        else:
            specify = specify
            
        if valueOnShortestCurve == 'valueOnUi':  
            ff1 = uiResetCurvesOutputDic[6]
            valueOnShortestCurve = cmds.floatField(ff1, q=True, value=True)
        else:
            valueOnShortestCurve = valueOnShortestCurve
            
        if valueOnLongestCurve == 'valueOnUi':  
            ff2 = uiResetCurvesOutputDic[9]
            valueOnLongestCurve = cmds.floatField(ff2, q=True, value=True)
        else:
            valueOnLongestCurve = valueOnLongestCurve
            
        if degree == 'valueOnUi':  
            rbg2 = uiResetCurvesOutputDic[10] 
            degree = cmds.radioButtonGrp(rbg2, q=True, select=True)*2-1
        else:
            degree = degree   
                                 
        if keepOriginalCurve == 'valueOnUi':  
            cb1 = uiResetCurvesOutputDic[11]
            keepOriginalCurve = cmds.checkBox(cb1, q=True, value=True)
        else:
            keepOriginalCurve = keepOriginalCurve 
        
        # Get value of curveTransformList.
        curveTransformList = cmds.ls(selection=True, type='transform') if curveTransformList == 'selected' else curveTransformList  
                    
        if len(curveTransformList) == 0:
            MESSAGE = 'There is no curve that has been selected.'
            result = cmds.confirmDialog(title="Notices", message=MESSAGE, messageAlign='center', button=['Confirm'], dismissString='Confirm')
        elif len(curveTransformList) == 1:
            t1 = uiResetCurvesOutputDic[5]
            b1 = uiResetCurvesOutputDic[7]
            t2 = uiResetCurvesOutputDic[8]
            ff2 = uiResetCurvesOutputDic[9]
            cmds.text(t2, e=True, enable=False)
            cmds.floatField(ff2, e=True, enable=False)
            t1Label = cmds.text(t1, q=True, label=True)
            MESSAGE = 'There is only one curve, the value of the "'+t1Label.split(':')[0]+'" will be used on the curve, do you want to continue it ?'
            result = cmds.confirmDialog(title="NOTES", message=MESSAGE, messageAlign='center', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No')   
            cmds.text(t2, e=True, enable=True)
            b1Bgc = cmds.button(b1, q=True, bgc=True)          
            b1Bgc = [round(num, 1) for num in b1Bgc] 
            if b1Bgc != [0.1, 0.2, 0.1]:
                b1Bgc = [0.1, 0.1, 0.15]
            cmds.floatField(ff2, e=True, bgc=b1Bgc, enable=True)             
        else:
            # Additional handling for multiple curves can go here.
            result=''
            
        print(curveTransformList, resetMethod, specify, valueOnShortestCurve, valueOnLongestCurve, degree, keepOriginalCurve, result)

        # Calculating on the curves.
        if result=='Confirm' or result=='No':
            pass
        else:
            cls.resetCurveShapeList=[]           
            # Detecting lengths of curves and storing in a dictionary curvesDic.
            curvesDic={}
            for curveTransform in curveTransformList:           
                curveInfoN = cmds.arclen(curveTransform,ch=True)
                length = cmds.getAttr(curveInfoN+".arcLength")
                cmds.delete(curveInfoN)
                curvesDic[curveTransform] = length                
                print(curvesDic)        
                minLength = min(curvesDic.values())
                maxLength = max(curvesDic.values())    
                print(minLength, maxLength)               
            # Create curve transform dictionary with calculated segment details.             
            curveTransformDic = {}
            for curveTransform in curveTransformList:
                if maxLength==minLength:     
                    curveLength = curvesDic[curveTransform]
                    coefficient=1
                    resetValue = valueOnShortestCurve
                    print('Case A: All curves are of equal length.')
                elif valueOnShortestCurve == valueOnLongestCurve:                    
                    curveLength = curvesDic[curveTransform]
                    coefficient=1 
                    resetValue = valueOnShortestCurve        
                    print('Case B: Same segment length for all curves.')
                else:
                    coefficient=(maxLength-minLength)/(valueOnLongestCurve-valueOnShortestCurve)        
                    curveLength = curvesDic[curveTransform] 
                    resetValue = valueOnShortestCurve + (curveLength-minLength) / coefficient 
                    print('Case C: Different segment lengths calculated based on curve length.')
                    
                if specify == 1:
                    segmentLength = resetValue  
                    numberOfSpans = round(curveLength/segmentLength)                                        
                    if degree == 1:
                        cvAmount = numberOfSpans+1
                    elif degree == 3:
                        cvAmount = numberOfSpans+3  
                    elif degree == 5:
                        cvAmount = numberOfSpans+5
                    else:
                        cvAmount = numberOfSpans+7
                else:
                    cvAmount = round(resetValue)  
                    if degree == 1:
                        numberOfSpans = cvAmount-1
                    elif degree == 3:
                        numberOfSpans = cvAmount-3  
                    elif degree == 5:
                        numberOfSpans = cvAmount-5
                    else:
                        numberOfSpans = cvAmount-7
                    segmentLength = curveLength/numberOfSpans
                        
                curveTransformDic[curveTransform] = [curveLength, segmentLength, numberOfSpans, cvAmount] 
                print(curveTransformDic)
                
            # Handle keeping the original curve.
            selectedCurveTransformList = []
            for curveTransform in curveTransformList:
                if keepOriginalCurve == True:
                    originalCurveTransformGrp = 'originalCurveTransform_grp'
                    if cmds.objExists(originalCurveTransformGrp):
                        pass
                    else:
                        cmds.group(em=True, name=originalCurveTransformGrp)
                        cmds.setAttr(originalCurveTransformGrp+'.visibility', 0)
                    
                    if curveTransform == curveTransformList[0]:
                        originalCurveTransformGrpVersion = 'originalCurveTransform_grp_version'
                        try:
                            n = len(cmds.listRelatives('originalCurveTransform_grp', children=True))
                        except TypeError:
                            n = 1
                        else:  
                            n += 1                     
                        cmds.group(em=True, name=originalCurveTransformGrpVersion+str(n))
                        cmds.parent(originalCurveTransformGrpVersion+str(n), originalCurveTransformGrp)
                    else:
                        pass  
                                            
                    duplicatedCurveTransform = cmds.duplicate(curveTransform, name='original_'+curveTransform+'_v'+str(n))[0]                   
                    cmds.parent(duplicatedCurveTransform, originalCurveTransformGrpVersion+str(n))                    
                else:
                    pass  
                    
                # Rebuild or sample the curve based on reset method.    
                if resetMethod=='Rebuild Curve(s)': 
                    cmds.rebuildCurve(curveTransform, ch=True, rpo=True, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, fr=1, s=curveTransformDic[curveTransform][2], d=degree, tol=0.01) 
                    selectedCurveTransform=curveTransform       
                else:
                    locatorShape = cmds.createNode('locator')
                    locatorTransform = cmds.listRelatives(locatorShape, parent=True)[0]
                    locatorTransform = cmds.rename(locatorTransform, curveTransform+'_locator')
                    motionPathName = cmds.pathAnimation(locatorTransform, curve=curveTransform, fractionMode=True)
                    cvAmount=curveTransformDic[curveTransform][3]
                    cvSpanValue=1/(cvAmount-1)    
                    cvValue=0
                    cvDic={}       
                    # Iterate through each CV number up to cvAmount.            
                    for cvNumber in range(0,cvAmount):  
                        cmds.setAttr(motionPathName+'.uValue', cvValue)
                        cvPosition = cmds.xform(locatorTransform, query=True, worldSpace=True, translation=True)
                        cvDic[cvNumber] = cvPosition                               
                        cvValue = min(cvValue + cvSpanValue, 1)
                    # Delete temporary objects and create a new curve from sampled points.     
                    cmds.delete(curveTransform, locatorTransform)                                         
                    newCuvreTransform = cmds.curve(n=curveTransform, p=list(cvDic.values()), degree=degree)
                    selectedCurveTransform = newCuvreTransform
                # Set display attributes for the selected curve shape.                                   
                selectedCurveShape = cmds.listRelatives(selectedCurveTransform, fullPath=True)[0]                  
                cmds.setAttr(selectedCurveShape+'.dispEP', cbg1valueArray[0])
                cmds.setAttr(selectedCurveShape+'.dispCV', cbg1valueArray[1])  
                selectedCurveTransformList.append(selectedCurveTransform) 
  
            cmds.select(selectedCurveTransformList)    
                        
        print(selectedCurveTransformList)    
            
        return selectedCurveTransformList


    @classmethod
    def cm_uiControl(cls, controlName):
        """
        This is a function for controling the controls on the UI. The valid values for the 'controlName' argument is only valid: 'cbg1','om1','b1','ff1','ff2','rbg1','cancel','Save Settings','Reset Settings','Reset Curves Information','Reset Curves PDF'."
        """   
        
        import maya.cmds as cmds
        import os
        
        # Variable definitions.
        variateInheritedList = ['resetCurves_image_0_0.png', 'resetCurves_image_0_1.png', 'resetCurves_image_1_0.png', 'resetCurves_image_1_1.png']      
       
        uiDefaultValueDic = uiResetCurvesOutputDic[12]
        uiValueDic = uiResetCurvesOutputDic[13]       
        presetFilePath = uiResetCurvesOutputDic[14]
        presetFile = uiResetCurvesOutputDic[15]
        variateValueDic = uiResetCurvesOutputDic[16] 
        windowName = uiResetCurvesOutputDic[0] 
        cbg1 = uiResetCurvesOutputDic[1]
        image1 = uiResetCurvesOutputDic[2] 
        om1 = uiResetCurvesOutputDic[3]        
        rbg1 = uiResetCurvesOutputDic[4]
        t1 = uiResetCurvesOutputDic[5] 
        ff1 = uiResetCurvesOutputDic[6]  
        b1 = uiResetCurvesOutputDic[7]   
        t2 = uiResetCurvesOutputDic[8] 
        ff2 = uiResetCurvesOutputDic[9]
        rbg2 = uiResetCurvesOutputDic[10]
        cb1 = uiResetCurvesOutputDic[11] 
          
        # This is for controling the 'checkBoxGrp' on the UI.
        if controlName == 'cbg1': 
            valueArray2=cmds.checkBoxGrp( cbg1, q=True, valueArray2=True )                   
            # Select the shape(s) or transform(s) of the object(s) to get 'selectedCurveTransformSet'.
            selectedObjectList=cmds.ls(selection=True)  
            selectedCurveTransformSet = set()
            if len(selectedObjectList)==0:
                cmds.checkBoxGrp( cbg1, e=True, valueArray2=[False, False] )
                MESSAGE = 'There is no curve transform or shape that have been selected.' 
                cmds.error(MESSAGE)
            else:               
                for selectedObject in selectedObjectList:           
                    type = cmds.objectType(selectedObject) 
                    if type == 'nurbsCurve':           
                        selectedCurveTransform = cmds.listRelatives(selectedObject,path=True,parent=True,type='transform')[0]
                        selectedCurveTransformSet.add(selectedCurveTransform)
                    elif type == 'transform':
                        shapeList = cmds.listRelatives(selectedObject,path=True,shapes=True,type='nurbsCurve')                
                        try:
                            len(shapeList)
                        except TypeError:
                            pass
                        else:  
                            selectedCurveTransform=selectedObject
                            selectedCurveTransformSet.add(selectedCurveTransform)
                    else:
                        pass
            # Control the 'Disp EP' and 'Disp CV' on selected curve(s). 
            if len(selectedCurveTransformSet)==0:
                cmds.checkBoxGrp( cbg1, e=True, valueArray2=[False, False] )
                MESSAGE = 'There is no curve transform or shape that have been selected.'  
                cmds.error(MESSAGE)
            else:
                valueList=[ int(valueArray2[0]), int(valueArray2[1]) ]                 
                for selectedCurveTransform in selectedCurveTransformSet:  
                    selectedCurveShape=cmds.listRelatives( selectedCurveTransform, fullPath=True )[0]  
                    cmds.setAttr(selectedCurveShape+'.dispEP', valueList[0])
                    cmds.setAttr(selectedCurveShape+'.dispCV', valueList[1])
            # Control the images. 
            valueArray2=cmds.checkBoxGrp( cbg1, q=True, valueArray2=True ) 
            if valueArray2==[False,False]:
                cmds.image(image1, e=True, image=variateInheritedList[0])   
            elif valueArray2==[True,False]:  
                cmds.image(image1, e=True, image=variateInheritedList[2])    
            elif valueArray2==[False,True]:  
                cmds.image(image1, e=True, image=variateInheritedList[1])      
            else:
                cmds.image(image1, e=True, image=variateInheritedList[3]) 
             
        # This is for controling the 'radioButtonGrp' on the UI.       
        elif controlName == 'rbg1':   
            radioButtonGrp1Select=cmds.radioButtonGrp( rbg1, q=True, select=True )
            cmds.text( t1, e=True, label=variateValueDic[radioButtonGrp1Select][0])
            cmds.text( t2, e=True, label=variateValueDic[radioButtonGrp1Select][1])
            if radioButtonGrp1Select == 1:
                cmds.floatField( ff1, e=True, minValue=uiValueDic['ff1']['v'][0][0], value=uiValueDic['ff1']['v'][0][1], precision=variateValueDic[radioButtonGrp1Select][2] )
                cmds.floatField( ff2, e=True, minValue=uiValueDic['ff2']['v'][0][0], value=uiValueDic['ff2']['v'][0][1], precision=variateValueDic[radioButtonGrp1Select][2] )
            else:  
                radioButtonGrp2Select=cmds.radioButtonGrp( rbg2, q=True, select=True )  
                ffMinValue=radioButtonGrp2Select*2                   
                ff1Value=uiValueDic['ff1']['v'][1][1]
                ff2Value=uiValueDic['ff2']['v'][1][1]
                if ff1Value < ffMinValue:
                    ff1Value=ffMinValue
                else:
                    pass
                cmds.floatField( ff1, e=True, minValue=ffMinValue, value=ff1Value, precision=variateValueDic[radioButtonGrp1Select][2] )
                if ff2Value < ffMinValue:
                    ff2Value=ffMinValue
                else:
                    pass
                cmds.floatField( ff2, e=True, minValue=ffMinValue, value=ff2Value, precision=variateValueDic[radioButtonGrp1Select][2] )
            bgc=cmds.button( b1, q=True, bgc=True )
            if bgc[1]<0.3:
                ff2Value=cmds.floatField( ff2, q=True, value=True )
                cmds.floatField( ff1, e=True, value=ff2Value )
            else:
                pass

        # This is for controling the 'button' on the UI.            
        elif controlName == 'b1':        
            bgc=cmds.button( b1, q=True, bgc=True )
            if bgc==[0.6,0.6,0.6]:
                cmds.button( b1, e=True, bgc=[0.1,0.2,0.1] )
                cmds.floatField( ff1, e=True, bgc=[0.1,0.2,0.1] )
                cmds.floatField( ff2, e=True, bgc=[0.1,0.2,0.1] )
                ff2Value=cmds.floatField( ff2, q=True, value=True )
                cmds.floatField( ff1, e=True, value=ff2Value )
            else:
                cmds.button( b1, e=True, bgc=[0.6,0.6,0.6] )
                cmds.floatField( ff1, e=True, bgc=[0.15,0.1,0.1] )
                cmds.floatField( ff2, e=True, bgc=[0.1,0.1,0.15] )
                
        # This is for controling the 'floatField' on the UI.        
        elif controlName == 'ff1':        
            bgc=cmds.button( b1, q=True, bgc=True )
            if bgc==[0.6,0.6,0.6]:
                pass
            else:
                ff1Value=cmds.floatField( ff1, q=True, value=True )
                cmds.floatField( ff2, e=True, value=ff1Value ) 
                
        # This is for controling the 'floatField' on the UI.        
        elif controlName == 'ff2':         
            bgc=cmds.button( b1, q=True, bgc=True )
            if bgc==[0.6,0.6,0.6]:
                pass
            else:
                ff2Value=cmds.floatField( ff2, q=True, value=True )
                cmds.floatField( ff1, e=True, value=ff2Value )  
                
        # This is for controling the 'radioButtonGrp' on the UI. 
        elif controlName == 'rbg2':   
            radioButtonGrp1Select=cmds.radioButtonGrp( rbg1, q=True, select=True ) 
            if radioButtonGrp1Select == 1:
                pass
            else:    
                radioButtonGrp2Select=cmds.radioButtonGrp( rbg2, q=True, select=True )  
                ffMinValue=radioButtonGrp2Select*2    
                ff1Value=cmds.floatField( ff1, q=True, value=True ) 
                ff2Value=cmds.floatField( ff2, q=True, value=True )            
                if ff1Value < ffMinValue:
                    ff1Value=ffMinValue
                else:
                    pass
                cmds.floatField( ff1, e=True, minValue=ffMinValue, value=ff1Value, precision=variateValueDic[radioButtonGrp1Select][2] )
                if ff2Value < ffMinValue:
                    ff2Value=ffMinValue                    
                else:
                    pass
                cmds.floatField( ff2, e=True, minValue=ffMinValue, value=ff2Value, precision=variateValueDic[radioButtonGrp1Select][2] )
                                
        # This is for the 'Cancel' and the 'closeWindow' button on the UI.
        elif controlName == 'cancel':          
            cmds.deleteUI(windowName) 
                    
        # This is for controling the 'Save Settings' on the UI.   
        elif controlName == 'Save Settings':  
            # Get the current value from the UI. 
            optionMenuValue=cmds.optionMenu( om1, q=True, value=True )
            radioButtonGrp1Select=cmds.radioButtonGrp( rbg1,q=True, select=True )
            floatField1CurrentValue=cmds.floatField( ff1, q=True, value=True )
            floatField2CurrentValue=cmds.floatField( ff2, q=True, value=True )
            ff1FloatField1BackgroundColor=cmds.floatField( ff1, q=True, bgc=True )
            ff2FloatField1BackgroundColor=cmds.floatField( ff2, q=True, bgc=True )
            buttonbBackgroundColor=cmds.button( b1, q=True, bgc=True )
            radioButtonGrp2Select=cmds.radioButtonGrp( rbg2, q=True, select=True )
            checkBoxValue=cmds.checkBox( cb1 ,q=True, value=True )
            
            segmentLengthMinValue=0.001
            cvNumberMinValue=radioButtonGrp2Select*2            
            if radioButtonGrp1Select==1:
                cvNumber=[ uiValueDic['ff1']['v'][1][1], uiValueDic['ff2']['v'][1][1] ]
                uiValueDic={'om1':{'value':optionMenuValue}, 'rbg1':{'select':radioButtonGrp1Select}, 'ff1':{'v':[ [segmentLengthMinValue, floatField1CurrentValue], [cvNumberMinValue, cvNumber[0]] ], 'bgc':ff1FloatField1BackgroundColor}, 'ff2':{'v':[ [segmentLengthMinValue, floatField2CurrentValue], [cvNumberMinValue, cvNumber[1]] ], 'bgc':ff2FloatField1BackgroundColor}, 'b1':{'bgc':buttonbBackgroundColor}, 'rbg2':{'select':radioButtonGrp2Select}, 'cb1':{'value':checkBoxValue} }     

            else:
                segmentLength=[ uiValueDic['ff1']['v'][0][1], uiValueDic['ff2']['v'][0][1] ]
                uiValueDic={'om1':{'value':optionMenuValue}, 'rbg1':{'select':radioButtonGrp1Select}, 'ff1':{'v':[ [segmentLengthMinValue, segmentLength[0]], [cvNumberMinValue, floatField1CurrentValue] ], 'bgc':ff1FloatField1BackgroundColor}, 'ff2':{'v':[ [segmentLengthMinValue, segmentLength[1]], [cvNumberMinValue, floatField2CurrentValue] ], 'bgc':ff2FloatField1BackgroundColor}, 'b1':{'bgc':buttonbBackgroundColor}, 'rbg2':{'select':radioButtonGrp2Select}, 'cb1':{'value':checkBoxValue} }     
            uiResetCurvesOutputDic[13] = uiValueDic
            # Save the current value in '.py' file.
            if presetFilePath != False:
                pyFile = open(presetFilePath,"w")
                pyFile.write('resetCurvesPresetValueDic='+str(uiValueDic))
                pyFile.close()
                print("The preset file have been saved in the directory: "+presetFilePath)                    
            else:
                print("Couldn't find the directory for saving the preset file: "+presetFile) 
                
        # This is for controling the 'Reset Settings' on the UI.            
        elif controlName == 'Reset Settings':  
            # Reset all settings in the UI.
            uiValueDic = uiDefaultValueDic
            uiResetCurvesOutputDic[13] = uiDefaultValueDic 
            cmds.optionMenu( om1, e=True, value=uiValueDic['om1']['value'] )
            cmds.radioButtonGrp( rbg1, e=True, select=uiValueDic['rbg1']['select'] )
            cmds.floatField( ff1, e=True, minValue=uiValueDic['ff1']['v'][(uiValueDic['rbg1']['select']-1)][0], value=uiValueDic['ff1']['v'][(uiValueDic['rbg1']['select']-1)][1], bgc=uiValueDic['ff1']['bgc'], precision=variateValueDic[uiValueDic['rbg1']['select']][2] )
            cmds.floatField( ff2, e=True, minValue=uiValueDic['ff2']['v'][(uiValueDic['rbg1']['select']-1)][0], value=uiValueDic['ff2']['v'][(uiValueDic['rbg1']['select']-1)][1], bgc=uiValueDic['ff2']['bgc'], precision=variateValueDic[uiValueDic['rbg1']['select']][2] )
            cmds.button( b1, e=True, bgc=uiValueDic['b1']['bgc'] )
            cmds.radioButtonGrp( rbg2, e=True, select=uiValueDic['rbg2']['select'])
            cmds.checkBox( cb1 ,e=True, value=uiValueDic['cb1']['value'] )            
            # Delete the preset '.py' file.
            if os.path.exists(presetFilePath):
                os.remove(presetFilePath)
                print("All the settings in the UI have been set to their default values." )
            else:
                pass   
                                                               
        # This is a function for the information about 'Reset Curve(s)'.      
        elif controlName == 'Reset Curves Information':           
            message='Author: RIST JIANWEN CHENG\nPython Version: 3.10.8\nSystem: Linux\nSupport: Updated as MAYA versions\nCreation Date: May 21, 2016\nUpdated Date: Aug 01, 2025\nVersion: 1.6'
            cmds.confirmDialog( title="Information", message=message, messageAlign='right', button=['CLOSE'], dismissString='CLOSE', backgroundColor=[1,1,1,] )

        # This is a function for opening the PDF help document about 'Reset Curve(s)'.          
        elif controlName == 'Reset Curves PDF': 
            import webbrowser
            
            url = 'https://pub-8231e5ac90c04ce199d0a2879d3ea6ec.r2.dev/Reset%20Curves_Document.pdf'
            webbrowser.open(url)
            
        # Invaild parameter.                                                        
        else:
            cmds.error('Invaild parameter '+option+' for varibable option')
                                              
        return controlName 




# In MAYA shelf edit as python.
"""
import importlib
import CFX.Reset_Curves.reset_curves as reset_curves
importlib.reload(reset_curves)
reset_curves.ui_resetCurves(position='default')
"""
