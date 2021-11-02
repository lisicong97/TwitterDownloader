import tweepy
import json

api_key = "9DRx899BVi0CSphy7j9IHmqOG"
api_key_secret = "ImeqOQzECJ0OYFzQJg6DYDRIDum5A1NMIVSERrsYBs8Vknhoxf"
access_token = "796793480458682369-ym0ndFjWEBF5cZx7Q50i1ZcHTmgO55u"
access_token_secret = "ePsyxtbz4YqXd3uzMzBaLjDBbLPGrlLD6eh4BdMrbvWvn"

user_ids = ["lscheard", "yua_mikami"]


class PullTweet:
    def __init__(self):
        self.since_id_dict = {}
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        with open("./data/since_ids.json") as f:
            self.since_id_dict.update(json.load(f))

    def store_since_ids(self):
        with open("./data/since_ids.json", "w") as f:
            json.dump(self.since_id_dict, f)

    def search_one_user(self, user_id):
        request_info = {"screen_name": user_id}
        if self.since_id_dict.get(user_id, "0") != "0":
            request_info["since_id"] = self.since_id_dict[user_id]
        user_tweets = self.api.user_timeline(**request_info)
        res = []
        has_set_since = False
        for tweet in user_tweets:
            if not has_set_since:
                self.since_id_dict[user_id] = tweet._json['id']
                has_set_since = True
            try:
                media_list = tweet._json['extended_entities']['media']
                url_list = []
                for i in media_list:
                    url_list.append(i['media_url'])
                if tweet._json['text'][:2] != "RT":
                    res.append((user_id, tweet._json['text'], url_list))
            except:
                pass
        return res

    # return a list of tuple(id, text, [urls])
    def search_group(self):
        res = []
        for user_id in user_ids:
            res.extend(self.search_one_user(user_id))
        self.store_since_ids()
        return res


if __name__ == "__main__":
    pullTweet = PullTweet()
    res = pullTweet.search_group()
