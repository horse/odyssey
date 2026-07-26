#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, unicodedata, urllib.request, xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

SOURCE_URL='https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/master/data/tlg0012/tlg002/tlg0012.tlg002.perseus-grc2.xml'
EXPECTED_SHA='f38f5f238d665eafb9c6878b11283822ed418a07'
EXPECTED_LINES={1:444,2:434,3:497,4:847,5:493,6:331,7:347,8:586,9:566,10:574,11:640,12:453,13:440,14:533,15:557,16:481,17:606,18:428,19:604,20:394,21:434,22:501,23:372,24:548}
TEI='{http://www.tei-c.org/ns/1.0}'
TARGET,MINIMUM,MAXIMUM=6200,3500,8200

@dataclass
class Verse:
    book:int; line:int; text:str; para:bool; quote:Optional[int]

@dataclass
class Atom:
    verses:list[Verse]; kind:str
    @property
    def chars(self): return count_chars(' '.join(v.text for v in self.verses))

def blob_sha(data:bytes)->str:
    return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()

def norm(s:str)->str:
    return re.sub(r'\s+',' ',unicodedata.normalize('NFC',s).replace('\u00a0',' ').replace('\u200b','')).strip()

def count_chars(s:str)->int:
    return sum(1 for c in s if not c.isspace())

def download(path:Path)->str:
    data=urllib.request.urlopen(SOURCE_URL,timeout=120).read()
    sha=blob_sha(data)
    if sha!=EXPECTED_SHA: raise SystemExit(f'Source SHA mismatch: {sha}')
    path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)
    return sha

def parse(path:Path):
    raw=path.read_bytes(); root=ET.fromstring(raw); books={}
    edition=root.find(f'.//{TEI}div[@type="edition"]')
    for b in edition.findall(f'./{TEI}div[@subtype="book"]'):
        bn=int(b.attrib['n']); qids={id(q):i+1 for i,q in enumerate(b.iter(f'{TEI}q'))}; out=[]
        def walk(el,qid=None):
            if el.tag==f'{TEI}q': qid=qids[id(el)]
            if el.tag==f'{TEI}l':
                out.append(Verse(bn,int(el.attrib['n']),norm(''.join(el.itertext())),any(x.tag==f'{TEI}milestone' and x.attrib.get('unit')=='para' for x in el.iter()),qid)); return
            for c in list(el): walk(c,qid)
        walk(b); books[bn]=out
    return books,blob_sha(raw)

def validate(books):
    counts={b:len(vs) for b,vs in sorted(books.items())}
    print(json.dumps({'parsed_books':sorted(books),'per_book_counts':counts,'total_lines':sum(counts.values())},ensure_ascii=False))
    assert sorted(books)==list(range(1,25))
    assert sum(len(v) for v in books.values())==12110
    for b,vs in books.items():
        assert len(vs)==EXPECTED_LINES[b]
        assert [v.line for v in vs]==list(range(1,len(vs)+1))
        assert all(v.text and unicodedata.normalize('NFC',v.text)==v.text and '<' not in v.text for v in vs)

def atoms(vs):
    out=[]; cur=[]; q=None
    def flush():
        nonlocal cur
        if cur: out.append(Atom(cur,'SPEECH' if q else 'NARRATIVE')); cur=[]
    for v in vs:
        if cur and (v.quote!=q or v.para): flush()
        q=v.quote; cur.append(v)
    flush(); return out

def split_atom(a):
    if a.chars<=MAXIMUM:return [a]
    out=[];cur=[];n=0
    for v in a.verses:
        c=count_chars(v.text)
        if cur and n+c>TARGET: out.append(Atom(cur,a.kind+'_CONTINUED'));cur=[];n=0
        cur.append(v);n+=c
    if cur:out.append(Atom(cur,a.kind+'_CONTINUED'))
    return out

def segment(vs):
    aa=[]
    for a in atoms(vs): aa.extend(split_atom(a))
    segs=[];cur=[];n=0
    for a in aa:
        if cur and n+a.chars>MAXIMUM and n>=MINIMUM: segs.append(cur);cur=[];n=0
        cur.append(a);n+=a.chars
        if n>=TARGET:segs.append(cur);cur=[];n=0
    if cur:
        if segs and n<MINIMUM and sum(a.chars for a in segs[-1])+n<=MAXIMUM+700:segs[-1].extend(cur)
        else:segs.append(cur)
    return segs

def main():
    root=Path('source'); original=root/'original'/'odyssey_perseus_grc2.xml'
    sha=download(original); books,sha2=parse(original); assert sha==sha2;validate(books)
    for d in ['books','lines','segments']: (root/d).mkdir(parents=True,exist_ok=True)
    manifest=[]
    for b in range(1,25):
        vs=books[b]
        (root/'lines'/f'book_{b:02d}_lines.tsv').write_text('\n'.join(f'{b}.{v.line}\t{v.text}' for v in vs)+'\n',encoding='utf-8')
        paras=[];cur=[];q=vs[0].quote
        for v in vs:
            if cur and (v.para or v.quote!=q):paras.append(' '.join(cur));cur=[]
            cur.append(v.text);q=v.quote
        if cur:paras.append(' '.join(cur))
        (root/'books'/f'book_{b:02d}_clean.txt').write_text('\n\n'.join(paras)+'\n',encoding='utf-8')
        for i,aa in enumerate(segment(vs),1):
            sv=[v for a in aa for v in a.verses]; sid=f'ODY-B{b:02d}-S{i:02d}'; chars=count_chars(' '.join(v.text for v in sv)); flags='|'.join(sorted({a.kind for a in aa}))
            body='\n'.join(f'[{b}.{v.line}] {v.text}' for v in sv)
            text=f'# {sid}\n\n- SOURCE_URN: urn:cts:greekLit:tlg0012.tlg002.perseus-grc2\n- SOURCE_GIT_BLOB_SHA: {sha}\n- BOOK: {b}\n- LINES: {b}.{sv[0].line}–{b}.{sv[-1].line}\n- GREEK_CHARS_NO_SPACE: {chars}\n- STRUCTURE_FLAGS: {flags}\n- STATUS: SOURCE_READY\n\n## Translation instruction\n\nLine numbers in square brackets are references only. Do not translate them. Translate all Greek content.\n\n## Greek source\n\n{body}\n'
            (root/'segments'/f'{sid}_SOURCE.md').write_text(text,encoding='utf-8')
            manifest.append([sid,b,sv[0].line,sv[-1].line,chars,flags,'SOURCE_READY'])
    header=['segment_id','book','start_line','end_line','greek_chars_no_space','flags','status']
    (root/'manifest.tsv').write_text('\t'.join(header)+'\n'+'\n'.join('\t'.join(map(str,r)) for r in manifest)+'\n',encoding='utf-8')
    info={'source_url':SOURCE_URL,'source_git_blob_sha':sha,'books':24,'verse_lines':12110,'segments':len(manifest),'target_chars':TARGET,'minimum_chars':MINIMUM,'maximum_chars':MAXIMUM}
    (root/'source_build.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (root/'README.md').write_text('# Ready-to-translate Greek source\n\nValidated: 24 books, 12,110 lines. Upload only the current book’s `segments/ODY-Bxx-*` files into a ChatGPT Project.\n',encoding='utf-8')
    print(json.dumps(info,ensure_ascii=False))
if __name__=='__main__':main()

# Workflow trigger: source build v1.0
