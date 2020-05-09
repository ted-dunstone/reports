from px_build_doc.util import WikipediaManager,fetch_query
from px_build_doc.image_util import build_cover, get_font, read_image

# an example that can be used with build cover
def test_draw(img,d,text=["title","subtitle"],
                locations=[(100,850),(100,900)],
                sizes=[50,20],
                colour=(255,255,255,255)):
    #for txt,loc,size in zip(text,locations,sizes):
    #    d.text(loc, txt, font=get_font(size), fill=colour)
    return
    images = [im for im in WikipediaManager().query(
        #fetch_query()
        "mastercard"
    ).images() if not im.endswith('svg')]
    url = images[1]
    url = 'https://unaavictoria.org.au/wp-content/uploads/2016/08/DFAT-logo.jpg'
    #url = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fsharedvalue.org.au%2Fprofiles%2Fdfat%2F&psig=AOvVaw0aPEl_e3z6EE9N48yMTh7i&ust=1582768657746000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMj8mu-O7ucCFQAAAAAdAAAAABAI'
    rim=read_image(url,(300,300))
    img.paste(rim, (500,80))

#build_cover('base_cover.png',test_draw)