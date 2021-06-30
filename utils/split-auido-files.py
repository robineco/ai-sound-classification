import os
import argparse
from os import listdir
from pydub import AudioSegment
from pydub.utils import make_chunks


# Parse the CLI arguments
# -f split only one audio file
# -d split all audio files in a direcotry
# -o output directory where the splitted files will be saved
def parse_arguments():
    parser = argparse.ArgumentParser(description='Split wav file in to parts')
    parser.add_argument('-f', '--file')
    parser.add_argument('-d', '--dir', type=dir_path)
    parser.add_argument(
        '-o', '--output', help='Output directory', required=True)

    return parser.parse_args()


# Check if the given path is valid
def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"readable_dir:{path} is not a valid path")


# Split audio file in 2000 second parts
def split_audio_file(file, output):
    audio = AudioSegment.from_file(file, "wav")
    chunk_length_ms = 2000
    chunks = make_chunks(audio, chunk_length_ms)
    for i, chunk in enumerate(chunks):
        chunk_name = os.path.basename(file).replace(
            '.wav', '_') + "{0}.wav".format(i)
        print("exporting", chunk_name)
        chunk.export(output + '/' + chunk_name, format="wav")


# Split all audio files a a direcotry
def split_audio_in_dir(directory, output):
    for file in listdir(directory):
        split_audio_file(directory + '/' + file, output)


# Script start
# parse all arguments and split the audio files
def main():
    args = parse_arguments()
    output_dir = dir_path(args.output)
    audio_file = args.file
    audio_dir = args.dir

    if audio_file != None:
        split_audio_file(audio_file, output_dir)
    elif audio_dir != None:
        split_audio_in_dir(dir_path(audio_dir), output_dir)


if __name__ == "__main__":
    main()
