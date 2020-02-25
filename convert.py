import azure.cognitiveservices.speech as speechsdk
import os
import time
import glob
import inflect
import argparse
from dotenv import load_dotenv
load_dotenv()

p = inflect.engine()
print(os.getenv('AZURE_SPEECH_KEY'))

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
speech_key, service_region = os.getenv('AZURE_SPEECH_KEY'), os.getenv('AZURE_RESOURCE_REGION')
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

answer = ""
def speech_recognize_continuous_from_file(audio_path):
    """performs continuous speech recognition with input from an audio file"""
    # global answer
    # <SpeechContinuousRecognitionWithFile>
 

    done = False

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        # print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    def recognized_cb(evt):
        global answer
        # print(answer)
        """callback for recognized event"""
        if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print('RECOGNIZED KEYWORD: {}'.format(evt))
        elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            # print('RECOGNIZED: {}'.format(evt.result.text))
            result = evt.result.text
            answer = answer + " " + result
            print("TRANSCRIBED : {}".format(answer))

        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print('NOMATCH: {}'.format(evt))
        

    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print("CURRENT FILE : {}".format(audio_path))

    speech_recognizer.recognized.connect(recognized_cb)
    # speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    # speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    speech_recognizer.stop_continuous_recognition()
    
    # </SpeechContinuousRecognitionWithFile>
    file_name = os.path.split(audio_path)[len(os.path.split(audio_path))-1].split(".",2)[0]

    tokenized_string = answer.split(' ')
    merged_string = []

    for word in tokenized_string:
        # print(word)

        if word.isnumeric():
            # print("Number")
            word = p.number_to_words(int(word))
            merged_string.append(word)

        else:
            # print("Not Number")
            merged_string.append(word)

    cleaned_string = ' '.join(merged_string)
    # print(cleaned_string)
    print("Transcript for file {} : {}".format(file_name, cleaned_string))
    
    file_activity = open("Transcript.txt","a") #append mode 
    file_activity.write("{}\t{}\n".format(file_name, cleaned_string)) 
    file_activity.close() 

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Azure batch transcription for audio files')
    parser.add_argument('--path', required=True)

    args = parser.parse_args()
    if args.path == "":
        print("No path to audio folder provided...")
    else:
        # print(args.path)
        print("Path Obtained : " + os.path.join(os.getcwd(), args.path))
        print("Collecting all .WAV files ... ")
        AUDIO_PATH = os.path.join(os.getcwd(), args.path, "*.wav")
        # execute_job(args.path)
        # print(args.path)
        print("STARTING TRANSCRIPTION!")
        for audio_path in glob.glob(AUDIO_PATH):
            print("Sleeping...")
            time.sleep(1)
            speech_recognize_continuous_from_file(audio_path)
            
            answer = ""
    
        print("All audio files transcribed!")

    
    



