import csv
from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

opts = Options()
opts.headless = True
opts.binary_location = "C:\\Users\\iokau\\AppData\\Local\\Mozilla Firefox\\firefox.exe" # Put the path file to your webdriver here
browser = Firefox(options=opts)
browser.get('https://www.modsquadhockey.com/patterndb/')

new_curve_data = []

company_select = browser.find_element_by_name("company")
options = company_select.find_elements_by_tag_name("option")

for i in range(1, len(options)):
    company_select.click()
    options[i].click()
    sleep(1)
    results_tbl = browser.find_element_by_id('results')
    result_rows = results_tbl.find_elements_by_tag_name('tr')
    new_curve_data.extend([[d.text for d in row.find_elements_by_tag_name('td')] for row in result_rows[1::]])

browser.close()

with open('curve_data.csv', mode='w', newline='') as curve_file:
    csv_writer = csv.writer(curve_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(
        ['NAME', 'MAKE', 'CURVE_TYPE', 'FACE_TYPE', 'DEPTH', 'TOE_TYPE', 'LIE', 'LENGTH', 'NICKNAMES', 'SIZE'])
    for new_data in new_curve_data:
        # Check if there's a name
        names = new_data[9].split(' ')
        nicknames = []
        if not names:
            name = new_data[0] + new_data[1] + new_data[3]
        elif len(names) == 1:
            name = names[0]
        else:
            name = names[0]
            nicknames = names[1::]

        #    0        1         2    3         4         5         6      7        8          9
        # Company	Type	Depth	Angle	Lie  	  Shape  	Size	Length	Rocker	Description	Image
        # ['CCM', 'Heel', 'Slight', 'Closed', '5.5', 'Square', '1/2"', 'Long', '', 'Stuart/Steen', '']
        csv_writer.writerow([name, new_data[0], new_data[1], new_data[3], new_data[2], new_data[5], new_data[4], new_data[7], nicknames, new_data[6]])
        #                     1     2              3            4           5             6               7       8            9
        #                   NAME, MAKE,          CURVE_TYPE,    FACE_TYPE, DEPTH,       TOE_TYPE,        LIE,    LENGTH,      NICKNAMES
        #                   P88, BAUER,          mid,        slightly-open, moderate,      round,          6,    medium,    "[Kane,Lindros]"