#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import urllib.request, urllib.error, urllib.parse

import xml.etree.ElementTree as ET

from myFunctions import (findVideoFiles, findSubFiles, 
                         getMirrorXml, getTimeXML, timeOut) 

def partRename(searchPath, recursive, extension, renameVideo, renameSub, verbose):
    videoFiles = []
    subFiles = []
    
    if renameVideo:
        videoFiles = findVideoFiles(searchPath, recursive, videoFiles, verbose)
        
    if renameSub:
        subFiles = findSubFiles(searchPath, recursive, extension, subFiles, False, verbose)
        
    if videoFiles:
        print("Videos found:")
        for videoFile in videoFiles:
            print(videoFile)
        print()
    if subFiles:
        print("Subtitles found:")
        for subFile in subFiles:
            print(subFile)
        print()
        
    # mirror = getTheTVdbMirror(verbose)
    # previousTime = getTheTVdbTime(verbose)

def getTheTVdbMirror(verbose):
    mirrors = []
    mirrorId = ""
    mirrorPath = ""
    mirrorTypemask = ""
    
    try:
        response = urllib.request.urlopen(getMirrorXml, timeout=timeOut).read()  # get data from server
        if verbose:
            print("--- Got data")
    except urllib.error.URLError as e:
        if verbose:
            print("*** There was an error: %r" % e)
            print("*** Could not get data")
    
    if verbose:
        print(response)
    
    xmlRoot = ET.fromstring(response)  # read xml
    
    for xmlChild in xmlRoot:
        if 'Mirror' in xmlChild.tag:
            for innerXmlChild in xmlChild:
                if 'id' in innerXmlChild.tag:
                    mirrorId = innerXmlChild.text
                elif 'mirrorpath' in innerXmlChild.tag:
                    mirrorPath = innerXmlChild.text
                elif 'typemask' in innerXmlChild.tag:
                    mirrorTypemask = innerXmlChild.text
            
                if mirrorId and mirrorPath and mirrorTypemask:
                    if int(mirrorTypemask) == 7:
                        hasXml = True
                        hasBanner = True
                        hasZip = True
                    elif int(mirrorTypemask) == 6:
                        hasXml = False
                        hasBanner = True
                        hasZip = True
                    elif int(mirrorTypemask) == 5:
                        hasXml = True
                        hasBanner = False
                        hasZip = True
                    elif int(mirrorTypemask) == 4:
                        hasXml = False
                        hasBanner = False
                        hasZip = True
                    elif int(mirrorTypemask) == 3:
                        hasXml = True
                        hasBanner = True
                        hasZip = False
                    elif int(mirrorTypemask) == 2:
                        hasXml = False
                        hasBanner = True
                        hasZip = False
                    elif int(mirrorTypemask) == 1:
                        hasXml = True
                        hasBanner = False
                        hasZip = False
                        
                    mirrors.append(
                                   {'id': mirrorId,
                                    'path': mirrorPath,
                                    'typemask': mirrorTypemask,
                                    'xml': hasXml,
                                    'banner': hasBanner,
                                    'zip': hasZip}
                                   )
                    mirrorId = ""
                    mirrorPath = ""
                    mirrorTypemask = ""
            
    for line in mirrors:
        print("\nId: %s\nPath: %s\nType mask: %s" % (line['id'], line['path'], line['typemask']))
        if line['xml']:
            print("Has XML")
        if line['banner']:
            print("Has banners")
        if line['zip']:
            print("Has zip")
        
        useMirror = line['path']
        
    print()
    return useMirror
        
def getTheTVdbTime(verbose):
    try:
        response = urllib.request.urlopen(getTimeXML, timeout=timeOut).read()  # get data from server
        if verbose:
            print("--- Got data")
    except urllib.error.URLError as e:
        if verbose:
            print("*** There was an error: %r" % e)
            print("*** Could not get data")
    
    if verbose:
        print(response)
    
    xmlRoot = ET.fromstring(response)  # read xml
    
    for xmlChild in xmlRoot:
        if 'Time' in xmlChild.tag:
            previousTime = xmlChild.text
            
    print("Server time: %s" % previousTime)
    return previousTime

