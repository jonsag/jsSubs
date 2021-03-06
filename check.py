#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import os

from myFunctions import (findSubFiles, hasLangCode, 
                         foundLang, checkLang, compareCodes, 
                         prefLangs, languages)

def partCheck(recursive, searchPath, extension, findCode, verbose):  # check if language code set is correct
    langSums = []
    subsFound = []
    num = 0
    subFiles = []
    ask = False

    subFiles = findSubFiles(searchPath, recursive, extension, subFiles, findCode, verbose)

    if subFiles: 
        for myFile in subFiles:
            print("\n%s" % myFile)
            existingCode = hasLangCode(os.path.join(searchPath, myFile))
            subsFound = foundLang(existingCode)
            if existingCode:
                
                if findCode != "all" and findCode != "pref" and findCode != "force":
                    if existingCode['code'] == str(findCode):
                        print("\n%s" % myFile)
                        print((
                               "--- Has language code %s - %s"
                               % (existingCode['code'], existingCode['name'].lower())
                               ))
                        checkedCode = checkLang(myFile, True)  # let detectlanguage.com see what language the file has
                        setCode = compareCodes(existingCode['code'],
                                               checkedCode, myFile, ask)  # compare existing and checked code
                        num += 1
                        langSums = foundLang(setCode)
                        
                elif findCode == "pref":
                    notPref = True
                    for lang in prefLangs:
                        if existingCode['code'] == lang:
                            notPref = False
                    if notPref:
                        print("\n%s" % myFile)
                        print((
                               "--- Has language code %s - %s"
                               % (existingCode['code'], existingCode['name'].lower())
                               ))
                        checkedCode = checkLang(myFile, True)  # let detectlanguage.com see what language the file has
                        setCode = compareCodes(existingCode['code'],
                                               checkedCode, myFile, ask)  # compare existing and checked code
                        num += 1
                        langSums = foundLang(setCode)
                        
                elif findCode == "all":
                    if existingCode:
                        print("\n%s" % myFile)
                        print((
                               "--- Has language code %s - %s"
                               % (existingCode['code'], existingCode['name'].lower())
                               ))
                        checkedCode = checkLang(myFile, 1)  # let detectlanguage.com see what language the file has
                        setCode = compareCodes(existingCode['code'],
                                               checkedCode, myFile, ask)  # compare existing and checked code
                        num += 1
                        langSums = foundLang(setCode)
                elif findCode == "force":
                    ask = True
                    if existingCode:
                        print("\n%s" % myFile)
                        print((
                               "--- Has language code %s - %s"
                               % (existingCode['code'], existingCode['name'].lower())
                               ))
                        checkedCode = checkLang(myFile, 1)  # let detectlanguage.com see what language the file has
                        setCode = compareCodes(existingCode['code'],
                                               checkedCode, myFile, ask)  # compare existing and checked code
                        num += 1
                        langSums = foundLang(setCode)
                    
            else:
                print("*** Has no language code")
    
    if subsFound:
        print("\nAll subtitles found:")
        for lang in languages:
            langSum = subsFound.count(lang['code'])
            if subsFound.count(lang['code']) > 0:
                print("%s - %s:  %d" % (lang['code'], lang['name'].lower(), langSum))
    
    if langSums:
        print("\nChecked:")
        for lang in languages:
            langSum = langSums.count(lang['code'])
            if langSums.count(lang['code']) > 0:
                print("%s - %s:  %d" % (lang['code'], lang['name'].lower(), langSum))
    print()
    
