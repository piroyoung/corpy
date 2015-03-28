from corpy.collector.tweetCollector import StreamCollector

if __name__ == '__main__':
    tw = StreamCollector()
    tw.getStream(30)
