import xml.dom.minidom as Dom

collection = Dom.parse('Record.xml').documentElement

movies = collection.getElementsByTagName('movie')

for movie in movies:
    print('***Movie***')
    if movie.hasAttribute('name'):
        print('Title: %s'%(movie.getAttribute('name')))
    type = movie.getElementsByTagName('type')[0]
    print('Type: %s'%(type.childNodes[0].data))
    main = movie.getElementsByTagName('main')[0]
    print('Main: %s' % (main.childNodes[0].data))