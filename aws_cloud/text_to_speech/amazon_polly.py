from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

# !!! Please fill out the 'credentials' field below to test. Remember the service is paid !!!
# I don't share my credentials inside any script for security reasons , it is unsecure.
# Altough the service is paid , we have free tier. Don't Panic for paying :)
# To use the service we need to have an aws account and to set a policy for IAM user.

# Initializing AWS Session
session = Session(aws_access_key_id="",
                  aws_secret_access_key="",
                  region_name='us-east-1')


# Creating Polly Service Client
polly_client = session.client("polly")

# Available voices for neural speech (NTTS)
Voices = ["Joanna", "Matthew"]

# Texts for converting to speech to test the service.
Text1 = """
Hi Sir. How can I help you? I am really excited to help you about machine learning.
So I just recommend you to search aws and google api to start quickly. Good Luck Sir."""

Text2 = """
Hi Sir! I'm Jarvis. I am really excited to help you. Today I recommend you to learn 
machine learning and artificial intelligence technologies . Good Luck Sir !"""


# a function for the test
def text_to_speech(text, voice_id=1):

    try:
        # Request speech synthesis
        polly_response = polly_client.synthesize_speech(Text=Text2,
                                                        OutputFormat="mp3",
                                                        VoiceId=Voices[voice_id],
                                                        Engine="neural")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the polly_response
    if "AudioStream" in polly_response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(polly_response["AudioStream"]) as stream:
            output = "speech.mp3"  # os.path.join(gettempdir(), "speech.mp3")

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The polly_response did not contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on Mac and Linux
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output])

