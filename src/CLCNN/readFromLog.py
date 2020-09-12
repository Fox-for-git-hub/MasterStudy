# ファイルをオープンする
# text_data = open("access_log", "r")
text_data = open("dumytext", "r")

logbin_list = []

# 一行ずつ読み込んでは表示する
for line in text_data:
    char_list = list(line)
    print(char_list)

    charbin_list = []

    for char in char_list:
        ord_char = ord(char)
        bin_char = format(ord_char, '08b')
        # print(bin_char)
        charbin_list.append(bin_char)

    print(charbin_list)
    print(len(charbin_list))
    print("\n")

    logbin_list.append(charbin_list)

print(logbin_list)
print(len(logbin_list))
print("\n")

# ファイルをクローズする
text_data.close()