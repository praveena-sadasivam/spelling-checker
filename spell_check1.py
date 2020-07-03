import re
import string
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from bloomfilter import BloomFilter, ScalableBloomFilter, SizeGrowthRate


regex = re.compile('[0-9]')



#loading into bloom filter object from file
with open("/Users/ADMIN/Desktop/py/spelling_checker/bloom_filter_english_dictionary.bin", "rb") as file_obj:
        common = BloomFilter.load(file_obj)

with open("/Users/ADMIN/Desktop/py/spelling_checker/bloom_filter_custom_dictionary.bin", "rb") as file_obj:
        custom = BloomFilter.load(file_obj)



def find_invalid_word(content):
    count=0
    invalid_words=set()
    word_dict={}
    #replacing punctuation with white space
    translator= str.maketrans(string.punctuation, ' '*len(string.punctuation))
    text=str(content).translate(translator)

    #word tokenization
    words=word_tokenize(text)

    #excluding digits
    words=[regex.sub('', word) for word in words]

    #testing and printing invalid word (word not in custom and common english dictionary)
    for word in words:
        if len(word)>=1:
            if word.isalpha():
                word = re.sub(r'[^\x00-\x7f]', r'', word)
                if word.casefold()  not in custom:
                    if word.casefold() not  in common:
                        invalid_words.add(word)
    lines=content.split('\n')
 
    if len(invalid_words)>=1:
        for line in lines:
            word_list=[]
            count+=1
            for word in invalid_words:
                if word in line:
                    word_list.append(word)
                if len(word_list)>0:
                    word_dict[count]=word_list
        
        return word_dict
    else:
        msg="All words are valid "
        return msg


