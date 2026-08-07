# Required Modules#
import scrapetube


class Backend:
    def __init__(self):
        self.cache = {}

    def search(self, query: str) -> dict:
        results = []
        final_results = {}
        if query in self.cache:
            final_results = self.cache.get(query)
        else:
            results = scrapetube.get_search(query, limit=20, results_type="video")
            for v in results:
                title = v["title"]["runs"][0]["text"]
                id = v["videoId"]
                url = f"https://youtube.com/watch?v={id}"
                channel = self.get_channel_name(v)

                final_results[id] = {"title": title, "url": url, "channelName": channel}

        self.cache[query] = final_results
        return final_results

    def get_channel_name(self, video):
        for key in ["longBylineText", "shortBylineText", "ownerText"]:
            txt = video.get(key, None)
            if txt is not None:
                return txt["runs"][0]["text"]
