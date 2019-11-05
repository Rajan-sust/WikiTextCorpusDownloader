import argparse
import os 
import tensorflow as tf
from gensim.corpora import WikiCorpus

"""
Source: https://en.wikipedia.org/wiki/List_of_Wikipedias (last accessed 25/10/2019)
302 Languages
"""

WIKIPEDIA_LANGUAGES = [
    "aa", "ab", "ace", "ady", "af", "ak", "als", "am", "an", "ang", "ar", "arc",
    "arz", "as", "ast", "atj", "av", "ay", "az", "azb", "ba", "bar", "bat-smg",
    "bcl", "be", "be-x-old", "bg", "bh", "bi", "bjn", "bm", "bn", "bo", "bpy",
    "br", "bs", "bug", "bxr", "ca", "cbk-zam", "cdo", "ce", "ceb", "ch", "cho",
    "chr", "chy", "ckb", "co", "cr", "crh", "cs", "csb", "cu", "cv", "cy", "da",
    "de", "din", "diq", "dsb", "dty", "dv", "dz", "ee", "el", "eml", "en", "eo",
    "es", "et", "eu", "ext", "fa", "ff", "fi", "fiu-vro", "fj", "fo", "fr",
    "frp", "frr", "fur", "fy", "ga", "gag", "gan", "gd", "gl", "glk", "gn",
    "gom", "gor", "got", "gu", "gv", "ha", "hak", "haw", "he", "hi", "hif",
    "ho", "hr", "hsb", "ht", "hu", "hy", "hz", "ia", "id", "ie", "ig", "ii",
    "ik", "ilo", "inh", "io", "is", "it", "iu", "ja", "jam", "jbo", "jv", "ka",
    "kaa", "kab", "kbd", "kbp", "kg", "ki", "kj", "kk", "kl", "km", "kn", "ko",
    "koi", "kr", "krc", "ks", "ksh", "ku", "kv", "kw", "ky", "la", "lad", "lb",
    "lbe", "lez", "lfn", "lg", "li", "lij", "lmo", "ln", "lo", "lrc", "lt",
    "ltg", "lv", "mai", "map-bms", "mdf", "mg", "mh", "mhr", "mi", "min", "mk",
    "ml", "mn", "mr", "mrj", "ms", "mt", "mus", "mwl", "my", "myv", "mzn", "na",
    "nah", "nap", "nds", "nds-nl", "ne", "new", "ng", "nl", "nn", "no", "nov",
    "nrm", "nso", "nv", "ny", "oc", "olo", "om", "or", "os", "pa", "pag", "pam",
    "pap", "pcd", "pdc", "pfl", "pi", "pih", "pl", "pms", "pnb", "pnt", "ps",
    "pt", "qu", "rm", "rmy", "rn", "ro", "roa-rup", "roa-tara", "ru", "rue",
    "rw", "sa", "sah", "sat", "sc", "scn", "sco", "sd", "se", "sg", "sh", "si",
    "simple", "sk", "sl", "sm", "sn", "so", "sq", "sr", "srn", "ss", "st",
    "stq", "su", "sv", "sw", "szl", "ta", "tcy", "te", "tet", "tg", "th", "ti",
    "tk", "tl", "tn", "to", "tpi", "tr", "ts", "tt", "tum", "tw", "ty", "tyv",
    "udm", "ug", "uk", "ur", "uz", "ve", "vec", "vep", "vi", "vls", "vo", "wa",
    "war", "wo", "wuu", "xal", "xh", "xmf", "yi", "yo", "za", "zea", "zh",
    "zh-classical", "zh-min-nan", "zh-yue", "zu"]

def tokenizer_func(text: str, token_min_len: int, token_max_len: int, lower: bool) -> list:
    return [token for token in text.split() if token_min_len <= len(token) <= token_max_len]


def store(corpus, lang):
    base_path = os.getcwd()
    store_path = os.path.join(base_path, '{}_corpus'.format(lang))
    if not os.path.exists(store_path):
        os.mkdir(store_path)
    file_idx=1
    for text in corpus.get_texts():
        current_file_path = os.path.join(store_path, 'article_{}.txt'.format(file_idx))
        with open(current_file_path, 'w' , encoding='utf-8') as file:
            file.write(bytes(' '.join(text), 'utf-8').decode('utf-8'))
        #endwith
        file_idx += 1
    #endfor

def retrive(lang='bn'):
    origin='https://dumps.wikimedia.org/{}wiki/latest/{}wiki-latest-pages-articles.xml.bz2'.format(lang,lang)
    fname='{}wiki-latest-pages-articles.xml.bz2'.format(lang)
    file_path = tf.keras.utils.get_file(origin=origin, fname=fname, untar=False, extract=False)
    corpus = WikiCorpus(file_path, lemmatize=False, lower=False, tokenizer_func=tokenizer_func)
    store(corpus, lang)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', required=True, choices=WIKIPEDIA_LANGUAGES)
    args = parser.parse_args()
    retrive(args.language)

if __name__ == '__main__':
    main()
