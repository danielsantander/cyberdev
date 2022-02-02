#!/usr/bin/python3

""" Unique methods to handle navigating through the operating system. """
import errno
import os
from pathlib import Path
from typing import Union, List
from utils.custom_exceptions import InvalidDirectory

def get_filenames(directory_path: Union[str,Path], return_as_path:bool=False) -> List[Union[str, Path]]:
    """
    Returns list of filenames from the given directory path.

    Keyword arguments:
    directory_path -- path of directory to iterate through
    return_as_path -- boolean value, set True to return a list of Path objects, set False to return list of filenames as strings.
    """
    filenames_list: List[Union[str, Path]] = []
    p = directory_path if isinstance(directory_path, Path) else Path(directory_path)
    if not p.is_dir() or not p.exists(): raise InvalidDirectory(p)
    filenames_list = [(x if return_as_path else x.name) for x in p.iterdir() if x.is_file()]
    return filenames_list

def make_directory(directory_path: Union[str, Path]) -> Path:
    """
    Returns the new directory as type pathlib.Path

    Keyword arguments:
    directory_path -- path of directory to create
    """
    p = directory_path if isinstance(directory_path, Path) else Path(directory_path)
    if not p.exists(): p.mkdir(parents=True, exist_ok=True)
    return p

def clean_directory(directory_path: Union[str, Path], remove_directory: bool=False) -> Path:
    """
    Returns pathlib.Path object of directory with all files removed.
    If 'remove_directory' flag set to True, then the directory itself will be removed.

    Keyword arguments:
    directory_path -- path of directory to purge
    remove_directory -- True to remove contents and directory, False to just remove contents of directory (default False)
    """
    p = directory_path if isinstance(directory_path, Path) else Path(directory_path)
    [x.unlink() for x in p.iterdir() if x.is_file()]
    assert(any(p.iterdir()) is False)
    if remove_directory: p.rmdir()
    return p

