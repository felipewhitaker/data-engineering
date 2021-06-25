from pytwitter import Api

class Scrapper:

    # TODO look into StreamApi Class
    
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACqJIQEAAAAAQIxjVwNQ%2Byihvyp6VhCENvJs%2B6s%3D8be4YlS92VEBFhsor2vEgt2AEIGY9XPKR4WzhYp9mgYR3VE7FD"

    def __init__(self):
        """[summary] Wrapper onto `pytwitter's` (https://github.com/sns-sdks/python-twitter) package

        Returns:
            None
        """
        self.api = Api(bearer_token = self.BEARER_TOKEN)
        return

    def query(self, query):
        """[summary] Wrapper onto `pytwitter's` Api object `self.search_tweets`

        Args:
            query (str): Twitter's query

        Returns:
            pytwitter.models.Response: Twitter's response, each with `id` and `text` as attributes
        """
        return s.api.search_tweets(query = query)


if __name__ == '__main__':

    # 128372940 == 'jairbolsonaro'

    s = Scrapper()
    res = s.query(query = 'from:jairbolsonaro')
    print(res.data[0].text)
