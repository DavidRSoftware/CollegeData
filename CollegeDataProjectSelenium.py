#The following method retrieves the HTML from the Binghamton college website
#The semester codes for four college semesters are
#Fall 2015="201590", Summer 2015="201560", 
#Spring 2015="201520", Winter 2015="201510"
def download_college_data(Semester1 = "201590", Semester2 = "201560", 
Semester3 = "201520", Semester4 = "201510"):
	semester_list = [Semester1, Semester2, Semester3, Semester4]
	semester_name_list = ["Semester1.txt", "Semester2.txt", "Semester3.txt", "Semester4.txt"]
	i = 0
	from selenium import webdriver#selenium is a software package that lets you visit and interact with web browsers
	from selenium.webdriver.support.ui import Select
	from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC
	import time
	binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
	for semester in semester_list:
		driver = webdriver.Firefox(firefox_binary=binary)#opens up a firefox web browser	
		driver.get('http://ssb.cc.binghamton.edu/banner/bwckschd.p_disp_dyn_sched')#visit the college website
		drop_down_list = Select(driver.find_element_by_name('p_term'))#finds the semester drop down list
		drop_down_list.select_by_value(semester)#selects the semester specified by the semester variable containing the semester code
		submit = driver.find_element_by_xpath("//input[@value='Submit']")#finds the submit button
		submit.click()#clicks the submit button
		WebDriverWait(driver, 30).until(EC.title_is("Class Schedule Search"))
		limit_search_menu = Select(driver.find_element_by_xpath("//select[@id='levl_id'][@name='sel_levl']"))#finds the course level drop down list
		limit_search_menu.deselect_all()
		limit_search_menu.select_by_value('UG')#select undergraduate in the course level drop down list
		submit = driver.find_element_by_xpath("//input[@type='submit']")#finds the submit button
		submit.click()#clicks the submit button
		WebDriverWait(driver, 60).until(EC.title_is("Class Schedule Listing"))
		file = open(semester_name_list[i], "wb")#specify the name of the file to write to
		the_file = driver.page_source#saves the html that is on the web browser
		file.write(the_file.encode('utf-8'))#writes the html that is on the web browser to a text file
		file.close()#close the text file
		i = i + 1#continue writing the html for other college semesters
		driver.close()#close the web browser

#The following method extracts information from HTML and stores that information in a .csv (spreadsheet) file
def write_to_excel():
	semester_name_list = ["Semester1.txt", "Semester2.txt", "Semester3.txt", "Semester4.txt"]
	semester_csv_name_list = ["Semester1.csv", "Semester2.csv", "Semester3.csv", "Semester4.csv"]
	i = 0
	import re
	for semester in semester_name_list:
		reader = open(semester, "rb")
		writer = open(semester_csv_name_list[i], "wb")
		writer.write(b'Course Name, Course Number, Class Section, Instructor\n')#gives a header to the .csv file
		course_name_number_section_pattern = re.compile(b'class="ddtitle">.*?>(.*?) - (.*?) - (.*?)</a></th>')
		instructor_pattern = re.compile(b'<td class="dddefault">(.*?)(<abbr title="Primary">P</abbr>)')
		
		for line in reader:#applies the regular expression pattern to every line of the text file
			search3 = course_name_number_section_pattern.search(line)
			search1 = instructor_pattern.search(line)
			if search3:#if the line contains information we are looking for 
				writer.write(search3.group(1) + b', ' + search3.group(2) + b', ' + search3.group(3) + b', ')#we record the information
			if search1:#if the line contains information we are looking for 
				modify = search1.group(1)
				start = b'('
				end = b' '
				modify = modify.translate(bytes.maketrans(start,end))
				writer.write(modify + b'\n')#we record the information
					
		print("The file named ",writer.name, "has been written.")
		reader.close()
		writer.close()
		i = i + 1