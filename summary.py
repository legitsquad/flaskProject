import requests
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube 

link = "https://www.youtube.com/watch?v=zarll9bx6FI"
yt = YouTube(link)

print(yt.vid_info)

print (yt.title)
print(yt.author)

video_id = "zarll9bx6FI"

textData = ""

transcript = YouTubeTranscriptApi.get_transcript(video_id)

for d in transcript:
    for t in d['text']:
      if (t != "\n"):
        textData += t
        
API_TOKEN = "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"

# API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
    "inputs": textData,
    
    "parameters": {"min_length": 120, "temperature": 20.0, "repetition_penalty" : 20.0}
    
})


# # print(textData)


# print("\n ----- Summary ------ \n")

print(output[0]['summary_text'])


