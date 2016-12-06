import redis

class RedisClass:
    config = {
        'dev': {
            'host': '192.168.102.17',
            'port': '6379'
        }
    }
    conn = False
    def __init__(self, env):
        self.config = self.config[env]
        self.conn = redis.StrictRedis(host=self.config['host'], port=self.config['port'], db=0)

    def get_conn(self):
        if self.conn.ping():
            return self.conn
        else:
            return False
