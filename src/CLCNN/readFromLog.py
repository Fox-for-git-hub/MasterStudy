# ファイルをオープンする
# text_data = open("access_log", "r")
text_data = open("dumytext", "r")

# 一行ずつ読み込んでは表示する
for line in text_data:
    print(line)

# ファイルをクローズする
text_data.close()