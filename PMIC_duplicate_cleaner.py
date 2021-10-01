##Author: Mario Bucalovic  mario.bucalovic@gmail.com OSS and Performance expert
##Python 3.8 libs used : json

#####Rhyme and reason:
#####PM duplicate cleaner
#####made to remove duplicate in multiple PMIC json exports, since duplicates in PMIC profile cause duplication in PM site files
#####also to remove counters if they already exist in predefined PMIC profile
import json


########SETUP part!!!
#Set paths to json exports of counters
# Which exports?: Ericsson Network Manager ->PM Initiation and Collection->edit profile->Counters tab->export

#Add filepaths to user defined counter export files
filepath="C:\\Users\\username\\Desktop\\PM_profili\\ERBS\\ERBS additional_original.json"
filepath2="C:\\Users\\username\\Desktop\\PM_profili\\ERBS\\ERBS_additionall.json"

#Add filepath to system defined counter export files
filepath_system_predefined="C:\\Users\\username\\Desktop\\PM_profili\\ERBS\\ERBS_Predefined.json"

#Add defined filepath var to this list:
putanje=[filepath,filepath2]

#set final output filename
final_filename='counteri_ocisceni.json'
#########SETUP part end!!!

template_intro = """
{{
        "groupName": "{}",
        "eventCounterNames": ["{}"]

}}
,"""

output_template=""" """
grupe_mo=set()




#build MO list and remove duplicates:
for fajl in putanje:
  with open(fajl) as json_file:
    # print (fajl)
    original = json.load(json_file)
    # print(original)
    for t in original:
      grupe_mo.add(t['groupName'])

#print(grupe_mo)

#Build loop to build new counter list for every MO and remove duplicates
for MO in grupe_mo:
  a = set()
  for fajl in putanje:
    #print('obradujem '+MO +' '+ fajl)
    with open(fajl) as json_file:
      #print (fajl)
      original = json.load(json_file)
      #print(original)
      for t in original:
        if t['groupName']==MO:
          #print (str(t['eventCounterNames']))
          for cnter in t['eventCounterNames']:
            if 'pmZtemp' not in cnter:
              #print (MO +' '+ cnter)
              #print(len(a))
              a.add(cnter)


  #print('prije ' + str(len(a)))
#Check all counters vs system predefined counters and if any found remove them
  with open(filepath_system_predefined) as json_file:
    predef = json.load(json_file)
    for item in predef:
      if item['groupName'] == MO:
        for cnter in item['eventCounterNames']:
          if cnter in a:
            a.discard(cnter)
  #print(len(a))


  kaunter_lista = ('","'.join(a))
  template_napunjen = template_intro.format(MO, kaunter_lista)
  output_template=output_template+template_napunjen

#Format the final json
output_template= output_template[:-1]
final="[{}]".format(output_template)

##write the file
with open(final_filename, 'w') as file:
  file.write(final)

#Import created fajl to Ericsson ENM :
#Ericsson Network Manager ->PM Initiation and Collection->new profile->Counters tab->import