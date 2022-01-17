'''
Unique methods to handle navigating through the operating system.
'''
import errno
import os
from pathlib import Path
from typing import Union, List
from utils.custom_exceptions import InvalidDirectory

def create_directory_OLD(dir_path:str) -> None:
    '''
    DEPRECATED
    '''
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

def list_directory_OLD(directory:str)->List:
    '''
    DEPRECATED
    '''
    return os.listdir(directory)

def get_filenames(directory_path: Union[str,Path], return_as_path_obj:bool=False) -> List[Union[str, Path]]:
    '''
    Returns list of filenames (of type str or pathlib.Path) from the given directory.
    '''
    filenames_list: List[Union[str, Path]] = []
    p = directory_path if isinstance(directory_path, Path) else Path(directory_path)
    if not p.is_dir() or not p.exists(): raise InvalidDirectory(p)
    filenames_list = [(x if return_as_path_obj else x.name) for x in p.iterdir() if x.is_file()]
    return filenames_list

def make_directory(dir_path: Union[str, Path]) -> Path:
    '''
    Returns the newly created directory (as type pathlib.Path)
    '''
    p = dir_path if isinstance(dir_path, Path) else Path(dir_path)
    if not p.exists(): p.mkdir(parents=True, exist_ok=True)
    return p

def clean_directory(directory_path: Union[str, Path], remove_directory: bool=False) -> Path:
    '''
    Returns pathlib.Path object of directory with all files removed.
    If 'remove_directory' flag set to True, then the directory itself will be removed as well.
    '''
    p = directory_path if isinstance(directory_path, Path) else Path(directory_path)
    [x.unlink() for x in p.iterdir() if x.is_file()]
    assert(any(p.iterdir()) is False)
    if remove_directory: p.rmdir()
    return p

