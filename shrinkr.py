import os
import sys
import subprocess
import argparse
import time
import itertools

def compress_file(input_file, target_size, output_dir, show_background):
    base_name = os.path.basename(input_file)
    name, _ = os.path.splitext(base_name)
    output_file = os.path.join(output_dir, f"{name}_compressed.mp4")
    min_bitrate = 0
    max_bitrate = 10000 
    audio_bitrate = "128k"
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    log_file = os.path.join(log_dir, 'ffmpeg2pass')
    os.makedirs(log_dir, exist_ok=True)
    

    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])

    print("Compressing files, please wait...", end="", flush=True)

    while max_bitrate - min_bitrate > 1:
        video_bitrate = (max_bitrate + min_bitrate) // 2
        cmd = ['ffmpeg', '-y', '-i', input_file, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '30', '-pass', '1', '-passlogfile', log_file, '-c:a', 'libopus', '-b:a', '64k', '-f', 'webm', '/dev/null']
        cmd2 = ['ffmpeg', '-y', '-i', input_file, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '30', '-pass', '2', '-passlogfile', log_file, '-c:a', 'libopus', '-b:a', '64k', '-f', 'webm', output_file]
        
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

    print(f"\nFile size: {size / 1024 / 1024}MB")

    return output_file

def parse_size(size_str):
    size_str = size_str.lower()
    if size_str.endswith('k'):
        return int(size_str[:-1]) * 1024
    elif size_str.endswith('m'):
        return int(size_str[:-1]) * 1024 * 1024
    elif size_str.endswith('g'):
        return int(size_str[:-1]) * 1024 * 1024 * 1024
    else:
        return int(size_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compress a video file.')
    parser.add_argument('file', help='The video file you want to compress.')
    parser.add_argument('-s', '--size', default='7m', help='Compress a file to a custom size (5m, 10m, etc.).', type=parse_size)
    parser.add_argument('-o', '--output', default='.', help='The output directory for the compressed file.')
    parser.add_argument('--show-background', action='store_true', help='Shows the ffmpeg output.')
    args = parser.parse_args()

    output_file = compress_file(args.file, args.size, args.output, args.show_background)
    print(f"Compressed file saved as {output_file}")