#!/usr/bin/python3

""" Unique methods to handle image management. """
import imageio
import logging
import os
from pathlib import Path
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from typing import Union, List
from utils.custom_exceptions import InvalidDirectory
from utils.date_helper import timestamp_to_date_string
from utils.custom_logging import create_logger
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFPageCountError

LOGGER_NAME = 'ImageHelper'
LOGGER_LEVEL = logging.DEBUG
LOGGER = create_logger(name=LOGGER_NAME, level=LOGGER_LEVEL)

def jpg_to_gif(img_dir:Union[str, Path, list[Path]], gif_dir:Union[str, Path]=None, gif_name:str=None, duration:float=None, do_sort:bool=True) -> None:
    """Combines a set of images from directory into a single gif image.

    Keyword arguments:
    img_dir -- directory path holding images to convert into gif image (required)
    gif_dir -- directory path to save the converted gif image, defaults to img_dir if not provided. (default img_dir)
    duration -- gif time duration (default 0.5)
    """
    duration:float = 0.5 if duration is None else duration
    img_path_list = []
    if isinstance(img_dir, list):
        img_path_list = img_dir
    elif isinstance(img_dir, str):
        img_dir=Path(img_dir)

    if isinstance(img_dir, Path):
        assert img_dir.exists() and img_dir.is_dir() #and any(img_dir.iterdir())
        img_path_list = [x for x in img_dir.iterdir() if x.is_file()]

    if gif_dir is None: gif_dir = img_dir
    else: gif_dir = gif_dir if isinstance(gif_dir, Path) else Path(gif_dir)

    # construct gif image name, defaults to current datetime value
    if gif_name is None: gif_name = f'{timestamp_to_date_string()}.gif'
    else: gif_name = gif_name if gif_name.endswith('.gif') else f'{gif_name}.gif'

    # construct gif image save path
    gif_path: Path = None
    if gif_dir.is_dir(): gif_path = gif_dir / gif_name
    elif gif_dir.name.endswith('.gif'): gif_path = gif_dir
    else: raise InvalidDirectory

    # gif conversion
    img_path_list = sorted(img_path_list, key=lambda i: i.name) if do_sort else img_path_list
    images = [imageio.imread(x.resolve()) for x in img_path_list if x.is_file()]
    imageio.mimsave(gif_path, images, 'GIF', duration=duration)
    return gif_path

def pdf_to_jpg(path:Union[str,Path], outPath:Union[str,Path]=None) -> None:
    """Convert PDF documents into JPG.

    Keyword arguments:
    path -- The directory or file path to the PDF document. If directory, will iterate and convert all pdf files in directory. (required)
    outPath -- directory path to export converted jpg file, defaults to the same path argument if not provided.
    """
    inPath = path if isinstance(path, Path) else Path(path)
    outDir: Path = outPath if outPath and isinstance(outPath, Path) and outPath.is_dir() else inPath.parent

    if inPath.exists() is False or inPath.is_file() is False: raise FileNotFoundError
    inDocs: List[Path] = [inPath] if inPath.is_file() else [ x for x in inPath.iterdir() if x.is_file() and x.name.lower().endswith('.pdf') ]
    LOGGER.debug("converting PDFs into JPG")
    for pdf_path in inDocs:
        if not pdf_path.name.lower().endswith('.pdf'): continue
        pdf_path_as_posix = pdf_path.as_posix()
        jpg_conversion = convert_from_path(pdf_path=pdf_path_as_posix, dpi=600, fmt="jpg")
        for page in jpg_conversion:
            out_file: Path = outDir / (pdf_path.name[:-4] + '.jpg')
            page.save(out_file)
    return

def yt_download(video_url:str, output_path:Union[str,Path], quality:str="highest", is_mp3:bool=False, title:str=None)->Path:
    out_path:Path = output_path if isinstance(output_path, Path) else Path(output_path)
    yt = YouTube(url=video_url)
    new_filename = yt.title if title is None else title
    new_filename += "" if new_filename.endswith(".mp4") else ".mp4"

    is_progressive = True
    order_by = "resolution"
    file_extension = "mp3" if is_mp3 else "mp4"
    try:
        if is_mp3:
            # TODO: pass
            return
        if quality.lower() in ['high', 'highest']:
            yt.streams.filter(progressive=is_progressive, file_extension=file_extension).order_by(order_by).desc().first().download(filename=new_filename, output_path=out_path)    # highest quality
        else:
            yt.streams.filter(progressive=is_progressive, file_extension=file_extension).order_by(order_by).asc().first().download(filename=new_filename, output_path=out_path)  # lowest quality
    except KeyError as err:
        print(f"ERROR downloading yt video: {err.__str__()}")
        return None
    return (out_path / str(new_filename))