'''
store_gcp.py

Storage collected samples through GCP.

Assumes you have an environment variable pointing to .JSON auth credentials.
Specifically:

export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
'''
import sounddevice as sd
import soundfile as sf 
import time, os, shutil 
from google.cloud import storage

def sync_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')
    return filename 


def upload_gcp(bucket_name, source_file_name):
    destination_blob_name=source_file_name
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
    

# Instantiates a client
storage_client = storage.Client()

# The name for the new bucket
bucket_name = 'test-bucket'

# Creates the new bucket
bucket = storage_client.create_bucket(bucket_name)
print('Bucket {} created.'.format(bucket.name))

# get a recording (can loop here too)
file=syn_record('test.wav', 10, 16000, 1)
# upload this recording to gcp
upload_gcp(bucket_name, file)
# delete file after the recording has been uploaded 
os.remove(file)
