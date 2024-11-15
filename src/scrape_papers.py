from bs4 import BeautifulSoup
import requests
import pypdfium2 as pdfium
import requests
from tika import parser
from PyPDF2 import PdfReader

def get_paper(paper_name):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    search_paper_name=paper_name.replace('+', '%2B').replace('%', '%25').replace('&', '&26').replace(':', '%3A').replace(' ', '+')
    url = f'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C48&q={search_paper_name}&btnG=&authuser=3'
    print(url)
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,'lxml')
    item=soup.select('[data-lid]')[0]
    ref=item.select('[data-clk-atid]')
    name=ref[1].text
    url=ref[0].attrs['href']
    if paper_name.lower()!=name.lower():
        print(f'names dont match! {paper_name.lower()} {name.lower()}')
    return name, url
    
def get_pdf(url, save_loc)
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    response = requests.get(url,headers=headers)

    file_name=os.path.join(save_loc, f'{paper_name}.pdf')
    print(file_name)
    pdf = open(file_name, 'wb')
    pdf.write(response.content)
    print(len(response.content))
    pdf.close()

    reader = PdfReader(file_name)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    print(text)
    
paper_name="Imagenet: A large-scale hierarchical image database"
name, url=get_paper(paper_name)
print(name, url)
get_pdf(url, "/scratch/github/")