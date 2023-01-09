from moviepy.editor import *
from gtts import *
import secret as s
import random
import os
import glob
import praw
if __name__ == '__main__':
    #exit()

    subreddit = "jokes"
    param = []
    reddit = praw.Reddit(client_id=s.CLIENT_ID,
                         client_secret=s.CLIENT_SECRET,
                         username=s.USERNAME, password=s.PASSWORD,
                         user_agent="ammarkhawaja")
    subreddit = reddit.subreddit(subreddit).hot(limit=20)

    # Clears post folder
    files = glob.glob('content/post/*')
    for f in files:
        os.remove(f)

    for post in subreddit:
        if not post.stickied:
            bad_post = False
            reddit_post = post.title
            print(reddit_post)
            if subreddit == "jokes":
                param = [post.title, post.selftext, " ", " "]
            if subreddit == "askreddit":
                param = [post.title, post.comments[0].body, post.comments[1].body]
            reddit_comments = post.comments
            for word in s.BLACKLISTED_WORDS:
                if word in reddit_post or word in post.comments[0].body or word in post.comments[1].body or len(reddit_post) > 100 or len(post.comments[0].body) > 200 or len(post.comments[1].body) > 200:
                    bad_post = True
            if not bad_post:
                post.title = post.title.replace("/", " or ")
                file_title = "content/post/" + post.title + " #askreddit #reddit .mp4"

                print("Audio Preparing")
                audio_references = ["content/title.mp3", "content/comment0.mp3", "content/comment1.mp3", "content/fullaudio.mp3"]
                all_audio = gTTS(text=post.title + " . . . " + post.comments[0].body + " . . . " + post.comments[1].body, lang="en", slow=False).save(audio_references[3])
                title_audio = gTTS(text=post.title, lang="en", slow=False).save(audio_references[0])
                comment0_audio = gTTS(text=post.comments[0].body, lang="en", slow=False).save(audio_references[1])
                comment1_audio = gTTS(text=post.comments[1].body, lang="en", slow=False).save(audio_references[2])

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
                background_image = ImageClip("content/background.png").set_start(0).set_duration(AudioFileClip(audio_references[0]).duration + 0.5).set_pos(("center", 500)).resize(1.1,1.1)
                title_text = TextClip(txt=reddit_post, font='Comic-Sans-MS-Bold', align="west", fontsize=32, size=(650,300), color="white", method="caption").set_position(("center", 600)).set_duration(AudioFileClip(audio_references[0]).duration)
                comment0_text = TextClip(txt=reddit_comments[0].body, font='Comic-Sans-MS-Bold', align="west", fontsize=42, size=(700,600), color="white", method="caption").set_position(("center", "center")).set_duration(AudioFileClip(audio_references[1]).duration)
                comment1_text = TextClip(txt=reddit_comments[1].body, font='Comic-Sans-MS-Bold', align="west", fontsize=42, size=(700,600), color="white", method="caption").set_position(("center", "center")).set_duration(AudioFileClip(audio_references[2]).duration)

                title_text.save_frame("content/title_text.png")
                comment0_text.save_frame("content/comment0_text.png")
                comment1_text.save_frame("content/comment1_text.png")
                print("Text Ready")

                final_audio.write_audiofile("content/finalaudio.mp3")
                video = video.set_audio(AudioFileClip("content/finalaudio.mp3"))

                print("Compiling Videos")
                finalvideo = CompositeVideoClip([
                    video, background_image, title_text.set_start(0).set_duration(title_audio_duration + 0.5),
                    comment0_text.set_start(title_audio_duration + 0.5).set_duration(comment0_audio_duration + 0.5),
                    comment1_text.set_start(title_audio_duration + comment0_audio_duration + 1).set_duration(comment1_audio_duration + 0.5)
                ]).set_duration(AudioFileClip("content/finalaudio.mp3").duration + 0.5)
                print("Compiled Videos")

                finalvideo.write_videofile(file_title, fps=30)
                exit()
