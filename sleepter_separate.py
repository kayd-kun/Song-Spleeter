from spleeter.separator import Separator

# Using embedded configuration.
separator = Separator('spleeter:2stems')

def separate_vocals_instruments(input_audio_path, output_dir_path):
    path_to_audio = input_audio_path
    output_dir = output_dir_path
    separator.separate_to_file(path_to_audio, output_dir)
