SLOW_URLS = [
    "https://bibliotek.solna.se/documents/334872/562522/Biblioteksplan_2017-2023_rev2020.pdf/60583013-1963-ce7f-5e3d-da7c9af7f730"
]

TIME_OUT_ERROR = [
    "https://biblioteket.stockholm.se/sites/default/files/bq_kufv059_biblioteksplan_remissversion_ta_pf.pdf"
]

# URLs where the link was broken or no PDF could be found
BLACKLISTED = [
    # Varberg - Chrome extention and non existing
    "chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/viewer.html?pdfurl=https%3A%2F%2Fwww.varbergsbibliotek.se%2Fdocuments%2F91678%2F897915%2FBiblioteksplan%2B2021.pdf%2F48e725ce-a2b9-7c73-2fa4-62484b7def0f&clen=225059",
    # Ale
    "https://ale.se/kultur--fritid/bibliotek/biblioteksplan.html",
    # Motala: TODO:
    "https://www.motala.se/media/uploads/Biblioteksplan-Motala-bibliotek-2020-2023.pdf",
    # Gagnef
    "https://gagnef.se/media/5703/9_biblioteksplan.pdf",
    # Timrå
    "http://web005.timra.se/contentassets/a459ee809e364ed882c2a1bb8e4f4684/kt30a.pdf",
    # Gellivare
    "https://cdn1.bibblo.se/files/5c18ca973ae44011e03ac841/G%C3%A4llivare%20kommuns%20biblioteksplan%20reviderad.pdf",
    # Haparanda
    "https://cdn1.bibblo.se/files/5d6d726e3ae44003e0b64966/Biblioteksplan%20f%C3%B6r",
    # Övrekalix
    "https://cdn2.bibblo.se/files/600ffc443ae44005e476962a/%C3%96verkalix%20Biblioteksplan%202021-2024.pdf"
    # Norrbotten
    "https://cdn1.bibblo.se/files/5d6d726e3ae44003e0b64966/Biblioteksplan",
    "https://cdn1.bibblo.se/files/5d6d726e3ae44003e0b64966/Biblioteksplan f%C3%B6r",
    # Arvidsjaur
    "https://www.bibblo.se/sv/library-page/arvidsjaur",
    # Kiruna
    "https://www.bibblo.se/sv/library-page/kiruna-stadsbibliotek",
]


# TODO: Left out for now
# Needs to be converted to PDFs from plain text on the webpage
MANUAL_TO_PDF = [
    "https://www.lidingo.se/biblioteket/stadsbiblioteket/sidfotslankarbibliotek/ombiblioteket/biblioteksplan20202023.4.320bcf2c17475aecd831a11.html",
    "https://www.alvkarleby.se/kommun-och-politik/planer-och-styrdokument/styrdokument.html",
    "https://www.askersund.se/uppleva-och-gora/bibliotek/biblioteksplan-for-askersunds-kommun.html#.Xy1ROTEzZaQ",
    "https://bibliotek.hogsby.se/web/arena/biblioteksplanen",
    "https://bibliotek.ludvika.se/sv/content-page/biblioteksplanen",
    "https://hudiksvall.se/Sidor/Kommun--politik/Styrdokument-och-planer---Forfattningssamling/Policy-riktlinjer-och-planer/Biblioteksplan-2021-2024.html",
    "https://www.arvika.se/kommunochpolitik/planerochstyrdokument/forfattningssamling/internariktlinjer/biblioteksplan.4.6b51ef5c153add4207dbba9e.html",
]


# TODO: Left out for now
# Needs to be converted from '.docx' to '.pdf'
DOCX_TO_PDF = {
    "https://www.v8biblioteken.se/biblioteksplan-2019?culture=sv": "https://cdn3.v8biblioteken.se/files/5f83ff29a89be511806fc36d/Biblioteksplan%20f%C3%B6r%20Storumans%20kommun%202020-2023%20(fastst%C3%A4lld%20KF_2020-09-15%20%C2%A7%20112)-%7BD3A8E55F-9C0B-48F7-9FD6-883DC2674A4A%7D.docx",
    # Cant for Arjang
    "https://arjang.se/Documents/Uppleva_gora/Maries mapp/Biblioteksplan f%c3%b6r %c3%85rj%c3%a4ngs kommun 2019 f%c3%b6r l%c3%a4nkning.docx?epslanguage=sv": "https://arjang.se/Documents/Uppleva_gora/Maries%20mapp/Biblioteksplan%20f%C3%B6r%20%C3%85rj%C3%A4ngs%20kommun%202019%20f%C3%B6r%20l%C3%A4nkning.docx?epslanguage=sv",
    "https://www.pajala.se/foreningsliv-fritid-kultur/biblioteken-i-pajala-kommun/": "https://www.pajala.se/media/jcylao53/biblioteksplan-2021-2023.docx",
}


# URLs that were not the same as those listed in the original url
# Either because the urls were wrong or moved.
# Others were hosted with a ling on the website and could be downloaded from there
# And even some were embedded on the site, requiring proving you are not a bot to download
# Docreader and docplayer has buttons where you could do this automatically also
REMAPPED_URLS = {
    # Was wrong and manually found correct addresses
    "https://bibliotek.uddevalla.se/documents/6143439/6155827/Biblioteksplan+2016-2020/030b6696-47d5-4447-b951-b7a0dac411c9": "https://docplayer.se/storage/39/18186353/1649686463/xvPiwr-dkidv94OrKveQWw/18186353.pdf",
    "https://enkoping.se/fritid-och-kultur/kultur-och-nojen/bibliotek/biblioteksplan-2018-2021.html#h-Lashelarapporten": "https://docplayer.se/storage/91/104941384/1649702095/98YJ6bXaJQj6Oo5Lipc8oQ/104941384.pdf",
    # Had PDF on website
    "https://bibliotek.trelleborg.se/web/arena/biblioteksplaner": "https://bibliotek.trelleborg.se/documents/345753/502295/Biblioteksplan+2018+-+2021.pdf/0411d187-1ee6-9573-e043-a7df44d7a1e6",
    "https://bibliotek.oskarshamn.se/documents/243765/0/Biblioteksplan+2016-2020.pdf/ab38e2c4-7f8e-4449-a612-454c10700402": "https://bibliotek.oskarshamn.se/documents/21230/215026/Remissf%C3%B6rslag+-+Oskarshamns+kommuns+Biblioteksplan+2021-2025.pdf/642f11a4-2309-7393-cff5-736ee0d70817",
    "https://bibliotek.ekero.se/sv/content-page/biblioteksplan-2019-2023": "https://cdn2.bibliotek.ekero.se/files/5d5d083044999313c44738d4/Biblioteksplan%20%202019-2023.pdf",
    "https://bibliotek.sundbyberg.se/sv/content-page/biblioteksplan": "https://cdn2.bibliotek.sundbyberg.se/files/5d887fd1ccb1d612301d1ef1/Biblioteksplan%202019-2023.PDF",
    "https://bibliotek.emmaboda.se/sv/content-page/biblioteksplan": "https://cdn2.bibliotek.emmaboda.se/files/5d380e7b98f06f11187b9025/Utskriftsv%C3%A4nlig%20version%20av%20Emmaboda%20biblioteksplan.pdf",
    "https://bibliotek.kavlinge.se/sv/content-page/biblioteksplan": "https://bibliotek.kavlinge.se/documents/313599/0/Biblioteksplan+2020+-+2023.pdf/9fcb0df5-cf2d-05f1-5514-94d01dbff02e",
    "https://www.bibliotek.trollhattan.se/biblioteksplan": "https://www.bibliotek.trollhattan.se/documents/6579176/6664807/G%C3%A4llande_Rev_Biblplan_20191107.pdf/955274e3-c0b3-8548-545f-15a53250149a",
    "https://bibliotek.avesta.se/styrdokument?refId=JQFb4R&culture=sv": "https://cdn2.bibliotek.avesta.se/files/60250098225ebb1230abe7a6/Biblioteksplan%20Avesta%20kommun.pdf",
    "https://docreader.readspeaker.com/docreader/?jsmode=1&cid=bpzos&lang=en_us&url=https%3A%2F%2Fwww.norrbotten.se%2Fpublika%2Fku%2Fnblb%2FBiblioteksplaner%2FBiblioteksplan%2520Boden%25202016-2020.pdf&v=Google%20Inc": "https://www.norrbotten.se/publika/ku/nblb/Biblioteksplaner/Biblioteksplan%20Boden%202016-2020.pdf",
    "https://docreader.readspeaker.com/docreader/?jsmode=1&cid=bpzos&lang=en_us&url=https%3A%2F%2Fwww.norrbotten.se%2Fpublika%2Fku%2Fnblb%2FBiblioteksplaner%2F%25c3%2584lvsbyns%2520biblioteksplan%25202018-2021.pdf&v=Google%20Inc": "https://www.norrbotten.se/publika/ku/nblb/Biblioteksplaner/%c3%84lvsbyns%20biblioteksplan%202018-2021.pdf",
    "https://docreader.readspeaker.com/docreader/?jsmode=1&cid=bpzos&lang=en_us&url=https%3A%2F%2Fwww.norrbotten.se%2Fpublika%2Fku%2Fnblb%2FBiblioteksplaner%2FLule%25c3%25a5%2520biblioteksplan%25202016-2020.pdf&v=Google%20Inc": "https://www.norrbotten.se/publika/ku/nblb/Biblioteksplaner/Lule%c3%a5%20biblioteksplan%202016-2020.pdf",
    # Has PDF behind wall
}

TODO_LIST = {
    "https://docplayer.se/112435407-Biblioteksplan-for-vaxholms-stad.html": "https://www.vaxholm.se/download/18.56fc80391773f590b4652f30/1613728613852/Biblioteksplan%20f%C3%B6r%20Vaxholms%20stad%202019-2022.pdf",
    "https://docplayer.se/185199940-Biblioteksplan-kalix-kommun-fritids-och-kulturnamnden.html": "https://docplayer.se/storage/108/185199940/1649702766/BIUXuzXQSFluDVBvBpY9Ow/185199940.pdf",
    "http://docplayer.se/187996605-Biblioteksplan-faststalld-av-kommunfullmaktige.html": "http://docplayer.se/storage/109/187996605/1633441604/Ris2JIuGk_TF5fuZMWZPQg/187996605.pdf",
    "https://docplayer.se/49725430-Biblioteksplan-for-lycksele-kommun-biblioteksplanen-skall-ligga-till-grund-for-biblioteksverksamheten-i-kommunen-under-aren.html": "https://docplayer.se/storage/63/49725430/1633441634/uwyCYpf2F0i65VDrqsomlA/49725430.pdf",
    "https://docplayer.se/107039276-Biblioteksplan-for-are-kommuns-biblioteksverksamhet.html": "https://docplayer.se/storage/91/107039276/1633441655/OZ85loxW0DukFNzOUVj7PQ/107039276.pdf",
    "https://docplayer.se/201317420-Biblioteksplan.html": "https://docplayer.se/storage/112/201317420/1633441676/msqrf6ZrFmWIAmbRgl8-ng/201317420.pdf",
    "https://docplayer.se/106226986-Biblioteksplan-for-hofors-kommun.html": "https://docplayer.se/storage/91/106226986/1633441702/N1TUcYbwC2kCj99hK5coPw/106226986.pdf",
    "https://docplayer.se/108059098-Biblioteksplan-for-laxa-kommun-antagen-av-kommunfullmaktige-84-dnr-ks.html": "https://docplayer.se/storage/92/108059098/1633441719/t-uvk8O6FCxTJ7gHRE3r7A/108059098.pdf",
    "https://docplayer.se/161950090-Biblioteksplan.html": "https://docplayer.se/storage/104/161950090/1633441741/koqR7uIrhcoMM2iT3pyNOg/161950090.pdf",
    "https://docplayer.se/116376929-Biblioteksplan-for-bollebygds-kommun.html": "https://docplayer.se/storage/88/116376929/1633441761/se6q2O5JjBKxPFadPo4I1w/116376929.pdf",
    "https://docplayer.se/107519986-Program-for-biblioteksverksamheten-i-tranas-kommun.html": "https://docplayer.se/storage/91/107519986/1633441776/_AhSpiuAbc0x-GcaF_D0jw/107519986.pdf",
    "http://docplayer.se/137273485-Biblioteksplan-mullsjo-kommun.html": "http://docplayer.se/storage/98/137273485/1633441794/idJ1CwXGZdKVg15PLS9txA/137273485.pdf",
    "http://docplayer.se/116733712-Biblioteksplan.html": "http://docplayer.se/storage/88/116733712/1633441834/XmPLvWxxWj2JfRAXXPy2qA/116733712.pdf",
    "https://docplayer.se/112435407-Biblioteksplan-for-vaxholms-stad.html": "https://docplayer.se/storage/93/112435407/1633357311/63YoXkL_THpWLLb8jQcynQ/112435407.pdf",
    "http://docplayer.se/116733712-Biblioteksplan.html": "http://docplayer.se/storage/88/116733712/1633357461/eYCWw5PfNxL8rHVi2n3lsA/116733712.pdf",
    "http://docplayer.se/137273485-Biblioteksplan-mullsjo-kommun.html": "http://docplayer.se/storage/98/137273485/1633357515/l6LJK4eHvFXVhpNXbjr0pQ/137273485.pdf",
    "https://docplayer.se/107519986-Program-for-biblioteksverksamheten-i-tranas-kommun.html": "https://docplayer.se/storage/91/107519986/1633357566/b8BvQqEld27nNqRR6SjPZw/107519986.pdf",
    "https://docplayer.se/116376929-Biblioteksplan-for-bollebygds-kommun.html": "https://docplayer.se/storage/88/116376929/1633357585/u2DMEA461JEPK3afcjbjbg/116376929.pdf",
    "https://docplayer.se/161950090-Biblioteksplan.html": "https://docplayer.se/161950090-Biblioteksplan.html",
    "https://docplayer.se/108059098-Biblioteksplan-for-laxa-kommun-antagen-av-kommunfullmaktige-84-dnr-ks.html": "https://docplayer.se/storage/92/108059098/1633357652/MILbPcyoMzrMME_HhwbyhA/108059098.pdf",
    "https://docplayer.se/201317420-Biblioteksplan.html": "https://docplayer.se/storage/112/201317420/1633357689/DUbdP274Cp2pFkvhg_7gJg/201317420.pdf",
    "https://docplayer.se/107039276-Biblioteksplan-for-are-kommuns-biblioteksverksamhet.html": "https://docplayer.se/107039276-Biblioteksplan-for-are-kommuns-biblioteksverksamhet.html",
    "https://docplayer.se/106226986-Biblioteksplan-for-hofors-kommun.html": "https://docplayer.se/storage/91/106226986/1633357760/DaSo3jmlEEu7vED1Na7WRg/106226986.pdf",
    "https://docplayer.se/49725430-Biblioteksplan-for-lycksele-kommun-biblioteksplanen-skall-ligga-till-grund-for-biblioteksverksamheten-i-kommunen-under-aren.html": "https://docplayer.se/storage/63/49725430/1633360038/QKepVl9aN4iOPCWnrLft2A/49725430.pdf",
    "http://docplayer.se/187996605-Biblioteksplan-faststalld-av-kommunfullmaktige.html": "http://docplayer.se/187996605-Biblioteksplan-faststalld-av-kommunfullmaktige.html",
    "https://docplayer.se/185199940-Biblioteksplan-kalix-kommun-fritids-och-kulturnamnden.html": "https://docplayer.se/storage/108/185199940/1633357821/s8KAoFpNvrJORG4TVBtENw/185199940.pdf",
    "https://docplayer.se/104941384-Biblioteksplan-vi-gor-det-tillsammans.html": "https://docplayer.se/storage/91/104941384/1633357834/7sZtpRvYaWCkTk8XGj0dng/104941384.pdf",
    "https://www.katrineholm.se/download/18.4e9c1505166c1878a4018f23/1547105282958/Biblioteksplan%20f%C3%B6r%20Katrineholms%20kommun%202018-2020.pdf": "https://www.katrineholm.se/download/18.182147b917c11a6636819544/1632827260929/Biblioteksplan%20f%C3%B6r%20Katrineholms%20kommun%20KF%202021-09-20.pdf",
    "https://enkoping.se/fritid-och-kultur/kultur-och-nojen/bibliotek/biblioteksplan-2018-2021.html#h-Lashelarapporten": "https://enkoping.se/download/18.5bc623f717f448bad9b2d5f7/1646291539907/plan-upn-langsiktig-2020-2023.pdf",
    "https://www.molndal.se/download/18.5016043e176f179bccc9a8d/1610609863122/Biblioteksplan%20M%C3%B6lndal%202020%20-%202023.pdf": "https://www.molndal.se/download/18.5400bf4417be432a11a3840/1631694816763/biblioteksplan%202020-2023.pdf",
    "https://sunne.se/globalassets/upload/styrdokument/program-och-planer/biblioteksplan.pdf": "https://sunne.se/globalassets/upload/politik-och-medborgardialog/kallelser-och-handlingar/2020/kommunstyrelsen/201201/28-regional-biblioteksplan-20212024---remiss.pdf",
    "https://www.lerum.se/globalassets/documents/forvaltningssidorna/uppleva-och-gora/bibliotek/fakta-och-info/biblioteksplan-for-lerums-kommun-2019-2022.pdf": "https://docplayer.se/storage/105/166390312/1649686677/E_IL7IJqg-EoxM7EqyeKtw/166390312.pdf",
    "https://cdn2.bibblo.se/files/600ffc443ae44005e476962a/%C3%96verkalix%20Biblioteksplan%202021-2024.pdf": "https://cdn1.bibblo.openlib.se/files/600ffc443ae44005e476962a/%C3%96verkalix%20Biblioteksplan%202021-2024.pdf",
    "https://docreader.readspeaker.com/docreader/?cid=bpzos&lang=en_us&url=https%3A%2F%2Fwww.norrbotten.se%2Fpublika%2Fku%2Fnblb%2FBiblioteksplaner%2F%25c3%2584lvsbyns%2520biblioteksplan%25202018-2021.pdf": "https://www.norrbotten.se/publika/ku/nblb/Biblioteksplaner/%c3%84lvsbyns%20biblioteksplan%202018-2021.pdf",
}
