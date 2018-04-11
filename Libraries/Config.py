

client_id = "fb79c2dd6754e3083342"
client_secret = "8c87f8a3a5b4a7450daccc671bb8bb056630451c"

# 登录地址
LoginUrl = "https://github.com/login/oauth/authorize?client_id={0}&scope=user".format(
    client_id)

# 获取token地址
TokenUrl = "https://github.com/login/oauth/access_token?client_id={0}&client_secret={1}&code=".format(
    client_id, client_secret)

# 获取用户信息
UserUrl = "https://api.github.com/user?access_token="

CachePath=""
StoragePath=""
