# -*- coding: utf-8 -*-
import sys, re, requests, xbmcgui, xbmcaddon, xbmc, json, os, random, time, hashlib, string, dataclasses
from concurrent.futures import ThreadPoolExecutor, as_completed
from resources.lib import utils
from resources.lib.vjackson import showFailedNotification
from urllib.parse import quote, urlparse, urlencode
try: 
	from infotagger.listitem import ListItemInfoTag
	tagger = True
except: tagger = False
tokencache = os.path.join(utils.cachepath, "token.json")
addon = xbmcaddon.Addon()

chanicons = ['13thstreet.png', '3sat.png', 'animalplanet.png', 'anixe.png', 'ard.png', 'ardalpha.png', 'arte.png', 'atv.png', 'atv2.png', 'automotorsport.png', 'axnblack.png', 'axnwhite.png', 'br.png', 'cartoonito.png', 'cartoonnetwork.png', 'comedycentral.png', 'curiositychannel.png', 'fix&foxi.png', 'dazn1.png', 'dazn2.png', 'deluxemusic.png', 'nationalgeographic.png', 'dmax.png', 'eurosport1.png', 'eurosport2.png', 'nickjunior.png', 'superrtl.png', 'heimatkanal.png', 'history.png', 'hr.png', 'jukebox.png', 'kabel1doku.png', 'pro7.png', 'pro7maxx.png', 'pro7fun.png', 'rtl2.png', 'kika.png', 'kinowelt.png', 'mdr.png', 'universaltv.png', 'discovery.png', 'mtv.png', 'n24doku.png', 'natgeowild.png', 'sky1.png', 'ndr.png', 'nickelodeon.png', 'nitro.png', 'romancetv.png', 'ntv.png', 'one.png', 'orf1.png', 'orf2.png', 'orf3.png', 'orfsportplus.png', 'phoenix.png', 'geotv.png', 'puls24.png', 'puls4.png', 'rbb.png', 'ric.png', 'motorvision.png', 'rtl.png', 'rtlcrime.png', 'rtlliving.png', 'kabel1.png', 'rtlpassion.png', 'rtlup.png', 'sat1.png', 'sat1emotions.png', 'sat1gold.png', 'servustv.png', 'silverline.png', 'sixx.png', 'skyatlantic.png', 'skycinemaaction.png', 'skycinemaclassics.png', 'skycinemafamily.png', 'skycinemahighlights.png', 'skycinemapremieren.png', 'skycrime.png', 'skydocumentaries.png', 'skykrimi.png', 'skynature.png', 'skyreplay.png', 'skyshowcase.png', 'spiegelgeschichte.png', 'kabel1classics.png', 'sport1.png', 'sportdigital.png', 'swr.png', 'syfy.png', 'tagesschau24.png', 'tele5.png', 'tlc.png', 'toggoplus.png', 'crime+investigation.png', 'vox.png', 'voxup.png', 'warnertvcomedy.png', 'warnertvfilm.png', 'warnertvserie.png', 'wdr.png', 'welt.png', 'weltderwunder.png', 'zdf.png', 'zdfinfo.png', 'zdfneo.png', 'zeeone.png', 'skycinemathriller.png']

def resolve_link(link):
	if not "vavoo" in link:
		link, headers = StalkerPortal(get_cache_or_setting("stalkerurl"), get_cache_or_setting("mac")).get_tv_stream_url(link)
		return link, "&".join([f"{k}={v}" for k, v in headers.items()])
	if addon.getSetting("streammode") == "1":
		_headers={"user-agent": "MediaHubMX/2", "accept": "application/json", "content-type": "application/json; charset=utf-8", "content-length": "115", "accept-encoding": "gzip", "mediahubmx-signature":utils.getAuthSignature()}
		_data={"language":"de","region":"AT","url":link,"clientVersion":"3.0.2"}
		url = "https://vavoo.to/mediahubmx-resolve.json"
		return requests.post(url, json=_data, headers=_headers).json()[0]["url"], None
	else: return "%s.ts?n=1&b=5&vavoo_auth=%s" % (link.replace("vavoo-iptv", "live2")[0:-12], utils.gettsSignature()), "User-Agent=VAVOO/2.6"

def filterout(name):
	name = name.encode().decode("ascii", errors="ignore")
	for r in(("   ", " "), ("  ", " "), ("SPORT1", "SPORT 1"), ("BIBELTV", "BIBEL TV"), ("DIGITALL", "DIGITAL"), ("EINS", "1"), ("ZWEI", "2"), ("DREI", "3"), ("SIEBEN", "7"), ("III", "3"), ("II", "2"), ("BR TV", "BR"), ("ʜᴅ", "")): name = name.replace(*r).strip()
	if "BLACK" in name: return "AXN BLACK"
	elif "AXN" in name or "WHITE" in name: return "AXN WHITE"
	elif "SONY" in name: return "AXN BLACK"
	elif "WARNER" in name or "TNT" in name:
		if "SERIE" in name: return "WARNER TV SERIE"
		elif "FILM" in name: return "WARNER TV FILM"
		elif "COMEDY" in name: return "WARNER TV COMEDY"
	elif all(ele in name for ele in ["1", "2", "3"]): return "1-2-3 TV"
	elif "CENTRAL" in name or "VIVA" in name: return "COMEDY CENTRAL"
	elif "NICK" in name:
		if "EON" in name: return "NICKELODEON"
		elif "TOONS" in name: return "NICKTOONS"
		elif "J" in name: return "NICK JUNIOR"
	elif "ANIXE" in name: return "ANIXE+" if "+" in name else "ANIXE"
	elif "ERSTE" in name and "DAS" in name: return "ARD"
	elif "ZDF" in name:
		if "INFO" in name: return "ZDF INFO"
		elif "NEO" in name: return "ZDF NEO"
		else: return "ZDF"
	elif "FERNSEHEN" in name: 
		if "BR" in name or "BAY" in name: return "BR"
		elif "HR" in name: return "HR"
	elif "DISNEY" in name:
		if "CHANNEL" in name: return "DISNEY CHANNEL"
		elif "J" in name: return "DISNEY JUNIOR"
	elif "SPIEGEL" in name or "CURIOSITY" in name:
		return "SPIEGEL GESCHICHTE" if "GESCHICHTE" in name else "CURIOSITY CHANNEL"
	elif "INVESTIGATION" in name or "A&E" in name: return "CRIME + INVESTIGATION"
	elif "WELT" in name: return "WELT DER WUNDER" if "WUNDER" in name else "WELT"
	elif "GEO" in name:
		if "WILD" in name: return "NAT GEO WILD"
		return "NATIONAL GEOGRAPHIC" if "NAT" in name else "GEO TV"
	elif "N-TV" in name or "NTV" in name: return "NTV"
	elif "PLANET" in name: 
		 return "ANIMAL PLANET" if "ANIMAL" in name else "PLANET"
	elif "TELE" in name and "5" in name: return "TELE 5"
	elif "VOX" in name:
		if "UP" in name or "+" in name: return "VOX UP"
		else: return "VOX"
	if "ORF" in name:
		if "SPORT" in name: return "ORF SPORT"
		if "3" in name: return "ORF 3"
		if "2" in name: return "ORF 2"
		if "1" in name: return "ORF 1"
		if "I" in name: return "ORF 1"
	elif "RTL" in name:
		if "SPORT" in name or "LUXE" in name: name=name
		elif "CRIME" in name: return "RTL CRIME"
		elif "SUPER" in name: return "SUPER RTL"
		elif "PLUS" in name or "UP" in name: return "RTL UP"
		elif "PASSION" in name: return "RTL PASSION"
		elif "LIVING" in name: return "RTL LIVING"
		elif "2" in name: return "RTL 2"
		elif "TOTALLY" in name: return "TOTALLY TURTLES"
		else: return "RTL"
	elif "KABE" in name:
		if "CLA" in name: return "KABEL 1 CLASSICS"
		return "KABEL 1 DOKU" if "DO" in name else "KABEL 1"
	elif "PRO" in name:
		if "FUN" in name: return "PRO 7 FUN"
		return "PRO 7 MAXX" if "MAXX" in name else "PRO 7"
	elif "EUROSPORT" in name:
		if "1" in name: return "EUROSPORT 1"
		if "2" in name: return "EUROSPORT 2"
	elif "ATV" in name:
		return "ATV 2" if "2" in name else "ATV"
	elif "SAT" in name:
		if "3" in name: return "3 SAT"
		elif "1" in name:
			if "GOLD" in name: return "SAT 1 GOLD"
			if "EMOT" in name: return "SAT 1 EMOTIONS"
			else: return "SAT 1"
	elif "SKY" in name:
		if not any(ele in name for ele in ["BUNDES", "SPORT", "SELECT", "BOX"]):
			if "DO" in name: return "SKY DOCUMENTARIES"
			elif "REPLAY" in name: return "SKY REPLAY"
			elif "CASE" in name: return "SKY SHOWCASE"
			elif "ATLANTIC" in name: return "SKY ATLANTIC"
			elif "ACTION" in name: return "SKY CINEMA ACTION"
			elif "HIGHLIGHT" in name or "BEST" in name: return "SKY CINEMA HIGHLIGHTS"
			elif "COMEDY" in name: return "SKY COMEDY"
			elif "FAMI" in name: return "SKY CINEMA FAMILY"
			elif "CLASS" in name or "NOSTALGIE" in name: return "SKY CINEMA CLASSICS"
			elif "KRIM" in name: return "SKY KRIMI"
			elif "CRIME" in name: return "SKY CRIME"
			elif "NATURE" in name: return "SKY NATURE"
			elif "SHOWS" in name: return "SKY SERIEN & SHOWS"
			elif "SPECIAL" in name: return "SKY CINEMA SPECIAL"
			elif "PREMIE" in name: return "SKY CINEMA PREMIEREN +24" if "24" in name else "SKY CINEMA PREMIEREN"
			elif ("ONE" in name or "1" in name) and not "CINEMA" in name: return "SKY ONE"
	elif "PULS" in name:
		if "24" in name: return "PULS 24"
		elif "4" in name: return "PULS 4"
	elif "DO" in name and "24" in name: return "N24 DOKU"
	for keyword in  [("ALLGAU" ,"ALLGAU TV"), ("HEIMA" ,"HEIMATKANAL"), ("ALPHA", "ARD ALPHA"), ("UNIVERSAL" ,"UNIVERSAL TV"), ("SERVUS" ,"SERVUS TV"), ("FOXI", "FIX & FOXI"), ("FOX" ,"SKY REPLAY"), ("STREET" ,"13TH STREET"), ("ZEE" ,"ZEE ONE"), ("DELUX" ,"DELUXE MUSIC"), ("DISCO" ,"DISCOVERY"), ("TAGESSCHAU" ,"TAGESSCHAU 24"), ("VISION" ,"MOTORVISION"), ("AUTO" ,"AUTO MOTOR SPORT"), ("ROMANCE" ,"ROMANCE TV"), "SIXX", "SWR", "EURONEWS", "ARTE", "MTV", "ARD", "MDR", "NDR", "RBB", "PHOENIX", "KIKA", "WDR", "TLC", "DMAX", "HISTORY", "SYFY", "NITRO", "JUKEBOX", "KINOWELT", "WAIDWERK"]:
		if isinstance(keyword, tuple):
			if keyword[0] in name: return keyword[1]
		elif keyword in name: return keyword
	name = re.sub(r"(^(DE|AT|CH) ?(:|\|)| (\|\w|(F|Q|U)?HD\+?|(2|4|8)K|(720|1080|2160)p?|AUSTRIA|GERMANY|DEUTSCHLAND|HEVC|H265|RAW|SD|YOU)|(\(|\[).*?(\)|\])| (DE|\.\D)$)", "", name).strip()
	if name == "SR FERNSEHEN" or name == "SR" or "SRF" in name: return "SRF"
	return name

def check_portal(url, maclist):
	faultymac = utils.get_cache("faultymac")
	if not faultymac: faultymac = {}
	faultymaclist = faultymac.get(url, [])
	progress = xbmcgui.DialogProgress()
	if utils.get_cache("stalkerurl") != url:
		utils.del_cache("stalker_groups")
	utils.set_cache("stalkerurl", url)
	addon.setSetting("stalkerurl", url)
	utils.del_cache("sta_channels")
	progress.create("TESTE STALKER MAC ADRESSEN", f"Verfügbare Mac Adressen {len(maclist)}")
	retry = int(addon.getSetting("stalker_retry"))
	for i in range(1, retry+1):
		if i >1: xbmc.Monitor().waitForAbort(2)
		if (progress.iscanceled()):
			progress.close()
			break
		utils.log(f"Versuch :{i}")
		addon.setSetting("portal_ok", f"Teste Mac Adressen, Versuch :{i}/{str(retry)}")
		progress.update(int(i/retry*100),f"Teste Mac Adressen, Versuch :{i}/{str(retry)}")
		while True:
			mac =random.choice(maclist)
			if mac not in faultymaclist: break
		addon.setSetting("mac", mac)
		utils.set_cache("mac", mac)
		portal =  StalkerPortal(url, mac)
		check = portal.check()
		if check == True:
			progress.close()
			xbmc.executebuiltin("Container.Refresh")
			return
		elif check == "IP BLOCKED":
			progress.update(int(i/retry*100),f"Teste Mac Adressen, Versuch :{i}/{str(retry)}\nFehler {check}")
			progress.close()
			return
		else: progress.update(int(i/retry*100),f"Teste Mac Adressen, Versuch :{i}/{str(retry)}\nFehler {check}")
	progress.close()
	xbmc.executebuiltin("Container.Refresh")
	utils.log("Keine funktionierende Mac")
	addon.setSetting("portal_ok", "Keine gültige Mac")

def choose_portal():
	maclists = requests.get("https://michaz1988.github.io/maclist.json").json()
	a, b, c = [], [], []
	for key, value in maclists.items():
		a.append(key)
		b.append(value)
		c.append("%s, %s mac" % (utils.urlsplit(key).hostname, len(value)))
	indicies = utils.selectDialog(c, "Stalkerurl auswählen")
	if indicies >=0: check_portal(a[indicies], b[indicies])

def new_mac():
	url = utils.get_cache("stalkerurl")
	maclists = requests.get("https://michaz1988.github.io/maclist.json").json()
	maclist = maclists[url]
	check_portal(url, maclist)

def vavoo_groups():
	groups=[]
	for c in requests.get("https://www2.vavoo.to/live2/index?output=json").json():
		if c["group"] not in groups: groups.append(c["group"])
	return sorted(groups)
	
def choose():
	groups = vavoo_groups()
	oldgroups = utils.get_cache("groups")
	preselect = []
	if oldgroups:
		for oldgroup in oldgroups:
			preselect.append(groups.index(oldgroup))
	indicies = utils.selectDialog(groups, "Choose VAVOO Groups", True, preselect)
	group = []
	if indicies:
		for i in indicies: group.append(groups[i])
		addon.setSetting("groups", json.dumps(group))
		return group

def get_cache_or_setting(setting):
	a = utils.get_cache(setting)
	if not a : a = addon.getSetting(setting)
	utils.set_cache(setting, a)
	return a

def get_stalker_channels(genres=None):
	sta_channels= {}
	if not genres:
		genres = utils.get_cache("stalker_groups")
		if not genres: genres = get_genres()
		if not genres: return {}
	mac = utils.get_cache("mac")
	stalkerurl = utils.get_cache("stalkerurl")
	portal = StalkerPortal(stalkerurl, mac)
	chan = portal.channels()
	for item in chan:
		if item["tv_genre_id"] not in genres: continue
		name = item["name"].upper()
		#if not name.isascii():continue
		if any(ele in name for ele in ["***", "###", "---"]): continue
		name= filterout(name)
		if not name:continue
		if name not in sta_channels: sta_channels[name] = []
		if item["cmd"] not in sta_channels[name]: sta_channels[name].append(item["cmd"])
	return sta_channels

def getchannels():
	allchannels = {} if addon.getSetting("stalker") == "false" else get_stalker_channels()
	vav_channels = {} if addon.getSetting("vavoo") == "false" else get_vav_channels()
	for k, v in vav_channels.items():
		if k not in allchannels: allchannels[k] = []
		for n in v: allchannels[k].append(n)
	return allchannels

def new_vav_channels(group):
	_headers={"user-agent": "okhttp/4.11.0", "accept": "application/json", "content-type": "application/json; charset=utf-8", "content-length": "1106", "accept-encoding": "gzip", "mediahubmx-signature": utils.getAuthSignature()}
	items = []
	cursor = 0
	while cursor != None: 
		_data={"language":"de","region":"AT","catalogId":"iptv","id":"iptv","adult":False,"search":"","sort":"name","filter":{"group":group},"cursor":cursor,"clientVersion":"3.0.2"}
		r = requests.post("https://vavoo.to/mediahubmx-catalog.json", json=_data, headers=_headers).json()
		items += r.get("items")
		cursor = r.get("nextCursor")
	return items

def vav_channels():
	chans = utils.get_cache("vav_channels")
	if chans: return chans
	items = []
	groups = vavoo_groups()
	with ThreadPoolExecutor(len(groups)) as executor:
		future_to_url = {executor.submit(new_vav_channels, group):group for group in groups}
		for future in as_completed(future_to_url):
			items += future.result()
	utils.set_cache("vav_channels", items, timeout = 60 * int(addon.getSetting("vav_cache")))
	return items

def get_vav_channels(groups=None):
	vavchannels = {}
	if not groups:
		try: groups = json.loads(addon.getSetting("groups"))
		except: groups = choose()
	for item in vav_channels():
		if item["group"] not in groups: continue
		name = filterout(item["name"])
		if name not in vavchannels: vavchannels[name] = []
		if item["url"] not in vavchannels[name]:
			vavchannels[name].append(item["url"])
	return vavchannels

@dataclasses.dataclass
class Token:
	value= None
	time= 0
	mac = None
	url = None

class StalkerPortal:
	def __init__(self, portal_url, mac):
		self.url = portal_url
		self.portal_url = portal_url.rstrip("/").replace('/c', '/server/load.php')
		self.mac = mac.strip()
		self.serial = self.generate_serial(self.mac)
		self.device_id = self.generate_device_id()
		self.device_id1 = self.device_id
		self.device_id2 = self.device_id
		#self.session = requests.Session()
		self.__token = Token()
		self.__load_cache()
		self.random= None
		self.retries = 3
		self.headers = self.generate_headers()
		self.backoff_factor = 1
		self.timeout = 10

	def __load_cache(self):
		utils.log('Loading token from cache')
		try:
			with open(tokencache, 'r') as f:
				self.__token.__dict__ = json.loads(f.read())
		except Exception as e: utils.log(e)

	def __save_cache(self):
		utils.log('Saving token to cache')
		self.__token.time = time.time()
		self.__token.mac = self.mac
		self.__token.url = self.portal_url
		with open(tokencache, 'w') as f:
			json.dump(self.__token.__dict__, f, indent=2)

	def generate_serial(self, mac):
		md5_hash = hashlib.md5(mac.encode()).hexdigest()
		return md5_hash[:13].upper()

	def generate_device_id(self):
		mac_exact = self.mac.strip()
		return hashlib.sha256(mac_exact.encode()).hexdigest().upper()

	def generate_random_value(self):
		return ''.join(random.choices('0123456789abcdef', k=40))

	def generate_headers(self, include_auth= True, include_token= True, custom_headers= None):
		headers = {}
		headers["Accept"] = "*/*"
		headers["User-Agent"] = 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Mobile Safari/533.3'
		headers["Referer"] = self.url
		headers["Accept-Language"] = "en-US,en;q=0.5"
		headers["Pragma"] = "no-cache"
		headers["X-User-Agent"] = "Model: MAG250; Link: WiFi"
		headers["Host"] = urlparse(self.portal_url).netloc
		if include_auth and self.__token.value: headers["Authorization"] = f"Bearer {self.__token.value}"
		headers["Cookie"] = self.generate_cookies(include_token=include_token)
		headers["Connection"] = "Close"
		headers["Accept-Encoding"] = "gzip, deflate"
		if custom_headers: headers.update(custom_headers)
		utils.log(f"Generated headers: {headers}")
		return headers

	def generate_cookies(self, include_token= True):
		cookies = {"mac": quote(self.mac),"stb_lang": "en","timezone": quote("Europe/Paris")}
		if include_token and self.__token.value: cookies["token"] = quote(self.__token.value)
		return "; ".join([f"{key}={value}" for key, value in cookies.items()])

	def make_request_with_retries(self, params):
		if not params.get("action") in ["handshake", "get_profile"]: self.ensure_token()
		params["JsHttpRequest"] = "1-xml"
		for attempt in range(1, self.retries + 1):
			try:
				utils.log(f"Attempt {attempt}: GET {self.portal_url} with params={params}")
				response = requests.get(self.portal_url, params=params, headers=self.headers, timeout=self.timeout)
				utils.log(f"Received response: {response.status_code}")
				a = response.text
				if "IP adresiniz engellenmistir." in a: return "IP BLOCKED"
				elif "js" in a: return json.loads(a)["js"]
				else: 
					faultymac = utils.get_cache("faultymac")
					if not faultymac: faultymac = {}
					if not self.portal_url in faultymac:
						faultymac[self.portal_url] = []
					if self.mac not in faultymac[self.portal_url]:
						faultymac[self.portal_url].append(self.mac)
					utils.set_cache("faultymac" , faultymac, timeout=False)
					continue
			except Exception as e: utils.log(e)
			if attempt < self.retries:
				sleep_time = self.backoff_factor * (2 ** (attempt - 1))
				utils.log(f"Retrying after {sleep_time} seconds...")
				xbmc.Monitor().waitForAbort(sleep_time)
			else: utils.log(f"All {self.retries} attempts failed for URL {self.portal_url}")

	def handshake(self):
		random_value = None
		token = None
		try:
			token = self.generate_token()
			prehash = self.generate_prehash(token)
			_params = {"type":"stb","action":"handshake","token":token, "prehash": prehash}
			response = self.make_request_with_retries(_params)
			if response == "IP BLOCKED": return "IP BLOCKED"
			token = response.get("token")
			random_value = response.get("random", None)
			if random_value: self.random = random_value.lower()
			else: self.random = self.generate_random_value()
		except Exception as e: utils.log(e)
		if token:
			self.__token.value = token
			self.__save_cache()
			self.headers["Authorization"] = f"Bearer {token}"

	def generate_token(self):
		token_length = 32
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=token_length))

	def generate_prehash(self, token):
		hash_object = hashlib.sha1(token.encode())
		return hash_object.hexdigest()

	def ensure_token(self):
		if self.__token.mac != self.mac or self.__token.url != self.portal_url or self.__token.value is None:
			utils.log("Token not present. Performing handshake to obtain token.")
			a = self.handshake()
			if a == "IP BLOCKED": return "IP BLOCKED"
			self.get_profile()
		elif (time.time() - self.__token.time) > 120:
			utils.log("Token expired. Performing refresh to obtain new token.")
			self.get_profile()
		else: utils.log("Existing token is still valid.")

	def get_profile(self):
		params = {"type": "stb", "action": "get_profile", "hd": "1",
			"ver": "ImageDescription: 0.2.18-r23-250; ImageDate: Thu Sep 13 11:31:16 EEST 2018; PORTAL version: 5.6.2; API Version: JS API version: 343; STB API version: 146; Player Engine version: 0x58c",
			"num_banks": "2",
			"sn": self.serial,
			"stb_type": "MAG250",
			"client_type": "STB",
			"image_version": "218",
			"video_out": "hdmi",
			"device_id": self.device_id1,
			"device_id2": self.device_id2,
			"signature": self.generate_signature(),
			"auth_second_step": "1",
			"hw_version": "1.7-BD-00",
			"not_valid_token": "0",
			"metrics": self.generate_metrics(),
			"hw_version_2": hashlib.sha1(self.mac.encode()).hexdigest(),
			"timestamp": int(time.time()),
			"api_signature": "262",
			"prehash": ""}
		try:
			response = self.make_request_with_retries(params)
			token = response.get("token")
			if token:
				utils.log(f"Profile token updated: {token}")
				self.__token.value = token
		except Exception as e: utils.log(e)
		else:
			self.__save_cache()
			self.headers["Authorization"] = f"Bearer {self.__token.value}"
			utils.log(f"Updatet headers: {self.headers}")

	def generate_signature(self):
		data = f"{self.mac}{self.serial}{self.device_id1}{self.device_id2}"
		signature = hashlib.sha256(data.encode()).hexdigest().upper()
		return signature

	def generate_metrics(self):
		if not self.random: self.random = self.generate_random_value()
		metrics = {"mac": self.mac,"sn": self.serial,"type": "STB","model": "MAG250","uid": "","random": self.random}
		metrics_str = json.dumps(metrics)
		return metrics_str

	def get_account_info(self):
		_params = {"type":"account_info","action":"get_main_info"}
		return self.make_request_with_retries(_params)
		
	def genres(self):
		categories = {}
		groups = self.make_request_with_retries({"type":"itv","action":"get_genres"})
		if not groups: return {}
		for i in groups:
			if i.get("title") and i.get("id") and i.get("id") !="*" : categories[i.get("title")] = i.get("id")
		return dict(sorted(list(categories.items()))) 
		
	def check(self):
		try:
			account_info = self.get_account_info()
			if account_info == "IP BLOCKED": 
				addon.setSetting("account_info", "IP BLOCKED")
				addon.setSetting("portal_ok", "IP BLOCKED")
				return "IP BLOCKED"
			elif not account_info:
				addon.setSetting("account_info", "")
				return "ACCOUNT Infos Empty"
			else:
				utils.log(account_info)
				account_info_str = ",".join([f"{k}:{v}" for k, v in account_info.items()])
				addon.setSetting("account_info", account_info_str)
			if not self.genres(): return "No Genres"
			try: 
				chans = self.channels()
				cmd = random.choice(chans)
			except: return "No Channels"
			if cmd["use_http_tmp_link"] == "0": streamurl = cmd['cmd'].split()[-1]
			else: streamurl, headers = self.get_tv_stream_url(cmd['cmd'])
			res = requests.get(streamurl, headers=self.headers ,timeout=self.timeout, stream=True)
			status = res.status_code
			if int(status) > 399:
				utils.log(f"Stream: {status}")
				return f"HTTP ERROR %s" % status
			addon.setSetting("portal_ok", "Status OK")
			return True
		except Exception as e: 
			utils.log(e)
			return e
	
	def channels(self):
		chan = utils.get_cache("sta_channels")
		if chan: return chan
		response = self.make_request_with_retries({"type":"itv","action":"get_all_channels"})["data"]
		chan =  [{"name": a["name"], "cmd": a["cmd"], "use_http_tmp_link": a["use_http_tmp_link"], "tv_genre_id":a["tv_genre_id"]} for a in response]
		utils.set_cache("sta_channels" , chan, timeout=60* int(addon.getSetting("stalk_cache")))
		return chan

	def get_tv_stream_url(self, cmd):
		cmd = self.make_request_with_retries({"type":"itv","action":"create_link", "cmd":cmd})["cmd"]
		return cmd.split()[-1], self.headers
				
def get_genres():
	titles, ids, preselect = [], [], []
	portal = StalkerPortal(get_cache_or_setting("stalkerurl"), get_cache_or_setting("mac"))
	gruppen = portal.genres()
	for title, groupid in  gruppen.items():
		titles.append(title)
		ids.append(groupid)
	oldgroups = utils.get_cache("stalker_groups")
	if oldgroups: preselect = [ids.index(i) for i in oldgroups]
	indicies = utils.selectDialog(titles, "Choose Groups", True, preselect)
	if indicies:
		group = [ids[i] for i in indicies]
		utils.set_cache("stalker_groups", group)
		return group

def handle_wait(kanal):
	progress = xbmcgui.DialogProgress()
	create = progress.create("Abbrechen zur manuellen Auswahl", "STARTE  : %s" % kanal)
	time_to_wait = int(addon.getSetting("count")) +1
	for secs in range(1, time_to_wait):
		secs_left = time_to_wait - secs
		if utils.PY2:progress.update(int(secs/time_to_wait*100),"STARTE  : %s" % kanal,"Starte Stream in  : %s" % secs_left)
		else:progress.update(int(secs/time_to_wait*100),"STARTE  : %s\nStarte Stream in  : %s" % (kanal, secs_left))
		xbmc.Monitor().waitForAbort(1)
		if (progress.iscanceled()):
			progress.close()
			return False
	progress.close()
	return True

def livePlay(name, type=None, group=None):
	if type == "vavoo": m = get_vav_channels([group]).get(name)
	elif type == "stalker": m = get_stalker_channels([group]).get(name)
	else: m = getchannels().get(name)
	if not m:
		showFailedNotification()
		return
	i, title = 0, None
	if len(m) > 1:
		if addon.getSetting("auto") == "0":
			# Autoplay - rotieren bei der Stream Auswahl
			# ist wichtig wenn z.B. der erste gelistete Stream nicht funzt
			if addon.getSetting("idn") == name:
				i = int(addon.getSetting("num")) + 1
				if i >= len(m): i = 0
			addon.setSetting("idn", name)
			addon.setSetting("num", str(i))
			title = "%s (%s/%s)" % (name, i + 1, len(m))  # wird verwendet für infoLabels
		elif addon.getSetting("auto") == "1":
			if not handle_wait(name):	# Dialog aufrufen
				cap = []
				for i, n in enumerate(m, 1):
					cap.append("STREAM %s" %i)
				i = utils.selectDialog(cap)
				if i < 0: return
			title = "%s (%s/%s)" %(name, i+1, len(m))  # wird verwendet für infoLabels
		else:
			cap=[]
			for i, n in enumerate(m, 1): cap.append("STREAM %s" %i)
			i = utils.selectDialog(cap)
			if i < 0: return
			title = "%s (%s/%s)" % (name, i + 1, len(m))  # wird verwendet für infoLabels
	n = m[i]
	title = title if title else name
	infoLabels={"title": title, "plot": "[B]%s[/B] - Stream %s von %s" % (name, i+1, len(m))}
	o = xbmcgui.ListItem(name)
	url, headers = resolve_link(n)
	utils.log("Spiele %s" % n)
	utils.log("Spiele %s" % url)
	inputstream = None
	if "hls" in url or "m3u8" in url:
		#o.setMimeType("application/vnd.apple.mpegurl")
		if xbmc.getCondVisibility("System.HasAddon(inputstream.ffmpegdirect)") and addon.getSetting("hlsinputstream") == "0": inputstream = "inputstream.ffmpegdirect"
		else: inputstream = "inputstream.adaptive"
		if utils.PY2: o.setProperty("inputstreamaddon", inputstream)
		else: o.setProperty("inputstream", inputstream)
	else:
		#o.setMimeType("video/mp2t")
		if xbmc.getCondVisibility("System.HasAddon(inputstream.ffmpegdirect)"): 
			o.setProperty("inputstream", "inputstream.ffmpegdirect")
			inputstream = "inputstream.ffmpegdirect"
	if inputstream == "inputstream.ffmpegdirect":
		if addon.getSetting("openmode") != "0": o.setProperty("inputstream.ffmpegdirect.open_mode", "ffmpeg" if  addon.getSetting("openmode") == "1" else "curl")
	if headers:
		if inputstream == "inputstream.adaptive":
			o.setProperty(f'{inputstream}.common_headers', headers)
			o.setProperty(f'{inputstream}.stream_headers', headers)
		else: url+=f"|{headers}"
	o.setPath(url)
	o.setProperty("IsPlayable", "true")
	if tagger:
		info_tag = ListItemInfoTag(o, 'video')
		info_tag.set_info(infoLabels)
	else: o.setInfo("Video", infoLabels) # so kann man die Stream Auswahl auch sehen (Info)
	utils.set_resolved(o)
	utils.end()
			
def makem3u():
	m3u = ["#EXTM3U\n"]
	for name in getchannels():
		m3u.append('#EXTINF:-1 group-title="Standart",%s\nplugin://plugin.video.vavooto/?name=%s\n' % (name.strip(), name.replace("&", "%26").replace("+", "%2b").strip()))
	m3uPath = os.path.join(utils.addonprofile, "vavoo.m3u")
	with open(m3uPath ,"w") as a:
		a.writelines(m3u)
	dialog = xbmcgui.Dialog()
	ok = dialog.ok('VAVOO.TO', 'm3u erstellt in %s' % m3uPath)
		
# edit kasi
def channels(items=None, type=None, group=None):
	try: lines = json.loads(addon.getSetting("favs"))
	except: lines=[]
	if items: results = json.loads(items)
	elif type == "vavoo": results = get_vav_channels([group])
	elif type == "stalker": results = get_stalker_channels([group])
	else: results = getchannels()
	for name in results:
		index = len(results[name])
		title = name if addon.getSetting("stream_count") == "false" or index == 1 else "%s  (%s)" % (name, index)
		o = xbmcgui.ListItem(name)
		img = "%s.png" % name.replace(" ", "").lower()
		iconimage = "DefaultTVShows.png"
		if img in chanicons: iconimage = "https://michaz1988.github.io/logos/%s" % img
		o.setArt({"icon":iconimage, "thumb":iconimage, "poster": iconimage})
		cm = []
		if not name in lines:
			cm.append(("zu TV Favoriten hinzufügen", "RunPlugin(%s?action=addTvFavorit&name=%s)" % (sys.argv[0], name.replace("&", "%26").replace("+", "%2b"))))
			plot = ""
		else:
			plot = "[COLOR gold]TV Favorit[/COLOR]" #% name
			cm.append(("von TV Favoriten entfernen", "RunPlugin(%s?action=delTvFavorit&name=%s)" % (sys.argv[0], name.replace("&", "%26").replace("+", "%2b"))))
		cm.append(("Einstellungen", "RunPlugin(%s?action=settings)" % sys.argv[0]))
		cm.append(("m3u erstellen", "RunPlugin(%s?action=makem3u)" % sys.argv[0]))
		o.addContextMenuItems(cm)
		infoLabels={"title": title, "plot": plot}
		if tagger:
			info_tag = ListItemInfoTag(o, 'video')
			info_tag.set_info(infoLabels)
		else: o.setInfo("Video", infoLabels)
		o.setProperty("IsPlayable", "true")
		param = {"name":name, "type": type, "group": group} if type else {"name":name}
		utils.add(param, o)
	utils.sort_method()
	utils.end()

def favchannels():
	try: lines = json.loads(addon.getSetting("favs"))
	except: return
	for name in getchannels():
		if not name in lines: continue
		o = xbmcgui.ListItem(name)
		img = "%s.png" % name.replace(" ", "").lower()
		iconimage = "DefaultTVShows.png"
		if img in chanicons: iconimage = "https://michaz1988.github.io/logos/%s" % img
		o.setArt({"icon":iconimage, "thumb":iconimage, "poster": iconimage})
		cm = []
		cm.append(("von TV Favoriten entfernen", "RunPlugin(%s?action=delTvFavorit&name=%s)" % (sys.argv[0], name.replace("&", "%26").replace("+", "%2b"))))
		cm.append(("Einstellungen", "RunPlugin(%s?action=settings)" % sys.argv[0]))
		o.addContextMenuItems(cm)
		infoLabels={"title": name, "plot": "[COLOR gold]Liste der eigene Live Favoriten[/COLOR]"}
		if tagger:
			info_tag = ListItemInfoTag(o, 'video')
			info_tag.set_info(infoLabels)
		else: o.setInfo("Video", infoLabels)
		o.setProperty("IsPlayable", "true")
		utils.add({"name":name}, o)
	utils.sort_method()
	utils.end()

def change_favorit(name, delete=False):
	try: lines = json.loads(addon.getSetting("favs"))
	except: lines= []
	if delete: lines.remove(name)
	else: lines.append(name)
	addon.setSetting("favs", json.dumps(lines))
	if len(lines) == 0: xbmc.executebuiltin("Action(ParentDir)")
	else: xbmc.executebuiltin("Container.Refresh")

# edit by kasi
def live():
	from resources.lib.vjackson import addDir2
	try: lines = json.loads(addon.getSetting("favs"))
	except:	lines = []
	if len(lines)>0: addDir2("Live - Favoriten", "DefaultAddonPVRClient", "favchannels")
	addDir2("Live - Alle", "DefaultAddonPVRClient", "channels")
	addDir2("Live - A bis Z", "DefaultAddonPVRClient", "a_z_tv")
	addDir2("Live - Gruppen", "DefaultAddonPVRClient", "group_tv")
	utils.end(cacheToDisc=False)

def group_tv(type=None):
	from resources.lib.vjackson import addDir2
	if type=="vavoo":
		gruppen = vavoo_groups()
		for group in gruppen: 
			addDir2(group, "DefaultAddonPVRClient", "channels", type=type, group=group)
	elif type=="stalker":
		portal = StalkerPortal(utils.get_cache("stalkerurl"), utils.get_cache("mac"))
		gruppen = portal.genres()
		for title, groupid in  gruppen.items():
			addDir2(title, "DefaultAddonPVRClient", "channels", type=type, group=groupid)
	else:
		addDir2("VAVOO - GRUPPEN", "DefaultAddonPVRClient", "group_tv", type="vavoo")
		addDir2("STALKER - GRUPPEN", "DefaultAddonPVRClient", "group_tv", type="stalker")
	utils.end()

def a_z_tv():
	from resources.lib.vjackson import addDir2
	from collections import defaultdict
	results = getchannels()
	res = defaultdict(dict)
	for key, val in results.items():
		prefix, number = key[:1].upper() if key[:1].isalpha() else "#", key
		res[prefix][number] = val
	res = dict(sorted(res.items()))
	for key, val in res.items():
		addDir2(key, "DefaultAddonPVRClient", "channels", items=json.dumps(val))
	utils.end()