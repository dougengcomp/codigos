import os
import shutil

#print (os.getcwd())
#print (os.listdir(os.getcwd()))
#shutil.move('practice.txt','C:\\Users\\rijul\\codigos\\lixo')
#shutil.move('C:\\Users\\rijul\\codigos\\lixo\\practice.txt',os.getcwd())

#f= open ('practice.txt','w+')
#f.write ('test')
#f.close

for folder , sub_folders , files in os.walk(os.getcwd()):
    
    print("Currently looking at folder: "+ folder)
    print('\n')
    print("THE SUBFOLDERS ARE: ")
    for sub_fold in sub_folders:
        print("\t Subfolder: "+sub_fold )
    
    print('\n')
    
    print("THE FILES ARE: ")
    for f in files:
        print("\t File: "+f)
    print('\n')
