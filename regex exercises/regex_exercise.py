import os
import zipfile
import re

def remove_barra_dupla (a):
    pattern=r"\\\\"
    a_limpo=re.sub(pattern,r'\\',a)
    print (a_limpo)
    return a_limpo 

def extrai_arquivos_zip_local():
    #esse funcao descobre e extrai todos aqruivos .zip da pasta local
    lista_diretorio=os.listdir()
    zipfiles_list=[]
    pattern=r'\w+\.zip$'
    for filename in lista_diretorio:
        objeto_pesquisa=re.search(pattern,str(filename))
        if objeto_pesquisa:
            zipfiles_list.append(str(filename))
        else: 
            continue
    #extract each zipfile
    for item in zipfiles_list:
        print (f'extracting: {item}')
        zip_obj = zipfile.ZipFile(str (item),'r')
        zip_obj.extractall()



#look for a instructions file and print it:

def busca_arquivo_de_instrucoes (caminho):
    instructions_pattern=r'.*instructions.*\.txt'
    for folder , sub_folders , files in os.walk(caminho):
        
        for f in files:
            search_obj=re.search(instructions_pattern,str(f),flags=re.IGNORECASE)
            if search_obj:
                caminho_completo=str(folder)+"\\"+str(f)
                b=remove_barra_dupla(caminho_completo)
                print (f"caminho completo é: {caminho_completo}")
                with open (b,'r') as file:
                    print (f"arquivo de texto é:",str(f))
                    file_contents = file.read()
                    print (file_contents)

    
def busca_telefone_nas_pastas (caminho):
    instructions_pattern=r'\d{3}-\d{3}-\d{3}'
    for folder , sub_folders , files in os.walk(caminho):    
        for f in files:
            caminho_completo=str(folder)+"\\"+str(f)
            #b=remove_barra_dupla(caminho_completo)
            #print (f"caminho completo é: {caminho_completo}")
            with open (caminho_completo,'r') as file:
                #print (f"arquivo de texto é:",str(f))
                file_contents = file.read()
                search_obj=re.search(instructions_pattern,file_contents,flags=re.IGNORECASE)
                if search_obj:
                    print (f"filename found is:", caminho_completo)
                    print (f'phone is:',search_obj.group())

    
busca_telefone_nas_pastas("C:\\Users\\rijul\\codigos\\regex exercises\\extracted_content")

