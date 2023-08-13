#Author-Paul Klinger
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
from math import cos, sin, pi

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        
        fileDlg = ui.createFileDialog()
        fileDlg.isMultiSelectEnabled = False
        fileDlg.title = 'Select time/strain file'
        fileDlg.filter = '*.*'
        
        # Show file open dialog
        dlgResult = fileDlg.showOpen()
        if dlgResult != adsk.core.DialogResults.DialogOK:
            raise ValueError("File not found")
        filename = fileDlg.filenames[0]
        
        (radius_input, cancelled) = ui.inputBox("Zero strain radius", "radius", "10 mm")
        if cancelled:
            raise ValueError("You need to enter a radius!")
        
        unitsMgr = design.unitsManager
        try:
            default_radius = unitsMgr.evaluateExpression(radius_input, unitsMgr.defaultLengthUnits)
        
        except Exception as e:
            raise ValueError("Invalid radius entered!")
            
        (height_input, cancelled) = ui.inputBox("Total height", "height", "200 mm")
        if cancelled:
            raise ValueError("You need to enter a height!")

        try:
            total_height = unitsMgr.evaluateExpression(height_input, unitsMgr.defaultLengthUnits)
        
        except Exception as e:
            raise ValueError("Invalid height entered!")
        
        data = []
        with open(filename) as f:
            for line in f:
                ts, sp, sc = line.split(",")
                data.append((float(ts),float(sp),float(sc)))
 
        rootComp = design.rootComponent        
        
        sketchesObj = rootComp.sketches        
        ctorPlanes = rootComp.constructionPlanes
        
        offset_mult = total_height / float(data[-1][0])

        profiles = []
        sketches = []
        
        for t, sp, sc in data:
            ctorPlaneInput1 = ctorPlanes.createInput()
            offset = adsk.core.ValueInput.createByString("{} cm".format(t * offset_mult))
            ctorPlaneInput1.setByOffset(rootComp.xZConstructionPlane, offset)
            ctorPlane1 = ctorPlanes.add(ctorPlaneInput1)
            sketch = sketchesObj.add(ctorPlane1)
            
            points = adsk.core.ObjectCollection.create()
            Nprofile = 20
            for i in range(Nprofile):
                alpha = 2 * pi * i / Nprofile
                radius = default_radius * (1 + (sp * cos(2 * alpha) + sc * sin(2 * alpha))/2)
                points.add(adsk.core.Point3D.create(
                    radius * cos(alpha),
                    radius * sin(alpha),
                    0))
            points.add(points[0])
            sketch.sketchCurves.sketchFittedSplines.add(points)
            
            profiles.append(sketch.profiles.item(0))
            
            sketches.append(sketch)
            adsk.doEvents()
            
        
        # Create loft feature input
        loftFeats = rootComp.features.loftFeatures
        loftInput = loftFeats.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        loftSectionsObj = loftInput.loftSections
        
        for profile in profiles:
            loftSectionsObj.add(profile)
            adsk.doEvents()
            
        loftInput.isSolid = True

        # Create loft feature
        loftFeats.add(loftInput)
        return
        for sketch in sketches:
            sketch.deleteMe()
            adsk.doEvents()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
