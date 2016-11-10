#The following method retrieves the HTML from the Binghamton college website
#The semester codes for four college semesters are
#Summer 2015="201560", Spring 2015="201520",
#Winter 2015="201510", Fall 2014="201490"
def download_college_data(Semester1 = 201560, Semester2 = 201520, 
Semester3 = 201510, Semester4 = 201490):
	semester_list = [Semester1, Semester2, Semester3, Semester4]
	semester_name_list = ["Semester1.txt", "Semester2.txt", "Semester3.txt", "Semester4.txt"]
	i = 0
	from splinter import Browser#splinter is a software package that lets you visit and interact with web browsers
	
	for semester in semester_list:
		browser = Browser('firefox')#opens up a firefox web browser	
		browser.visit('http://ssb.cc.binghamton.edu/banner/bwckschd.p_disp_dyn_sched')#visit the college website
		drop_down_list = browser.find_by_name('p_term')#finds the semester drop down list
		drop_down_list.select(semester)#selects the semester specified by the semester variable containing the semester code
		submit = browser.find_by_value('Submit')#finds the submit button
		submit.click()#clicks the submit button
		limit_search_menu = browser.find_by_name('sel_levl')#finds the course level drop down list
		limit_search_menu.select('UG')#select undergraduate in the course level drop down list
		limit_search_menu.select('%')#select all in the course level drop down list
		submit = browser.find_by_value('Class Search')#finds the submit button
		submit.click()#clicks the submit button
		file = open(semester_name_list[i], "wb")#specify the name of the file to write to
		the_file = browser.html#saves the html that is on the web browser
		file.write(the_file)#writes the html that is on the web browser to a text file
		file.close()#close the text file
		i = i + 1#continue writing the html for other college semesters
		browser.quit()#close the web browser

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
