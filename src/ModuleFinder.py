import os
import json
import importlib

def findAllJSONs(folderPath):
    foundJSONs = []
    for root, _, files in os.walk(folderPath):
        for file in files:
            if file.lower().endswith(".json"):
                foundJSONs.append(os.path.join(root, file))
    return foundJSONs

validPackages = ["renderer", "environment", "cell"]
def validatePackageJSON(JSON):
    if "package type" in JSON and JSON["package type"] in validPackages:
        return True
    return False

def findPackageJSONs(folderPath):
    JSONPaths = findAllJSONs(folderPath)
    JSONs = []
    for path in JSONPaths:
        with open(path, "r") as file:
            JSON = json.load(file)

            if validatePackageJSON(JSON):
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