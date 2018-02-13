################################################################################
#
# Watchcartoon Plex Channel
#
################################################################################


################################################################################
# Defining resources
TITLE = "Watch Cartoon"
PREFIX = "/video/watchcartoon"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_LIST = "icon-list.png"
ICON_NEXT = "icon-next.png"
ICON_COVER = "icon-cover.png"
ICON_SEARCH = "icon-search.png"
ICON_QUEUE = "icon-queue.png"
ICON_PREFS = "icon-prefs.png"
BASE_URL = "https://www.watchcartoononline.io"
ICON_NUM = "icon-num.png"
ICON_A = "icon-a.png"
ICON_B = "icon-b.png"
ICON_C = "icon-c.png"
ICON_D = "icon-d.png"
ICON_E = "icon-e.png"
ICON_F = "icon-f.png"
ICON_G = "icon-g.png"
ICON_H = "icon-h.png"
ICON_I = "icon-i.png"
ICON_J = "icon-j.png"
ICON_K = "icon-k.png"
ICON_L = "icon-l.png"
ICON_M = "icon-m.png"
ICON_N = "icon-n.png"
ICON_O = "icon-o.png"
ICON_P = "icon-p.png"
ICON_Q = "icon-q.png"
ICON_R = "icon-r.png"
ICON_S = "icon-s.png"
ICON_T = "icon-t.png"
ICON_U = "icon-u.png"
ICON_V = "icon-v.png"
ICON_W = "icon-w.png"
ICON_X = "icon-x.png"
ICON_Y = "icon-y.png"
ICON_Z = "icon-z.png"

################################################################################
# Array for catergories
letters = [
    "#","A","B","C","D","E","F","G","H",
    "I","J","K","L","M","N","O","P","Q",
    "R","S","T","U","V","W","X","Y","Z"
]
icons = [
    ICON_NUM,ICON_A,ICON_B,ICON_C,ICON_D,ICON_E,ICON_F,ICON_G,ICON_H,
    ICON_I,ICON_J,ICON_K,ICON_L,ICON_M,ICON_N,ICON_O,ICON_P,ICON_Q,
    ICON_R,ICON_S,ICON_T,ICON_U,ICON_V,ICON_W,ICON_X,ICON_Y,ICON_Z
]


def Start():
    """Set global variables"""

    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)

    VideoClipObject.thumb = R(ICON_COVER)
    VideoClipObject.art = R(ART)    

    HTTP.CacheTime = CACHE_1HOUR
    HTTP.Headers['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:22.0) Gecko/20100101 Firefox/51.0'

    Log("Watch Cartoon Starting")


@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():
    """Params page_count & offset are used for paginating results and should not be changed"""

    oc = ObjectContainer()

    oc.add(
        DirectoryObject(
            key = Callback(SplitCategory, category = "dubbed-anime-list"),
            title = "Dubbed Anime",
            thumb = R(ICON_LIST)
        )
    )

    oc.add(
        DirectoryObject(
            key = Callback(SplitCategory, category = "cartoon-list"),
            title = "Cartoon",
            thumb = R(ICON_LIST)
        )
    )

    oc.add(
        DirectoryObject(
            key = Callback(SplitCategory, category = "subbed-anime-list"),
            title = "Subbed Anime",
            thumb = R(ICON_LIST)
        )
    )

    oc.add(
        DirectoryObject(
            key = Callback(SplitCategory, category = "movie-list"),
            title = "Movie",
            thumb = R(ICON_LIST)
        )
    )

    oc.add(
        DirectoryObject(
            key = Callback(SplitCategory, category = "ova-list"),
            title = "Ova",
            thumb = R(ICON_LIST)
        )
    )

    oc.add(
        DirectoryObject(
            key = Callback(RecentEpisodes),
            title = "Recent Episodes",
            thumb = R(ICON_LIST)
        )
    )

    oc.add(
        DirectoryObject(
            key = Callback(Bookmarks),
            title = "Bookmarks",
            thumb = R(ICON_QUEUE)
        )
    )

    oc.add(PrefsObject(title = "Settings", thumb = R(ICON_PREFS)))

    return oc


def CategoryDataFromCategorySlug(category_slug):
    """Central place to get category data"""

    return {
        'dubbed-anime-list': {
            'title': 'Dubbed Anime',
            'ova': False,
            'thumb': R(ICON_LIST),
            'prefix': '/anime'
        },

        'cartoon-list': {
            'title': 'Cartoon',
            'ova': False,
            'thumb': R(ICON_LIST),
            'prefix': '/anime'
        },

        'subbed-anime-list': {
            'title': 'Subbed Anime',
            'ova': False,
            'thumb': R(ICON_LIST),
            'prefix': '/anime'
        },

        'movie-list': {
            'title': 'Movie',
            'ova': False,
            'thumb': R(ICON_LIST),
            'prefix': ''
        },

        'ova-list': {
            'title': 'OVA',
            'ova': True,
            'thumb': R(ICON_LIST),
            'prefix': ''
        },

        'recent-list': {
            'title': 'Recent Episodes',
            'thumb': R(ICON_LIST)
        },

        'bookmarks-list': {
            'title': 'Bookmarks',
            'thumb': R(ICON_QUEUE)
        }
    }[category_slug]


@route(PREFIX + "/list/{category}")
def SplitCategory(category):
    """Splits Shows and OVA groupings by first letter"""

    category_data = CategoryDataFromCategorySlug(category)

    oc = ObjectContainer(title1 = category_data['title'])

    if category_data['ova'] == True:
        cb = ShowCategoryOVA
    else:
        cb = ShowCategory

    for l in xrange(0,27):
        oc.add(
            DirectoryObject(
                key = Callback(cb, category = category, letter = l),
                title = letters[l],
                thumb = R(icons[l])
            )
        )
    return oc


@route(PREFIX + "/recent")
def RecentEpisodes():
    """Loops over episode list"""

    page_data = HTML.ElementFromURL(BASE_URL)
    eps_list = page_data.xpath("//div[@class='mansetlisteleme']/ul/li/a")
    oc = ObjectContainer(title1 = "Recent Episodes")

    for each in eps_list:
        try:
            oc.add(
                EpisodeObject(
                    url = each.xpath("./@href")[0],
                    title = FixString(each.xpath("./text()")[0])
                )
            )
        except:
            Log("Episode error")
            continue

    return oc


@route(PREFIX + "/bookmarks")
def Bookmarks():
    """Directory for bookmarks"""
    oc = ObjectContainer(title1 = "Bookmarks")
    keys = list(Dict)
    keys.sort(key=str.lower)
    for each in keys:
        oc.add(GetShow(show_title = each, show_url = Dict[each]))
    return oc


@route(PREFIX + "/show-category-ova/{category}/{letter}")
def ShowCategoryOVA(category, letter):
    """Get shows starting with specific character for OVA and Movies"""

    category_data = CategoryDataFromCategorySlug(category)
    letter = int(letter)

    page_data = HTML.ElementFromURL(BASE_URL + "/" + str(category))
    table_data = page_data.xpath("//div[@class='ddmcc']/ul/ul/li/a")

    oc = ObjectContainer(title1 = category_data['title'] + ' - ' + letters[letter])

    if len(table_data)==0:
        table_data = page_data.xpath("//div[@class='ddmcc']/ul/li/a")

    Log("table_data len: " + str(len(table_data)))

    for each in table_data:
        try:
            show_slug = each.xpath("./@href")[0].replace(BASE_URL + category_data['prefix'] + '/', '')
            show_title = FixString(each.xpath("./text()")[0])
        except:
            continue

        isAlpha = letter != 0 and show_title[0:1].upper() == letters[letter]
        isSpecial = letter == 0 and show_title[0:1].isalpha() == False

        if isAlpha or isSpecial:
            episode = GetEpisode(category = category, show_slug = "", episode_slug = show_slug, get_data = False)
            episode.title = show_title
            oc.add(episode)

    if len(oc) < 1:
        Log ("No Shows")
        return ObjectContainer(header="Error", message="No Shows/Movies found for " + letters[letter])

    return oc


@route(PREFIX + "/show-category/{category}/{letter}")
def ShowCategory(category, letter):
    """Get shows starting with specific character"""

    category_data = CategoryDataFromCategorySlug(category)
    letter = int(letter)

    oc = ObjectContainer(title1 = category_data['title'])

    page_data = HTML.ElementFromURL(BASE_URL + "/" + str(category))
    table_data = page_data.xpath("//div[@class='ddmcc']/ul/ul/li/a")

    if len(table_data) == 0:
        table_data = page_data.xpath("//div[@class='ddmcc']/ul/li/a")

    Log("table_data len: " + str(len(table_data)))

    if category_data['prefix'] == "":
        is_direct = True
    else:
        is_direct = False

    for each in table_data:
        try:
            show_slug = each.xpath("./@href")[0].replace(BASE_URL + category_data['prefix'] + '/', '')
            show_title = FixString(each.xpath("./text()")[0])
        except Exception as ex:
            continue

        isAlpha = letter != 0 and show_title[0:1].upper() == letters[letter]

        isSpecial = letter == 0 and show_title[0:1].isalpha() == False

        if isAlpha or isSpecial:
            if is_direct:
                episode = GetEpisode(category = category, show_slug = "", episode_slug = show_slug, get_data = False)
                episode.title = show_title
                oc.add(episode)
            else:
                oc.add(
                    DirectoryObject(
                        key = Callback(GetShow, category = category, show_slug = show_slug),
                        title = show_title,
                        thumb = R(ICON_COVER)
                    )
                )

    if len(oc) < 1:
        Log ("No Shows")
        return ObjectContainer(header="Error", message="No Shows/Movies found for " + letters[letter])
    
    return oc


def PageEpisodes(container, page_data, category, show_slug):
    """Breaks episodes up into groups of 25"""

    eps_list = page_data.xpath("//div[@class='menustyle']/li/a")
    eps_cnt = len(eps_list)
    oc = container

    pageLength = int(float(Prefs['pageLength']))

    ep_rem = eps_cnt % pageLength
    pages_cnt = (eps_cnt - ep_rem) / pageLength

    if ep_rem > 0:
        pages_cnt = pages_cnt + 1

    reverse = Prefs['ReverseOrder']

    for x in xrange(1, pages_cnt + 1):
        start_ep = (x - 1) * pageLength
        end_ep = (x * pageLength)
        if reverse == False:
            start_ep = eps_cnt - start_ep
            end_ep = eps_cnt - end_ep
        if end_ep <= 0 :
            end_ep = 1
        if end_ep > eps_cnt:
            end_ep = eps_cnt
        oc.add(
            DirectoryObject(
                key = Callback(
                    ListEps,
                    category = category,
                    show_slug = show_slug,
                    estart = (x - 1) * pageLength,
                    ecnt = pageLength),
                title = str(start_ep + 1) + " to " + str(end_ep)
            )
        )

    return oc

@route(PREFIX + "/list-episodes/{category}/{show_slug}/{estart}/{ecnt}")
def ListEps(category, show_slug, estart, ecnt):
    """Loops over episode list within a given range"""

    estart = int(estart)
    ecnt = int(ecnt)

    category_data = CategoryDataFromCategorySlug(category)

    show_url = BASE_URL + category_data['prefix'] + '/' + show_slug

    page_data = HTML.ElementFromURL(show_url)
    eps_list = page_data.xpath("//div[@class='menustyle']/li/a")

    show_title = GetShowTitleFromPage(page_data)

    oc = ObjectContainer(title1 = show_title)

    episode_list = list(doReverse(eps_list))
    eend = estart + ecnt
    episode_list = episode_list[estart:eend]

    for each in episode_list:
        try:
            episode_slug = each.xpath("./@href")[0].replace(BASE_URL + '/', '')
            episode_title = FixString(each.xpath("./text()")[0])
        except:
            continue

        episode = GetEpisode(category = category, show_slug = show_slug, episode_slug = episode_slug, get_data = False)
        episode.title = episode_title

        oc.add(episode)

    if len(oc) <= 1:
        Log ("No Episodes")
        return ObjectContainer(header="Error", message="Something has gone wrong.")    

    return oc


def GetEpisode(category, show_slug, episode_slug, get_data = True):
    """Collects metadata from ep_url and returns EpisodeObject"""

    Log("GetEpisode")

    episode_url = BASE_URL + '/' + episode_slug

    episode_title = ""
    episode_thumb = R(ICON_COVER)
    episode_summary = ""

    if get_data:
        # Get Episodes Thumbnail and Summary
        ep_page_data = HTML.ElementFromURL(episode_url)

        episode_title = GetEpisodeTitleFromPage(ep_page_data)

        try:
            episode_thumb = ep_page_data.xpath("//link[@rel='image_src']/@href")[0]
        except:
            episode_thumb = R(ICON_COVER)

        try:
            ep_description = ep_page_data.xpath("//meta[@name='description']/@content")[0]
            ep_description = FixString(ep_description)

            episode_summary = HTML.StringFromElement(ep_page_data.xpath("//div[@class='iltext']/p")[0])
            episode_summary = String.StripTags(episode_summary)
            episode_summary = episode_summary.splitlines()[0]
            episode_summary = FixString(episode_summary)
            episode_summary = episode_summary.replace(ep_description, "")
        except:
            episode_summary = "???"

    return EpisodeObject(
        url = episode_url,
        title = episode_title,
        thumb = episode_thumb,
        summary = episode_summary
    )

def GetEpisodeTitleFromPage(page_data):
    title_element = page_data.xpath("//h1/a/text()")

    if len(title_element) > 0:
        episode_title = FixString(title_element[0])
    else:
        Log("No title!")
        episode_title = ""

    return episode_title

def GetShowTitleFromPage(page_data):
    title_element = page_data.xpath("//h2[1]/text()")

    if len(title_element) > 0:
        show_title = FixString(title_element[0])
    else:
        Log("No title!")
        show_title = ""

    return show_title

@route(PREFIX + "/get-show/{category}/{show_slug}")
def GetShow(category, show_slug):
    """Collects metadata from show_url and returns DirectoryObject"""

    category_data = CategoryDataFromCategorySlug(category)

    show_url = BASE_URL + category_data['prefix'] + '/' + show_slug

    show_page_data = HTML.ElementFromURL(show_url)

    try:
        show_title = GetShowTitleFromPage(show_page_data)
    except Exception, e:
        Log(str(e))
        show_title = ""

    try:
        show_thumb = show_page_data.xpath("//div[@class='katcont'][1]/div[1]/img[1]/@src")[0]
    except:
        show_thumb = R(ICON_COVER)

    try:
        show_summary = FixString(show_page_data.xpath("//div[@class='iltext']/p[1]/text()")[0])
    except:
        show_summary = ""

    oc = ObjectContainer(
        title1 = show_title
    )

    return PageEpisodes(container = oc, page_data = show_page_data, category = category, show_slug = show_slug)

def FixString(str):
    """Removes weird Characters from string"""

    str = str.encode('ascii', 'xmlcharrefreplace')
    str = String.Unquote(str)
    str = str.replace("&amp;","&")
    str = str.replace("&#8211;","-")
    str = str.replace("&#8217;","'")
    return str

def doReverse(list):
    """Reverse list on condition"""

    reverse = Prefs['ReverseOrder']

    if reverse == True:
        return reversed(list)

    return list

def EditBookmark(show_title, show_url):
    """Adds or removes bookmark from dictionary"""

    if show_title in Dict:
        del Dict[show_title]
        Dict.Save()
        oc = ObjectContainer(
            header = show_title,
            message = 'This show has been removed from your bookmarks.'
        )

    else:
        Dict[show_title] = show_url
        Dict.Save()
        oc = ObjectContainer(
            header = show_title,
            message = 'This show has been added to your bookmarks.'
        )

    return oc;

    

