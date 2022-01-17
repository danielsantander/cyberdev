import imageio
from pathlib import Path
from typing import Union, List
from utils.custom_exceptions import InvalidDirectory
from utils.date_helper import timestamp_to_date_string

def jpg_to_gif(img_dir:Union[str, Path], gif_dir:Union[str, Path]=None, gif_name:str=None, duration:float=0.5)->None:
    '''
    Combines a set of images from a given directory into a single gif image.
    '''    
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
