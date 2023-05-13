import pyaudiowpatch as pyaudio
import time
import wave
import datetime
import keyboard


# Variables

duration = None
filename = f"sample_{datetime.datetime.now().strftime('%H-%M-%S')}.wav"
stop_recording = False


# Create PyAudio instance via context manager.

if __name__ == "__main__":
    with pyaudio.PyAudio() as p: 
        try:
            # Get default WASAPI info
            wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            print("WASAPI is not available on the system. Exiting...")
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
                exit()
                
        print(f"Recording from: {default_speakers['name']}...")
        
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
            print(f'Recording started. Press spacebar to stop and save the recording...')
            start_time = time.monotonic()
            while not stop_recording:
                if keyboard.is_pressed(' '):
                    stop_recording = True
                elif duration and (time.monotonic() - start_time) >= duration:
                    break
                time.sleep(0.1)
        
        waveFile.close()
        
        if stop_recording:
            print(f'Recording stopped. Sample saved as "{filename}"...')
        else:
            print(f'Recording finished. Sample saved as "{filename}"...')
            
        time.sleep(1)
        
