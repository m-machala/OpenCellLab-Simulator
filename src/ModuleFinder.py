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

validPackages = ["renderer", "environment", "cell", "loader", "loader data"]
def validatePackageJSON(JSON):
    output = False
    if "package type" in JSON and JSON["package type"] in validPackages and "package name" in JSON and JSON["package name"] != "" and "package path" in JSON and JSON["package path"] != "":
        if JSON["package type"] == "cell":
            output = True
            if not "cell types" in JSON or len(JSON["cell types"]) <= 0:
                output = False
            else:
                for cellType in JSON["cell types"]:
                    if not ("cell name" in cellType and "cell class" in cellType and cellType["cell name"] != "" and cellType["cell class"] != ""):
                        output = False
        elif JSON["package type"] == "loader data":
            output = True
            if len(JSON["cell types"]) <= 0 or ("environment type"  in JSON and JSON["environment type"] == "any"):
                output = False
        else:
            if "package class" in JSON and JSON["package class"] != "":
                output = True
            
    return output

def findPackageJSONs(folderPath):
    JSONPaths = findAllJSONs(folderPath)
    JSONs = []
    for path in JSONPaths:
        with open(path, "r") as file:
            JSON = json.load(file)
            if validatePackageJSON(JSON):
                directory = os.path.dirname(path)
                JSON["package path"] = os.path.join(directory, JSON["package path"])
                if "package image path" in JSON:
                    JSON["package image path"] = os.path.join(directory, JSON["package image path"])
                if "cell types" in JSON:
                    for cellType in JSON["cell types"]:
                        if "cell image path" in cellType:
                            cellType["cell image path"] = os.path.join(directory, cellType["cell image path"])
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
    loaders = filterJSONsByType(JSONList, "loader")
    loaderData = filterJSONsByType(JSONList, "loader data")

    rendererClassNames = []
    for renderer in renderers:
        rendererClassNames.append(renderer["package class"])
    
    validEnvironments = []
    environmentClassNames = []
    for environment in environments:
        if "renderer class" in environment and environment["renderer class"] != "" and environment["renderer class"] in rendererClassNames:
            environmentClassNames.append(environment["package class"])
            validEnvironments.append(environment)
                    
    validCellPacks = []
    cellClassNames = []
    for cellPack in cellPacks:
        if "environment class" in cellPack and cellPack["environment class"] != "" and cellPack["environment class"] in environmentClassNames:
            empty = True
            for cellType in cellPack["cell types"]:
                empty = False
                cellClassNames.append(cellType["cell class"])
            if not empty:
                validCellPacks.append(cellPack)

    validLoaders = []
    loaderClassNames = []
    for loader in loaders:
        if "package class" in loader and loader["package class"] != "":
            validLoaders.append(loader)
            loaderClassNames.append(loader["package class"])

    validLoaderData = []
    for loaderDatum in loaderData:
        if "environment class" in loaderDatum and loaderDatum["environment class"] != "" and (loaderDatum["environment class"] in environmentClassNames or loaderDatum["environment class"] == "any") and "loader class" in loaderDatum and loaderDatum["loader class"] in loaderClassNames:
            empty = True
            complete = True
            for cellClass in loaderDatum["cell classes"]:
                if cellClass in cellClassNames:
                    empty = False
                else:
                    complete = False
            
            if not empty:
                loaderDatum["complete"] = complete
                validLoaderData.append(loaderDatum)

    return (renderers, validEnvironments, validCellPacks, validLoaders, validLoaderData)

def loadRenderer(rendererJSON):
    moduleSpec = importlib.util.spec_from_file_location(rendererJSON["package name"], rendererJSON["package path"])
    if moduleSpec is None:
        return None
    foundModule = importlib.util.module_from_spec(moduleSpec)

    try:
        moduleSpec.loader.exec_module(foundModule) # type: ignore
        classReference = getattr(foundModule, rendererJSON["package class"])

        return classReference
    except Exception as e:
        return None

def loadEnvironment(environmentJSON):
    return loadRenderer(environmentJSON)

def loadCellPack(cellPackJSON):
    cells = []
    moduleSpec = importlib.util.spec_from_file_location(cellPackJSON["package name"], cellPackJSON["package path"])
    if moduleSpec is None:
        return cells
    
    foundModule = importlib.util.module_from_spec(moduleSpec) 
    try:
        moduleSpec.loader.exec_module(foundModule) # type: ignore

        for cellType in cellPackJSON["cell types"]:
            classReference = getattr(foundModule, cellType["cell class"])
            cells.append((classReference, cellType))

    except Exception as e:
        pass        
    return cells

def loadLoader(loaderJSON):
    return loadRenderer(loaderJSON)
    
