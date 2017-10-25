import random
from msic.common import agents


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents.AGENTS_ALL)
        request.headers['User-Agent'] = agent


