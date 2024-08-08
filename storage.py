import os
from tkinter import messagebox
fileName = "data.txt"
data = {}
keys = ['userName', 'userPassword', 'userToken', 'src_path', 'dst_path', 'extra']
def readData():
    if not os.path.exists(fileName):
        print("Data not found, creating data...")
        with open(fileName, 'w') as f:
            f.write(f"{keys[0]} = \"\"" + '\n')
            f.write(f"{keys[1]} = \"\"" + '\n')
            f.write(f"{keys[2]} = \"\"" + '\n')
            f.write(f"{keys[3]} = \"\"" + '\n')
            f.write(f"{keys[4]} = \"\"" + '\n')
            f.write(f"{keys[5]} = \"\"" + '\n')
    if os.path.getsize(fileName) == 0:
        with open(fileName, 'w') as f:
            f.write(f"{keys[0]} = \"\"" + '\n')
            f.write(f"{keys[1]} = \"\"" + '\n')
            f.write(f"{keys[2]} = \"\"" + '\n')
            f.write(f"{keys[3]} = \"\"" + '\n')
            f.write(f"{keys[4]} = \"\"" + '\n')
            f.write(f"{keys[5]} = \"\"" + '\n')
    with open(fileName) as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            line = line.replace('\n', '')
            k, value = line.split(' = ')
            data[k] = value.strip('"')
        return data

def writeData(datas):
    try:
        print("Writing data...")
        print(datas[0])
        with open(fileName, 'w') as f:
            for i in range(len(keys)):
                if datas[i] != '':
                    f.write(f"{keys[i]} = \"{datas[i]}\"" + '\n')
                else:
                    f.write(f"{keys[i]} = \"{data[keys[i]]}\"" + '\n')
    except Exception as e:
        messagebox.showerror("Error", f"An error occured while writing data: {e}")
        print(f"An error occured while writing data: {e}")
        with open(fileName, 'w') as f:
            f.write(f"{keys[0]} = \"\"" + '\n')
            f.write(f"{keys[1]} = \"\"" + '\n')
            f.write(f"{keys[2]} = \"\"" + '\n')
            f.write(f"{keys[3]} = \"\"" + '\n')
            f.write(f"{keys[4]} = \"\"" + '\n')
            f.write(f"{keys[5]} = \"\"" + '\n')
                    

# data = ['username', 'password', 'token', 'destination', 'source', 'execution']