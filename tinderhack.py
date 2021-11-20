# -*- coding: utf-8 -*-

from tinderbot import Tinderbot
from logger import logger
from time import sleep

logger.info('[SCRIPT START]')

FB_USER = "email"
FB_PASS = "password"

print('Starting Tinder Second Like script...')
bot = Tinderbot()
bot.login_with_fb(FB_USER, FB_PASS)
bot.prepare_for_swiping()

second_swipe_working = True
matches = 0
while second_swipe_working:
    try:
        bot.dislike()
    except Exception as e:
        if bot.check_for_empty_swipe():
            logger.warning('Tinder ran out of girls')
            print("Tinder ran out of girls!!")
            break
        raise e
    bot.like()
    if bot.check_for_match():
        matches += 1
        logger.info('Success! Match #%s', matches)
        print('Success! Match #{}.'.format(matches))
        bot.refresh_tinder()
    else:
        if bot.check_for_no_likes_left():
            logger.warning('Bot ran out of likes!')
            print('Bot ran out of likes!')
        else:
            logger.info('Second like stopped working')
            print('Second like stopped working')
        second_swipe_working = False
    continue

bot.stop()

logger.info('[SCRIPT END]')
