#!/usr/bin/env python
# -*- coding: utf-8 -*-
# xml_declaration=True
# encoding="utf-8"

import xml.dom.minidom #only used to pretty print the xml file after the elements are created
from lxml import etree
import sys
import csv
import json
import xml.etree.ElementTree as ET


print('python file name:', str(sys.argv[0]))#2017510017.py
print('input file:', str(sys.argv[1]))#file to be converted/validated
print('output/xsd file:', str(sys.argv[2]))#converted/xsd file
print('type:', str(sys.argv[3]))#1,2,3,4,5,6,7


#csv to xml
if sys.argv[3] == '1':#python3 2017510017.py DEPARTMENTS.csv csvtoxml.xml 1
    linecount = 0
    unicount = 0
    with open(str(sys.argv[1]), "r") as f:
        line_data = f.readline()
        field = line_data.split(";") #first line is splitted as field, ";" used as separator
    
        elements = []

        line_data = f.readline()
        departments = ET.Element('departments')#this is the root
        elements = line_data.split(";")

        university = ET.SubElement(departments, "university")#first department, 2nd line of the file is created before the other elements because in my algorithm the loop compares the current element's university name and previous element's university name. so in order to not lose the first university, i have to create it before the for loop
        university.set('name',elements[1])
        university.set("uType",elements[0])
        item = ET.SubElement(university, "item")#after the uni name and type is set to the university element, a subelement of univeristy is created, and is called 'item', this is the first department 
        item.set('id',elements[3])
        item.set('faculty',elements[2])
            
        name = ET.SubElement(item, "name")
        if(elements[5] == 'İngilizce'):
            name.set('lang' , 'en')
        else:
            name.set('lang', 'empty')#if the language part is null, then we set 'empty' as the value
    
        if(elements[6] == 'İkinci Öğretim'):
            name.set('second','iö')
        else:
            name.set('second','öö')#if its a second education, then iö (ikinci öğretim); if its first, then öö (örgün öğretim)
        name.text = elements[4]
    
        period = ET.SubElement(item,"period")
        period.text = elements[8]

        quota = ET.SubElement(item,"quota")
        quota.set('spec',elements[11])
        quota.text = elements[10]

        field = ET.SubElement(item,"field")
        field.text = elements[9]

        last_min_score = ET.SubElement(item,"last_min_score")
        last_min_score.set('order',elements[12])
        last_min_score.text = elements[13]

        grant = ET.SubElement(item,"grant")
        grant.text = elements[7]#other attributes are set
        for line in f: #this for loop takes care of the other lines in the same way above
            linecount+=1
            prevelement = elements#store the previously created element
            elements = line.split(";")#now split the current element
          
            if (linecount > 1):#if the line doesnt point at the first line, whcih we have already created
                if prevelement[1] != elements[1]:#compare the previously created element and current element's university names. if they are different; create the new university as a subelement of departments. if its the same university, move on
                    university = ET.SubElement(departments, "university")
                    university.set('name',elements[1])
                    university.set("uType",elements[0])
            
            item = ET.SubElement(university, "item")
            item.set('id',elements[3])
            item.set('faculty',elements[2])
          
            name = ET.SubElement(item, "name")
            if(elements[5] == 'İngilizce'):
                name.set('lang' , 'en')
            else:
                name.set('lang', 'empty')
    
            if(elements[6] == 'İkinci Öğretim'):
                name.set('second','iö')
            else:
                name.set('second','öö')
            name.text = elements[4]
    
            period = ET.SubElement(item,"period")
            period.text = elements[8]

            quota = ET.SubElement(item,"quota")
            quota.set('spec',elements[11])
            quota.text = elements[10]

            field = ET.SubElement(item,"field")
            field.text = elements[9]

            last_min_score = ET.SubElement(item,"last_min_score")
            last_min_score.set('order',elements[12])
            last_min_score.text = elements[13]

            grant = ET.SubElement(item,"grant")
            grant.text = elements[7]#rest of the attributes are set

    
    xmlstr = ET.tostring(departments,encoding="unicode",method='xml')#create the xml file
    dom = xml.dom.minidom.parseString(xmlstr)
    pretty_xml_as_string = dom.toprettyxml()#take care of the turkish characters
    pretty_xml_as_string.replace("","null")
    xmlfile = open(str(sys.argv[2]), "w")
    xmlfile.write(pretty_xml_as_string)#writing the xml string to the file

   


#xml to csv
elif sys.argv[3] == '2':#python3 2017510017.py csvtoxml.xml xmltocsv.csv 2

    tree = ET.parse(str(sys.argv[1]))
    root = tree.getroot()#get the root of the xml file

    with open(str(sys.argv[2]), 'w') as csvfile:#open an empty csvfile to write
        csv.register_dialect("semicolon", delimiter=";")#the delimiter is ";" like in the original DEPARTMENTS.csv file
        writer = csv.writer(csvfile, dialect='semicolon')
        fieldrow = "ÜNİVERSİTE_TÜRÜ","ÜNİVERSİTE","FAKÜLTE","PROGRAM_KODU","PROGRAM","DİL","ÖĞRENİM_TÜRÜ","BURS","ÖĞRENİM_SÜRESİ","PUAN_TÜRÜ","KONTENJAN","OKUL_BİRİNCİSİ_KONTENJANI","GEÇEN_YIL_MİN_SIRALAMA","GEÇEN_YIL_MİN_PUAN"
        writer.writerow(fieldrow)#write the filedrow into the file

        for elem in root:#for every element in root, meaning every university
            for subelem in elem.findall('item'):#for every subelement in root that contains 'item', meaning every deparment (item) of the university

                tuple_elements = (elem.get('uType'),elem.get('name'),subelem.get('faculty'),subelem.get('id'),subelem.find('name').text, subelem.find('name').get('lang'),subelem.find('name').get('second'),subelem.find('grant').text, subelem.find('period').text, subelem.find('field').text,subelem.find('quota').text, subelem.find('quota').get('spec'),subelem.find('last_min_score').get('order'),subelem.find('last_min_score').text) #this part finds all the necessary attributes in the order of the field row and assigns them into a tuple. for example: uType is an attribute of elem and elem is a child of root. elem.get('uType') means i'm accessing the 'uType' attribute of the elem (university). subelem.find('last_min_score').get('order') means i'm trying to access attribute 'order' which is inside 'last_min_score'. i have to use subelem (since last_min_score is inside item, not directly inside university) and subelem.find, since i don't want 'last_min_score' but 'order', an attribute of 'last_min_score'. so i 'find' 'last_min_score' and access 'order'
                
                last_element = tuple_elements[13].replace("\n","")#the last element of tuple has '\n' at the end of line, so i'm getting rid of it to make it look better in this part
                list_elements = list(tuple_elements)#converting tuple into list
                list_elements[13] = last_element#change the '\n'element in the list into ''
                tuple_elements = tuple(list_elements)#convert list into tuple again
                writer.writerow(tuple_elements)#write the tuple into the csv file as a row
       
        
       
#xml to json
elif sys.argv[3] == '3':#python3 2017510017.py csvtoxml.xml xmltojson.json 3
    tree = ET.parse(str(sys.argv[1]))
    root = tree.getroot()#get root
    fieldrow = "ÜNİVERSİTE_TÜRÜ","ÜNİVERSİTE","FAKÜLTE","PROGRAM_KODU","PROGRAM","DİL","ÖĞRENİM_TÜRÜ","BURS","ÖĞRENİM_SÜRESİ","PUAN_TÜRÜ","KONTENJAN","OKUL_BİRİNCİSİ_KONTENJANI","GEÇEN_YIL_MİN_SIRALAMA","GEÇEN_YIL_MİN_PUAN"
    
    json_dict = ""
    jsonloadedestr =""
    with open(str(sys.argv[1]), 'r') as xmlfile:
        with open(str(sys.argv[2]), 'w') as json_file:#open xml and json files to read and write, consecutively
            json_file.write("[")#i wrote the [] file to avoid the error "end of file expected" whenever a new university is created
            unicount = 0
            for elem in root:
                unicount+=1#counting universities to decide which ones will get "," after the paranthesis are closed
                
                json_dict ={ #create the json element and put the university information in it
                    'university name': elem.get('name'),
                    'uType': elem.get('uType'),
                    'items':
                    [  
                        {
                            'faculty':elem.find('item').get('faculty'),
                            'department':[]
                        }
                    ],
                }
                item = json_dict['items']#find the 'items' of json_dict so i can access 'department' and add the departments of the university inside of it
                
                for subelem in elem.findall('item'):
                    first_element = item[0]
                    deps = first_element['department']#access the departments[] of json_dict
                    
                    json_dict_departments = {
                        'id' : subelem.get('id'),
					    'name': subelem.find('name').text,
					    'lang': subelem.find('name').get('lang'),
					    'second':subelem.find('name').get('second'),
					    'period': subelem.find('period').text,
					    'spec': subelem.find('quota').get('spec'),
					    'quota': subelem.find('quota').text,
					    'field': subelem.find('field').text,
					    'last_min_score': subelem.find('last_min_score').text,
					    'last_min_order': subelem.find('last_min_score').get('order'),
					    'grant': subelem.find('grant').text

                               
                    }
                    deps.append(json_dict_departments)#add the department info into departments
                    jsonstr = json.dumps(json_dict, ensure_ascii=False,indent = 4, sort_keys=False).encode('utf8')#ensure_ascii and encode parts are used to handle the turkish characters
                    json_loaded = json.loads(jsonstr)#load string as json dictionary
                jsonloadedestr = json.dumps(json_loaded, ensure_ascii=False,indent = 4, sort_keys=False).encode('utf8')#load it as a string after all the departments of a university is added
                
                if(unicount!=8):
                    json_file.write(jsonloadedestr.decode()+",")
                elif unicount == 8:
                    json_file.write(jsonloadedestr.decode())#if its not the last university, add "," else don't (because its the end of the file)

            json_file.write("]")
#json to xml
elif sys.argv[3] == '4':#python3 2017510017.py xmltojson.json jsontoxml.xml 4
    with open(str(sys.argv[1]),'r') as jsonfile:
        departments = ET.Element('departments')
        loaded_deps = json.load(jsonfile) #load the jsonfile as string
        for uni in loaded_deps: #for every element in loaded json
            uniname = (json.dumps(uni['university name'],ensure_ascii=False))
            uType = (json.dumps(uni['uType'],ensure_ascii=False))
            university = ET.SubElement(departments, "university")
            university.set('name',uniname)
            university.set("uType",uType)#add the university name and type as a university object
            for i in range(len(uni['items'][0]['department'])):#for each department of the university
                item = ET.SubElement(university, "item")
                item.set('id',json.dumps(uni['items'][0]['department'][i]['id'],ensure_ascii=False))#i here traverses the json object's department elements for each university. so [items][0][department][i][id] means that: use [items][0] to access[departments] (or [faculty] since there is only one 'items' for each university) and [departments][i] to access the 'i'th department of a university.
                item.set('faculty',json.dumps(uni['items'][0]['faculty'],ensure_ascii=False))

                name = ET.SubElement(item, "name")
                if(json.dumps(uni['items'][0]['department'][i]['lang'],ensure_ascii=False) == 'İngilizce'):
                    name.set('lang' , 'en')
                else:
                    name.set('lang', 'empty')
    
                if(json.dumps(uni['items'][0]['department'][i]['second'],ensure_ascii=False) == 'İkinci Öğretim'):
                    name.set('second','iö')
                else:
                    name.set('second','öö')
                name.text = json.dumps(uni['items'][0]['department'][i]['name'],ensure_ascii=False)
    
                period = ET.SubElement(item,"period")
                period.text = json.dumps(uni['items'][0]['department'][i]['period'],ensure_ascii=False)

                quota = ET.SubElement(item,"quota")
                quota.set('spec',json.dumps(uni['items'][0]['department'][i]['spec'],ensure_ascii=False))
                quota.text = json.dumps(uni['items'][0]['department'][i]['quota'],ensure_ascii=False)

                field = ET.SubElement(item,"field")
                field.text = json.dumps(uni['items'][0]['department'][i]['field'],ensure_ascii=False)

                last_min_score = ET.SubElement(item,"last_min_score")
                last_min_score.set('order',json.dumps(uni['items'][0]['department'][i]['last_min_order'],ensure_ascii=False))
                last_min_score.text = json.dumps(uni['items'][0]['department'][i]['last_min_score'],ensure_ascii=False)

                grant = ET.SubElement(item,"grant")
                grant.text = json.dumps(uni['items'][0]['department'][i]['grant'],ensure_ascii=False)#add other attributes of the department

        xmlstr = ET.tostring(departments,encoding="unicode",method='xml')
        xmlfile = open(str(sys.argv[2]), "w")#create the xml file
        
        dom = xml.dom.minidom.parseString(xmlstr)
        newxmlstr = dom.toprettyxml()#take care of the turkish characters

        newxmlstr = newxmlstr.replace("&quot;","")#get rid of the escape character of quotation mark
        newxmlstr = newxmlstr.replace("\\n","")#get rid of the '\n' at the end of line
        xmlfile.write(newxmlstr)#write the new string into the xml file

#csv to json
elif sys.argv[3] == '5':#python3 2017510017.py DEPARTMENTS.csv csvtojson.json 5

    
    with open(str(sys.argv[2]), 'w') as jsonfile:
        with open(str(sys.argv[1]),'r') as csvfile:#open json and csvfiles to write and read, consecutively
            json_dict = []
            json_dict_departments=[]
            unidepcount=[13,9,28,28,10,4,5,8]#i keep the universities' department counts in a list because when i tried to write into the file in the for loop, every university was written again and again everytime a new department was added. for example dokuz eylül was written 13 different times, each of them had one more department compared to the other one. so i used these department counts to make sure theyre only written once, that is after the last of the deparments were added

            unicount=0#counts the universities
            depcount = 0#counts the departments
            linecount = 0#counts lines

            lines = csvfile.readline()
            fields = lines.split(";")
            jsonfile.write("[")#writing [] into the json file to avoid "end of file expected" whenever a new university is added

            for line in csvfile:#reads every line
                linecount+=1              
                data = line.split(";")
                first_element=[]
                
                if((linecount==1) | (linecount==14) | (linecount==23) |(linecount==51) |(linecount==79) |(linecount==89 )|(linecount==93) |(linecount==98 )):#if a new university is being added
                    depcount=1#whenever a new university and its first department is added, the department count becomes 1
                    unicount+=1#incrementing the university count 
                    if(data[5]=='İngilizce'):
                        data[5]="en"
                    if(data[6]=='İkinci Öğretim'):
                        data[6]="yes"
                    else:
                        data[6]="no"

                    json_dict = {#first department of each university
                        'university name': data[1],
                        'uType': data[0],
                        'items':
                        [  
                            {
                                'faculty':data[2],
                                'department':
                                [
                                    {'id' : data[3],
                                    'name': data[4],
                                    'lang': data[5],
                                    'second':data[6],
                                    'period': data[8],
                                    'spec': data[11],
                                    'quota': data[10],
                                    'field': data[9],
                                    'last_min_score': data[13],
                                    'last_min_order': data[12],
                                    'grant': data[7]}
                                ]
                            }
                        ]
                    }
                    jsonstr = json.dumps(json_dict, ensure_ascii=False,indent = 4, sort_keys=False).encode('utf8')
                    jsondata = json.loads(jsonstr)#saving json_dict in a way i can use as a list and append rest of the departments in it
                    
                else:
                    depcount+=1#incrementing the department count if a theres no new university
                    if(data[5]=='İngilizce'):
                        data[5]="en"
                    if(data[6]=='İkinci Öğretim'):
                        data[6]="yes"
                    else:
                        data[6]="no"
                    json_dict_departments={#for departments other than the first one
                            
                        'id' : data[3],
                        'name': data[4],
                        'lang': data[5],
                        'second':data[6],
                        'period': data[8],
                        'spec': data[11],
                        'quota': data[10],
                        'field': data[9],
                        'last_min_score': data[13],
                        'last_min_order': data[12],
                        'grant': data[7]                   
                    }
                    
                    jsondata['items'][0]['department'].append(json_dict_departments)#getting the 'department[]' object of the university and appending the department we just created at the end
                    
                    if(unidepcount[unicount-1]==depcount):#if the department count we have been incrementing is equal to its corresponding university's total department count, then it means all of the departments have been appended to jsondata and they are ready to be written into the file. after this, the program will start over for another university 
                        jsonstr = json.dumps(jsondata, ensure_ascii=False,indent = 4, sort_keys=False).encode('utf8')
                        json_loaded = json.loads(jsonstr)
                        jsonloadedestr = json.dumps(json_loaded, ensure_ascii=False,indent = 4, sort_keys=False).encode('utf8')
                        

                        if(unicount!=8):
                            jsonfile.write(jsonloadedestr.decode()+",")
                        elif(unicount==8):
                            jsonfile.write(jsonloadedestr.decode())#after the conversion into a more readable variable, the university with its departments is written to the json file. if it is not the last university, add a comma.

            jsonfile.write("]")

#json to csv
elif sys.argv[3] == '6': #python3 2017510017.py xmltojson.json jsontocsv.csv 6 OR python3 2017510017.py csvtojson.json jsontocsv.csv 6
    linecount = 0
    with open(str(sys.argv[2]), 'w') as csvfile:
        with open(str(sys.argv[1]),'r') as jsonfile:#open csvfile and jsonfile to write and read consecutively
            loaded_deps = json.load(jsonfile) 
            fieldrow = "ÜNİVERSİTE_TÜRÜ;ÜNİVERSİTE;FAKÜLTE;PROGRAM_KODU;PROGRAM;DİL;ÖĞRENİM_TÜRÜ;BURS;ÖĞRENİM_SÜRESİ;PUAN_TÜRÜ;KONTENJAN;OKUL_BİRİNCİSİ_KONTENJANI;GEÇEN_YIL_MİN_SIRALAMA;GEÇEN_YIL_MİN_PUAN\n"
            csvfile.write(fieldrow)#write the fields into csvfile
            for uni in loaded_deps:#for each university
                uniname = ((json.dumps(uni['university name'],ensure_ascii=False)).replace("\"","")+";")#replacing the unnecessary quotation marks with ";"
                uType =  ((json.dumps(uni['uType'],ensure_ascii=False)).replace("\"","")+";")#added the university name and type for each university
              
                for i in range(len(uni['items'][0]['department'])):#for each department of the university
                    faculty =  ((json.dumps(uni['items'][0]['faculty'],ensure_ascii=False)).replace("\"","")+";")
                    id = ((json.dumps(uni['items'][0]['department'][i]['id'],ensure_ascii=False)).replace("\"","")+";")
                    name = ((json.dumps(uni['items'][0]['department'][i]['name'],ensure_ascii=False)).replace("\"","")+";")
                    if (json.dumps(uni['items'][0]['department'][i]['lang'],ensure_ascii=False).replace("\"","") == "en"):
                        lang = "İngilizce;"
                    else:
                        lang = "Türkçe;"#changing the value from en to english and if its null, making it turkish

                    if (json.dumps(uni['items'][0]['department'][i]['second'],ensure_ascii=False).replace("\"","") == "yes"):
                        second = "İkinci Öğretim;"#if second="yes" then its ikinci öğretim
                    else:
                        second = "Örgün Öğretim;"

                    grant = (json.dumps(uni['items'][0]['department'][i]['grant'],ensure_ascii=False).replace("\"","").replace("\"","")+";")
                    period = ((json.dumps(uni['items'][0]['department'][i]['period'],ensure_ascii=False)).replace("\"","")+";")
                    field = ((json.dumps(uni['items'][0]['department'][i]['field'],ensure_ascii=False)).replace("\"","")+";")
                    quota = ((json.dumps(uni['items'][0]['department'][i]['quota'],ensure_ascii=False)).replace("\"","")+";")
                    spec = ((json.dumps(uni['items'][0]['department'][i]['spec'],ensure_ascii=False)).replace("\"","")+";")
                    last_min_order = ((json.dumps(uni['items'][0]['department'][i]['last_min_order'],ensure_ascii=False)).replace("\"","")+";")
                    last_min_score = ((json.dumps(uni['items'][0]['department'][i]['last_min_score'],ensure_ascii=False)).replace("\"",""))

                    csvfile.write(uType)
                    csvfile.write(uniname)
                    csvfile.write(faculty)
                    csvfile.write(id)
                    csvfile.write(name)
                    csvfile.write(lang)
                    csvfile.write(second)
                    csvfile.write(grant)
                    csvfile.write(period)
                    csvfile.write(field)
                    csvfile.write(quota)
                    csvfile.write(spec)
                    csvfile.write(last_min_order)
                    csvfile.write(last_min_score.replace("\\n",""))#writing all of the variables into the csvfile

                    csvfile.write("\n")#for a newline

#xsd validation
elif sys.argv[3] == '7': #python3 2017510017.py csvtoxml.xml validate.xsd 7 OR python3 2017510017.py jsontoxml.xml validate.xsd 7
    xmlpath = str(sys.argv[1])
    xsdpath = str(sys.argv[2])#get paths of both the input and putput files

    xmlschema_doc = etree.parse(xsdpath)#parse xsd
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xmlpath)#parse xml
    validation_result = xmlschema.validate(xml_doc)#validate and keep the result

    print(validation_result)
    xmlschema.assert_(xml_doc)
