import json
import re

def levenshtein_distance(a, b):
    distances = [[0 for _ in range(len(b) + 1)] for _ in range(len(a) + 1)]
    
    for i in range(len(a) + 1):
        distances[i][0] = i
    for j in range(len(b) + 1):
        distances[0][j] = j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i-1] == b[j-1] else 1
            distances[i][j] = min(distances[i-1][j] + 1,  
                                  distances[i][j-1] + 1,    
                                  distances[i-1][j-1] + cost) 

    return distances[-1][-1]


import re
def count_syllables(word) :
    word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables

    exception_add = ['serious','crucial']
    exception_del = ['fortunately','unfortunately']

    co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
    co_two = ['coapt','coed','coinci']

    pre_one = ['preach']

    syls = 0 #added syllable number
    disc = 0 #discarded syllable number

    #1) if letters < 3 : return 1
    if len(word) <= 3 :
        syls = 1
        return syls

    #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed" :
        doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]',word))
        if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
                pass
            else :
                disc+=1

    #3) discard trailing "e", except where ending is "le"  

    le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']

    if word[-1:] == "e" :
        if word[-2:] == "le" and word not in le_except :
            pass

        else :
            disc+=1

    #4) check if consecutive vowels exists, triplets or pairs, count them as one.

    doubleAndtripple = len(re.findall(r'[eaoui][eaoui]',word))
    tripple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
    disc+=doubleAndtripple + tripple

    #5) count remaining vowels in word.
    numVowels = len(re.findall(r'[eaoui]',word))

    #6) add one if starts with "mc"
    if word[:2] == "mc" :
        syls+=1

    #7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui" :
        syls +=1

    #8) add one if "y" is surrounded by non-vowels and is not in the last word.

    for i,j in enumerate(word) :
        if j == "y" :
            if (i != 0) and (i != len(word)-1) :
                if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
                    syls+=1

    #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.

    if word[:3] == "tri" and word[3] in "aeoui" :
        syls+=1

    if word[:2] == "bi" and word[2] in "aeoui" :
        syls+=1

    #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"

    if word[-3:] == "ian" : 
    #and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian" :
            pass
        else :
            syls+=1

    #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:2] == "co" and word[2] in 'eaoui' :

        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
            syls+=1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
            pass
        else :
            syls+=1

    #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui' :
        if word[:6] in pre_one :
            pass
        else :
            syls+=1

    #13) check for "-n't" and cross match with dictionary to add syllable.

    negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]

    if word[-3:] == "n't" :
        if word in negative :
            syls+=1
        else :
            pass   

    #14) Handling the exceptional words.

    if word in exception_del :
        disc+=1

    if word in exception_add :
        syls+=1     

    # calculate the output
    return numVowels - disc + syls


def vowelsnconsonants(word):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Z']
    vowels_count = 0
    consonants_count = 0
    for letter in word:
        if letter in vowels:
            vowels_count += 1
        elif letter in consonants:
            consonants_count += 1
    return vowels_count, consonants_count 



nicksFile = open("textforcombo.txt", "r")
nicksHelp = nicksFile.read()
nicks = nicksHelp.capitalize().split("\n")
nicksFile.close()

         
allFile = open("cleaned_english_fulllist.json", "r")
allWords = json.load(allFile)
allFile.close()


print(nicks)

cuteNicksDict = {}
uglyNicksDict = {"bc": "1", "bd": "1", "bf": "1", "bg": "1", "bh": "1", "bk": "1", "bp": "1", "bq": "1", "bw": "1", "bx": "1", "bz": "1", "cb": "1", 
                 "cd": "1", "cf": "1", "cg": "1", "cj": "1", "cn": "1", "cp": "1", "cv": "1", "cw": "1", "cx": "1", "cz": "1", "dc": "1", "dk": "1", 
                 "dq": "1", "dx": "1", "dz": "1", "fb": "1", "fc": "1", "fd": "1", "fg": "1", "fh": "1", "fj": "1", "fk": "1", "fm": "1", "fp": "1", 
                 "fq": "1", "fx": "1", "fw": "1", "fz": "1", "gz": "1", "hz": "1", "jz": "1", "kz": "1", "lz": "1", "mz": "1", "pz": "1", "rz": "1", 
                 "sz": "1", "uz": "1", "vz": "1", "yz": "1", "yy": "1", "jy": "1", "iy": "1", "zx": "1", "yx": "1", "wx": "1", "vx": "1", "tx": "1", 
                 "sx": "1", "rx": "1", "qx": "1", "px": "1", "mx": "1", "lx": "1", "kx": "1", "jx": "1", "hx": "1", "gx": "1", "zw": "1", "xw": "1", 
                 "ww": "1", "vw": "1", "uw": "1", "qw": "1", "pw": "1", "mw": "1", "jw": "1", "iw": "1", "gw": "1", "zv": "1", "yv": "1", "wv": "1", 
                 "qv": "1", "qa": "1", "gb": "1", "jb": "1", "kb": "1", "pb": "1", "qb": "1", "vb": "1", "wb": "1", "xb": "1", "zb": "1", "gc": "1", 
                 "hc": "1", "jc": "1", "kc": "1", "pc": "1", "qc": "1", "vc": "1", "wc": "1", "zc": "1", "jd": "1", "kd": "1", "md": "1", "pd": "1", 
                 "qd": "1", "td": "1", "vd": "1", "xd": "1", "zd": "1", "qe": "1", "gf": "1", "jf": "1", "pf": "1", "qf": "1", "vf": "1", "yf": "1", 
                 "zf": "1", "hg": "1", "jg": "1", "mg": "1", "pg": "1", "vg": "1", "wg": "1", "xg": "1", "zg": "1", "hh": "1", "jh": "1", "mh": "1", 
                 "qh": "1", "ih": "1", "yh": "1", "zh": "1", "qi": "1", "gj": "1", "hj": "1", "jj": "1", "kj": "1", "lj": "1", "mj": "1", "pj": "1", 
                 "qj": "1", "sj": "1", "tj": "1", "vj": "1", "wj": "1", "xj": "1", "zj": "1", "gk": "1", "hk": "1", "jk": "1", "kk": "1", "mk": "1", 
                 "pk": "1", "qk": "1", "tk": "1", "vk": "1", "wk": "1", "xk": "1", "zk": "1", "xl": "1", "jm": "1", "vm": "1", "wm": "1", "xm": "1", 
                 "zm": "1", "fn": "1", "jn": "1", "pn": "1", "qn": "1", "zn": "1", "qo": "1", "gp": "1", "jp": "1", "kp": "1", "vp": "1", "zp": "1", 
                 "gq": "1", "hq": "1", "jq": "1", "lq": "1", "mq": "1", "pq": "1", "qq": "1", "tq": "1", "uq": "1", "wq": "1", "xr": "1", "zr": "1", 
                 "qs": "1", "vs": "1", "xs": "1", "zs": "1", "qt": "1", "vt": "1", "zt": "1", "uu": "1", "wu": "1", "yu": "1"}

# robi quita po litty kitty a potem od razu kbity
for nick in nicks:
    
    
    nickDummy = nick
    n=97
    i=0
    j=0
    length = len(nick)
    
    while i < length:
        while j < 27:
            nickDummy = nick
            if n == 123:
                n = 97
            nickDummy = nickDummy[:i] + chr(n) + nickDummy[i+1:]
            j+=1
            n+=1
            cuteNicksDict.update({nickDummy.lower(): nick})
        j=0
        i+=1
            
    
resultFile = open("results.txt", "w")

processed_words = set() 

print(cuteNicksDict)

for cuties in cuteNicksDict:
    for words in allWords:
        if cuties in words and len(words) >= (len(cuties)+2):
            mainword_syllables = count_syllables(words)
            modified_word = re.sub(rf'{cuties}', cuteNicksDict[cuties], words, flags=re.IGNORECASE)
            cuties_syllables = count_syllables(cuties)
            word_syllables = count_syllables(modified_word)
            distance = levenshtein_distance(cuties.lower(), modified_word.lower())

            if len(words) <= 10 and len(words) >= 4 and vowelsnconsonants(words) == vowelsnconsonants(modified_word):
                if distance > 2 and mainword_syllables < 5:
                    if not any(ugly_nick in modified_word for ugly_nick in uglyNicksDict):
                        resultFile.write(modified_word.capitalize() + " " + words + "\n")# + "                 " + words + " " + cuties + " " + cuteNicksDict[cuties] +  " " + str(mainword_syllables) + "\n")
                        #print(modified_word + "           " + words + " " + cuties + " " + cuteNicksDict[cuties])
                        processed_words.add(words.lower()) 
                        continue  

            if len(words) <= 10 and len(words) >= 4 and abs(cuties_syllables - word_syllables) <= 1 and mainword_syllables < 5 and vowelsnconsonants(words) == vowelsnconsonants(modified_word): 
                if not any(ugly_nick in modified_word for ugly_nick in uglyNicksDict):
                    resultFile.write(modified_word.capitalize() + " " + words + "\n")# + "                     " + " " + words + " " + cuties + " " + cuteNicksDict[cuties] + " " + str(mainword_syllables) + " " +"\n")
                    #print(f"Matched: {modified_word} (Syllable match with {cuties})")
                    processed_words.add(words.lower()) 
                    
                    
                    
                    
resultFile.close()
print("Done")