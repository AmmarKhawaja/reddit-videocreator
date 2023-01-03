from moviepy.editor import *
from gtts import *
import secret as s
#change_settings({"IMAGEMAGICK_BINARY": "./ImageMagick-7.0.10"})
import praw
if __name__ == '__main__':
    print(TextClip.list('font'))
    #exit()
    reddit = praw.Reddit(client_id=s.CLIENT_ID,
                         client_secret=s.CLIENT_SECRET,
                         username=s.USERNAME, password=s.PASSWORD,
                         user_agent="bismillah")
    subreddit = reddit.subreddit('askreddit').hot(limit=5)

    BLACKLISTED_WORDS = ["nigger", "nigga", "sex", "sexual", "chink", "cracker", "fuck", "cock", "nazi","hitler", "gay",
                         "lesbian", "faggot", "transgender", "blm", "israel", "binary", "bitch", "whore", "negro",
                         "sand monkey", "coon", "retard", "autistic", "hong kong", "cpp", "communist", "communism",
                         "uyghers", "japs"]
    for post in subreddit:
        if not post.stickied:
            bad_post = False
            reddit_post = post.title
            reddit_comments = post.comments
            for word in BLACKLISTED_WORDS:
                if word in reddit_post or len(reddit_post) > 50 or len(post.comments[0].body) > 150 or len(post.comments[1].body) > 150:
                    bad_post = True
            if not bad_post:
                break

    print("Audio Preparing")
    audio_references = ["content/title.mp3", "content/comment0.mp3", "content/comment1.mp3", "content/fullaudio.mp3"]
    all_audio = gTTS(text=post.title + " . . . " + post.comments[0].body + " . . . " + post.comments[1].body, lang="en", slow=False).save(audio_references[3])
    title_audio = gTTS(text=post.title, lang="en", slow=False).save(audio_references[0])
    comment0_audio = gTTS(text=post.comments[0].body, lang="en", slow=False).save(audio_references[1])
    comment1_audio = gTTS(text=post.comments[1].body, lang="en", slow=False).save(audio_references[2])
    print("Audio Ready")

    print("Text Preparing")
    video = VideoFileClip("content/backgroundmovie.mov").set_duration(AudioFileClip(audio_references[3]).duration + 3)
    background_image = ImageClip("content/background.png").set_start(0).set_duration(video.duration).set_pos(("center","center")).resize(.35,.4)
    title_text = TextClip(txt=reddit_post, fontsize=10, align="west", size=(200,150), color="white", method="caption").set_position("center").set_duration(AudioFileClip(audio_references[0]).duration)
    comment0_text = TextClip(txt=reddit_comments[0].body, align="west", fontsize=8, size=(200,150), color="white", method="caption").set_position("center").set_duration(AudioFileClip(audio_references[1]).duration)
    comment1_text = TextClip(txt=reddit_comments[1].body, align="west", fontsize=8, size=(200,150), color="white", method="caption").set_position("center").set_duration(AudioFileClip(audio_references[2]).duration)

    title_text.save_frame("content/title_text.png")
    comment0_text.save_frame("content/comment0_text.png")
    comment1_text.save_frame("content/comment1_text.png")
    print("Text Ready")

    video = video.set_audio(AudioFileClip("content/fullaudio.mp3")).set_start(0)

    print("Compiling Videos")
    finalvideo = CompositeVideoClip([
        video, background_image, title_text.set_start(0).set_duration(AudioFileClip(audio_references[0]).duration),
        comment0_text.set_start(AudioFileClip(audio_references[0]).duration + 1).set_duration(AudioFileClip(audio_references[1]).duration),
        comment1_text.set_start(AudioFileClip(audio_references[0]).duration + AudioFileClip(audio_references[1]).duration+ 2).set_duration(AudioFileClip(audio_references[2]).duration)
    ])
    print("Compiled Videos")
    finalvideo.write_videofile("content/finalmovie.mp4", fps=30, codec="mpeg4")
