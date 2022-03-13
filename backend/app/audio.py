from pydub import AudioSegment
from os import environ, path
import random
import boto3
import botocore.exceptions
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


### Retrieve an mp3 file from S3 and return it as an AudioSegment
def getAudioFiles(podcast, file_list):
    s3 = boto3.client(
        's3',
        aws_access_key_id = environ.get('AWS_S3_KEY_ID'),
        aws_secret_access_key = environ.get('AWS_S3_SECRET_ACCESS_KEY'),
        region_name = 'us-west-2')

    print(file_list)

    ### Get all s3 audio files based on input list
    s3_file_list = [s3.get_object(
        Bucket='dreamworld-podcasts',
        Key=f'{filename}') for filename in file_list]

    ### Convert s3 objects to Pydub files then return them
    return([AudioSegment.from_file(io.BytesIO(audio_file["Body"].read())) for audio_file in s3_file_list])

### Given an ordered list of audtio segments, append them with some amount of crossfade
def createAudioFile(audioSegments, filepath, cf):
    combined_audio = audioSegments[0]
    for audioSegment in audioSegments[1:]:
        combined_audio = combined_audio.append(audioSegment, crossfade=cf)
    return(combined_audio.export(filepath, format="mp3"))


def buildPodcast(podcast, length, directory):

    # Generate a path for the finished file
    generated_file = 'generated_audio.mp3'
    sample_path = path.join(directory, generated_file)

    exercise_folder = 'Exercises'

    # Build list of audio segments
    intro = getRandomAudiofiles('dreamworld-podcasts', podcast + '/Intro')
    exercise = getRandomAudiofiles('dreamworld-podcasts', exercise_folder)
    expo = getRandomAudiofiles('dreamworld-podcasts', podcast + '/Expo', 2)
    outro = getRandomAudiofiles('dreamworld-podcasts', podcast + '/Outro')
    podcast_segments = intro + exercise + expo + outro
    print(podcast_segments)

    # Retrieve audio segments
    time1 = perf_counter()
    audio_files = getAudioFiles(podcast, podcast_segments)
    time2 = perf_counter()
    print(f"time to load s3 narration:\t\t {time2 - time1}")

    # Append them with 1s of crossfade
    time1 = perf_counter()
    finished_sample = createAudioFile(audio_files,  sample_path, 1000)
    time2 = perf_counter()
    print(f"time to assemble narration:\t\t {time2 - time1}")

    # Return location to generated file
    return(generated_file)

# Return filename of a random s3 object or objects based on a certain prefix
def getRandomAudiofiles(bucket, folder, length=1):
    try:
        s3 = boto3.resource(
            's3',
            aws_access_key_id = environ.get('AWS_S3_KEY_ID'),
            aws_secret_access_key = environ.get('AWS_S3_SECRET_ACCESS_KEY'),
            region_name = 'us-west-2'
        )

        # Get a list of items in specified folders
        bucket = s3.Bucket(name=bucket)
        filtered_bucket = bucket.objects.filter(Prefix=folder)
        
        # Filter only items that end in .mp3 then choose random items from list based on length
        select_files = random.sample([x.key for x in filtered_bucket if x.key.endswith('.mp3')], length)
        
        # Use list comprehension to return key of objects in list
        return(select_files)

    except botocore.exceptions as err:
        print("Error with s3 connection")
    except ValueError as err:
        print("Error: Not enough files to sample")
    
    else:
        raise





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