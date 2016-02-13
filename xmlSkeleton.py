import xml.etree.cElementTree as ET
import pprint
import json
import datetime as dt



''' *** You only need to change the following variables ****'''
#working directory
path = 'C:/working/directory/goes-here'
# the file to be explored ( it should be located in the working directory)
fileToDisect = 'riyadh_saudi-arabia.osm'
# the result file ( will be created in the working directory)
fileAfterDisection = 'final-stripped222.xml'
# this is informational only.. to give an idea about the informal XPaths generated
informalXPathsFile ='stripped222.txt'


def mergeAttribs(x):
    '''This method will take a set() as parameter the (x) containing
    the informal xpaths.
    then we loop over them
    in each step we divide the path into xpath and attribs array
    then compare each item in the xpath set() with the items below it
    if they have the same xpath we will join all attribs in one finalItem'''
    
    # x is supposed to be a set() of the (informal) xpaths .[i.e. unique items]
    # we need to change it to a sorted list
    xpaths =sorted(list(x))
    l = len(xpaths)
    finalList =set()
    filtered = False
    for i in range(l):
        item = xpaths[i]
        parts = item.split(' attribs=')
        att = set(parts[1].split(','))
        att.discard('')
        
        if parts[0]!='%':
            combList = ['','']
            
            #print 'filtered before inner loop  = ', filtered
            filtered = False
            for j in range(i+1,l):
                
                nextitem = xpaths[j]
                nextparts = nextitem.split(' attribs=')
                if nextparts[0] != parts[0]:
                    break
                att.update(set(nextparts[1].split(',')))
                att.discard('')
                attStr = ','.join(list(att))
                
                combList[0] = parts[0]
                combList[1] = attStr
                
                finalItem = ' attribs='.join(combList)
                
                xpaths[j] = finalItem
                xpaths[i] = finalItem
                finalList.add(finalItem)
                
                filtered = True
     
            if(filtered == False):
                finalList.add(item)

        
    
    return sorted(set(xpaths))





def breakStr(s):
    '''
    this function will break the string supplied into
    xpath and comma-separated attributes keys
    '''
    attribs = None
    name = s
    result = s.split(' attribs=')
    
    #if thre is attribute keys
    if len(result) > 1:
        name = result[0]
        
        arr = result[1].strip('[]').split(',')
        
        attribs={}
        for i in arr:
            i = i.strip("'")
            attribs[i]=''
        
    return name, attribs
    


def buildXML(s, root):
    
    '''
    This method will take the xpath (informal), and the root Element.
    Then it will process the (informal) xpath via the breakStr() method
    and start building the tree elements
    e.g: the informal xpath will be:
    bookstore/book/author attribs=nationality,fname,lname
    the (bookstore = root) already supplied through the method parameters
    then we will append the 2nd level element (book)
    after that we will use this method recursively on the rest of the nodes'''
    
    listy = s.split('/')
    l = len(listy)
    name, attribs = breakStr(listy[1])
    
    el = root.find(name)
    if el == None:
        el = ET.SubElement(root, name)
    
    
    #print attribs
    if attribs != None and  attribs.keys() !=['']:
        el.attrib.update(attribs)
        
    
    #print el, 'el.. and attrib = ', el.attrib
    for i in range(2,l):
        name, attribs = breakStr(listy[i])
        el2 = el.find(name)
        
        if el2 == None:
            el2 = ET.SubElement(el,name)
        
        
        if attribs != None and  attribs.keys() !=['']:
            #print attribs, len(attribs)
            el2.attrib.update( attribs)
        
        el = el2
        el2 = None
        

print dt.datetime.now(),'Start'


def extractXMLSkeleton(xmlFile):
    '''This is the main method.. it starts by taking the xml file and use iterparse() method
    to loop over all elements , using the other methods in this file to give us what we call the XMLSkeleton
    which is an XML document that has the unique node structures that appeared in every tree element
    
    e.g if the xml file contains 10000 elements of (book), this method will return only one Element of book
    containing the subelements and attributes without any text values iside them
    The purpose is to have a broad idea of the nodes in the file.'''
    xpaths = set()
    x = ''
    currTag = ''
    tagStack = []
    xpathStack = []
    level = -1
    
    
    # we will loop over the elements; when we reach to an END tag we will record the 
    # path and attributes and sent it to the xpaths set() so that it will remember unique values only
    for event, element in ET.iterparse(xmlFile, events=('start','end')):
                if event == 'start':
                    level += 1
                    currTag = element.tag

                    x += '/' + currTag

                    tagStack.append(element.tag)
                    xpathStack.append(x)

                elif event == 'end':
                    x2 = x  +' attribs='+ ','.join(element.attrib.keys())

                    xpaths.add(x2)

                    if level >0:
                        xpathStack.pop()
                        tagStack.pop()
                        level-=1

                        x = xpathStack[level]
                        currTag = tagStack[level]

                    else:
                        xpathStack.pop()                 
                        tagStack.pop()


    strAll =''
    
    
    # the previous loop could capture the unique xpaths but the attributes are problematic
    # e.g. bookstore/book/author is captured only once in the xpaths set()
    # but the following three paths are all unique
    # bookstore/book/author attribs=fname
    # bookstore/book/author attribs=fname,lname
    # bookstore/book/author attribs=nationality
    # we need a unique universal xpath that looks like the following:
    # bookstore/book/author attribs=fname,lname,nationality
    # and that is the role of the mergeAttribs() method in the next line
    xpathsList = mergeAttribs(xpaths)
    
    # We want to convert the xpathList into string
    # One line for each item; to save it in a text file
    # This step is informational; and remving it will not
    # affect the final result
    for i in sorted(xpathsList):
        strAll += i.strip('/') + '\n'


    strippedPaths = [q[1:] for q in xpathsList]
    name, attribs = breakStr(strippedPaths[0])
    
    root = ET.Element(name)
    if attribs != None and attribs.keys() !=['']:
        root.attrib = attribs
        


    # Now we have built the root element to start building the tree
    for w in strippedPaths[1:]:
        buildXML(w[1:],root)
    
    with open(path + fileAfterDisection, 'w') as f:
        f.write(ET.tostring(root))
    with open(path + informalXPathsFile, 'w') as f:
        f.write(strAll)

        
extractXMLSkeleton(path + fileToDisect)

print dt.datetime.now(), 'END --'
