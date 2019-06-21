# from urllib.parse import urlparse
#
#
# url = "https://www.tohomh123.com/nanzigaozhongshengderichang/33.html"
#
# result = urlparse(url)
#
# print(result[1])
#
# aa = urlparse(scheme=result[0], netloc=result[1])
# # urlparse.urljoin
# bb = urlparse.urljoin(result[0], result[1])
# print(bb)


import uuid

namespace = uuid.NAMESPACE_URL
# namespace = "zkteam_manhua"
name = "zifu" #79668674-9a8a-347b-b3c7-4149ab965181
name = "zifu1" #79668674-9a8a-347b-b3c7-858632e8aed7
name = "1zifu1" #82421c0a-d1b2-374d-b3ee-443f36766a16

token = uuid.uuid3(namespace, name)

print(token)