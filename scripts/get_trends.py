import requests

url='https://twitter-trends.iamrohit.in/united-states'

def get_top_trends(n=2):
    response = requests.get(url)
    content = response.content.decode()
    # Some special trimming to get to the required content
    content = content[content.index('<tbody id="copyData">'):]
    top_trends = []
    for i in range(n):
        content = content[ content.index('<tr>')+4 : ]
        row = content[:content.index('</tr>')]
        link = row[row.index('<a'):]
        topic = link[ link.index('>')+1:link.index('</a>') ]
        top_trends.append(topic)
    return top_trends