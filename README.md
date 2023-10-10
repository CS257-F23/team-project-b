# CS257-F23-B
This repo was created by Daniel, Cuong, London, and Marshall to store group deliverables for Group B during the class CS 257 of Fall 2023.


<br>
Currently, the website has three main functionalities: the great filter, get site, and get year.

### The Great Filter
The great Filter is a tool that allows the user to look for data entries that contain multiple parameters of interest.
<br>
<br>To use, add /and/ or /or/ depending on if you want each data entry to contain all of the given parameters(/and/), or if partial matches should be included (/or/)
<br>
<br> For example, if you wanted to see all cases of Liver cancer in Alabama, in the year 2000, you would type: "http://127.0.0.1:5000/and/Alabama,Liver,2000"
<br>
<br>Or, if you wanted to see any cases of breast cancer, or any cases that happened in Wyoming, you would type: "http://127.0.0.1:5000/or/Wyoming,Breast"

<br>

### Get Site

The functionality of get site is considerably simpler: if you're only interested in one specific cancer site, and want to see all data entries that correspond to that site, simply type /site/ followed by the name of the cancer. The availible sites are listed on the home page.<br>
<br>For example, if you wanted to see every instance of Liver cancer, simply type in: "http://127.0.0.1:5000/site/Liver"

<br>

### Get Year
<br> 
Get year works almost identically to get site: simply add /year/ to the url followed by the year you're interested in. This will output every piece of data that occurred in the given year. <br>
<br> For example, to find every piece of data from 2007, simply type in: "http://127.0.0.1:5000/year/2007"


