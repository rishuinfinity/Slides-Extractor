# Slides-Extractor

Extract slides from a lecture video

## Pre-requisites

To use this code, use the following to install required packages.

```bash
pip install numpy
pip install opencv
pip install Pillow
```

### How to use this tool

1. Download the file slides-extractor.py

2. Put the python script in the same folder as the video file

3. On Windows/ Linux open CommandPrompt/ Terminal in the same folder and run the following command to start extraction.

   ```bash
   python slides-extractor.py {filename}
   ```

   Note: If the name has spaces in it, then use " \ " before the space or put the name inside inverted-commas

4. Alternatively, on Linux, you can make the file executable using chmod

   ```bash
   chmod +x slides-extractor.py
   ```

   and then run the following command with the video filename as its argument

   ```bash
   ./slides-extractor.py {filename}
   ```

5. To know usage commands again, you can use this

   ```bash
   python slides-extractor.py --help
   ```

6. If you interrupt it midway, then you would find a folder named cache in the same directory and it would contain unfinished work, so delete the said cache folder

## How it works

The main goal of this tool is to look at consecutive frames and notice when a subsequent change has happened. In that situation, it would recognize different slides.

* We starts by taking three consecutive frames(with the specified time delay), lets call it frame1, frame2 and frame3.
* Then we calculate the MSE(mean square error) between "frame1 and frame2" and between "frame2 second and frame3"
* We find their difference and compare it with a threshold to decide whether new slide has been found or not.
* In case the difference is higher than threshold, then frame 1 is saved into cache folder and we move on with other frames.
* In the end, all images in the cache are combined to form a pdf file.

## Why this method

While working on this, I noticed that consecutive frames, even with very little time delay, had some difference in pixel values. This means that even though the same slide is up in the video for some time, the MSE would still be non-zero between consecutive frames. This noise was the issue that I wanted to ignore.

My first approach was to see MSE between consecutive frames and compare it with threshold. If MSE was higher than threshold then I would consider it a new frame. This approach didn't work properly as the noise contributed some portion of MSE and adjusting threshold for each video needed work. Since videos from different sources have different amount of noise in them( due to different compression techniques and different aspect ratios). So I found a need for an approach to auto remove whatever noise there is.
The current approach works with the assumption that noise is distributed evenly i.e. noise b/w frame1 and frame 2 is equal to noise b/w frame2 and frame3. So when I take the difference between their MSE, then the noise part gets removed.


## License

[GNU General Public License v3.0](LICENSE)

Copyright © 2022- [Rishu Raj](https://github.com/rishuinfinity)
