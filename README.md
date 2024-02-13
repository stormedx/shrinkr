# Shrinkx
Shrinkx is a Python tool for effortlessly compressing media files using ffmpeg. The tool is inspired by the website https://8mb.video and the annoyance of memorizing ffmpeg command arguments 😩.

## Demo
https://github.com/stormedx/shrinkx/assets/88412569/1937f006-138b-4cea-b86b-2b10a71ce76a

## Requirements

- Python 3.8 or higher 
- ffmpeg 5.x or higher is required and needs to be a $PATH variable on your system. Please read [ffmpeg](#ffmpeg) for additional information.

## Commands
- '-f', '--format': Choose the file format you want to encode the output to (i.e .mp4, .webm, .mov, .mkv).
- '-s', '--size': Allows you to compress a file to a specific size (kilobytes, megabytes, gigabytes).
- '-o', '--output': Output directory for the compressed file. If no location is given, the output file will output to the parent working directory of the source file.
- '--no-audio' : Removes all audio in the output file.
- '--chan' : Shortcut for compressing files into a .webm suitable for 4chan (<3.5mb in size, no audio).
- '--discord' : Shortcut for compressing files into an .mp4 >8mb in size

## Usage Examples

In it's simplest form, `shrinkx file.mov` will automatically compress & encode to .mp4 for sharing easily on platforms such as Discord.

`shrinkx --size 5mb -f webm video.mp4`

### ffmpeg installation
WIP
