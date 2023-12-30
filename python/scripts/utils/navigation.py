#!/usr/bin/env python
#!/usr/bin/python3

""" Unique methods to handle navigating through the operating system. """
import logging
import shutil
from pathlib import Path
from typing import List, Optional, Union
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
    if not (p.exists() or p.is_dir()): p.mkdir(parents=True, exist_ok=True)
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

def move_file(file_src:Path, dst_dir:Path, rename:str=None, lgr:logging.Logger=None)->Optional[Path]:
    """
    Move a file from given source path (file_src) to the given directory path (dst_dir).
    Returns moved filepath if file successfully moved, else returns None.

    Keyword arguments:
    file_src -- The source file path to move.
    dst_dir -- The destination of the directory to move file into.
    rename -- A new name to give the file to move.
    lgr (optional) -- optional logger

    """
    assert file_src.exists() and file_src.is_file()

    if not dst_dir.exists() or not dst_dir.is_dir():
        dst_dir = make_directory(dst_dir)
    assert dst_dir.exists() and dst_dir.is_dir()

    # TODO: ensure rename does not have an extension in it
    filename = str(file_src.name) if rename is None else str(rename + file_src.suffix)
    target_file_path: Path = (dst_dir / filename)

    if target_file_path.exists():
        if lgr: lgr.debug('move_file - File already exists at destination path.')
        return None

    # TODO: add options to copy instead of only move

    # Use `shutil` if moving file_src to dst_dir involves more than one system.
    # target_file_path = media.rename(target_file_path)
    target_file_path = Path(shutil.move(file_src.absolute(), target_file_path.absolute()))

    try:
        assert target_file_path.exists() and target_file_path.is_file()
    except AssertionError as err:
        if lgr: lgr.error(f'move_file - Failed to move file {file_src.absolute()}')
        return None
    return target_file_path
