import asyncpraw
import config
from vkwave.bots import SimpleBotEvent, SimpleLongPollBot
from vkwave.bots.utils.uploaders import PhotoUploader

reddit = asyncpraw.Reddit(
    client_id=config.settings['CLIENT_ID'],
    client_secret=config.settings['SECRET_CODE'],
    user_agent='random_raddit_bot/0.0.1')

SUBREDDIT_NAME = 'memes'
POST_LIMIT = 1

bot = SimpleLongPollBot(tokens=config.settings['TOKEN'],
                        group_id=214415883)


@bot.message_handler(bot.command_filter('mem'))
async def send_mem(event: SimpleBotEvent) -> str:
    user_id = event.object.object.message.peer_id
    memes_submissions = await reddit.subreddit(SUBREDDIT_NAME)
    memes_submissions = memes_submissions.new(limit=POST_LIMIT)
    item = await memes_submissions.__anext__()

    photo = await PhotoUploader(
        bot.api_context).get_attachment_from_link(
            peer_id=user_id, link=item.url)
    await event.answer(message=item.title, attachment=photo)


@bot.message_handler(bot.regex_filter(r'(?i)спасибо(.*?)'))
async def my_pleasure(event: SimpleBotEvent) -> str:
    return 'Всегда рад помочь &#128521;'


@bot.message_handler(bot.text_filter(['привет', 'здарова', 'хай']))
async def greet(event: SimpleBotEvent) -> str:
    await event.answer('Привет!')


bot.run_forever()
