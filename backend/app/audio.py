from pydub import AudioSegment
import random
from time import perf_counter
from mutagen.mp3 import MP3

def mixAmbiance(narration_audio, ambiance_path, start_padding=5000, end_padding=10000, fade_out=False):

    ### Get ambiance file length
    ambiance_file = MP3(ambiance_path)
    ambiance_file_length = int(ambiance_file.info.length * 1000)

    ### Calculate duration
    narration_duration = len(narration_audio)
    final_duration = narration_duration + start_padding + end_padding
    rand_start_ms = random.randint(0, (ambiance_file_length - final_duration))

    ### Get ambiance snippit
    ambiance_audio = AudioSegment.from_file(ambiance_path, format="mp3", start_second=int(rand_start_ms/1000), duration=int(final_duration/1000))

    ### Combine the segments
    mixed_audio = ambiance_audio.overlay(narration_audio, start_padding)

    ### Add fadeout if last file
    if fade_out:
        mixed_audio = mixed_audio.fade_out(duration=5000)

    return(mixed_audio)



time1 = perf_counter()
ambiance_file = "./assets/sleepcasts/Test_Ambiance.mp3"
outro_sample = AudioSegment.from_mp3("./assets/sleepcasts/Test_Outro.mp3")
intro_sample = AudioSegment.from_mp3("./assets/sleepcasts/Test_Intro.mp3")
expo_sample = AudioSegment.from_mp3("./assets/sleepcasts/Test_Expo.mp3")
time2 = perf_counter()
print(f"time to load narration:\t\t {time2 - time1}")

time1 = perf_counter()
mixed_intro = mixAmbiance(intro_sample, ambiance_file)
mixed_expo = mixAmbiance(expo_sample, ambiance_file)
mixed_outro = mixAmbiance(outro_sample, ambiance_file, fade_out=True)
time2 = perf_counter()
print(f"time to add ambiance:\t\t {time2 - time1}")

time1 = perf_counter()
combined_audio = mixed_intro.append(mixed_expo, crossfade=3000)
combined_audio = combined_audio.append(mixed_outro, crossfade=3000)
file_handle = combined_audio.export("./assets/sleepcasts/test_output.mp3", format="mp3")
time2 = perf_counter()
print(f"time to append files:\t\t {time2 - time1}")