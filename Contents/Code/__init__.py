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
BASE_URL = "http://www.watchcartoononline.io"
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

################################################################################
# Set global variables
def Start():
	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_COVER)
	VideoClipObject.art = R(ART)	
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0'
	Log("Watch Cartoon Starting")

################################################################################
# Params page_count & offset are used for paginating results and should not be changed
@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():
	oc = ObjectContainer()
	oc.add(DirectoryObject(key = Callback(SplitCategory, title="Dubbed Anime", category = "/dubbed-anime-list",ova=False), title = "Dubbed Anime", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(SplitCategory, title="Cartoon", category = "/cartoon-list",ova=False), title = "Cartoon", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(SplitCategory, title="Subbed Anime", category = "/subbed-anime-list",ova=False), title = "Subbed Anime", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(SplitCategory, title="Movie", category = "/movie-list",ova=True), title = "Movie", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(SplitCategory, title="Ova", category = "/ova-list",ova=True), title = "Ova", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(RecentEpisodes), title = "Recent Episodes", thumb = R(ICON_LIST)))
	oc.add(DirectoryObject(key = Callback(Bookmarks), title = "Bookmarks", thumb = R(ICON_QUEUE)))
	oc.add(PrefsObject(title = "Settings", thumb = R(ICON_PREFS)))
	return oc

################################################################################
# Splits Shows and OVA groupings by first letter
def SplitCategory(title, category, ova):
	oc = ObjectContainer(title1 = title)
	lett = 0;
	if ova==True:
		cb = ShowCategoryOVA
	else :
		cb = ShowCategory
	for l in xrange(0,27):
		oc.add(
			DirectoryObject(
				key = Callback(cb, title = title, category = category, letter = l),
				title = letters[l],
				thumb = R(icons[l])
			)
		)
	return oc

################################################################################
# Loops over episode list 
def RecentEpisodes():
	page_data = HTML.ElementFromURL(BASE_URL)
	eps_list = page_data.xpath("//div[@class='mansetlisteleme']/ul/li/a")
	oc = ObjectContainer(title1 = "Recent Episodes")
	for each in eps_list:
		try:
			ep_url = each.xpath("./@href")[0]
			ep_title = FixString(each.xpath("./text()")[0])
			Log("Adding: " +	ep_title + " :: " + ep_url)
		except:
			Log("Episode error")
			continue
		oc.add(GetEpisode(ep_title=ep_title,ep_url=ep_url))
	return oc

################################################################################
# Directory for bookmarks
def Bookmarks():
	oc = ObjectContainer(title1 = "Bookmarks")
	keys = list(Dict)
	keys.sort(key=str.lower)
	for each in keys:
		oc.add(GetShow(show_title = each, show_url = Dict[each]))
	return oc

################################################################################
# Get shows starting with specific character for OVA and Movies
def ShowCategoryOVA(title, category, letter):
	oc = ObjectContainer(title1 = title)
	page_data = HTML.ElementFromURL(BASE_URL + str(category))
	table_data = page_data.xpath("//div[@class='ddmcc']/ul/ul/li/a")
	if len(table_data)==0:
		table_data = page_data.xpath("//div[@class='ddmcc']/ul/li/a")
	Log("table_data len: " + str(len(table_data)))
	for each in table_data:
		try:
			show_url = each.xpath("./@href")[0]
			show_title = FixString(each.xpath("./text()")[0])
		except:
			continue
		isAlpha = letter != 0 and show_title[0:1].upper()==letters[letter]
		isSpecial = letter == 0 and show_title[0:1].isalpha()==False
		if isAlpha or  isSpecial:
			oc.add(Callback(GetEpisode, ep_title = show_title, ep_url=show_url))

	if len(oc) < 1:
		Log ("No Shows")
		return ObjectContainer(header="Error", message="No Shows/Movies found for " + letters[letter])

	return oc

################################################################################
# Get shows starting with specific character
def ShowCategory(title, category, letter):
	oc = ObjectContainer(title1 = title)
	page_data = HTML.ElementFromURL(BASE_URL + str(category))
	table_data = page_data.xpath("//div[@class='ddmcc']/ul/ul/li/a")
	if len(table_data)==0:
		table_data = page_data.xpath("//div[@class='ddmcc']/ul/li/a")
	Log("table_data len: " + str(len(table_data)))
	for each in table_data:
		try:
			show_url = each.xpath("./@href")[0]
			show_title = FixString(each.xpath("./text()")[0])
		except Exception as ex:
			continue
		isAlpha = letter!=0 and show_title[0:1].upper()==letters[letter]
		isSpecial = letter==0 and show_title[0:1].isalpha()==False
		if isAlpha or  isSpecial:
			oc.add(GetShow(show_title = show_title, show_url = show_url))

	if len(oc) < 1:
		Log ("No Shows")
		return ObjectContainer(header="Error", message="No Shows/Movies found for " + letters[letter])
	
	return oc

################################################################################
# Breaks episodes up into groups of 25
def PageEpisodes(show_title, show_url):
	page_data = HTML.ElementFromURL(show_url)
	eps_list = page_data.xpath("//div[@class='menustyle']/li/a")
	eps_cnt =len(eps_list)
	oc = ObjectContainer(title1 = show_title)

	pageLength = int(float(Prefs['pageLength']))

	ep_rem = eps_cnt%pageLength
	pages_cnt = (eps_cnt-ep_rem)/pageLength
	if ep_rem>0 :
		pages_cnt = pages_cnt+1
	reverse = Prefs['ReverseOrder']
	for x in xrange(1,pages_cnt+1):
		start_ep = (x-1)*pageLength
		end_ep = (x*pageLength)
		if reverse==False :
			start_ep = eps_cnt - start_ep
			end_ep = eps_cnt - end_ep
		if end_ep<=0 :
			end_ep = 1
		if end_ep>eps_cnt:
			end_ep = eps_cnt
		oc.add(
			DirectoryObject(
				key = Callback(
					ListEps,
					show_title = show_title,
					show_url = show_url,
					estart = (x-1)*pageLength,
					ecnt = pageLength),
				title = str(start_ep+1) + " to " + str(end_ep)
			)
		)
	if show_title in Dict:
		book_title = "Remove from bookmarks"
	else:
		book_title = "Add to bookmarks"
	oc.add(DirectoryObject(
			key = Callback(EditBookmark, show_title = show_title, show_url = show_url),
			title = book_title,
			thumb = R(ICON_QUEUE)
		)
	)
	return oc

################################################################################
# Loops over episode list within a given range
def ListEps(show_title, show_url, estart, ecnt):
	page_data = HTML.ElementFromURL(show_url)
	eps_list = page_data.xpath("//div[@class='menustyle']/li/a")
	oc = ObjectContainer(title1 = show_title)
	elist = list(doReverse(eps_list))
	elist = elist[estart:estart+ecnt]
	for each in elist:
		try:
			ep_url = each.xpath("./@href")[0]
			ep_title = FixString(each.xpath("./text()")[0])
		except:
			continue
		oc.add(GetEpisode(ep_title,ep_url))
	if len(oc) <= 1:
		Log ("No Episodes")
		return ObjectContainer(header="Error", message="Something has gone wrong.")	
	return oc

################################################################################
# Collects metadata from ep_url and returns EpisodeObject 
def GetEpisode(ep_title,ep_url) :
	ShowThumbCat = Prefs['ShowThumbEps']
	if ShowThumbCat == True :
		# Get Episodes Thumbnail and Summary
		ep_page_data = HTML.ElementFromURL(ep_url)
		try: 
			ep_thumb = ep_page_data.xpath("//link[@rel='image_src']/@href")[0]
		except:
			ep_thumb = R(ICON_COVER)
		try: 
			ep_desc = ep_page_data.xpath("//meta[@name='description']/@content")[0]
			ep_desc = FixString(ep_desc)
			ep_sum = HTML.StringFromElement(ep_page_data.xpath("//div[@class='iltext']/p")[0])
			ep_sum = String.StripTags(ep_sum)
			ep_sum = ep_sum.splitlines()[0]
			ep_sum = FixString(ep_sum)
			ep_sum = ep_sum.replace(ep_desc,"")
		except:
			ep_sum = "???"
	else :
		ep_thumb = R(ICON_COVER)
		ep_sum = ""

	return EpisodeObject(
		url = ep_url,
		title = ep_title,
		thumb = ep_thumb,
		summary = ep_sum
	)


################################################################################
# Collects metadata from show_url and returns DirectoryObject 
def GetShow(show_title, show_url):
	ShowThumbCat = Prefs['ShowThumbCat']
	if ShowThumbCat == True :
		show_page_data = HTML.ElementFromURL(show_url)
		try:
			show_thumb = show_page_data.xpath("//div[@class='katcont'][1]/div[1]/img[1]/@src")[0] 
		except:
			show_thumb = R(ICON_COVER)
		try:
			show_summary = FixString(show_page_data.xpath("//div[@id='hm']/p[1]/text()")[0])
		except:
			show_summary = ""
	else :
		show_thumb = R(ICON_COVER)
		show_summary = ""
	return DirectoryObject(
			key = Callback(PageEpisodes, show_title = show_title, show_url = show_url),
			title = show_title,
			thumb = show_thumb,
			summary = show_summary
		)

################################################################################
# Removes weird Characters from string
def FixString(str):
	str = str.encode('ascii', 'xmlcharrefreplace')
	str = String.Unquote(str)
	str = str.replace("&amp;","&")
	str = str.replace("&#8211;","-")
	str = str.replace("&#8217;","'")
	return str
	
################################################################################
# Reverse list on condition
def doReverse(list):
	reverse = Prefs['ReverseOrder']
	if reverse==True:
		return reversed(list)
	return list

################################################################################
# Adds or removes bookmark from dictionary
def EditBookmark(show_title, show_url):
	if show_title in Dict:
		del Dict[show_title]
		Dict.Save()
		oc = ObjectContainer(
			header=show_title,
			message='This show has been removed from your bookmarks.'
		)
	else:
		Dict[show_title] = show_url
		Dict.Save()
		oc = ObjectContainer(
			header=show_title,
			message='This show has been added to your bookmarks.'
		)
	return oc;

	

