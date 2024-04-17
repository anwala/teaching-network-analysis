'''
imdb_scraper.py
Scrape IMDb director credits and movie crew
Alexander C. Nwala 
W&M DATA 340-02 - Network Science

Requirements:
* BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ (pip install beautifulsoup4)
* NwalaTextUtils: https://github.com/oduwsdl/NwalaTextUtils (pip install NwalaTextUtils)
* PyMovieDb: https://github.com/itsmehemant7/PyMovieDb (pip install PyMovieDb)
* isoduration: https://github.com/bolsote/isoduration (pip install isoduration)
'''
import json
import re

from bs4 import BeautifulSoup
from datetime import timedelta
from isoduration import parse_duration
from warnings import warn

from NwalaTextUtils.textutils import derefURI
from NwalaTextUtils.textutils import genericErrorInfo
from NwalaTextUtils.textutils import getPgTitleFrmHTML

from PyMovieDb import IMDB

def get_full_credits_for_director(dir_id):

    def get_movie_link(mov_elm, mov_year):
        
        mov_links = mov_elm.find_all('a')

        for m in mov_links:
            
            title = m.text.strip()
            m = m['href'].strip()
            mov_year = mov_year.text.strip() if mov_year is not None else ''

            if( m.startswith('/title/tt') ):
                movie_note = mov_elm.text.replace(title, '').replace(mov_year, '')
                movie_note = ' '.join(movie_note.split())
                return {'title': title, 'uri': f'https://www.imdb.com{m}', 'year': mov_year, 'note': movie_note}

        return {}

    def get_movies_section(soup):

        film_sections = soup.find_all(class_='filmo-category-section')
    
        for fs in film_sections:
            is_director_section = fs.find('div')
            if( is_director_section is not None and is_director_section.get('id', '').startswith('director-') ):
                return fs
        
        return None

    uri = f'https://www.imdb.com/name/{dir_id}/fullcredits/'
    html_pg = derefURI(uri)
    title = ''

    try:
        soup = BeautifulSoup(html_pg, 'html.parser')
        title = getPgTitleFrmHTML(html_pg)
        title = title.split('-')[0].strip()
    except:
        genericErrorInfo()
        return {}


    movies = get_movies_section(soup)
    if( movies is None ):
        return {}
    
    dir_credits = {'director_name': title, 'imdb_uri': uri, 'credits': []}
    movies = movies.find_all('div', class_='filmo-row')      
    for m in movies:
        
        m = get_movie_link(m, m.find(class_='year_column'))
        if( len(m) != 0 ):
            dir_credits['credits'].append(m)
        
    return dir_credits

def get_full_crew_for_movie(title_id, set_imdb_details=False):

    def get_crew_table_dets(crew_tab):
    
        crew = []    
        rows = crew_tab.find_all('tr')

        for r in rows:
            
            dets = {}
            cols = r.find_all('td')
            
            for c in cols:
                
                class_name = c.get('class', '')
                if( class_name == '' ):
                    continue

                
                class_name = class_name[0].lower().strip()
                if( class_name in ['name', 'credit'] ):
                
                    dets[class_name] = c.text.strip()
                    link = c.find('a')
                    if( link is not None ):
                        dets['link'] = link.get('href', '')
                        dets['link'] = 'https://www.imdb.com'+dets['link']
            

            if( len(dets) != 0 ):
                crew.append(dets)

        return crew

    full_credits = {}
    uri = f'https://www.imdb.com/title/{title_id}/fullcredits/'
    html_pg = derefURI(uri)

    try:
        soup = BeautifulSoup(html_pg, 'html.parser')
        title = getPgTitleFrmHTML(html_pg)
        title = title.split('-')[0].strip()
    except:
        genericErrorInfo()
        return {}


    soup = soup.find('div', id='fullcredits_content')
    if( soup is None ):
        return {}

    headers = soup.find_all(class_='dataHeaderWithBorder')
    tables = soup.find_all('table')
    
    if( len(headers) != len(tables) ):
        warn(f'len(headers) != len(tables), check for result for integrity: {uri}')


    full_credits = {'title_uri': uri, 'title': title, 'full_credits': [], 'imdb_details': get_movie_imdb_details(title_id) if set_imdb_details is True else {}}
    for i in range(len(headers)):
        
        h = headers[i]
        h = ' '.join(h.text.split())
        
        crew = []
        if( i < len(tables) ):
            crew = get_crew_table_dets(tables[i])
        
        full_credits['full_credits'].append({'role': h, 'crew': crew})

    return full_credits

def get_movie_imdb_details(title_id):
    
    try:
        imdb = IMDB()
        movie = imdb.get_by_id(title_id)
        return json.loads(movie)
    except:
        genericErrorInfo()
        return {}

def get_movie_duration_seconds(title_id, movie=None):

    try:
        if( movie is None ):
            imdb = IMDB()
            movie = imdb.get_by_id(title_id)
            movie = json.loads(movie)

        #duration example: PT2H7M
        duration = movie.get('duration', '')
        if( duration is None or duration == '' ):
            return -1
            
        duration = parse_duration(duration)
    except:
        genericErrorInfo()
        return -1
    
    delta = timedelta(
        days=int(duration.date.years)*365 + int(duration.date.months)*30 + int(duration.date.days), 
        weeks=int(duration.date.weeks),
        hours=int(duration.time.hours),
        minutes=int(duration.time.minutes),
        seconds=int(duration.time.seconds)
    )

    return delta.total_seconds()


def normalize_movie_role(role):
    
    '''
        Notes
        1. Don't create distinction between series and movie roles, therefore remove "Series prefix"
        2. Nomalize all variant of "Cast" and "Writing Credit" to their root roles
    '''

    '''
        Oscar categories
        https://awardsdatabase.oscars.org/
        ACTING
        ANIMATED FEATURE FILM
        CINEMATOGRAPHY
        COSTUME DESIGN
        DIRECTING
        DOCUMENTARY
        FILM EDITING
        INTERNATIONAL FEATURE FILM
        MAKEUP
        MUSIC - SCORING
        MUSIC - SONG
        PICTURE
        PRODUCTION DESIGN
        SCIENTIFIC AND TECHNICAL
        SHORT FILMS - ANIMATED
        SHORT FILMS - LIVE ACTION
        SOUND
        SPECIAL EFFECTS
        VISUAL EFFECTS
        WRITING
    '''

    '''
        Raw crew roles from IMDB
        1. Additional Crew 1666
        2. Animation Department 405
        3. Art Department 1427
        4. Art Direction by 1226
        5. Camera and Electrical Department 1661
        6. Cast 739
        7. Cast (in credits order) 506
        8. Cast (in credits order) complete, awaiting verification 332
        9. Cast (in credits order) verified as complete 795
        10. Cast complete, awaiting verification 9
        11. Casting By 1241
        12. Casting Department 1200
        13. Cinematography by 1866
        14. Costume Design by 1247
        15. Costume and Wardrobe Department 1282
        16. Directed by 2573
        17. Editorial Department 1509
        18. Film Editing by 1832
        19. Location Management 1209
        20. Makeup Department 1399
        21. Music Department 1436
        22. Music by 1652
        23. Produced by 2078
        24. Production Department 3
        25. Production Design by 1358
        26. Production Management 1462
        27. Script and Continuity Department 1215
        28. Second Unit Director or Assistant Director 1446
        29. Series Additional Crew 386
        30. Series Animation Department 127
        31. Series Art Department 362
        32. Series Art Direction by 326
        33. Series Camera and Electrical Department 383
        34. Series Cast 376
        35. Series Cast complete, awaiting verification 21
        36. Series Cast verified as complete 9
        37. Series Casting By 333
        38. Series Casting Department 331
        39. Series Cinematography by 372
        40. Series Costume Design by 339
        41. Series Costume and Wardrobe Department 345
        42. Series Directed by 419
        43. Series Editorial Department 371
        44. Series Film Editing by 381
        45. Series Location Management 327
        46. Series Makeup Department 358
        47. Series Music Department 367
        48. Series Music by 350
        49. Series Produced by 415
        50. Series Production Design by 347
        51. Series Production Management 367
        52. Series Script and Continuity Department 334
        53. Series Second Unit Director or Assistant Director 360
        54. Series Set Decoration by 328
        55. Series Sound Department 383
        56. Series Special Effects by 289
        57. Series Stunts 329
        58. Series Thanks 136
        59. Series Transportation Department 320
        60. Series Visual Effects by 334
        61. Series Writing Credits 406
        62. Series Writing Credits (WGA) 1
        63. Set Decoration by 1121
        64. Sound Department 1644
        65. Special Effects by 1096
        66. Stunts 1121
        67. Thanks 1020
        68. Transportation Department 1154
        69. Visual Effects by 1184
        70. Writing Credits 692
        71. Writing Credits (WGA) 541
        72. Writing Credits (WGA) (in alphabetical order) 6
        73. Writing Credits (in alphabetical order) 639
    '''

    '''
        Arthur's final list of crew roles and subroles (* subrole)
        
        Casting by
        Cinematography by
        Costume Design by
        Directed by
        Film Editing by
        Music by
        Production Design by
        Writing Credits
        
        Makeup Department 
        * makeup department head
        * hair department head
        Produced by
        * producer
        * producer produced by
        * producer produced by p.g.a.
        Sound Department*
        * sound designer* didn't find this
        * re-recording mixer
        * supervising sound editor
        Special Effects by*
        * special effects coordinator
        Visual Effects by* 
        * visual effects supervisor
    '''

    if( role.startswith('Series ') ):
        role = role[7:]

    for pre in ['Cast ', 'Writing Credits ']:
        if( role.startswith(pre) ):
            role = pre[:-1]

    return role.strip()

def normalize_crew_credit(role_credit):

    '''
        #implemented by normalize_exclude_some_mov_roles() - start
        Split multiple credits, e.g.,
            technical director/compositor (uncredited) -> 
                technical director
                compositor (uncredited)

            fight choreographer / utility stunts -> 
                fight choreographer
                utility stunts
        #implemented by normalize_exclude_some_mov_roles() - end
    

        Remove context after credit, e.g.,
            stereo artist: Legend 3D (uncredited) ->
                stereo artist

            visual effects on set surveyor: SPI ->
                visual effects on set surveyor

        Remove alias in name, e.g.,
            co-producer (as Tom Peitzman) ->
                co-producer

        Remove "uncredited", e.g.,
            makeup artist (uncredited) ->
                makeup artist

        Remove the following tokens 'and', '&', etc

        Skip entry with quote (most likely movie) or containing "based on"
    '''
    role_credit = role_credit.strip().lower()
    role_credit = role_credit.split(':')[0]
    
    role_credit = role_credit.split('(as')[0]
    
    for tok in ['and', '&', '(uncredited)', '(', ')']:
        role_credit = role_credit.replace(tok, '')

    for tok in ['"', 'based on', 'based upon']:
        if tok in role_credit:
            return ''
    
    role_credit = re.sub(' +', ' ', role_credit)
    return role_credit

def normalize_movie_subrole(mov_crew):
    
    #normalize subrole (aka credit) for crew - start
    for j in range(len(mov_crew)):
        
        if( 'credit' not in mov_crew[j] ):
            continue

        norm_subroles = re.split('\(segment|\/', mov_crew[j]['credit'])
        norm_subroles = [normalize_crew_credit(nsub).strip() for nsub in norm_subroles]
        norm_subroles = [nsub for nsub in norm_subroles if nsub != '']
        
        if( len(norm_subroles) >0 ):
            mov_crew[j]['normalized_credit'] = norm_subroles
    #normalize subrole (aka credit) for crew - end



def is_feature_film(title_id, movie=None):

    if( movie is None ):
        try:
            imdb = IMDB()
            movie = imdb.get_by_id(title_id)
            movie = json.loads(movie)
        except:
            genericErrorInfo()

    mov_type = movie.get('type', '').strip().lower()
    mov_dur_secs = get_movie_duration_seconds(title_id, movie=movie)

    if( mov_type in ['tvseries'] ):
        return False
    if( mov_type == 'movie' and mov_dur_secs >= 70*60 ):
        #feature film must be at least 70 minutes long
        return True
    
    if( mov_dur_secs == -1 ):
        return is_feature_film_v2(title_id)

    return False

def is_feature_film_v2(title_id):

    full_credits = {}
    uri = f'https://www.imdb.com/title/{title_id}/'
    html_pg = derefURI(uri)

    try:
        soup = BeautifulSoup(html_pg, 'html.parser')
    except:
        genericErrorInfo()
        return False

    header = soup.find('h1')
    if( header is None ):
        return False

    year_rating_duration = header.find_next('ul', class_='ipc-inline-list')
    if( year_rating_duration is None or len(year_rating_duration) == 0 ):
        return False
    year_rating_duration = list(year_rating_duration)

    #movie_type_or_yyyy example: "2023", "TV Series", "TV Mini Series", 
    movie_type_or_yyyy = year_rating_duration[0].text.strip().lower()
    if( 'series' in movie_type_or_yyyy ):
        return False

    #duration example: 1h 39m
    duration = year_rating_duration[-1].text.split(' ')

    total_seconds = 0
    for d in duration:

        try:
            d = d.strip()
            if( d.endswith('h') ):
                total_seconds += int(d.replace('h', '')) * 60 * 60
            elif( d.endswith('m') ):
                total_seconds += int(d.replace('m', '')) * 60
            elif( d.endswith('s') ):
                total_seconds += int(d.replace('s', ''))
        except:
            genericErrorInfo()

    if( movie_type_or_yyyy.isnumeric() and total_seconds >= 70*60 ):
        #feature film must be at least 70 minutes long
        return True

    return False
