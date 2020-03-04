import os
import csv
import operator

def voteAnalysis(file_path):
    with open(file_path) as file_handler:
        vote_file = csv.reader(file_handler)
        #skip header
        next(vote_file)
        #define variable to store total count value and candidate&vote count.
        vote_count = 0
        candidate_list = {}
        #loop through each row to count total vote count, and obtain candiate names and votes
        for row in vote_file:
            vote_count += 1

            if row[2] in candidate_list:
                candidate_list[row[2]] += 1
            else:
                candidate_list.update({row[2]:1})
        #add results to a dictionary and return the result
        result = {"vote_count":vote_count, "candidate_list":candidate_list}
        return result

#define file path and run the function to calculate results
file_path = os.path.join("election_data.csv")
result = voteAnalysis(file_path)

#calculate vote percentage for each candidate and store candidate/percentage to a dictionary
candidate_list = result["candidate_list"]
percentage_list = {}
for key in candidate_list:
    vote_percentage = candidate_list[key]/result["vote_count"]
    percentage_list.update({key:vote_percentage})

#sort candidate list (candidate+vote number))based on number of votes
sorted_candidate_list = sorted(candidate_list.items(), key=operator.itemgetter(1), reverse=True)


#creating new file to write the result and print to terminal
file_path = os.path.join("election_result.txt")
with open (file_path, "w") as result_file:
    line1 = "Election Analysis"
    line2 = "-"*70
    line3 = f"Total Votes: {result['vote_count']}"
    line4 = "-"*70
    line5 = "-"*70
    line6 = f"Winner: {sorted_candidate_list[0][0]}"
    line7 = "-"*70
    result_lines = [line1,line2,line3,line4] + [f"{candidate[0]}: {percentage_list[candidate[0]]:.3%} ({candidate[1]})" for candidate in sorted_candidate_list] + [line5,line6,line7]

    for line in result_lines:
        print(line)
        result_file.writelines(line+"\n")

result_file.close()
