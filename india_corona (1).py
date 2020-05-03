#!/usr/bin/env python
# coding: utf-8

# In[433]:


import folium
import pandas as pd
import numpy as np
from folium.features import Choropleth
from folium.plugins import MarkerCluster
import os
import vincent, json
from mpld3 import utils


# In[434]:


#reading the data statewise
state=pd.read_csv("State_corona.csv")
#url='https://www.mohfw.gov.in/#'
#response = urllib.request.urlopen(url)
#webContent = response.read()
#strweb=str(webContent)
html = requests.get('https://www.mohfw.gov.in/#').content
df_list = pd.read_html(html)
df_list[0]


# In[435]:


coordinates=(20.5937, 78.9629)
map1=folium.Map(location=coordinates,zoom_start=4.5)
cases_num=df_list[0]["Total Confirmed cases (Including 111 foreign Nationals)"]
state


# In[442]:


htmls="""
<html>
<body align="center">
<h1>COVID 19 - INDIA</h1>
<br>
<img src="data:image/jpeg;base64,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">
<p><h4>Number of corona virus cases:  
"""
htmls+=sizes[0]
htmls+="""
</h4></p>
<br>
<p><h4>Cured/Discharged/Migrated:
"""
htmls+=sizes[1]
htmls+="""
</h4></p>
<br>
<p><h4>Death:
"""
htmls+=sizes[2]
htmls+="""
</h4></p>
 
</body>
</html>
"""
def htmlgen(id):
    htmls="""
    <html>
    <body>
    <div>
    <h3 align="center">
    """
    htmls+=state["Name"][id]
    htmls+="""
    </h3>
    <br>
    <p><h6>Total Confirmed cases: 
    """
    htmls+=df_list[0]["Total Confirmed cases (Including 111 foreign Nationals)"][id]
    htmls+="""
    </p>
    <br>
    <p>Cured/Discharged/Migrated:
    """
    htmls+=df_list[0]["Cured/Discharged/Migrated"][id]
    htmls+="""
    </p>
    <br>
    <p>Death:
    """
    htmls+=df_list[0]["Death"][id]
    htmls+="""
    </p>
    </h6>
    <p style="color:Red"><h5>Helpline Number:
    """
    htmls+=state["Helpline"][id]
    htmls+="""
    </h5></p>
    </div>
    </body>
    </html>
    """
    return htmls
def popups(id):
    labels=["Total Confirmed cases","Cured/Discharged/Migrated","Death"]
    sizes=[df_list[0]["Total Confirmed cases (Including 111 foreign Nationals)"][id],df_list[0]["Cured/Discharged/Migrated"][id],df_list[0]["Death"][id]]
    data={labels[0]:sizes[0],labels[1]:sizes[1],labels[2]:sizes[2]}
    a=vincent.Pie(data,width=500,height=300)
    a.legend(state["Name"][i])
    popup=folium.Popup(width=550,height=100)
    folium.Vega(a).add_to(popup)
    return popup


# In[443]:


labels=["Total Confirmed cases (Including 111 foreign Nationals)","Cured/Discharged/Migrated","Death"]
sizes=[df_list[0]["Total Confirmed cases (Including 111 foreign Nationals)"][32],df_list[0]["Cured/Discharged/Migrated"][32],df_list[0]["Death"][32]]
data={labels[0]:sizes[0],labels[1]:sizes[1],labels[2]:sizes[2]}
a=vincent.Pie(data,width=500,height=300)
a.legend("Covid 19 India")
popup=folium.Popup(width=500,height=100)
folium.Vega(a).add_to(popup)


# In[444]:


#Now placing the markers on each of the location
i=0
while(i<32):
    folium.Marker(location=[state["X "][i],state["Y"][i]],tooltip=htmlgen(i),popup=popups(i),clustered_marker=True).add_to(map1)
    i=i+1
folium.Marker(location=coordinates,tooltip=htmls,popup=popup,icon=folium.Icon(color='darkgreen', icon='info-sign')).add_to(map1)
map1.save("mm.html")
map1


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




