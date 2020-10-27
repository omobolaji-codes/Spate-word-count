import gspread
from collections import Counter
import csv

# Open google sheet
gc = gspread.service_account(filename="../service_account.json")
sh = gc.open("Batch 20200929 Pull 4 Combined - Invisible Tech - Working Sheet")
workingSheet = sh.sheet1

urls = workingSheet.col_values(11)
keywords = workingSheet.col_values(6)
keywords = keywords[1:]


commonID = []
count = 0
checked_url = []
for url in urls[1:]:
    if url not in checked_url:
        checked_url.append(url)
        count+=1
        commonID.append(count)
    else: 
        commonID.append(count)
print("commonID length",len(commonID))
# workingSheet.update('E2:E16966', commonID)

unique_dict = {}
for i, id_ in enumerate(commonID):
    keyword = keywords[i]
    if id_ not in unique_dict:
        unique_dict[id_] = [key for key in keyword.split(" ")]
    else:
        unique_dict[id_].extend(key for key in keyword.split(" "))
# print(unique_dict)

value_count_dict_total = {}
for key, values in unique_dict.items():
    value_count = Counter(values).most_common(500)
    value_count_dict = dict(value_count)
    value_count_dict_total[key] = value_count_dict
# print("value count dict length", value_count_dict_total)

def takeSecond(elem):
    return elem[1]

total_rows = []
allRows = workingSheet.get_all_values()
allRows = allRows[1:]
for row in allRows:
    try:
        commonID = int(row[4])
        keywords = row[5]
        keyword_list = keywords.split(" ")

        words_count = value_count_dict_total[commonID]
        keyword_rows = []
        for key in keyword_list:
            word_count = words_count[key]
            pair = [key, word_count]
            keyword_rows.append(pair)
            keyword_rows.sort(key = takeSecond, reverse=True)
            flat_list = [item for sublist in keyword_rows for item in sublist]
        total_rows.append(flat_list)
    except ValueError: pass
# seedTerms.append_rows(values = total_rows, value_input_option='RAW')
print(total_rows)
print("here")
with open("output4.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(total_rows)