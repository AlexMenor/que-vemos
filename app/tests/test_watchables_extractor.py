import pytest
from ..data.watchables_extractor.watchables_extractor import parse_watchable
from ..entities.watchable import WatchableType

@pytest.fixture
def movie_db_movie():
    return {'id': 604822, 'video': False, 'vote_count': 6, 'vote_average': 7.3, 'title': 'Vanguard', 'release_date': '2020-09-30', 'original_language': 'zh', 'original_title': '急先锋', 'genre_ids': [28, 12, 80], 'backdrop_path': '/fX8e94MEWSuTJExndVYxKsmA4Hw.jpg', 'adult': False, 'overview': "Covert security company Vanguard is the last hope of survival for an accountant after he is targeted by the world's deadliest mercenary organization.", 'poster_path': '/vYvppZMvXYheYTWVd8Rnn9nsmNp.jpg', 'popularity': 44.943, 'media_type': 'movie'}

@pytest.fixture
def movie_db_series():
    return {'backdrop_path': '/f7PJT5Vvc99vjEmo6JyfDs3p3ei.jpg', 'first_air_date': '2020-11-20', 'genre_ids': [99, 10764], 'id': 102693, 'name': "Marvel's 616", 'origin_country': ['US'], 'original_language': 'en', 'original_name': "Marvel's 616", 'overview': 'The series explores Marvel’s rich legacy of pioneering characters, creators and storytelling to reflect the world outside your window. Each documentary, helmed by a unique filmmaker, showcases the intersections of storytelling, pop culture, and fandom within the Marvel Universe. Episodes in this anthology series will cover topics including Marvel’s world-spanning artists, the trailblazing women of Marvel Comics, discovering the “forgotten” characters of Marvel, and much more.', 'poster_path': '/wBOIVb6zgsnfRhvCgdX04pLaYXQ.jpg', 'vote_average': 0.0, 'vote_count': 0, 'popularity': 43.364, 'media_type': 'tv'}

@pytest.fixture
def movie_db_movie_without_date():
    return {'id': 604822, 'video': False, 'vote_count': 6, 'vote_average': 7.3, 'title': 'Vanguard', 'original_language': 'zh', 'original_title': '急先锋', 'genre_ids': [28, 12, 80], 'backdrop_path': '/fX8e94MEWSuTJExndVYxKsmA4Hw.jpg', 'adult': False, 'overview': "Covert security company Vanguard is the last hope of survival for an accountant after he is targeted by the world's deadliest mercenary organization.", 'poster_path': '/vYvppZMvXYheYTWVd8Rnn9nsmNp.jpg', 'popularity': 44.943, 'media_type': 'movie'}

@pytest.fixture
def movie_db_series_without_date():
    return {'backdrop_path': '/f7PJT5Vvc99vjEmo6JyfDs3p3ei.jpg', 'genre_ids': [99, 10764], 'id': 102693, 'name': "Marvel's 616", 'origin_country': ['US'], 'original_language': 'en', 'original_name': "Marvel's 616", 'overview': 'The series explores Marvel’s rich legacy of pioneering characters, creators and storytelling to reflect the world outside your window. Each documentary, helmed by a unique filmmaker, showcases the intersections of storytelling, pop culture, and fandom within the Marvel Universe. Episodes in this anthology series will cover topics including Marvel’s world-spanning artists, the trailblazing women of Marvel Comics, discovering the “forgotten” characters of Marvel, and much more.', 'poster_path': '/wBOIVb6zgsnfRhvCgdX04pLaYXQ.jpg', 'vote_average': 0.0, 'vote_count': 0, 'popularity': 43.364, 'media_type': 'tv'}

def test_parse_watchable_with_movie(movie_db_movie):
    watchable = parse_watchable(movie_db_movie)
    assert watchable.type == WatchableType.MOVIE
    assert watchable.synopsis == movie_db_movie['overview']
    assert watchable.popularity == movie_db_movie['popularity']
    assert watchable.title == movie_db_movie['title']

def test_parse_watchable_with_series(movie_db_series):
    watchable = parse_watchable(movie_db_series)
    assert watchable.type == WatchableType.SERIES
    assert watchable.synopsis == movie_db_series['overview']
    assert watchable.popularity == movie_db_series['popularity']
    assert watchable.title == movie_db_series['name']

def test_parse_watchable_with_movie_without_date(movie_db_movie_without_date):
    watchable = parse_watchable(movie_db_movie_without_date)

def test_parse_watchable_with_series_without_date(movie_db_series_without_date):
    watchable = parse_watchable(movie_db_series_without_date)
