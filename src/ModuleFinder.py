import os
import json
import importlib
import importlib.util

def findAllJSONs(folderPath):
    foundJSONs = []
    for root, _, files in os.walk(folderPath):
        for file in files:
            if file.lower().endswith(".json"):
                foundJSONs.append(os.path.join(root, file))
    return foundJSONs

validPackages = ["renderer", "environment", "cell"]
def validatePackageJSON(JSON):
    output = False
    if "package type" in JSON and JSON["package type"] in validPackages and "package name" in JSON and "package path" in JSON:
        if JSON["package type"] == "cell" and "cell types" in JSON:
            output = True
            if len(JSON["cell types"]) < 0:
                output = False
            else:
                for cellType in JSON["cell types"]:
                    if not ("cell name" in cellType and "cell class" in cellType):
                        output = False
        else:
            if "package class" in JSON:
                output = True
            
    return output

def findPackageJSONs(folderPath):
    JSONPaths = findAllJSONs(folderPath)
    JSONs = []
    for path in JSONPaths:
        with open(path, "r") as file:
            JSON = json.load(file)
            if validatePackageJSON(JSON):
                JSON["package path"] = path + "\\" + JSON["package path"]
                JSONs.append(JSON)
    return JSONs

def filterJSONsByType(JSONList, packageType):
    filteredList = []

    for JSON in JSONList:
        if not validatePackageJSON(JSON):
            continue

        if JSON["package type"] == packageType:
            filteredList.append(JSON)
    
    return filteredList

def removeJSONsWithoutDependencies(JSONList):
    renderers = filterJSONsByType(JSONList, "renderer")
    environments = filterJSONsByType(JSONList, "environment")
    cellPacks = filterJSONsByType(JSONList, "cell")

    rendererClassNames = []
    for renderer in renderers:
        if "package class" in renderer and renderer["package class"] != "":
            rendererClassNames.append(renderer["package class"])
    
    validEnvironments = []
    environmentClassNames = []
    for environment in environments:
        if "package class" in environment and environment["package class"] != "":
            if "renderer class" in environment and environment["renderer class"] != "":
                if environment["renderer class"] in rendererClassNames:
                    environmentClassNames.append(environment["package class"])
                    validEnvironments.append(environment)
                    
    validCellPacks = []
    for cellPack in cellPacks:
        if "environment class" in cellPack and cellPack["environment class"] != "":
            if cellPack["environment class"] in environmentClassNames:
                validCellPacks.append(cellPack)

    return (renderers, validEnvironments, validCellPacks)

def loadRenderer(rendererJSON):
    moduleSpec = importlib.util.spec_from_file_location("LoadedRenderer", rendererJSON["package path"])
    if moduleSpec is None:
        return None
    foundModule = importlib.util.module_from_spec(moduleSpec)

    try:
        moduleSpec.loader.exec_module(foundModule)
        classReference = getattr(foundModule, rendererJSON["package class"])

        return classReference
    except Exception as e:
        return None

def loadEnvironment(environmentJSON):
    moduleSpec = importlib.util.spec_from_file_location("LoadedEnvironment", environmentJSON["package path"])
    if moduleSpec is None:
        return None   
    foundModule = importlib.util.module_from_spec(moduleSpec)

    try:
        moduleSpec.loader.exec_module(foundModule)
        classReference = getattr(foundModule, environmentJSON["package class"])

        return classReference

    except Exception as e:
        return None

def loadCellPack(cellPackJSON):
    cells = []
    moduleSpec = importlib.util.spec_from_file_location("LoadedCellPack", cellPackJSON["package path"])
    if moduleSpec is None:
        return cells
    
    foundModule = importlib.util.module_from_spec(moduleSpec) 
    try:
        moduleSpec.loader.exec_module(foundModule)

        for cellType in cellPackJSON["cell types"]:
            classReference = getattr(foundModule, cellType["cell class"])
            cells.append(classReference)

    except Exception as e:
        pass        
    return cells