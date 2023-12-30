from typing import List

DEFAULT_DATETIME_FMT_SHORT = '%Y%m%d'
DEFAULT_DATETIME_FMT_LONG = '%Y%m%d%H%M%S'

DEFAULT_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

# DEFAULT_LOGGING_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DEFAULT_LOGGING_DATE_FORMAT = "%Y-%m-%d %I:%M:%S"

DEFAULT_IGNORE_FILES_MACOS = ['.DS_Store']
DEFAULT_IGNORE_FILES = [] + DEFAULT_IGNORE_FILES_MACOS

IMAGE_EXTENSION: str = 'jpg'
IMAGE_EXTENSION_LIST: List[str] = ["png", "jpg", "jpeg"]

VIDEO_EXTENSION: str = "mp4"
VIDEO_EXTENSION_LIST: List[str] = ["mp4", "gifv", "gif"]

# ---------
# REGEX
# ---------
# IMG_XXXX.jpg | Screen Shot YYYY-MM-DD at HH.MM.SS AM|PM.png
RE_APPLE_SCREEN_SHOT = r'^((?P<phone_screenshot>IMG\_(?P<image_id>\d+))|(?P<mac_screenshot>Screen\sShot\s(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\sat\s(?P<time>[0-9]{1,2}.[0-9]{2}.[0-9]{2})\s(?P<meridiem>[A|P]M)))([-|_](?P<category>[^-]*)-?)?.*\.(?P<extension>\w*)$'

RE_FILE_EXTENSION = r'\.(?P<extension>\w+$)'

# IMG_XXXX.jpg
RE_IPHONE_SCREEN_SHOT = r'^IMG\_(?P<image_id>\d+)(?P<extension>\.\w*)$'

# Screen Shot YYYY-MM-DD at HH.MM.SS AM|PM.png
RE_MAC_OS_SCREEN_SHOT = r'^Screen\sShot\s(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})\sat\s(?P<time>[0-9]{1,2}.[0-9]{2}.[0-9]{2})\s(?P<meridiem>[A|P]M)(?P<extension>\.png)$'

# YYYY-MM-DD HH:MM:SS w/ grouping of: year month, date
RE_NASA_IMG_DATES = "^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<date>\d{1,2}).*$"

# posix timestamp: "1659238453"
RE_POSIX_TIME = r'.*(?P<date>\d{10}).*$'

# scan_yyyymmddhhmmss
RE_SCAN_FILE = r'scan_(?P<date>\d{4}\d{2}\d{2})(?P<time>\d{2}\d{2}\d{2})\.(?P<extension>\w+)$'

# Screen Shot YYYY-MM-DD at H.MM.SS MERIDIEM(AM/PM).png
RE_SCREENSHOT_FILENAME = r'Screen Shot (?P<date>\d{4}-\d{2}-\d{2}) at (?P<time>\d{1,2}\.\d{1,2}\.\d{1,2})\s?(?P<meridiem>\w{2})\.(?P<extension>\w+)$'


DESKTOP_USER_AGENT_LIST = [
    # Windows 10-based PC using Edge browser
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",

    # Chrome OS-based laptop using Chrome browser (Chromebook)
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"

    # Mac OS X-based computer using a Safari browser
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",

    # Current Mac OS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

    # Windows 7-based PC using a Chrome browser
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",

    # Linux-based PC using a Firefox browser
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
]

# Media directory names
MEDIA_DIR_NAMES = [
    'images',
    # 'pics',
    'videos',
    # 'vids'
]

XPATH_LIST = [
    "video"
    "video/source[@src and @type='video/mp4']",
    "//video/source[@src and @type='video/mp4']",
    "//video/source[@src]",
    "//video/source",
    "//video/source[@type='video/mp4']",
]