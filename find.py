#this function is used to find the string in the file
#but it is not used in the code
#此程式未完成

def find_string_in_file(file_path, string_to_search):
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_path, 'r') as read_obj:
        line = read_obj.readline()
        while line:
            line_number += 1
            # For each line, check if line contains the string
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
            line = read_obj.readline()

    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results
line=find_string_in_file('./output.txt', '牛五花')
print(line)
