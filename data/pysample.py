import pyaudiowpatch as pyaudio
import numpy as np
import time
import wave
import datetime as dt


# Variables

duration = 5.0
filename = "sample_(datetime.datetime.now).wav"
    

# Create PyAudio instance via context manager.
    
if __name__ == "__main__":
    with pyaudio.PyAudio() as p: 
        try:
            # Get default WASAPI info
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            print("WASAPI is not available on the system. Exiting...")
            stop()
            exit()

        
        # Get default WASAPI speakers

        default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in p.get_loopback_device_info_generator():

                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break
            else:
                print("Default loopback output device not found.\nRun this to check available devices.\nExiting...\n")
                stop()
                exit()
                
        print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")
        
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(default_speakers["maxInputChannels"])
        waveFile.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(int(default_speakers["defaultSampleRate"]))
        
        def callback(in_data, frame_count, time_info, status):
            waveFile.writeframes(in_data)
            return (in_data, pyaudio.paContinue)
        
        with p.open(format=pyaudio.paInt16,
                channels=default_speakers["maxInputChannels"],
                rate=int(default_speakers["defaultSampleRate"]),
                frames_per_buffer=pyaudio.get_sample_size(pyaudio.paInt16),
                input=True,
                input_device_index=default_speakers["index"],
                stream_callback=callback
        ) as stream:
            print(f"The next {duration} seconds will be written to {filename}")
            time.sleep(duration) # Blocking execution while playing
        
        waveFile.close()