# xmlSkeleton_py
Find the Skeleton of XML document regardless of the data content

Imagine that you have an xml document that contains 20000 element inside it. When you open it in a file reader and see the nodes you will be overwelmed to recognise the data model.

take the following example:
```xml
<bookstore>
   <book>
     <author firstName ='John' lastName='JK'> 
     </author>
    <price currency='SR' > 900</price>
  </book>

  <book>
    <title>Harry Potter</title>
    <author nickName='Wild'> 
    </author>
    <price> 26</price>
  </book>


  <book hardcover='yes'>
    <title>Great code</title>
    <author country='Italy'> 
    </author>
    <price> 26</price>
    <version>3rd</version>
  </book>

</bookstore>
```

now Imagein that you are having many books elements and every element differ than the other by adding a sub element or adding a new attribute then you will wish that there is a code that will abstract the data model as the following:


```xml
<bookstore>
  <book hardcover=''>
    <author firstName='' lastName='' nickName='' country='' /> 
    <price currency='' />
    <version/>
  </book>
</bookstore>
```
### Disadvatage(s) and limitation(s):
- Although it can show the skeleton of any XML file. However it canpt show the element that has mutually execluded items. e.g.:
```
<bookstore>
<book>
<type ebook="True"/>
</book>

<book>
<type paperback="True"/>
</book>

</bookstore>
```

now suppose that the type of the book version is either ebook or paperback but not both ( just assume that). This code will not detect that . it will give both attribute on the same element as follow

```
<bookstore>
<book>
<type ebook="True" paperback="True"/>
</book>
</bookstore>
```

- The second disadvantage is that this code didn't take in consideration the namespaces elements.

## Get started

To get started; all you have to do is copy the code to your python environment and edit the variables at the top of the file and run the code.
```python

'''*** You only need to change the following variables ****'''
#working directory
path = 'C:/working/directory/goes-here/'
# the file to be explored ( it should be located in the working directory)
fileToDisect = 'riyadh_saudi-arabia.osm'
# the result file ( will be created in the working directory)
fileAfterDisection = 'final-stripped.xml'
# this is informational only.. to give an idea about the informal XPaths generated
informalXPathsFile ='stripped.txt'
```
