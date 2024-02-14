#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import time
import itertools

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
        
def compress_file(input_file, target_size, output_format, show_background, no_audio, output_dir=None):
    
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
        
    base_dir = os.path.dirname(input_file)
    base_name = os.path.basename(input_file)
    name, _ = os.path.splitext(base_name)
    output_file = os.path.join(output_dir, f"{name}_compressed.{output_format}")
    min_bitrate = 0
    max_bitrate = 10000 
    audio_bitrate = "128k"
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    log_file = os.path.join(log_dir, 'ffmpeg2pass')
    os.makedirs(log_dir, exist_ok=True)
    
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    print("Compressing files, please wait...", end="", flush=True)

    codec_map = {
        'mp4': ('libx264', 'aac', ['-preset', 'ultrafast']),
        'webm': ('libvpx-vp9', 'libopus', ['-speed', '4', '-row-mt', '1']),
        'mkv': ('libx264', 'aac', ['-preset', 'ultrafast']),
        'avi': ('mpeg4', 'mp3', ['-qscale:v', '5']),
    }
    
    if output_format not in codec_map:
        print(f"Unsupported output format: {output_format}")
        return
    
    if output_dir is None:
        output_dir = base_dir
    video_codec, audio_codec, codec_options = codec_map[output_format]
    
    while max_bitrate - min_bitrate > 1:
        video_bitrate = (max_bitrate + min_bitrate) // 2
        cmd = ['ffmpeg', '-y', '-i', input_file, '-c:v', video_codec, '-b:v', f'{video_bitrate}k'] + codec_options

        if not no_audio:
            cmd += ['-c:a', audio_codec, '-b:a', audio_bitrate]
        else:
            cmd += ['-an']

        cmd += [output_file]
            
        if show_background:
            subprocess.run(cmd)
        else:
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            while process.poll() is None:
                sys.stdout.write(next(spinner))  
                sys.stdout.flush()  
                sys.stdout.write('\b') 
                time.sleep(0.1)

        size = os.path.getsize(output_file)

        if size > target_size:
            max_bitrate = video_bitrate
        else:
            min_bitrate = video_bitrate

    print(f"\nFinal file size: {size / 1024 / 1024}MB")
    return output_file

def parse_size(size_str):
    size_str = size_str.lower()
    if size_str.endswith('kb'):
        return int(float(size_str[:-2]) * 1024)
    elif size_str.endswith('mb'):
        return int(float(size_str[:-2]) * 1024 * 1024)
    elif size_str.endswith('gb'):
        return int(float(size_str[:-2]) * 1024 * 1024 * 1024)
    else:
        return int(size_str)
    
def main(args):
    output_file = compress_file(args.file, args.size, args.format, args.show_background, args.no_audio, args.output)
    print(f"Compressed file saved as {output_file}")

def main():
    parser = CustomArgumentParser(description='Compress a video file.', usage='%(prog)s [flag] file')
    parser.add_argument('file', help='The video file you want to compress.')
    parser.add_argument('-f', '--format', default='mp4', help='The output format for the compressed file.')
    parser.add_argument('-s', '--size', default='7mb', help='Compress a file to a custom size (400kb, 5mb, etc).', type=parse_size)
    parser.add_argument('-o', '--output', help='Output directory for the compressed file.')
    parser.add_argument('--show-background', action='store_true', help='Shows the ffmpeg output.')
    parser.add_argument('--no-audio', action='store_true', help='Remove all audio from the output.')
    parser.add_argument('--chan', action='store_true', help='Shortcut for compressing files into webms suitable for 4chan (<3.5mb, webm format, no audio).')
    parser.add_argument('--discord', action='store_true', help='Shortcut for for compressing files suitable for Discord (<8mb, mp4 format).')

    try:
        args = parser.parse_args()
        if args.format == 'webm':
            print("Warning: .webm conversions may take longer than usual.")
        if args.chan:
            args.format = 'webm'
            args.size = parse_size('3mb')
            args.no_audio = True
        if args.discord:
            args.format = 'mp4'
            args.size = parse_size('7mb')
        compress_file(args.file, args.size, args.format, args.show_background, args.no_audio)
    except Exception as e:
        print(str(e))
        parser.print_help()
    except SystemExit:
        sys.exit(0)

if __name__ == "__main__":
    main()