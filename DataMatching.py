from csv import reader
import csv
from collections import Counter
import datetime
Amazon=[]
Google=[]
#数据结构：
#[ ['b000jz4hqo', 'clickart 950 000 - premier image pack (dvd-rom)', '', 'broderbund', '0'],...]
#列表中每个元素代表一行数据子列表中每一个元素代表一列
Amazon_tokens=[]
Google_tokens=[]
#[ ['b000jz4hqo', ['clickart', '950', '000', '-', 'premier', 'image', 'pack', '(dvd-rom)', '', 'broderbund', '0']],...]
#列表中每一个元素代表一行数据的id和对应的tokens
Amazon_keywords=[]
Google_keywords=[]
#['clickart', '950', '000', '-', 'premier', 'image', 'pack', '(dvd-rom)', '', 'broderbund', '0', 'ca', 'international',...]
Amazon_TF_tokens=[]
Google_TF_tokens=[]
#[ ['b000jz4hqo', [['clickart', 0.09090909090909091], ['950', 0.09090909090909091], ['000', 0.09090909090909091], 
# ['-', 0.09090909090909091], ['premier', 0.09090909090909091], ['image', 0.09090909090909091], ['pack', 0.09090909090909091], 
# ['(dvd-rom)', 0.09090909090909091], ['', 0.09090909090909091], ['broderbund', 0.09090909090909091], ['0', 0.09090909090909091]]],... ]
#每个元素代表一行数据的id和对应的每个token的TF值
Amazon_TF_IDF_tokens=[]
Google_TF_IDF_tokens=[]
#[ [['clickart', 18.181818181818183], ['950', 18.181818181818183], ['000', 0.8658008658008658], ['-', 0.05941770647653001], 
# ['premier', 9.090909090909092], ['image', 0.5509641873278237], ['pack', 2.0202020202020203], ['(dvd-rom)', 18.181818181818183], 
# ['', 0.8658008658008658], ['broderbund', 9.090909090909092], ['0', 0.3305785123966942]],... ]
#每个元素代表一行数据的token和对应的TF_IDF值
stopwords=[]
#['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should',...]
Amazon_norms=[]
Google_norms=[]
#[1163.0216060217206, 561.4083153450882, 1554.5411533912609, 82.7850339240295, 374.6684037464485, ...]
Amazon_reverse_dictionary={}
Google_reverse_dictionary={}
#{'clickart': [0], '950': [0], '000': [0, 35, 40, 43, 73, 115, 126, 158], 
# '-': [0, 1, 3, 4, 6, 7, 11, 36, 38, 39, 45, 49, 50, 51, 54, 62, 66, 67, 69, 71, 75, 79, 80, 84, 89, 92, 99, 106, 107, 110, 122, 127, 
# 134, 135, 137, 142, 149, 154, 156, 157, 161, 165, 166, 170, 172, 174, 178, 182, 183, 185, 186, 187, 189, 190, 193, 197, 198], 
# 'premier': [0, 114], ...}
#反向索引字典，标记了每个token在数据的哪些行出现
Amazon_Google_perfectMapping=[]
#[['b000jz4hqo', 'http://www.google.com/base/feeds/snippets/18441480711193821750'], ...]
#最佳id匹配
def openfile():
	with open('Amazon.csv', 'rt', newline='') as csvfile:
		readers  = reader(csvfile)
		for line in readers:
			Amazon.append(line)
		del Amazon[0]
		csvfile.close()
	with open('Google.csv', 'rt', newline='') as csvfile:
		readers  = reader(csvfile)
		for line in readers:
			Google.append(line)
		del Google[0]
		csvfile.close()
	with open('stopwords.txt', 'rt') as file:
		readers  = reader(file)
		for line in readers:
			stopwords.append(line[0])
		file.close()
#计算tokens （Amazon,Google）
def compute_tokens(a,b):
	#提取Amazon数据的tokens
	for i in a:
		#i是每行数据
		temp=[]
		#添加id
		temp.append(i[0])
		string=''
		#对每行数据中除id列进行合并，列之间用‘ ’隔开
		for j in range(len(i)):
			if j!=0:
				if j!=1:
					string=string+' '+i[j]
				else:
					string=string+i[j]
		#不区分大小写
		ls=string.lower().split(' ')
		ls1=[]
		#去除常见词
		for t in ls:
			if t not in stopwords:
				ls1.append(t)
				Amazon_keywords.append(t)
		temp.append(ls1)
		Amazon_tokens.append(temp)
	#同上
	for i in b:
		temp=[]
		temp.append(i[0])
		string=''
		for j in range(len(i)):
			if j!=0:
				if j!=1:
					string=string+' '+i[j]
				else:
					string=string+i[j]
		ls=string.lower().split(' ')
		ls1=[]
		for t in ls:
			if t not in stopwords:
				ls1.append(t)
				Google_keywords.append(t)
		temp.append(ls1)
		Google_tokens.append(temp)
#计算TF （Amazon_tokens,Google_tokens）
def compute_TF_tokens(a,b):
	for i in a:		
		temp=[]
		for j in i[1]:
			#i[1]为['clickart', '950', '000', '-', 'premier', 'image', 'pack', '(dvd-rom)', '', 'broderbund', '0']
			ls=[]
			#对每一行数据的token计数
			count=0
			for k in i[1]:
				if j==k:
					count=count+1
			ls.append(j)
			#计算TF
			ls.append(count/len(i[1]))
			#去重存储
			if ls not in temp:
				temp.append(ls)
		ls1=[]
		ls1.append(i[0])
		ls1.append(temp)
		Amazon_TF_tokens.append(ls1)
	for i in b:		
		temp=[]
		for j in i[1]:
			ls=[]
			count=0
			for k in i[1]:
				if j==k:
					count=count+1
			ls.append(j)
			ls.append(count/len(i[1]))
			if ls not in temp:
				temp.append(ls)
		ls1=[]
		ls1.append(i[0])
		ls1.append(temp)
		Google_TF_tokens.append(ls1)
#计算TF_IDF （Amazon_TF_tokens,Google_TF_tokens,Amazon_keywords,Google_keywords）
def compute_TF_IDF_tokens(a,b,c,d):
	Amazon_tokens_number=len(a)
	Google_tokens_number=len(b)
	#**_keywords是一个对每一行数据去重的关键字列表，所以每个关键字在列表中的出险次数即为该关键字在数据中出现了几行
	Amazon_dictionary=dictionary(c)
	Google_dictionary=dictionary(d)
	for i in a:
		temp=[]
		for j in i[1]:
			#i[1]:[['clickart', 0.09090909090909091], ['950', 0.09090909090909091], ['000', 0.09090909090909091]
			#根据关键字在字典中取得出现行数
			count=Amazon_dictionary[j[0]]			
			ls=[]
			ls.append(j[0])
			#求得TF_IDF
			ls.append(Amazon_tokens_number/count*j[1])
			temp.append(ls)
		Amazon_TF_IDF_tokens.append(temp)
	for i in b:
		temp=[]
		for j in i[1]:
			count=Google_dictionary[j[0]]
			ls=[]
			ls.append(j[0])
			ls.append(Google_tokens_number/count*j[1])
			temp.append(ls)
		Google_TF_IDF_tokens.append(temp)
#Amazon_keywords
def dictionary(a):
	#对列表a进行计数，并返回一个字典
	return dict(Counter(a))
#取模 （Amazon_TF_IDF_tokens,Google_TF_IDF_tokens）
def compute_norms(a,b):
	for i in a:
		#i：
		#[['clickart', 18.181818181818183], ['950', 18.181818181818183], ['000', 0.8658008658008658], ['-', 0.05941770647653001], 
		# ['premier', 9.090909090909092], ['image', 0.5509641873278237], ['pack', 2.0202020202020203], ['(dvd-rom)', 18.181818181818183], 
		# ['', 0.8658008658008658], ['broderbund', 9.090909090909092], ['0', 0.3305785123966942]]
		norms=0
		for j in i:
			norms=norms+j[1]*j[1]
		Amazon_norms.append(norms)
	for i in b:
		norms=0
		for j in i:
			norms=norms+j[1]*j[1]
		Google_norms.append(norms)
#匹配函数 (Amazon_TF_IDF_tokens,Google_TF_IDF_tokens,Amazon_tokens,Google_tokens)
def perfect_mapping(a,b,c,d):
	for i in range(len(a)):
		#记录最大余弦相似度和对应的index
		max_index=0
		max_cos=0		
		index=[]
		#对a中一行数据的所有token查找其是否在Google_reverse_dictionary中，若在，将所有行号存到index列表中
		for k in a[i]:
			if k[0] in Google_reverse_dictionary:	
				for t in Google_reverse_dictionary[k[0]]:
					if t not in index:
						index.append(t)
		#查找所有与该行数据有关（在Google中同样出现过该token）的行
		for s in index:	
			temp=0
			for t in a[i]:					
				for m in b[s]:
					#若id相同，则TF_IDF相乘
					if t[0]==m[0]:
						temp=temp+t[1]*m[1]
			current_cos=temp/Amazon_norms[i]*Google_norms[s]
			#若该行的余弦相似度比之前的大，则更新max_cos和max_index
			if current_cos>max_cos:
				max_cos=current_cos
				max_index=s
		ls=[]
		#完成匹配
		ls.append(c[i][0])
		ls.append(d[max_index][0])
		Amazon_Google_perfectMapping.append(ls)
#反向索引 （Amazon_TF_tokens,Google_TF_tokens）
def reverse_index(a):
	for i in range(len(a)):
		temp=a[i][1]
		#[['clickart', 0.09090909090909091], ['950', 0.09090909090909091], ['000', 0.09090909090909091], 
		# ['-', 0.09090909090909091], ['premier', 0.09090909090909091], ['image', 0.09090909090909091], ['pack', 0.09090909090909091], 
		# ['(dvd-rom)', 0.09090909090909091], ['', 0.09090909090909091], ['broderbund', 0.09090909090909091], ['0', 0.09090909090909091]]
		for j in range(len(temp)):
			if temp[j][0] in Google_reverse_dictionary:
			#若该id已在字典中，则先取出原来的index列表，再添加当前行号
				ls=Google_reverse_dictionary[temp[j][0]]
				ls.append(i)
				Google_reverse_dictionary[temp[j][0]]=ls
			else:
			#若该id已在字典中，则直接插入当前行号组成的列表
				ls=[]
				ls.append(i)
				Google_reverse_dictionary[temp[j][0]]=ls
def showdata(a):
	with open("data_Mapping.csv", "w", newline='') as f:
		writer = csv.writer(f)
		for line in a:
			writer.writerow(line)
		f.close()
def accuracy():
	data_Mapping=[]
	Amazon_Google_perfectMapping=[]
	with open('data_Mapping.csv', 'rt', newline='') as csvfile:
		readers  = reader(csvfile)
		for line in readers:
			data_Mapping.append(line)
		csvfile.close()
	with open('Amazon_Google_perfectMapping.csv', 'rt', newline='') as csvfile:
		readers  = reader(csvfile)
		for line in readers:
			Amazon_Google_perfectMapping.append(line)
		del Amazon_Google_perfectMapping[0]
		csvfile.close()
	Amazon_Google_perfectMapping=dict(Amazon_Google_perfectMapping)
	count=0
	for i in range(len(data_Mapping)):
		if data_Mapping[i][0] in Amazon_Google_perfectMapping:
			if data_Mapping[i][1]==Amazon_Google_perfectMapping[data_Mapping[i][0]]:
				count=count+1
	return count/len(data_Mapping)
if __name__ == "__main__":
	openfile()
	compute_tokens(Amazon,Google)
	compute_TF_tokens(Amazon_tokens,Google_tokens)
	reverse_index(Google_TF_tokens)
	compute_TF_IDF_tokens(Amazon_TF_tokens,Google_TF_tokens,Amazon_keywords,Google_keywords)
	compute_norms(Amazon_TF_IDF_tokens,Google_TF_IDF_tokens)
	perfect_mapping(Amazon_TF_IDF_tokens,Google_TF_IDF_tokens,Amazon_tokens,Google_tokens)
	showdata(Amazon_Google_perfectMapping)
	# print(accuracy())