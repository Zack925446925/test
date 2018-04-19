def tm_repetition_process(num,names):
#将多规格多名称合并
    df = pd.read_excel(filePath + 'tqdt_' +names, sheetname = num)
    danping = []
    guige = []
    for name in df.columns:
        if '单品' in name:
            danping.append(name)
        elif '规格' in name:
            guige.append(name)
    if len(danping) > 1:
        df['单品'] = np.NaN
        for i in range(len(df[danping[0]])):
            if df[danping[0]][i] == df[danping[1]][i]:
                df['单品'][i] = df[danping[0]][i]
            else:
                df['单品'][i] = str(df[danping[0]][i]) + str(df[danping[1]][i])
        del df[danping[0]]
        del df[danping[1]]
    if len(guige) > 1:
        df['规格'] = np.NaN
        for i in range(len(df[guige[0]])):
            if df[guige[0]][i] == df[guige[1]][i]:
                df['规格'][i] = df[guige[0]][i]
            else:
                df.loc[i,'规格'] = str(df[guige[0]][i])  + str(df[guige[1]][i])
        del df[guige[0]]
        del df[guige[1]]
#以产品名称去除重复部分，将不同链接及合并在一个商品名下
    cp = []
    cp_gg_all = []
    cp_url_all = []
    for i in df['单品']:
        if i not in cp:
            cp.append(str(i).strip())
    for i in cp:
        cp_gg = ''
        cp_url = ''
        for j in range(len(df['单品'])):
            if i == df['单品'][j]:
                cp_url += df['页面网址'][j] + '~'
                cp_gg += str(df['规格'][j])
        cp_gg_all.append(cp_gg)
        cp_url_all.append(cp_url)
    path = filePath + 'fianl_tm_' + names
    path = path.replace('xls','csv')
    with open(path, 'a+') as f:
        f.write('商品名称' + ',' + '规格' + ',' + '商品网址' + '\n')
    for i in range(len(cp)):
        cp[i] = cp[i].replace('?', '')
        cp_gg_all[i] = cp_gg_all[i].replace('?', ' ')
        cp_gg_all[i] = cp_gg_all[i].replace('nan', '')
        with open(path, 'a+') as f:
            f.write(str(cp[i]).replace(u'\xa0', u'') + ',' + str(cp_gg_all[i]).replace(u'\xa0', u'') + ',' + str(cp_url_all[i]).replace(u'\xa0', '') + u'\n')
