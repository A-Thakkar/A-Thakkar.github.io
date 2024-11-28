from scholarly import scholarly
import os
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class PublicationRecord:
    """Class detailing the publication information
    """
    title: str
    collection: str
    category: str
    excerpt: str
    permalink: str
    date: str
    venue: str
    paperurl: str


author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
scholarly.fill(author, sections=['publications'])

for publication in author['publications']:
   scholarly.fill(publication)

for publication in author['publications']:
    bib = publication['bib']
    title = bib['title']
    year = f'{bib.get('pub_year', '2000')}-01-01' # TODO: better control over year
    permalink=f'/publication/{year}-{publication['author_pub_id'].replace(':','-')}'
    record = PublicationRecord(title=title.replace(':','-'),
                               collection='publications',
                               category='manuscripts',
                               excerpt='',
                               permalink=permalink,
                               date=year,
                               venue= bib.get('journal', '').replace(':','-'), # TODO: why are some journals missing?
                               paperurl=publication['pub_url']
                               )
    publication_path = Path(Path().cwd().parent, '_publications')
    with open(Path(publication_path, f'{year}-{publication['author_pub_id'].replace(':','-')}'), 'w') as f:
        f.write('---\n')
        for key, value in asdict(record).items():
            f.write(f'{key}: {value}\n')
        f.write('---')



