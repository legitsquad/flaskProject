from flask import Flask
from flask import render_template, request
from flask import make_response
import pdfkit
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from extractiveSummary import summarize


app = Flask(__name__)


config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

data=[]


def summarizer(link):
    yt = YouTube(link)

    title = yt.title
    channel = yt.author

    video_id = link[len(link) - 11 :]

    textData = ""

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    for d in transcript:
        textData += " "
        for t in d["text"]:
            if t != "\n":
                textData += t
            else:
                textData += ""
        

    API_TOKEN = "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"

    # API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query(
        {
            "inputs": textData,
            "parameters": {
                "min_length": 120,
                "temperature": 20.0,
                "repetition_penalty": 20.0,
            },
        }
    )

    transcript = textData
    summary = output[0]["summary_text"]

    return [title, channel, transcript, summary]


app = Flask(__name__)

# transcript, summary, name of channel, video title


@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/summary", methods=["POST"])
def summary():
    link = request.form["link"]
    

    info = summarizer(link=link)
    

    keyPoints = summarize(text=info[2])
    
    data.append(info)
    data.append(keyPoints)
    

    html = render_template(
        "report.html",
        title=info[0],
        channel=info[1],
        transcript=info[2],
        summary=info[3],
        keyPoints=keyPoints,
    )
    
    data.append(html)
    
    return html

@app.route("/pdf")
def makepdf():
    # html = render_template(
    #     "report.html",
    #     title=data[0][0],
    #     channel=data[0][1],
    #     transcript=data[0][2],
    #     summary=data[0][3],
    #     keyPoints=data[1],
    # )
    pdf = pdfkit.from_string(data[2], False, configuration=config)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response

# @app.route("/dl")
# def dl():
#     return pdfkit.from_url('http://google.com', 'out.pdf')


if __name__ == "__main__":
    app.run(port=5000, threaded=True)
