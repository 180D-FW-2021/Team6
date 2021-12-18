import pyttsx3
import time
import timeit
import sys

start = 0
end = 0

def read(engine, already_processed, sample_text):
        outfile = "temp.wav"
        start = time.time()
        if not already_processed:
                engine.setProperty('rate', 100)
                engine.save_to_file(sample_text, outfile)
                engine.runAndWait()
                end = time.time()
        # pygame.mixer.music.load(outfile)
        # pygame.mixer.music.play()
        return

def speech_and_text(sample_text):
        engine = pyttsx3.init()
        already_processed = False
        read(engine, already_processed, sample_text)

def main():
        sampletextfile = open(sys.argv[1], "r")
        sampleText = sampletextfile.read()
        print("word count: ", len(sampleText.split()))
        t = timeit.Timer(lambda: speech_and_text(sampleText))
        print( "exe time: ", t.timeit(number=1))

if __name__=='__main__':
        main()
