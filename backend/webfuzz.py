from itertools import product
from re import sub
from requests import request
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def webfuzz(args):
    url = args.url
    wordlists = args.wordlists
    headers = args.headers
    method = args.method
    data = args.data

    no_verify = args.no_verify
    if no_verify:
        disable_warnings(InsecureRequestWarning)

    status_codes = args.status_codes
    sizes = args.sizes

    no_status_codes = args.no_status_codes
    no_sizes = args.no_sizes

    words = []
    variablesNumber = len(wordlists)
    wordsSpaceCardinality = 1
    for variableIndex in range(variablesNumber):
        with open(wordlists[variableIndex],"r") as wordlistFile:
            words += [wordlistFile.read().splitlines()]
            wordsSpaceCardinality *= len(words[-1])

    wordsSpace = product(*words)
    wordsIteration = 0
    for wordsTuple in product(*words):
        wordsIteration += 1
        print(f"{wordsIteration}/{wordsSpaceCardinality}")
        parameters = [method,url]
        if not data:
            parameters += [""]
        if not headers:
            parameters += []
        for variableIndex in range(variablesNumber):
            for index in range(len(parameters)):
                parameters[index] = sub(f"<{variableIndex + 1}>",wordsTuple[variableIndex],parameters[index])
        response = request(method=parameters[0],url=parameters[1],data=parameters[2],headers=parameters[3:],verify=(not no_verify))
        size = len(response.content)
        if  ((   response.status_code in status_codes and
                response.status_code not in no_status_codes    ) and
            (   size in sizes and
                 size in no_sizes   )):
            print(f"{response.status_code}\t{size}\t{parameters}")
