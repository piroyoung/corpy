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

    def getStream(self, num):
        i = 0
        iter = self.twitter.statuses.sample()
        for tweet in iter:
            try:
                #日本語以外とリンクを含むツイートを削除する．
                if tweet['lang'] != 'ja' or 'http' in tweet['text']:
                    continue

            except:
                continue

            yield tweet
            if i == num:
                break


    def getBow(self, tweet):
        bow = lambda tw: self.parser.parseToBow(tw['text'])
        return bow(tweet)

    def getInfo(self, tweet):
        info = lambda tw: [
            tw['id_str'],
            tw['user']['id_str'],
            tw['user']['screen_name'],
            str(tw['user']['friends_count']),
            # ':'.join(tweet['entities']['hashtags']),
            tw['created_at'],
            str(tw['retweet_count']),
            str(tw['favorite_count']),
            str(tw['geo']),
            str(tw['place']),
        ]
        return info(tweet)

    # json形式確認のためのテスト用メソッド
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





