#import csv and os module to read and write files
import csv
import os
import locale

locale.setlocale(locale.LC_ALL, '')

#define function to read source data and perform calculations
def financialAnalysis(file_path):
    with open (file_path) as file_handler:
        file_reader = csv.reader(file_handler)

        #skip the header
        next(file_reader)

        #define variables to store values
        month_count = 0
        total = 0
        last_row_value = 0
        date_list = []
        period_change_list = {}
    
        #loop through each row to read data and calculate results based on requirements
        for row in file_reader:
            row_value = float(row[1])
            month_count += 1
            total += row_value
            date_list.append(row[0])
            period_change_list.update({row[0]: row_value - last_row_value})

            last_row_value = row_value

        #remove jan-2020(first period) from both lists as the value and date are irrelevant
        del date_list[0]
        period_change_list.pop("Jan-2010")
        
        date_list = sorted(date_list, key=period_change_list.get)        
        
        #calculate average change
        count = 0
        total_change = 0
        for key in period_change_list:
            count += 1
            total_change += period_change_list[key]
        average_change = total_change/count

        #get geatets increase and decrease
        inc_month = date_list[-1]
        inc_value = period_change_list[inc_month]
        dec_month = date_list[0]
        dec_value = period_change_list[dec_month]
        
        #create dictionary to save all returning result and return result
        result = {"month_count":month_count, "total":total, "average_change":average_change, "inc_month":inc_month, "inc_value":inc_value, "dec_month":dec_month, "dec_value":dec_value}
        return result 

#set path file to read data
data_path = os.path.join("budget_data.csv")
#run function to calculate required financial data and get the result
result = financialAnalysis(data_path)


#creating new file to write the result and print to terminal
file_path = os.path.join("result.txt")
with open (file_path, "w") as result_file:
    line1 = "Financial Analysis"
    line2 = "-"*70+""
    line3 = f"Total Months: {result['month_count']}"
    line4 = f"Total profit/(losses): {locale.currency(result['total'],grouping = True)}"
    line5 = f"Average Change: {locale.currency(result['average_change'],grouping = True)}"
    line6 = f"Greatest Increase in Profits: {result['inc_month']} ({locale.currency(result['inc_value'],grouping = True)})"
    line7 = f"Greatest Decrease in Profits: {result['dec_month']} ({locale.currency(result['dec_value'],grouping = True)})"
    line8 = "-"*70+""
    lines = [line1,line2,line3,line4,line5,line6,line7,line8]

    for line in lines:
        print(line)
        result_file.writelines(line+"\n")

result_file.close()
