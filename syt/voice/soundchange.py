from pydub import AudioSegment

def mp4towav(filePath):
    audio = AudioSegment.from_file(filePath, format="m4a")
    wavFilePath = filePath.replace("m4a", "wav")
    audio.export(wavFilePath, format="wav")
    print(wavFilePath, "done") #확인용 출력 


if __name__ == "__main__":
    for i in ["/media/smc/0F1A-0D21/syt/voice/세명컴퓨터고등학교 3.m4a", "/media/smc/0F1A-0D21/syt/voice/세명컴퓨터고등학교 4.m4a", "/media/smc/0F1A-0D21/syt/voice/세명컴퓨터고등학교 5.m4a", "/media/smc/0F1A-0D21/syt/voice/세명컴퓨터고등학교 6.m4a", "/media/smc/0F1A-0D21/syt/voice/세명컴퓨터고등학교 7.m4a"]:
        mp4towav(i)