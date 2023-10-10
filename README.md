# CS257-F23-B
This repo was created by Daniel, Cuong, London, and Marshall to store group deliverables for Group B during the class CS 257 of Fall 2023. 

<br>
<br>
Currently, the project can be used by running app.py, and navigating to the provided website or running the program directly in the command line. <strong> See how to use both below! </strong>


<br>

## Website Functionality
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

<br>
<br>

## Command Line Functionality
<br>

### Get Year
<br>
A simple function that allows a user to access all of the data in a given year. It also lists the total case count for the given year. To use from the main directory, just send >python3 ProductionCode/watch.py --year (year of interest)
<br>
<br>
For example, to see all the data from 2005, I would send "python3 ProductionCode/watch.py --year 2005"

<br>
<br>

### Get Site
<br>
A simple function that allows the user to access all the data from a given site. Like Get Year, it also provides the user with the total case count for the given site. Get Year can be accessed using the --site argument followed by '(cancer type)'. 
<br>
<br>
To see all searchable sites, simply send "python3 ProductionCode/watch.py -help"
<br>
<br>
For example, to see all cancer data relating to Melanoma of the skin, I would send "python3 ProductionCode/watch.py --site 'Melanoma of the Skin'
<br>
<br>
<strong>Note: For sites that are multiple words long (ie:Oral Cavity and Pharynx), you must put the whole site in quotes, as shown in the example above. </strong>


