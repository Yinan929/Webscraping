#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


# print "hello world"
f = open("task2.txt", "a")
log = open("log.txt", "a")
missingData = open("missingData.txt", "a")

def main():

		# LAST ATC CODE: V08CA01

		# set up web driver and request the page
		driver = webdriver.Chrome("/usr/local/bin/chromedriver")
		driver.get("http://pospopuli.minsalud.gov.co/MEDCOL-STAT/POSEstadisticasMedicamentos.aspx")

		#clicking on Generar Reportes
		generar = driver.find_element_by_css_selector(".arrow[src='images/arrowDown2.png']")
		generar.click()
		# print "generar -->	", generar, "\n"

		# time.sleep(1)
		
		# click on Indicador de uso
		driver.maximize_window()
		firstSelection = driver.find_element_by_css_selector("select#cmbTipoReporte > option[value='1']").click()
		# print "first selection -->	", firstSelection, "\n"

		# time.sleep(1)

		# click on DDD dispensadas por ATC (EPS) Nacional
		driver.maximize_window()
		secondSelection = driver.find_element_by_css_selector("select#cmbReporte1 > option[value='57']").click()
		# print "second selection -->	", secondSelection, "\n"

		atcCode = getAtc()

		for i in range(457, 492):

			process(i, atcCode, driver)
			print "------------------------------------ ", i, " COMPLETED\n"
			# f.write("------------------------------------ " + str(i) + " COMPLETED\n")
			log.write("------------------------------------ " + str(i) + " COMPLETED\n")
		# print "\t\trequest ", i
		# if (request("cmbIPS_DDD_L_LBI" + str(i) + "T0", driver, i)):
		# 	f.write("done writing #" + str(i) + " NO DATA\n")
		# 	print "skip no-data-page !!!! "
		# 	driver.close()
		# 	continue

		# f.write("done writing #" + str(i) + " SUCCESSFULY\n")
		# print "done writing #" + str(i)
		# close driver to disconnect
		driver.close()

def process(atcNum, codeList, driver):
	
	time.sleep(1)
	arrowDown = driver.find_element_by_id("cmbCodigoATC_B-1").click()

	# # select ATC code
	# for i in range(atcNum+200):
	# 	driver.find_element_by_id("cmbCodigoATC_I").send_keys(Keys.DOWN)

	# ATCtable = driver.find_element_by_id("cmbCodigoATC_DDD_L_LBT")
	# ATCs = ATCtable.find_elements(By.TAG_NAME, "tr")
	# print len(ATCs)

	# idx = 0
	# for atc in ATCs:
	# 	print idx, "\t", atc.text
	# 	idx += 1

	# print "\n\n\n\n"
	
	atcCode = codeList[atcNum]

	# time.sleep(1)
	# driver.find_element_by_id("cmbCodigoATC_DDD_L_LBI" + str(atcNum) +"T0").click
	print "code: ", atcCode
	driver.find_element_by_id("cmbCodigoATC_I").clear()
	
	for index in range(len(atcCode)):
		time.sleep(0.2)
		driver.find_element_by_id("cmbCodigoATC_I").send_keys(atcCode[index])
	time.sleep(3)

	# close the dropdown
	arrowDown = driver.find_element_by_id("cmbCodigoATC_B-1").click()

	# driver.find_element_by_id("cmbCodigoATC_DDD_L_LBI163T1").click()
	driver.maximize_window()
	time.sleep(2)

	# generate report
	driver.find_element_by_id("btnConsultar").click()

	time.sleep(6)

	# read the ATC Code
	# atcCode =  driver.find_element_by_xpath("//td[contains(@style, 'WIDTH:29.63mm;min-width: 28.22mm;HEIGHT:6.35mm;')]").find_elements(By.TAG_NAME, "div")[0].text
	# atcCode = driver.find_element_by_id("cmbCodigoATC_DDD_L_LBI1T0")
	driver.maximize_window()

	table = driver.find_element_by_xpath("//table[contains(@style, 'border-collapse:collapse;')]")

	trs = table.find_elements(By.TAG_NAME, "tr") 


	# print len(trs)
	# if the table contains no data, do not scrape
	if (len(trs) == 2):
		return


	for i in range(2, len(trs)):
		f.write(atcCode)
		print "================="
		tr = trs[i].text.split("\n")
		j = 0
		for item in tr:
			if (len(item) < 1):
				print "\tLength zero", item, "\n\n"
			if (item[0] == " "):
				missingData.write("possible missing data in " + atcCode)
			print item
			f.write("," + item)
		f.write("\n")




def getAtc():
	f = open("atc.txt", "r")
	content = f.readlines()
	lst = []
	for item in content:
		line = item.split("\t")
		code = line[1].split(" ")[0]
		lst.append(code)
	return lst


main()
f.close()
log.close()
missingData.close()
