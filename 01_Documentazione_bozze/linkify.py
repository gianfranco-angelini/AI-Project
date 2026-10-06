"""Rende cliccabili i run il cui testo è esattamente un URL http(s), dopo S.scrivi."""
import re, zipfile, shutil, os, html

def linkify(path, colore="757F9B"):
    tmp = path + ".tmp"
    zin = zipfile.ZipFile(path)
    doc = zin.read("word/document.xml").decode("utf-8")
    rels = zin.read("word/_rels/document.xml.rels").decode("utf-8")
    urls = {}
    def sost(m):
        rpr, testo = m.group(1) or "", m.group(2)
        url = html.unescape(testo)
        rid = urls.setdefault(url, "rIdLink%d" % (len(urls) + 1))
        rpr = rpr.replace("</w:rPr>", '<w:color w:val="%s"/><w:u w:val="single"/></w:rPr>' % colore) if rpr else \
            '<w:rPr><w:color w:val="%s"/><w:u w:val="single"/></w:rPr>' % colore
        rpr = re.sub(r'<w:color w:val="[0-9A-Fa-f]{6}"/>(?=.*<w:color)', '', rpr, count=1)
        return '<w:hyperlink r:id="%s" w:history="1"><w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:hyperlink>' % (rid, rpr, testo)
    doc = re.sub(r'<w:r>(<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)?<w:t(?: xml:space="preserve")?>(https?://[^<\s]+)</w:t></w:r>', sost, doc)
    nuove = "".join('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="%s" TargetMode="External"/>'
                    % (rid, html.escape(u, quote=True)) for u, rid in urls.items())
    rels = rels.replace("</Relationships>", nuove + "</Relationships>")
    zout = zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED)
    for it in zin.infolist():
        dati = zin.read(it.filename)
        if it.filename == "word/document.xml":
            dati = doc.encode("utf-8")
        elif it.filename == "word/_rels/document.xml.rels":
            dati = rels.encode("utf-8")
        zout.writestr(it, dati)
    zout.close(); zin.close()
    shutil.move(tmp, path)
    return len(urls)
