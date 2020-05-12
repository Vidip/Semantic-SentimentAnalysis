import requests
import math
import xlwt
from xlwt import Workbook

def checkwords(list_of_words,returned_count):
	file_dict = {}
	max_count = 0
	prev_count = 0
	count = 0
	file_name = ''
	total_words = 0
	file_counter = 1
	file_counter2 = 1
	canada_dict = {}
	wb = Workbook()
	sheet1 = wb.add_sheet('Sheet 1')
	sheet1.write(0,0, "Search Query") 
	sheet1.write(0,1, "Document containing Term") 
	sheet1.write(0,2, "Total Documents(N)/(df)number of documents term appeared") 
	sheet1.write(0,3, "Log10(N/df)")
	wb2 = Workbook()
	sheet2 = wb2.add_sheet('Sheet 1')
	sheet2.write(0,0, "Canada appeared in documents") 
	sheet2.write(0,1, "Total Words") 
	sheet2.write(0,2, "Frequency") 
	for jk in list_of_words:
		number_of_count = 0
		for i in range(1,returned_count-1):
			with open('new_files/news_collection'+str(i)+'.txt') as file_obj:
				contents = file_obj.read()
				if jk in contents:
					number_of_count += 1
				if jk == 'Canada':
					new_st = str(contents)
					total_words = len(new_st.split())
					max_count = contents.count("Canada")
					if count < 1:
						prev_count = max_count
					count += 1
					if max_count >= prev_count:
						file_name = "new_files/news_collection"+str(i)+".txt"
						prev_count = max_count
					canada_dict["new_files/news_collection"+str(i)+".txt"] = [max_count,total_words]
					file_obj.close()
			max_count = 0
			total_words = 0
		file_dict[jk] = number_of_count
	print(file_dict)
	print(file_name)
	print(canada_dict)
	for k,v in file_dict.items():
		mod_val = 0
		sheet1.write(file_counter,0, k) 
		sheet1.write(file_counter,1, v) 
		try:
			mod_val = returned_count/v
		except ZeroDivisionError:
			mod_val = 0
		if v == 0:
			log_val = 0
		else:
			log_val = math.log10(mod_val)
		sheet1.write(file_counter,2, mod_val) 
		sheet1.write(file_counter,3, log_val)
		wb.save("first_table.xls")
		file_counter += 1
	for k2,v2 in canada_dict.items():
		sheet2.write(file_counter2,0, k2.split("/")[1]) 
		sheet2.write(file_counter2,1, canada_dict[k2][1]) 
		sheet2.write(file_counter2,2, canada_dict[k2][0]) 
		wb2.save("second_table.xls")
		file_counter2 += 1
	calculate_relative_frequency(canada_dict)

def calculate_relative_frequency(canada_dict):
	relative_freq = 0
	maintain_count = 0
	highest_relative_freq = 0
	prev_relative_fre = 0
	prev_count = 0
	file_name_max = ''
	for key,value in canada_dict.items():
		relative_freq = canada_dict[key][0]/canada_dict[key][1]
		if prev_count < 1:
			prev_relative_fre = relative_freq
			prev_count += 1
			file_name_max = key
		if relative_freq > prev_count:
			prev_relative_fre = relative_freq
			file_name_max = key
	if file_name_max is not None:
		with open(file_name_max) as file_obj:
			print(file_obj.read())


if __name__ == "__main__":
	returned_count = 500
	list_of_words = ["Canada","Halifax","Dalhousie University","Canada Education","University"]
	checkwords(list_of_words,returned_count)