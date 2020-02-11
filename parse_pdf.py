from path import get_path
from pdfminer.high_level import extract_text

path = get_path() + '/data/pdf/'
file = path + 'tmp.pdf'
text = extract_text(file)
text_list = text.split('\n')
name = text_list[4].encode("latin-1").decode('cp1251')
