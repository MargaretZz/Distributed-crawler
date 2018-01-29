import jieba

txt = ''
fin = open('data.txt', 'rt')
while True:
    line = fin.readline()
    if not line:
        break
    txt += line

fout = open('data_jieba.txt', 'wt')


seg_list = jieba.cut(txt, cut_all=True)
fout.write(" ".join(seg_list))  # 全模式