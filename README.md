# Slides-Extractor

Extract slides from a lecture video

## Features

This extension has following features:

* Highly Customizable
* Minimal and elegant look
* Speed is shown with just one letter
  * K means KB/s
  * M means MB/s
  * G means GB/s
  * T means TB/s
* Similarly, data used is also shown with one letter after '=' symbol.
* Upload and Download speeds are shown after '↑' and '↓' respectively.
* If encountered any error, it prints the error in place
   of the extension so that the user if capable can solve it on their own.

## Pre-requisites

To use this code, use the following to install required packages.
```bash
pip install numpy
pip install opencv
pip install numpy
```

### How to use this tool

1. Download the file slides-extractor.py

2. Put the video file in the same folder as the python script

3. If on Linux, make the file executable using chmod and then run
   ```bash
   ./slides-extractor.py {filename}
   ```
4. Alternatively you can also run it without making it executable
   ```bash
   python slides-extractor.py {filename}
   ```
5. Otherwise, on Windows open cmd and run 
   ```bash
   python slides-extractor.py {filename}
   ```
6. For available options, run the following
   ```bash
   python slides-extractor.py --help
   ```
7. If you interrupt it midway, delete the cache folder
 

## License

[GNU General Public License v3.0](LICENSE)

Copyright © 2022- [Rishu Raj](https://github.com/rishuinfinity)
