import requests
from flask import Flask, render_template, jsonify, request
import pdb
app = Flask(__name__)


def fetch_song(song_id):
    """Given a song id, return a JSON blob from genius.comself.

    Args:
        song_id (int): The Genius ID of the song.
    Returns:
        A JSON blob.
    """
    url = "https://genius.com/api/songs/{0}".format(song_id)
    r = requests.get(url)
    song = r.json().get('response').get('song')

    return song


def fetch_media(song):
    """Given a JSON blob from Genius, return the 'media' attribute.

    Args:
        song (dict or list): The Genius Song JSON blob.
    Returns:
        List of media services to listen to the song.
    """
    return song.get('media')


def fetch_metadata(song):
    """Given a JSON blob from Genius, return a dict of song metadata.

    Args:
        song (dict or list): The Genius Song JSON blob.
    Returns:
        Dict of song metadata.
    """
    metadata = {
        'id': song.get('id'),
        'header_image_url': song.get('header_image_url'),
        'header_image_thumbnail_url': song.get('header_image_thumbnail_url'),
        'song_art_image_thumbnail_url': song.get('song_art_image_thumbnail_url'),
        'song_art_image_url': song.get('song_art_image_url'),
        'full_title': song.get('full_title'),
        'title_with_featured': song.get('title_with_featured'),
        'artist': song.get('primary_artist').get('name'),
        'share_url': song.get('share_url')
    }

    return metadata


def fetch_search_results(q):
    """Searches Genius.com for the given term.

    Args:
        q (string): The search query.
    Returns:
        A list of dicts containing the metadata for each result.
    """
    url = 'https://genius.com/api/search/'
    r = requests.get(url, params={'q': q})

    results = [
        fetch_metadata(hit.get('result'))
        for hit in r.json().get('response').get('hits')
        if hit.get('type') == 'song'
    ]

    return results

@app.route('/')
def home():
    return render_template('index.html.j2')

@app.route('/search/', methods=['GET'])
def search():
    # TODO: are args being formatted correctly for genius?
    q = request.args.get('q')
    return render_template('results.html.j2', results=fetch_search_results(q))

@app.route('/songs/<id>')
def result(id):
    song = fetch_song(id)
    media = fetch_media(song)
    metadata = fetch_metadata(song)
    # return jsonify({'media': media, 'metadata': metadata})
    return render_template('song.html.j2', media=media, metadata=metadata)
