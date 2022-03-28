import redis


class KeywordManager:
  def __init__(self, redis: redis.Redis):
    self.redis = redis
    self.keywords = {}
    """keywords structure:
    {
      "word": ["1234", "5678"],
    }
    """
    self.load_keywords()

  def load_keywords(self):
    for key in self.redis.scan_iter("schwi:keywords:*"):
      key = key.decode("utf-8")
      keyword = key.split(":")[-1]
      users = self.redis.smembers(key)
      self.keywords[keyword] = list(map(lambda x: x.decode("utf-8"), users))

  def add_keyword(self, keyword: str, user_id: str):
    keyword = keyword.lower()
    if keyword not in self.keywords:
      self.keywords[keyword] = []
    self.keywords[keyword].append(user_id)
    self.redis.sadd("schwi:keywords:{}".format(keyword), user_id)

  def remove_keyword(self, keyword: str, user_id: int):
    keyword = keyword.lower()
    if keyword in self.keywords:
      if user_id in self.keywords[keyword]:
        self.keywords[keyword].remove(user_id)
        self.redis.srem("schwi:keywords:{}".format(keyword), user_id)
        if len(self.keywords[keyword]) == 0:
          del self.keywords[keyword]
          self.redis.delete("schwi:keywords:{}".format(keyword))

  def get_keywords(self, user_id: str) -> list[str]:
    return [
      keyword for keyword, users in self.keywords.items() if str(user_id) in users
    ]

  def get_interested_users(self, text: str):
    text = text.lower()
    interested_users = []
    for keyword in self.keywords:
      if keyword in text:
        interested_users += self.keywords[keyword]
    return interested_users


class KeywordNotFoundError(Exception):
  def __init__(self, keyword: str):
    self.keyword = keyword

  def __str__(self):
    return "Keyword not found: {}".format(self.keyword)
