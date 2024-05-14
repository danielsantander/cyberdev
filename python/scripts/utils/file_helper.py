#!/usr/bin/python3

""" Unique methods to handle IO to and from the OS. """
import datetime
import json
import re
import os
import platform
import sys
from pathlib import Path
from typing import Union, List

import PyPDF2 # python3 -m pip install PyPDF2
from reportlab.pdfgen.canvas import Canvas # python3 -m pip install reportlab
from utils.custom_exceptions import InvalidDirectory


def create_pdf(name:Union[str, Path]="", input_text:str='Hello World!', font_name:str="Times-Roman", font_size:int=18)->Path:
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
    return name


def combine_pdfs(inputDir: Union[str, Path], outputDir: Union[str, Path]=None):
    """ Combines all PDFs in the given directory into a single PDF document.

    Keyword arguments:
    inputDir -- path of directory holding the PDFs to combine
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


def encrypt_pdf(path: Union[str,Path], pw:str='', outpath:Path=None)->Path:
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
            encrypt_file_path = outpath / f'{file.name[:-4]}ENCRYPTED.pdf'
            encrypted_pdf = open(encrypt_file_path.absolute(), 'wb')
            pdf_writer.write(encrypted_pdf)
            encrypted_pdf.close()
            return encrypt_file_path

    # PDF file not found.
    except FileNotFoundError as err:
        raise err

    # Invalid PDF file.
    except OSError as err:
        raise err

def file_creation_date(filename:Union[str, Path], timezone=datetime.timezone.utc, use_timestamp:bool=False)->datetime.datetime:
    """
    Returns datetime of file creation date.
    Keyword arguments:
    - filepath (str, Path): path of file to retrieve date created.
    - timezone
    - use_timestamp (bool): return timestamp value instead of datetime.
    """
    filename = filename if isinstance(filename, Path) else Path(filename)
    if not filename.exists() or not filename.is_file(): return None
    path_to_file = filename.resolve()
    file_timestamp = None

    # source: https://stackoverflow.com/a/39501288/14745606
    # if platform.system() == 'Windows':
    if platform.system().lower() in ['windows']:
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            #return stat.st_birthtime
            file_timestamp = stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            #return stat.st_mtime
            file_timestamp = stat.st_mtime
    if use_timestamp: return file_timestamp
    return datetime.datetime.fromtimestamp(file_timestamp, tz=timezone)

def file_modification_date(filename: Union[str, Path], timezone=datetime.timezone.utc)->datetime.datetime:
    """
    Returns datetime of file modification date.

    Keyword arguments:
    - filepath (str, Path): path of file to retrieve modification date.
    - timezone [datetime.timezone.utc]: timezone of returned datetime
    """
    # source: https://stackoverflow.com/a/1526089/14745606
    filename = filename if isinstance(filename, Path) else Path(filename)
    if filename.exists() is False: return None
    path_to_file = filename.resolve()
    t = os.path.getmtime(path_to_file)  # os.stat(filename).st_mtime
    return datetime.datetime.fromtimestamp(t, tz=timezone)

def get_recently_created_files(directory_path:Path, within_hrs:int=24)->list[Path]:
    """
    Iterates through given directory and returns a list of files recently  created.

    Keyword arguments:
    - directory_path: Path object of directory to search.
    - within_hrs: number of hours to define to check when files are created. Defaults to 24 checking for files created within the past day.

    Returns list of Path objects for files recently created.
    """
    results: list[Path] = []
    assert directory_path.exists() and directory_path.is_dir()
    for file in directory_path.iterdir():
        # TODO: implement recursion of iterating directory files?
        if is_file_recently_created(file, within_hrs):
            results.append(file)
    return results

def is_file_recently_created(p:Path, within_hrs:int=24)->bool:
    now = datetime.datetime.utcnow()
    created_date = file_creation_date(p)
    return bool(now-datetime.timedelta(hours=within_hrs) <= created_date <= now+datetime.timedelta(hours=within_hrs)) if created_date else False

def iterate_directory(directory_path:Union[str,Path], excludeHiddenFiles:bool=True, raise_exception:bool=True)->List[Path]:
    """
    Iterates through given directory path and returns a list of Paths in directory.

    Keyword arguments:
    directory_path -- Directory path to iterate.
    exclude_hidden_files -- If True, skips hidden files. Defaults to True.
    raise_exception -- If True, raises exception if invalid directory, else returns empty list.
    """
    file_path_list:List[Path] = []
    p = directory_path if isinstance(directory_path, Path) else Path(directory_path)
    if not p.is_dir() or not p.exists():
        if raise_exception: raise InvalidDirectory(p)
        else: return file_path_list
    if next(p.iterdir(),None) is None: return file_path_list
    file_path_list = [x for x in p.iterdir() if not x.name.startswith('.')] if excludeHiddenFiles else [x for x in p.iterdir()]
    return file_path_list


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

def rename_path(path:Union[str, Path], new_name:Union[str, Path], overwrite:bool=False)->Path:
    """Renames (moves) a directory or file path given a new name.
    If renaming a directory, new_name must be a directory Path object or a string name else NotADirectoryError is raised.

    Keyword arguments:
    path -- path of an existing directory or file to rename
    new_name -- new name to replace current directory/filename.
    """
    # usage: results = rename_path(path, f"APPEND_TO_FILENAME____{path.name}")
    path = path if isinstance(path, Path) else Path(path)
    try:
        if (overwrite is False and (path.parent / new_name).exists()): raise FileExistsError(f'File {new_name} already exists.')

        path = path.rename(new_name)

    # path file does not exist, file path not found.
    except FileNotFoundError as err:
        raise err

    # On Windows, if target exists, FileExistsError will be raised.
    except FileExistsError as err:
        raise err

    # cannot rename a directory given a file path as new_name
    except NotADirectoryError as err:
        raise err
    return path

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
    p = p if str(p.name).endswith('.json') else p.parent/f"{p.stem}.json"

    with open(p.absolute(), "w") as f:
        # json.dump(dict, f, indent=2)  # should work as well
        f.write(json.dumps(dic_obj, indent=2))

