# Apps

# raspistill

[doc source](https://www.raspberrypi.com/documentation/accessories/camera.html#raspistill)

`raspistill` is a camera application that can be used within the command line for capturing still images with the Raspberry Pi and a camera module.

```shell
# take and save photo
raspistill -v -o photo.jpg

# capture every 2s over a total of 30s, named image1.jpg, image0002.jpg...image0015.jpg
raspistill -t 30000 -tl 2000 -o image%04d.jpg

# set the longitude with EXIF tag to add GPS metadata, the following would set 5degs, 10 minutes, 15 seconds:
raspistill --exif GPS.GPSLongitude=5/1,10/1,15/100
```

| option           | desc.                               | notes                                                                                                    |
|------------------|-------------------------------------|----------------------------------------------------------------------------------------------------------|
| --width, -w      | Set image width <size>              |                                                                                                          |
| --height, -h     | Set image height <size>             |                                                                                                          |
| --quality, -q    | Set jpeg quality <0 to 100>         | 100 is almost completely uncompressed. 75 is a good  value.                                              |
| --raw, -r        | Add raw Bayer data to jpeg metadata | Insert the raw Bayer data from the camera into the JPEG metadata.                                        |
| --output, -o     | Output filename <filename>          | If not specified, no file is saved. If filename is '-', then all output is sent to stdout.               |
| --verbose, -v    | Output verbose information          | Outputs debugging/information messages                                                                   |
| --timeout, -t    | Time before capture and shut down   | The program will run for this length of time, then take the capture. Default is  5 seconds.              |
| --timelapse, -tl | Timelapse mode.                     | The specific value is the time between shots in milliseconds.                                            |
| --encoding, -e   | Encoding to use as output file.     | Valid options are jpg, bmp, gif and png. The filename suffix is completely ignored when encoding a file. |
| --exif, -x       | EXIF tag (format as 'key=value')    | Insertion of EXIF tags into the JPEG image. May have up to 32 EXIF tge entries.                          |

> specify `%04d` at the point in the filename where you want a frame count number to appear. For example: `-t 30000 -tl 2000 -o image%04d.jpg`
>
> `%04d` indicates a four-digit number with leading zeros added to pad to the required number of digits. So, for example, `%08d` would result in an eight-digit number.
