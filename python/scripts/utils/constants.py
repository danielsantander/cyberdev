from typing import List

DEFAULT_DATETIME_FMT = '%Y%m%d%H%M%S'

IMAGE_EXTENSION_LIST:List[str] = ['png', 'jpg', 'jpeg']

# Screen Shot YYYY-MM-DD at HH.MM.SS AM|PM.png
MAC_OS_SCREENSHOT_REGEX = r'^Screen\sShot\s(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\sat\s(?P<time>[0-9]{1,2}.[0-9]{2}.[0-9]{2})\s(?P<meridiem>[A|P]M)(?P<extension>\.png)$'

# IMG_XXXX.jpg
IPHONE_SCREENSHOT_REGEX = r'^IMG\_(?P<image_id>\d+)(?P<extension>\.\w*)$'

# IMG_XXXX.jpg | Screen Shot YYYY-MM-DD at HH.MM.SS AM|PM.png
APPLE_SCREENSHOT_REGEX = r'^((?P<phone_screenshot>IMG\_(?P<image_id>\d+))|(?P<mac_screenshot>Screen\sShot\s(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\sat\s(?P<time>[0-9]{1,2}.[0-9]{2}.[0-9]{2})\s(?P<meridiem>[A|P]M)))([-|_](?P<category>[^-]*)-?)?.*\.(?P<extension>\w*)$'

EXTENSION_REGEX = r'\.(?P<extension>\w+$)'