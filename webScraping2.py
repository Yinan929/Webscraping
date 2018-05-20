#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


# print "hello world"
f = open("/Users/RuiZ/Desktop/URLs.txt", "a")

# get all the URLs
def hallelujah():
	print "Ready to start driver\n"

	driver = webdriver.Chrome("/usr/local/bin/chromedriver")
	driver.get("http://www.imprenta.gov.co/gacetap/gaceta.portals")


	time.sleep(1)

	# click on Historico Gacetas
	driver.find_element_by_xpath("//input[contains(@value, 'Historico Gacetas')]").click()

	# click on Consulta por Documento
	driver.find_element_by_xpath("//input[contains(@value, 'Consulta por Documento')]").click()

	
	# select Acta de Plenaria
	optionList = driver.find_element_by_xpath("//select[contains(@name, 'v_nombre')]")
	optionList.click()
	optionList.find_elements_by_tag_name('option')[28].click()
	optionList.click()

	# click on Iniciar Busqueda
	driver.find_element_by_xpath("//input[contains(@value, 'Iniciar Busqueda')]").click()

	# iterate over pages 
	###TODO: have no prior knowledge about he number of pages
	page = 1
	for i in range(5000): # assuming there is 500 pages


		# now get the URLs for the current page
		### example URL: http://www.imprenta.gov.co/gacetap/gaceta.mostrar_texto?p_tipo=02&p_numero=25&p_consec=14831
		### corresponding href: 				   /gacetap/gaceta.mostrar_texto?p_tipo=02&p_numero=25&p_consec=14831


		count = 0
		# iterate over each document on the current page
		for tr in driver.find_element_by_xpath("//table[contains(@border, '3')]").find_elements_by_tag_name('tr'):
			# skip the first row which is the title
			if (count == 0):
				count += 1
				continue

			# get the href of each docoment
			url = tr.find_elements_by_tag_name('td')[0].find_element_by_css_selector('a').get_attribute('href')
			f.write(url)
			f.write("\n")
			# print url
			# print tr.text
			count += 1

		print "--------- page ", page, " done; ", count," URLs written-------------"
		# move to the next page
		driver.find_element_by_xpath("//input[contains(@value, 'Siguiente')]").click()
		
		time.sleep(1)
		page+=1


	time.sleep(5)
	driver.close()
	print "\nDriver closed"

def processTable(driver):
	table = driver.find_element_by_xpath("//html//body//div[1]//table[1]//tbody")
	rowNum = 0
	toWrite = ""
	for tr in table.find_elements_by_tag_name('tr'):
		if (rowNum == 0 or rowNum == 1):
			rowNum += 1
			continue

		if "Ausente" in tr.find_elements_by_tag_name("td")[0].text:
			break

		# print "================== ", rowNum, " ====================="
		# print tr.find_elements_by_tag_name("td")[1].text
		toWrite += tr.find_elements_by_tag_name("td")[1].text
		toWrite += "\n"
		rowNum += 1
	return toWrite

urlFailures = open("/Users/RuiZ/Desktop/URLfalilure.txt", "a")
senators = open("/Users/RuiZ/Desktop/senators.txt", "a")

def processParagraph(driver):
	allPara= driver.find_elements_by_css_selector('p')

	toPrint = False
	toWrite = ""
	for p in allPara:

		p_text = p.text.encode('ascii','ignore')
		# print type(p_text)

		if ("excusa" in p_text):
			break
		if toPrint:
			# print p_text
			toWrite += p_text
			toWrite += "\n"
		if ("asistencia" in p_text): # or (("honorables Senadores" in p_text) and ("excusa" not in p_text)):
			toPrint = True
	return toWrite

def logUrl(url):
	urlFailures.write(url)
	urlFailures.write("\n")

# given the URL, find the all the senators that show up
def getSenators(url):
	# print "\t\t", url
	driver = webdriver.Chrome("/usr/local/bin/chromedriver")
	driver.get(url)

	# firstly need to categorize Camera or Senado
	title = driver.find_element_by_xpath("//html//body//center[1]//p[2]").text
	# print title

	# in case of Camara
	if "MARA" in title:
		print "CAMARA!!!\n"
		try:
			toWrite = processTable(driver)
			if len(toWrite) == 0:
				logUrl(url)
				return
			senators.write(url)
			senators.write("\n")
			print "hahaha"
			print toWrite
			rigou = "ri le gou le"
			senators.write(rigou)
			senators.write(toWrite)
			senators.write("===============\n")
		except:
			pass
			try:
				print "!!!!!!!!!!!!!"
				toWrite = processParagraph(driver)
				if len(toWrite) == 0:
					logUrl(url)
					return
				senators.write(url)
				senators.write("\n")
				senators.write(toWrite)
				senators.write("===============\n")
				
			except:
				print "~~~~~~~~~~~~~~~"
				logUrl(url)
			#print("need to process CAMERA page with paragraphs")
			
	elif "SENADO" in title:
		# print "SENADO!!!\n"
		try:
			toWrite = processTable(driver)
			if len(toWrite) == 0:
				logUrl(url)
				return
			senators.write(url)
			senators.write("\n")
			senators.write(toWrite)
			senators.write("===============\n")
		except:
			pass
			try:
				toWrite = processParagraph(driver)
				if len(toWrite) == 0:
					logUrl(url)
					return
				senators.write(url)
				senators.write("\n")
				senators.write(toWrite)
				senators.write("===============\n")
			except:
				# log url since we cannot process it
				logUrl(url)
	else:
		logUrl(url)
		print "Neither Camera Nor Senado. URL: ", url
		# exit(1)

	time.sleep(1)
	driver.close()


with open("/Users/RuiZ/Desktop/URLs.txt") as f:
	count = 1
	for line in f:
		getSenators(line[:-1])
		print "============== ", count, " ================="
		print line[:-1]
		count += 1
        # print "=================================================================="

### table CAMERA
getSenators("http://www.imprenta.gov.co/gacetap/gaceta.mostrar_texto?p_tipo=02&p_numero=174&p_consec=35631")
# getSenators("http://www.imprenta.gov.co/gacetap/gaceta.mostrar_texto?p_tipo=02&p_numero=90&p_consec=43761")
### non-table CAMERA
# getSenators("http://www.imprenta.gov.co/gacetap/gaceta.mostrar_texto?p_tipo=02&p_numero=096&p_consec=966")

# Senado
# getSenators("http://www.imprenta.gov.co/gacetap/gaceta.mostrar_texto?p_tipo=02&p_numero=17&p_consec=46862")


# Neither Camera Nor Senado
# getSenators("http://www.imprenta.gov.co/gacetap/gaceta.mostrar_texto?p_tipo=02&p_numero=090&p_consec=972")

def old():
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

#hallelujah()
f.close()