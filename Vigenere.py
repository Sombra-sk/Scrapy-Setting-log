from string import ascii_uppercase as uppercase
from itertools import cycle
 
#创建密码表
table=dict()
for ch in uppercase:
    index=uppercase.index(ch)
    table[ch]=uppercase[index:]+uppercase[:index]
    
#创建解密码表
deTable={'A':'A'}
start='Z'
for ch in uppercase[1:]:
    index=uppercase.index(ch)
    deTable[ch]=chr(ord(start)+1-index)
 
#解密密钥
def deKey(key):
    return ''.join([deTable[i] for i in key])
 
#加密/解密
def encrypt(plainText,key):
    result=[]
    #创建cycle对象，支持密钥字母的循环使用
    currentKey=cycle(key)
    for ch in plainText:
        if 'A'<=ch<='Z':
            index=uppercase.index(ch)
        #获取密钥字母
            ck=next(currentKey)
            result.append(table[ck][index])
        else:
            result.append(ch)
    return ''.join(result)
 
#进行加密
# key=input('请输入你的密钥：')#输入只能大写字母
# p=input('请输入你想要的加密的内容：')#输入只能大写字母
# c=encrypt(p,key)
# print('加密后的内容为',c)
#进行解密
q=input('请输入你想要解密的内容：')
key1=input('请输入密钥：')
print('解密后的内容为：',encrypt(q,deKey(key1)))