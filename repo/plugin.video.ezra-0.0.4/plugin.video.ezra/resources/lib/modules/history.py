# -*- coding: utf-8 -*-
import json
from urllib.parse import unquote
from datetime import timedelta
from caches.main_cache import main_cache
from modules import kodi_utils
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
icon = kodi_utils.translate_path('special://home/addons/script.ezart/resources/media/search.png')
four_insert_string, five_insert_string = '%s %s %s %s', '%s %s %s %s %s'
delete_str, search_str, hist_str, vid_str, mov_str, key_str = ls(32785), ls(32450), ls(32486), ls(32491), ls(32028), ls(32092)
tv_str, furk_str, easy_str, peop_str, imdb_str, tmdb_str, coll_str = ls(32029), ls(32069), ls(32070), ls(32507), ls(32064), ls(32068), ls(32499)
clear_history_list = [(four_insert_string % (delete_str, mov_str, search_str, hist_str), 'movie_queries'),
					(four_insert_string % (delete_str, tv_str, search_str, hist_str), 'tvshow_queries'), 
					(four_insert_string % (delete_str, peop_str, search_str, hist_str), 'people_queries'),
					(five_insert_string % (delete_str, imdb_str, key_str, mov_str, hist_str), 'imdb_keyword_movie_queries'),
					(five_insert_string % (delete_str, imdb_str, key_str, tv_str, hist_str), 'imdb_keyword_tvshow_queries'),
					(five_insert_string % (delete_str, furk_str, vid_str, search_str, hist_str), 'furk_video_queries'), 
					(four_insert_string % (delete_str, easy_str, search_str, hist_str), 'easynews_video_queries'), 
					(five_insert_string % (delete_str, tmdb_str, coll_str, search_str, hist_str), 'tmdb_collections_queries')]

def get_search_term(params):
	kodi_utils.close_all_dialog()
	media_type = params.get('media_type', '')
	search_type = params.get('search_type', 'media_title')
	if search_type == 'media_title':
		mode, action, string = ('build_movie_list', 'tmdb_movies_search', 'movie_queries') if media_type == 'movie' else ('build_tvshow_list', 'tmdb_tv_search', 'tvshow_queries')
		url_params = {'mode': mode, 'action': action}
	elif search_type == 'people': string = 'people_queries'
	elif search_type == 'imdb_keyword':
		url_params, string = {'mode': 'imdb_build_keyword_results', 'media_type': media_type}, 'imdb_keyword_%s_queries' % media_type
	elif search_type == 'furk_direct':
		url_params, string = {'mode': 'furk.search_furk', 'media_type': media_type}, 'furk_video_queries'
	elif search_type == 'easynews_video':
		url_params, string = {'mode': 'easynews.search_easynews'}, 'easynews_video_queries'
	if search_type == 'tmdb_collections':
		url_params, string = {'mode': 'build_movie_list', 'action': 'tmdb_movies_search_collections'}, 'tmdb_collections_queries'
	query = params.get('query', None) or kodi_utils.dialog.input('Fen')
	if not query: return
	query = unquote(query)
	add_to_search_history(query, string)
	if search_type == 'people':
		from indexers.people import person_search
		return person_search(query)
	url_params['query'] = query
	if kodi_utils.external_browse(): return kodi_utils.execute_builtin('ActivateWindow(10025,%s,return)' % kodi_utils.build_url(url_params))
	return kodi_utils.execute_builtin('Container.Update(%s)' % kodi_utils.build_url(url_params))

def add_to_search_history(search_name, search_list):
	try:
		result = []
		cache = main_cache.get(search_list)
		if cache: result = cache
		if search_name in result: result.remove(search_name)
		result.insert(0, search_name)
		result = result[:50]
		main_cache.set(search_list, result, expiration=timedelta(days=365))
	except: return

def remove_from_search_history(params):
	try:
		result = main_cache.get(params['setting_id'])
		result.remove(params.get('query'))
		main_cache.set(params['setting_id'], result, expiration=timedelta(days=365))
		kodi_utils.notification(32576, 2500)
		kodi_utils.execute_builtin('Container.Refresh')
	except: return

def clear_search_history():
	try:
		list_items = [{'line1': item[0], 'icon': icon} for item in clear_history_list]
		kwargs = {'items': json.dumps(list_items), 'heading': ls(32036), 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		setting = kodi_utils.select_dialog([item[1] for item in clear_history_list], **kwargs)
		if setting == None: return
		main_cache.set(setting, '', expiration=timedelta(days=365))
		kodi_utils.notification(32576, 2500)
	except: return

	
