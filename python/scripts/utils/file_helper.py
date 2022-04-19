#!/usr/bin/python3

""" Unique methods to handle IO to and from the OS. """
import datetime
import json
import re
import sys
from pathlib import Path
from typing import Union

import PyPDF2 # python3 -m pip install PyPDF2
from reportlab.pdfgen.canvas import Canvas # python3 -m pip install reportlab
from utils.custom_exceptions import InvalidDirectory

def open_json_from_file(filepath:Union[str,Path]):
    """ Open JSON from filepath and return as dictionary object. 
    
    Keyword arguments:
    filepath -- JSON filepath to open (required)
    """
    data = {}
    p = filepath if isinstance(filepath, Path) else Path(filepath)
    with open(p) as f:
        data = json.load(f)
    return data

def write_json_to_file(filename:Union[str,Path], dic_obj:dict):
    """ Write dictionary object to file as JSON. 
    
    Keyword arguments:
    filename -- name or path of file to write json to (required)
    dict_obj -- dictionary object to convert into JSON file (required)
    """
    p = filename if isinstance(filename,Path) else Path(filename)
    if not p.exists():
        if not p.parent.exists(): p.parent.mkdir()
        p.touch()

    with open(p.absolute(), "w") as f:
        # json.dump(dict, f, indent=2)  # should work as well
        f.write(json.dumps(dic_obj, indent=2))

def combine_pdfs(inputDir: Union[str, Path], outputDir: Union[str, Path]=None):
    """ Combines all PDFs in the given directory into a single PDF document.

    Keyword arguments:
    inputDir -- path of direcotry holding the PDFs to combine
    outputDir -- path to output the combined PDF [defaults to the given inputDir]
    """
    inputDir = inputDir if isinstance(inputDir, Path) else Path(inputDir)

    if (outputDir == '' or outputDir is None): outputDir = inputDir
    outputDir = outputDir if isinstance(outputDir, Path) else Path(outputDir)
    outputPDF = outputDir / 'Combined.pdf'

    if not inputDir.is_dir(): raise InvalidDirectory()

    # loop through all PDFs to open each pdf, add each pdf, then save.    
    pdf_writer = PyPDF2.PdfFileWriter()
    for filepath in inputDir.iterdir():
        if not filepath.name.endswith(".pdf"): continue
        with open(filepath.as_posix(), 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            # loop through all the pages (except the first) and add them
            # for page_num in range(1, pdf_reader.numPages):
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                pdf_writer.addPage(page)

            # save combined PDF to a file.        
            with open(outputPDF.absolute(), 'wb') as pdf_output:
                pdf_writer.write(pdf_output)
                pdf_output.close()

def create_pdf(name:Union[str, Path]="", input_text:str='Hello World!', font_name:str="Times-Roman", font_size:int=18):
    if isinstance(name, str):
        if name == '':
            now = datetime.datetime.utcnow()                      # utc time
            # now_timestamp = str(now.timestamp()).split('.')[0]  # epoch time
            # name = f'{now_timestamp}.pdf'
            dateformat = now.strftime("%Y%m%d%H%M%S") # YYYMMDDHHMMSS format
            name = f'{dateformat}.pdf'
        else:
            name = re.sub(r'(?i)\.\w*$', '', name)
            name += ".pdf" 
    name = name if isinstance(name, Path) and name.exists() else Path(name)
    pdf_file_as_posix = name.as_posix()

    # create a new Canvas instance
    # canvas = Canvas("font-example.pdf", pagesize=LETTER)
    canvas = Canvas(pdf_file_as_posix)
    

    # set the font to Times New Roman with a size of 18 points
    canvas.setFont(font_name, font_size)

    # add some text to the PDF
    """
    The values passed to .drawString() are measured in points. 
    Since a point equals 1/72 of an inch, .drawString(72, 72, "Hello, World")
    draws the string "Hello, World" one inch from the left and one inch from the bottom of the page.
    """
    canvas.drawString(72, 720, input_text)
    
    # save the PDF to a file
    canvas.save()

def encrypt_pdf(path: Union[str,Path], pw:str='', outpath:Path=None):
    """ Encrypt a given PDF file.
    
    Keyword arguments:
    path -- path of the PDF file to encrypt
    pw -- password for the file to encrypt with [defaults to 'fairbanks']
    outpath -- outpath of encrypted file to be extracted [defaults to same directory as given input path]
    """
    file = path if isinstance(path, Path) else Path(path)
    outpath = outpath if outpath is not None else file.parent
    pw = 'fairbanks' if (pw == '' or pw is None) else pw

    try:
        with open(file.absolute(), 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            pdf_writer = PyPDF2.PdfFileWriter()
            for page_num in range(pdf_reader.numPages):
                pdf_writer.addPage(pdf_reader.getPage(page_num))
            pdf_writer.encrypt(pw)
            encrypt_file = outpath / f'{file.name[:-4]}ENCRYPTED.pdf'
            encrypted_pdf = open(encrypt_file.absolute(), 'wb')
            pdf_writer.write(encrypted_pdf)
            encrypted_pdf.close()

    # PDF file not found.
    except FileNotFoundError as err:
        raise err

    # Invalid PDF file.
    except OSError as err:
        raise err
