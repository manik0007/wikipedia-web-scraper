from tkinter import *
import bs4
try:
    import urllib.request as urllib3
except ImportError:
    import urllib3
from bs4 import BeautifulSoup
import lxml
import requests
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import urllib.request
subtopics=[]
firstparah=""
topicdata=[]
parah=""
x=0
title=""
def update():
    global title
    flag=0
    global x
    global subtopics
    global topicdata
    global parah
    global firstparah
    x=0
    counter=0
    stop=""
    topicdata=[]
    subtopics=[]
    parah=""
    firstparah=""
    var=""
    T.config(state=NORMAL)
    T.delete('1.0', END)
    v=search.get()
    title=v
    T.insert(END,v)
    t=len(v)
    b="1.%i"%(t)
    T.tag_add("start","1.0",b)
    T.tag_config("start", foreground="blue")
    T.insert(END,"\n \n \n \n")
    search.delete(0, 'end')
    for i in v:
        o=ord(i)
        if(o==32):
            var=var+'_'
        else:
            var=var+i
    values={'q' : var}
    try:
        link="https://en.wikipedia.org/w/index.php?title="+var+"&printable=yes"
        print(link)
        req = urllib2.Request(link)
        resp = urllib2.urlopen(req)
        respData = resp.read()
        
        
        
        soup= BeautifulSoup(respData)
        print(soup)
        mark = soup.find('div',id="bodyContent").find("p")

        for elt in mark.nextSiblingGenerator():
            if elt.name == "h2":
                break
            if hasattr(elt, "text"):
        
                if(elt.name=="p"):     
                    pass
                    T.insert(END,(str(elt.text)))
                    T.insert(END,"\n\n")
                    firstparah+=(str(elt.text))
                    firstparah+="\n\n"
            
        mark = soup.find('div',id="bodyContent").find("p")
        for elt in mark.nextSiblingGenerator():
            if elt.name == "h2":
                x=1
            if hasattr(elt, "text"):
        
                if(elt.name=="p"):     
                    pass
                if(x==1 and elt.name=="h2"):
                    if(str(elt.text)!="References" and str(elt.text)!="See also"):
                        
                        subtopics.append(str(elt.text))
                    else:
                        break
        mark = soup.find('div',id="bodyContent").find("p")
        length=len(subtopics)+1
        subtopicslen=len(subtopics)
        stop=subtopics[subtopicslen-1]
        previous=2
        for elt in mark.nextSiblingGenerator():
            if hasattr(elt, "text"):
                if hasattr(elt, "text"):
            
                    if(elt.name=="p"):     
                        pass
                    
                    if(x>1 and (elt.name=="h3" or elt.name!="h2")):
                       parah+=(str(elt.text))
                       parah+="\n\n"
                if(elt.name=="h2" and counter==1):
                    if(x>1):
                        topicdata.append(parah)
                        parah=""
                    x=x+1 
                if (elt.name == "h2" and (str(elt.text)in subtopics)):
                    
                    if(x>1):
                        topicdata.append(parah)
                        parah=""
                    x=x+1
                    if(stop==(str(elt.text))):
                       counter=1
                  
                if(x==length+1):
                    
                    print("game on")
                    break
                
                    



        stop=0
        print(len(topicdata),len(subtopics))
        
        
        for text1 in subtopics:
            T.insert(END, text1, ('link',str(flag)))
            T.insert(END, "\n")
            flag+=1
        T.tag_config('link', foreground="blue")
        T.tag_bind('link', '<Button-1>', showLink)
        T.config(state=DISABLED)


        count=0
        data=""
        file=v+".txt"
        with open(file,"wb+") as fil:
            
            fil.write("%%%")
            for textin in subtopics:
                fil.write(textin)
                fil.write("%%%")
                for char in topicdata[count]:
                    data=data+char
                    mine=data.encode('latin-1').strip()
                count+=1
                fil.write("%%%")


        





        
    finally :
        print("Unexpected error:", sys.exc_info())



def showLink(event):
    global title
    flag=0
    stop=0
    global x
    global subtopics
    global topicdata
    global parah
    global firstparah
    t=len(title)
    b="1.%i"%(t)
    idx= int(event.widget.tag_names(CURRENT)[1])
    T.config(state=NORMAL)
    T.delete('1.0', END)
    T.insert(END,title)
    T.tag_add("start","1.0",b)
    T.tag_config("start", foreground="blue")
    T.insert(END,"\n \n \n \n")
    T.insert(END, firstparah)
    
    for text1 in subtopics:
        T.insert(END, text1, ('link',str(flag)))
        T.insert(END, "\n")
        flag+=1
    T.tag_config('link', foreground="blue")
    T.tag_bind('link', '<Button-1>', showLink)
    T.insert(END," \n \n")
    T.insert(END, topicdata[idx])
     
 
root = Tk()
frame1=Frame(root)
frame1.pack()
scroll = Scrollbar(frame1, orient=VERTICAL)
T = Text(frame1,yscrollcommand=scroll.set, height=35, width=80)
scroll.config (command=T.yview)
scroll.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT,fill=BOTH, expand=TRUE)
T.insert(END, " Enter Search query \n")

frame2=Frame(root)
frame2.pack(fill=BOTH)
label=Label(frame2,text="Search Query",height=5,width=10)
label.pack(side=LEFT)
query=StringVar()
search=Entry(frame2,textvariable=query)
search.pack(side=LEFT)
b1=Button(frame2,text=" Search ", command=update)
b1.pack(side=LEFT)

