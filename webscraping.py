#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


f = open("task1.txt", "a")

def main():

	# iterate over all the EPS
	for i in range(51, 100): 
		# set up web driver and request the page
		driver = webdriver.Chrome("/usr/local/bin/chromedriver")
		driver.get("http://pospopuli.minsalud.gov.co/MEDCOL-STAT/POSEstadisticasMedicamentos.aspx")


		

		print "\t\trequest ", i
		if (request("cmbIPS_DDD_L_LBI" + str(i) + "T0", driver, i)):
			f.write("done writing #" + str(i) + " NO DATA\n")
			print "skip no-data-page !!!! "
			driver.close()
			continue

		f.write("done writing #" + str(i) + " SUCCESSFULY\n")
		print "done writing #" + str(i)
		# close driver to disconnect
		driver.close()

def request(epsID, driver, iii):

	#designed to add checking if necessary
	#assert "Python" in driver.title

	#clicking on Generar Reportes
	generar = driver.find_element_by_css_selector(".arrow[src='images/arrowDown2.png']")
	generar.click()
	# print "generar -->	", generar, "\n"

	time.sleep(1)

	driver.maximize_window()
	firstSelection = driver.find_element_by_css_selector("select#cmbTipoReporte > option[value='3']").click()
	# print "first selection -->	", firstSelection, "\n"


	driver.maximize_window()
	secondSelection = driver.find_element_by_css_selector("select#cmbReporte3 > option[value='50']").click()
	# print "second selection -->	", secondSelection, "\n"

	time.sleep(1)


	# click the arrow to show all the eps
	driver.maximize_window()
	arrowDown = driver.find_element_by_id("cmbIPS_B-1").click()


	# pause to make sure all the eps' show up	
	time.sleep(1)
	# select eps
	#TODO: need to loop through all elements
	driver.maximize_window()

	allEPS = driver.find_element_by_xpath("//table[contains(@id, 'cmbEPS_DDD_L_LBT')]").find_elements(By.TAG_NAME, "td")
	# print "-------------"
	# print allEPS.text
	# print "-------------"


	# iterate over all 17 eps
	# for i in range(1, 17):

	driver.maximize_window()
	# scroll down 
	# driver.execute_script("arguments[0].scrollTop = arguments[1];", driver.find_element_by_id("cmbEPS_DDD_PW-1"), 500);
	# driver.execute_script("return arguments[0].scrollIntoView();", driver.find_element_by_id("cmbEPS_DDD_PW-1"))

	for i in range(iii+2):
		driver.find_element_by_id("cmbIPS_I").send_keys(Keys.DOWN)
		time.sleep(0.3)

	print "!!!!!!!!!!!!!!!\n\n"
	time.sleep(1)

	driver.maximize_window()
	
	# this line get the name of the EPS
	eps = driver.find_element_by_id(epsID)

	# print eps

	

	# xpath = "//td[contains(@id, '" + epsID + "')]"
	# eps = driver.find_element_by_xpath(xpath)
	# eps.location_once_scrolled_into_view()

	return processEPS(eps, driver, epsID)
	# time.sleep(3)

	# raise ValueError("stop")

	# for eps in allEPS:
	# 	print "damn!!! ", eps.text
	# 	processEPS(eps)
	# 	# print "\t\t", eps.text

	# raise ValueError("stop")



	
	# time.sleep(2)

	# driver.maximize_window()

	# # table = driver.find_element_by_xpath("//*//input[@type='text'][contains(@class,'form-control')][contains(@name,'projectsurvey')]")#/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[19]/td[3]/table/tbody")
	# # table = driver.find_element_by_xpath("//td[contains(@style, 'zoom: 100%;')]")
	# table = driver.find_element_by_xpath("//table[contains(@style, 'border-collapse:collapse;')]")
	# # print "\n\n", table.text

	# tableItems = table.text.split("\n")
	# print "========================"
	# print tableItems
	# print "========================"

	# atc = ""
	# expenditure = ""
	# for i in range(4, len(tableItems)):
	# 	if (i % 4 == 0):
	# 		atc = tableItems[i]
	# 	if (i % 4 == 2):
	# 		expenditure = tableItems[i]
	# 	if (i % 4 == 3):
	# 		print epsName + "," + atc + "," + expenditure








def processEPS(eps, driver, epsID):

	epsName = eps.text
	print "\n\t\tEPS: ", epsName, 

	f.write("------------------ IPS: " + epsName + " ------------------")
	eps.click()
	# get the name of the eps

	# print eps.text
	#eps = driver.find_element_by_css_selector("tr#dxeListBoxItemRow > td[id='cmbEPS_DDD_L_LBI1T0']")


	# elem.send_keys("pycon")
	# elem.send_keys(Keys.RETURN)

	# print "elem -->		", elem
	# print elem.get_attribute('value')

	# print "elem.text -->	", elem.text
	# assert "No results found." not in driver.page_source
	
	time.sleep(1)

	# click on Generar Reporte
	driver.maximize_window()
	driver.find_element_by_id("btnConsultar").click()

	# now the final table is ready
	# print "the final table is ready!"


	time.sleep(3)
	# let's see how many pages are there in the table
	numPages = driver.find_element_by_xpath("//span[contains(@style, 'font-family:Verdana;font-size:8pt;white-space:nowrap;')]")
	print numPages.text, " pages in ", epsName


	time.sleep(3)

	table = driver.find_element_by_xpath("//table[contains(@style, 'border-collapse:collapse;')]")

	# print "\n\n", table.text

	trs = table.find_elements(By.TAG_NAME, "tr") 

	epsCode = "Original no data"
	if (len(trs) > 2):

		# this line overwrite existing EPS to be the code
		epsCode = driver.find_element_by_xpath("//div[contains(@style, 'WIDTH:27.16mm;')]").text
		print "\n eps element: ", epsCode

	# print "\nepsCode: ", epsCode.innerHTML

	time.sleep(3) 

	# iterate over each page
	for i in range(int(numPages.text)):

		# handle special case for FAMISANAR
		# if (epsID == 7) and (i == (int(numPages) - 1)):
		# 	continue

		print "------------------- ", i , " --------------------"

		# if the current page has no data
		if (scrapeCurrentPage(epsName, driver, epsCode)):
			return True

		time.sleep(2)
		# go to the next page
		if (i != (int(numPages.text) - 1)):
			driver.find_element_by_xpath("//input[contains(@title, 'Next Page')]").click()

	return False

### return true if the current EPS/IPS has no data and false otherwise
def scrapeCurrentPage(epsName, driver, epsCode):
	time.sleep(2)

	driver.maximize_window()

	# table = driver.find_element_by_xpath("//*//input[@type='text'][contains(@class,'form-control')][contains(@name,'projectsurvey')]")#/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[19]/td[3]/table/tbody")
	# table = driver.find_element_by_xpath("//td[contains(@style, 'zoom: 100%;')]")
	
	table = driver.find_element_by_xpath("//table[contains(@style, 'border-collapse:collapse;')]")

	# print "\n\n", table.text

	trs = table.find_elements(By.TAG_NAME, "tr") 

	atc = ""
	expenditure = ""

	# print "============"
	# print trs[0].text
	# print "#######"
	# print trs[1].text
	# print "============"
	# # print trs[2].text
	# print "#######"


	if (len(trs) == 2):
		return True

	# print len(trs)
	for i in range(2, len(trs)):

		tr = trs[i]
		# print tr.text
		row = tr.text.split("\n")
		# print "--------", len(row)
		# print row
		if len(row) == 4:
			atc = row[0]
			expenditure = row[2]
		elif len(row) == 3:
			atc = row[0]
			if row[2][0] == '$':
				expenditure = row[2]
			else:
				expenditure = "MISSING DATA"
		else:
			print "!!!!!!!!!!!!!\tlength: ", len(row) 

		print epsCode + "," + atc + "," + expenditure
		f.write(epsCode + "," + atc + "," + expenditure + "\n")

	return False

main()
f.close()
