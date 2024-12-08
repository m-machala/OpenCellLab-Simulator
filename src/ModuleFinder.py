import os
import json

def findAllJSONs(folderPath):
    foundJSONs = []
    for root, _, files in os.walk(folderPath):
        for file in files:
            if file.lower().endswith(".json"):
                foundJSONs.append(os.path.join(root, file))
    return foundJSONs

def findPackageJSONs(folderPath):
    JSONPaths = findAllJSONs(folderPath)
    JSONs = []
    validPackages = ["renderer", "environment", "cell"]
    for path in JSONPaths:
        with open(path, "r") as file:
            JSON = json.load(file)

            if "package type" in JSON and JSON["package type"] in validPackages:
                JSONs.append(JSON)
    return JSONs