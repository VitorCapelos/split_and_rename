import tkinter
import tkinter.filedialog
import tkinter.ttk
import zipfile
import os
from pdfminer.high_level import extract_text
from PyPDF2 import PdfFileWriter, PdfFileReader

def rename_file(pdf):
    is_pdf.destroy()
    folhas.destroy()
    path_file = []
    my_dir = "./"
    directory = "pdfs/"
    path = os.path.join(my_dir, directory)
    os.mkdir(path)

    progress = tkinter.ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    
    progress.grid(column= 0, row=0)
    progress["maximum"] = pdf.numPages
    progress["value"] = 0

    name_zip = "Relatórios por funcionário.zip"
    my_zipfile = zipfile.ZipFile(name_zip, "w")
    label = tkinter.Label(root, text="Operando...")
    label.grid()
    
    for i in range(pdf.numPages):
        output = PdfFileWriter()
        output.addPage(pdf.getPage(i))

        item = directory + "document-page%s.pdf" % i

        with open(item, "wb") as outputStream:
            output.write(outputStream)

        text = extract_text(item)
        text_split = text.split()

        rename = text_split[text_split.index("NOME:") + 1] + "_" + text_split[text_split.index("PIS/PASEP:") + 1] + ".pdf"

        file_name = my_dir + item
        rename = path + rename

        os.rename(r"{}".format(file_name),r"{}".format(rename))
        my_zipfile.write(rename)
        progress["value"] += 1
        progress.update()
    
    label["text"] = "Finalizado!"
    root.update()
    progress.update()
    my_zipfile.close()
    progress.mainloop()

def select_file():
    file_path = tkinter.filedialog.askopenfile(mode="r")
    
    name_file = file_path.name
    
    if ".pdf" in name_file.lower():
        is_pdf["text"] = "O arquivo é PDF!"
        inputpdf = PdfFileReader(open(file_path.name, "rb"))
        if inputpdf.numPages <= 1:
            folhas["text"] = "Arquivo muito pequeno"
        else:            
            rename_file(inputpdf)
    else:
        is_pdf["text"] = "O arquivo não é PDF..."
    root.update()


root = tkinter.Tk()

root.geometry('500x50')
root.title("Separador de PDF's")
photo = tkinter.PhotoImage(file = "C:/Users/vcape/Documents/Ficheiro/Programação/Python/Rename_Files/03/assets/rename_pdf_logo.png")
root.iconphoto(False, photo)

button = tkinter.Button(text="Escolher arquivo", command=select_file)
button.grid(column= 2, row=0)
is_pdf = tkinter.Label()
is_pdf.grid()
folhas = tkinter.Label()
folhas.grid()



root.mainloop()