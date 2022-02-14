from pydub import AudioSegment
from os import environ
import random
import boto3
import io
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


def getAudioFile(filename):
    s3 = boto3.client(
        's3',
        aws_access_key_id = environ.get('AWS_S3_KEY_ID'),
        aws_secret_access_key = environ.get('AWS_S3_SECRET_ACCESS_KEY'),
        region_name = 'us-west-2')

    ### Get file as object
    audio_file = s3.get_object(
        Bucket='dreamworld-podcasts',
        Key=f'test-cast/{filename}')

    ### Convert s3 object to Pydub file
    s3_obj_data = io.BytesIO(audio_file["Body"].read())
    return(AudioSegment.from_file(s3_obj_data))


def createAudioFile(audioSegments, filepath, cf):
    combined_audio = audioSegments[0]
    for audioSegment in audioSegments[1:]:
        combined_audio = combined_audio.append(audioSegment, crossfade=cf)
    return(combined_audio.export(filepath, format="mp3"))


def testConfiguration():
    print(environ.get('AWS_S3_KEY_ID'))
    print(environ.get('AWS_S3_SECRET_ACCESS_KEY'))
    return()


### test = getAudioFile("Test_Outro.mp3")
### print(environ.get('AWS_S3_KEY_ID'))
### print(environ.get('AWS_S3_SECRET_ACCESS_KEY'))

'''
time1 = perf_counter()
ambiance_file = "./assets/sleepcasts/Test_Ambiance.mp3"
outro_sample =  getAudioFile("Test_Outro.mp3")
intro_sample = getAudioFile("Test_Intro.mp3")
expo_sample = getAudioFile("Test_Expo.mp3")
time2 = perf_counter()
print(f"time to load s3 narration:\t\t {time2 - time1}")


time1 = perf_counter()
mixed_intro = mixAmbiance(intro_sample, ambiance_file)
mixed_expo = mixAmbiance(expo_sample, ambiance_file)
mixed_outro = mixAmbiance(outro_sample, ambiance_file, fade_out=True)
time2 = perf_counter()
print(f"time to add ambiance:\t\t {time2 - time1}")

time1 = perf_counter()
createAudioFile([intro_sample, expo_sample, outro_sample], "./assets/sleepcasts/test_output.mp3", 3000)
time2 = perf_counter()
print(f"time to append files:\t\t {time2 - time1}")
'''