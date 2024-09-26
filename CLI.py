import os

#使用cli控制程式運作
#1. 選擇使用本地端檔案或是網路檔案
#2. 選擇使用的模型
#完成

def main():
    print("Welcome to the CLI of the program")
    print("Please select the source of the file")
    print("1. Local File")
    print("2. Online File")
    source = input("Please enter the number of the source: ")
    if source == "1":
        print("Please enter the path of the file")
        path = input("Please enter the path: ")
        if os.path.exists(path):
            print("File exists")
        else:
            print("File does not exist")
    elif source == "2":
        print("Please enter the URL of the file")
        url = input("Please enter the URL: ")
        print("URL is: ", url)
    else:
        print("Invalid input")
        return
    print("Please select the model you want to use")
    print("1. Model 1")
    print("2. Model 2")
    model = input("Please enter the number of the model: ")
    if model == "1":
        print("Model 1 selected")
    elif model == "2":
        print("Model 2 selected")
    else:
        print("Invalid input")
        return
    print("Program finished")

