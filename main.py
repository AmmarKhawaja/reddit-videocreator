from moviepy.editor import *
from gtts import *
import secret as s
import random
import os
import glob
import praw
if __name__ == '__main__':
    #exit()

    sub = "jokes"
    param = []
    pause = 0.0

    reddit = praw.Reddit(client_id=s.CLIENT_ID,
                         client_secret=s.CLIENT_SECRET,
                         username=s.USERNAME, password=s.PASSWORD,
                         user_agent="ammarkhawaja")
    subreddit = reddit.subreddit(sub).hot(limit=10)

    # Clears post folder
    files = glob.glob('content/post/' + sub + '/*')
    for f in files:
        os.remove(f)

    for post in subreddit:
        if sub == "jokes":
            param = [post.selftext, "lol"]
            pause = 1
        if sub == "askreddit":
            param = [post.comments[0].body, post.comments[1].body]
            pause = 0.5
        if sub == "showerthoughts":
            param = ["shower", "thoughts"]
            pause = 0.5
        if not post.stickied:
            bad_post = False
            for word in s.BLACKLISTED_WORDS:
                for text in param:
                    if word in text or word in post.title:
                        bad_post = True
            if not bad_post:
                post.title = post.title.replace("/", " or ")
                file_title = "content/post/" + sub + "/" + post.title + " #" + sub + " #reddit .mp4"
                print("Audio Preparing")
                audio_references = ["content/title.mp3", "content/comment0.mp3", "content/comment1.mp3", "content/fullaudio.mp3"]
                all_audio = gTTS(text=post.title + " . . . " + param[0] + " . . . " + param[1], lang="en", slow=False).save(audio_references[3])
                title_audio = gTTS(text=post.title, lang="en", slow=False).save(audio_references[0])
                comment0_audio = gTTS(text=param[0], lang="en", slow=False).save(audio_references[1])
                comment1_audio = gTTS(text=param[1], lang="en", slow=False).save(audio_references[2])

                title_audio_duration = AudioFileClip(audio_references[0]).duration
                comment0_audio_duration = AudioFileClip(audio_references[1]).duration
                comment1_audio_duration = AudioFileClip(audio_references[2]).duration
                final_audio = CompositeAudioClip([AudioFileClip(audio_references[0]),
                                                  AudioFileClip(audio_references[1]).set_start(title_audio_duration + 1),
                                                  AudioFileClip(audio_references[2]).set_start(title_audio_duration + comment0_audio_duration + 2)]).set_fps(44100)
                print("Audio Ready")

                print("Text Preparing")
                randomint = random.randrange(2000)
                video = VideoFileClip("content/backgroundmovie.mp4").resize((1080, 1920)).subclip(randomint, randomint + 60)
                background_image = ImageClip("content/background.png").set_start(0).set_duration(AudioFileClip(audio_references[0]).duration + pause).set_pos(("center", 500)).resize(1.1,1.1)
                title_text = TextClip(txt=post.title, font='Comic-Sans-MS-Bold', align="west", fontsize=32, size=(650,300), color="white", method="caption").set_position(("center", 600)).set_duration(AudioFileClip(audio_references[0]).duration)
                comment0_text = TextClip(txt=param[0], font='Comic-Sans-MS-Bold', align="west", fontsize=42, size=(700,600), color="white", method="caption").set_position(("center", "center")).set_duration(AudioFileClip(audio_references[1]).duration)
                comment1_text = TextClip(txt=param[1], font='Comic-Sans-MS-Bold', align="west", fontsize=42, size=(700,600), color="white", method="caption").set_position(("center", "center")).set_duration(AudioFileClip(audio_references[2]).duration)

                title_text.save_frame("content/title_text.png")
                comment0_text.save_frame("content/comment0_text.png")
                comment1_text.save_frame("content/comment1_text.png")
                print("Text Ready")

                final_audio.write_audiofile("content/finalaudio.mp3")
                video = video.set_audio(AudioFileClip("content/finalaudio.mp3"))

                print("Compiling Videos")
                finalvideo = CompositeVideoClip([
                    video, background_image, title_text.set_start(0).set_duration(title_audio_duration + pause),
                    comment0_text.set_start(title_audio_duration + pause).set_duration(comment0_audio_duration + pause),
                    comment1_text.set_start(title_audio_duration + comment0_audio_duration + pause * 2).set_duration(comment1_audio_duration + pause)
                ]).set_duration(AudioFileClip("content/finalaudio.mp3").duration + pause)
                print("Compiled Videos")
                finalvideo.write_videofile(file_title, fps=30)

