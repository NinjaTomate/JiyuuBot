import requests
import html
from urllib import parse
from . import command, send

@command
def wiki(msginfo):
    """
        .wiki <query> - searches Wikipedia for a query
    """
    UA = "JiyuuBot/1 (http://github.com/JiyuuProject/JiyuuBot; bob@bob131.so) BasedOnRequests/%s" % requests.__version__
    query = " ".join(msginfo['msg'].split()[1:])
    searchresult = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={}&format=json&srprop=redirecttitle&srprop=snippet".format(query) , headers={"user-agent": UA}).json()['query']['search'][0]
    title = searchresult['title']
    url = parse.quote(title)
    summaries = requests.get("http://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=&explaintext=&format=json&cllimit=10&cldir=descending&titles={}&redirects=".format(query), headers={"user-agent": UA}).json()["query"]["pages"]
    summaries = summaries[list(summaries.keys())[0]]
    if not "missing" in summaries.keys():
        snippet = summaries["extract"].split('\n')[0][:400]
    else:
        snippet = html.unescape(searchresult['snippet'].replace("<span class=\"searchmatch\">", "").replace("</span>", ""))
    send("\x02{}:\x02 {}...".format(title,snippet))
    send("https://en.wikipedia.org/wiki/{}".format(url))

