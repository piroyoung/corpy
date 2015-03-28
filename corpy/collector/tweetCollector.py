from corpy.utils.textParser import TextParser
import json
import twitter

class StreamCollector():

    def __init__(self):
        keys = json.load(open('../../resource/setting_staging.json'))['twitter_api']
        self.parser = TextParser()
        self.twitter = twitter.TwitterStream(
            auth=twitter.OAuth(
                keys['token'],
                keys['token_secret'],
                keys['api_key'],
                keys['api_secret']))

    def getStream(self, num = 30):
        tw_bow = open('../../data/tweet_bow.dat', 'w', encoding='utf8')
        tw_info = open('../../data/tweet_info.dat', 'w', encoding='utf8')
        i = 0
        iter = self.twitter.statuses.sample()
        for tweet in iter:
            try:
                #日本語以外とリンクを含むツイートを削除する．
                if tweet['lang'] != 'ja' or 'http' in tweet['text']:
                    continue

            except:
                continue

            for line in self.getBow(tweet):
                tw_bow.write(line)

            tw_info.write(self.getInfo(tweet))
            i += 1
            if i == num:
                break

        tw_bow.close()
        tw_info.close()

    def getBow(self, tweet):
        bow = lambda: self.parser.parseToBow(tweet['text'])
        for b in bow():
            yield '\t'.join([tweet['id_str'], b[0], str(b[1])]) + '\n'

    def getInfo(self, tweet):
        info = lambda tweet: [
            tweet['id_str'],
            tweet['user']['id_str'],
            tweet['user']['screen_name'],
            str(tweet['user']['friends_count']),
            # ':'.join(tweet['entities']['hashtags']),
            tweet['created_at'],
            str(tweet['retweet_count']),
            str(tweet['favorite_count']),
            str(tweet['geo']),
            str(tweet['place']),
        ]
        return '\t'.join(info(tweet)) + '\n'

    def getRaw(self, num=3):
        tw_raw = open('../../data/tweet_raw.dat', 'w', encoding='utf8')
        i = 0
        iter = self.twitter.statuses.sample()
        for tweet in iter:
            try:
                #日本語以外とリンクを含むツイートを削除する．
                if tweet['lang'] != 'ja' or tweet['filter_level'] != 'low':
                    continue

            except:
                continue

            tw_raw.write(str(tweet) + '\n')
            i += 1
            if i == num:
                break

        tw_raw.close()





