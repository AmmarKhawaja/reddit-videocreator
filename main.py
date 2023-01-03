from moviepy.editor import *
from gtts import *
import secret as s
#change_settings({"IMAGEMAGICK_BINARY": "./ImageMagick-7.0.10"})
import praw
if __name__ == '__main__':
    #exit()
    reddit = praw.Reddit(client_id=s.CLIENT_ID,
                         client_secret=s.CLIENT_SECRET,
                         username=s.USERNAME, password=s.PASSWORD,
                         user_agent="bismillah")
    subreddit = reddit.subreddit('askreddit').hot(limit=10)
    for post in subreddit:
        if not post.stickied:
            bad_post = False
            reddit_post = post.title
            reddit_comments = post.comments
            for word in s.BLACKLISTED_WORDS:
                if word in reddit_post or len(reddit_post) > 50 or len(post.comments[0].body) > 300 or len(post.comments[1].body) > 300:
                    bad_post = True
            if not bad_post:
                break
    print(len(post.comments[1].body))
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
                                      AudioFileClip(audio_references[1]).set_start(title_audio_duration + 2),
                                      AudioFileClip(audio_references[2]).set_start(title_audio_duration + comment0_audio_duration + 4)]).set_fps(44100)
    print("Audio Ready")

    print("Text Preparing")
    video = VideoFileClip("content/backgroundmovie.mov").resize((1080, 1920))
    background_image = ImageClip("content/background.png").set_start(0).set_duration(video.duration).set_pos(("center","center")).resize(1.2,1.2)
    title_text = TextClip(txt=reddit_post, fontsize=32, align="west",size=(700,300), color="white", method="caption").set_position("center").set_duration(AudioFileClip(audio_references[0]).duration)
    comment0_text = TextClip(txt=reddit_comments[0].body, align="west", fontsize=26, size=(700,300), color="white", method="caption").set_position("center").set_duration(AudioFileClip(audio_references[1]).duration)
    comment1_text = TextClip(txt=reddit_comments[1].body, align="west", fontsize=26, size=(700,300), color="white", method="caption").set_position("center").set_duration(AudioFileClip(audio_references[2]).duration)

    title_text.save_frame("content/title_text.png")
    comment0_text.save_frame("content/comment0_text.png")
    comment1_text.save_frame("content/comment1_text.png")
    print("Text Ready")

    final_audio.write_audiofile("content/finalaudio.mp3")
    video = video.set_audio(AudioFileClip("content/finalaudio.mp3"))

    print("Compiling Videos")
    finalvideo = CompositeVideoClip([
        video, background_image, title_text.set_start(0).set_duration(title_audio_duration + 2),
        comment0_text.set_start(title_audio_duration + 2).set_duration(comment0_audio_duration + 2),
        comment1_text.set_start(title_audio_duration + comment0_audio_duration + 4).set_duration(comment1_audio_duration + 2)
    ]).set_duration(AudioFileClip("content/finalaudio.mp3").duration)
    print("Compiled Videos")

    finalvideo.write_videofile("content/finalmovie.mp4", fps=30)
