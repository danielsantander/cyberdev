from typing import List

DEFAULT_DATETIME_FMT = '%Y%m%d%H%M%S'
DEFAULT_LOGGING_DATE_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
DEFAULT_LOGGING_DATE_FMT = "%Y-%m-%d %I:%M:%S"

IMAGE_EXTENSION_LIST:  List[str]=['png', 'jpg', 'jpeg']

# Screen Shot YYYY-MM-DD at H.MM.SS MERIDIEM(AM/PM).png
RE_SCREENSHOT_FILENAME = r'Screen Shot (?P<date>\d{4}-\d{2}-\d{2}) at (?P<time>\d{1,2}\.\d{1,2}\.\d{1,2})\s?(?P<meridiem>\w{2})\.(?P<extension>\w+)$'

# Screen Shot YYYY-MM-DD at HH.MM.SS AM|PM.png
RE_MAC_OS_SCREEN_SHOT = r'^Screen\sShot\s(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\sat\s(?P<time>[0-9]{1,2}.[0-9]{2}.[0-9]{2})\s(?P<meridiem>[A|P]M)(?P<extension>\.png)$'

# IMG_XXXX.jpg
RE_IPHONE_SCREEN_SHOT = r'^IMG\_(?P<image_id>\d+)(?P<extension>\.\w*)$'

# IMG_XXXX.jpg | Screen Shot YYYY-MM-DD at HH.MM.SS AM|PM.png
RE_APPLE_SCREEN_SHOT = r'^((?P<phone_screenshot>IMG\_(?P<image_id>\d+))|(?P<mac_screenshot>Screen\sShot\s(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\sat\s(?P<time>[0-9]{1,2}.[0-9]{2}.[0-9]{2})\s(?P<meridiem>[A|P]M)))([-|_](?P<category>[^-]*)-?)?.*\.(?P<extension>\w*)$'

# scan_yyyymmddhhmmss
RE_SCAN_FILE = r'scan_(?P<date>\d{4}\d{2}\d{2})(?P<time>\d{2}\d{2}\d{2})\.(?P<extension>\w+)$'

# posix timestamp: "1659238453"
RE_POSIX_TIME = r'.*(?P<date>\d{10}).*$'

RE_FILE_EXTENSION = r'\.(?P<extension>\w+$)'