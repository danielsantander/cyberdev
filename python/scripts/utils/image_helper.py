#!/usr/bin/python3

""" Unique methods to handle image management. """
import imageio
import logging
import os
from pathlib import Path
from typing import Union, List
from utils.custom_exceptions import InvalidDirectory
from utils.date_helper import timestamp_to_date_string
from utils.custom_logging import create_logger
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError

LOGGER_NAME = 'ImageHelper'
LOGGER_LEVEL = logging.DEBUG
LOGGER = create_logger(name=LOGGER_NAME, level=LOGGER_LEVEL)

def jpg_to_gif(img_dir:Union[str, Path], gif_dir:Union[str, Path]=None, gif_name:str=None, duration:float=0.5) -> None:
    """Combines a set of images from directory into a single gif image.

    Keyword arguments:
    img_dir -- directory path holding images to convert into gif image (required)
    gif_dir -- directory path to save the converted gif image, defaults to img_dir if not provided. (default img_dir)
    duration -- gif time duration (default 0.5)
    """   
    # ensure input directories are pathlib.Path objects
    img_dir = img_dir if isinstance(img_dir, Path) else Path(img_dir)
    if gif_dir == None: 
        gif_dir = img_dir
    else:
        gif_dir = gif_dir if isinstance(gif_dir, Path) else Path(gif_dir)
    
    # construct gif image name, defaults to current datetime value
    if not gif_name:
        date_str = timestamp_to_date_string()
        gif_name = f'{date_str}.gif'
    else:
        gif_name = gif_name if gif_name.endswith('.gif') else f'{gif_name}.gif'
    
    # construct gif image save path
    gif_path: Path = None
    if gif_dir.is_dir():
        gif_path = gif_dir / gif_name
    elif gif_dir.name.endswith('.gif'):
        gif_path = gif_dir
    else: raise InvalidDirectory

    # gif conversion
    images = [imageio.imread(x.resolve()) for x in img_dir.iterdir() if x.is_file()]
    imageio.mimsave(gif_path, images, 'GIF', duration=duration)
    return

def pdf_to_jpg(path:Union[str,Path], outPath:Union[str,Path]=None) -> None:
    """Convert PDF documents into JPG.

    Keyword arguments:
    path -- The directory or file path to the PDF document. If directory, will iterate and convert all pdf files in directory. (required)
    outPath -- directory path to export converted jpg file, defaults to the same path argument if not provided.
    """
    inPath = path if isinstance(path, Path) else Path(path)
    outDir: Path = outPath if outPath and isinstance(outPath, Path) and outPath.is_dir() else inPath.parent

    inDocs: List[Path] = [inPath] if inPath.is_file() else [ x for x in inPath.iterdir() if x.is_file() and x.lower().endswith('.pdf') ]
    LOGGER.debug("converting PDFs into JPG")
    for pdf_path in inDocs:
        if not pdf_path.name.lower().endswith('.pdf'): continue
        pdf_path_as_posix = pdf_path.as_posix()

        try:
            jpg_conversion = convert_from_path(pdf_path=pdf_path_as_posix, dpi=600, fmt="jpg")
            for page in jpg_conversion:
                out_file: Path = outDir / (pdf_path.name[:-4] + '.jpg')
                page.save(out_file)

        except PDFPageCountError as err:
            err_msg = "ERROR: invalid pdf"
            print(err_msg)
            LOGGER.error(err_msg)

        except FileNotFoundError:
            err_msg = "ERROR: file not found."
            print(err_msg)
            LOGGER.error(err_msg)
    return
