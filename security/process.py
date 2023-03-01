import jieba

file_path="test.txt"
new_file_path="security_test.txt"


def get_label(path):
    with open(path,encoding="UTF-8") as file:
        label_list=[]
        for line in file.readlines():
            line_split=line.split(" ")
            if len(line_split)>0:
                try:
                    label=line_split[1]
                    label=label[:-1]
                    if(label not in label_list):
                        label_list.append(label)
                    else:
                        continue
                except:
                    pass
    return label_list
# ['B-Identity', 'I-Identity', 'O', 'B-Malware', 'I-Malware', 'B-Threat_Actor', 'I-Threat_Actor', 'B-Attack_Pattern', 'I-Attack_Pattern', 'B-Location', 'I-Location', 'B-Software', 'I-Software', 'B-ip', 'I-ip', 'B-Hardware', 'I-Hardware', 'B-Course_of_Action', 'I-Course_of_Action', 'B-url', 'I-url', 'B-Vulnerability', 'I-Vulnerability', 'B-OS', 'I-OS', 'B-path', 'I-path', 'B-hash', 'I-hash']

def data_build(path):
    word_res=[]
    label_res=[]
    seg_res=[]
    word_list = []
    label_list=[]
    with open( path ,'r' , encoding='utf8' ) as f :
         datas = f.read()
         sentences = datas.split('\n')
         for idx,sentence in enumerate(sentences):
             if sentence :
                split=sentence.split(" ")
                word=split[0]
                label=split[1]
                word_list.append(word)
                label_list.append(label)
                if(idx == len(sentences)-1):
                    word_res.append( word_list )
                    label_res.append( label_list )
                    word_list = [ ]
                    label_list = [ ]
             else :
                if(len(word_list)>0):
                    word_res.append(word_list)
                    label_res.append(label_list)
                    word_list=[]
                    label_list=[]
    for test_content in word_res:
        text="".join(test_content)
        res = jieba.tokenize( text)
        seg_list = [ 0 ] * len( text )
        for r in res :
            #实现分词，限定分词长度为4
            if (len( r [ 0 ] ) > 1 and len(r[0])<5) :#word:蔓灵花		 start:7	 end:10
                print( 'word:{}\t start:{}\t end:{}'.format( *r ) )
                start=r[1]
                end=r[2]
                seg_list[start:end]=[i for i in range(0,end-start)]
        seg_res.append(seg_list)
    with open( new_file_path , 'w' , encoding='utf8' ) as file :
        str_text=[]
        for idx1,w in enumerate(word_res):
            for idx2,l in enumerate(w):
                str_text.append(word_res[idx1][idx2])
                try:
                    seg=seg_res [ idx1 ] [ idx2 ]
                    seg=str(seg)
                    str_text.append( seg )
                except:
                    print("")
                str_text.append(" ")
                str_text.append( label_res [ idx1 ] [ idx2 ] )
                str_text.append("\n")
            if(idx1!=len(word_res)-1):
                str_text.append("\n")
        file.writelines(str_text)
        file.close()
if __name__=='__main__':
    res=data_build(file_path)
