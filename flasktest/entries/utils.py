from datetime import date, timedelta

from flask_jwt_extended import get_jwt_identity

from flasktest import db
from flasktest.models import Links, Category, Text
from flasktest.users.utils import current_user


def add_link_to_db(entry_title, url, category):
    '''
    If category is not empty, create entry with category already added.
    '''
    CURRENT_USER = current_user(get_jwt_identity())
    url_validation = check_for_http(url)
    if (category):
        category_id = category_exists(category)
        link = Links(entry_title=entry_title, url=url_validation,
                     users=CURRENT_USER, category_id=category_id.id)
    else:
        link = Links(entry_title=entry_title,
                     url=url_validation, users=CURRENT_USER)
    db.session.add(link)
    db.session.commit()


def check_for_http(link):
    '''
    Checks if link contains http or https prefix
    '''
    print('This ran')
    if "http" in link or "https" in link:
        return link
    else:
        return "http://" + link


def add_text_to_db(entry_title, text_content, category):
    CURRENT_USER = current_user(get_jwt_identity())
    '''
    If category is not empty, create entry with category already added.
    '''
    if (category):
        category_validation = category_exists(category)
        text = Text(entry_title=entry_title, text_content=text_content,
                    users=CURRENT_USER, category_id=category_validation.id)
    else:
        text = Text(entry_title=entry_title,
                    text_content=text_content, users=CURRENT_USER)
    db.session.add(text)
    db.session.commit()


def category_exists(title):
    '''
    Checks if there is an existing Category which matches the title. If not, a new one is created.
    '''
    category = Category.query.filter_by(title=title).first()
    if not category:
        category = Category(title=title)
        db.session.add(category)
        db.session.commit()
    return category


def home_page_links(user_id):
    '''
    Gets links for dashboard. These are entries that will be sent within 3 days.
    '''
    today = date.today()
    list_of_links = Links.query.filter_by(user_id=user_id).filter(
        Links.date_of_next_send <= (today + timedelta(days=3)))

    return generate_links_dict(list_of_links)


def home_page_text(user_id):
    '''
    Gets text entries for dashboard. These are entries that will be sent within 3 days.
    '''
    today = date.today()
    list_of_text = Text.query.filter_by(user_id=user_id).filter(
        Text.date_of_next_send <= (today + timedelta(days=3)))

    return generate_text_dict(list_of_text)


def get_all_links(user_id):
    '''
    Returns all links.
    '''
    list_of_links = Links.query.filter_by(user_id=user_id)

    return generate_links_dict(list_of_links)


def get_all_texts(user_id):
    '''
    Returns all text entries.
    '''
    list_of_text = Text.query.filter_by(user_id=user_id)

    return generate_text_dict(list_of_text)


def generate_links_dict(db_links):
    '''
    Returns dictionary formated with days until next send instead of having the date itself.
    '''
    urls = []
    today = date.today()
    for link in db_links:
        elements = {}
        date_diff = (link.date_of_next_send - today).days
        if date_diff == 0:
            date_diff = 'Today'
        elif date_diff == 1:
            date_diff = 'Tomorrow'
        elements['entry_title'] = link.entry_title
        elements['url'] = link.url
        elements['days'] = date_diff
        elements['id'] = link.id
        category = Category.query.filter_by(id=link.category_id).first()
        if category == None:
            elements['category'] = ''
        else:
            elements['category'] = category.title
        urls.append(elements)

    return urls


def generate_text_dict(db_text):
    '''
    Returns dictionary formated with days until next send instead of having the date itself.
    '''
    texts = []
    today = date.today()
    for text in db_text:
        elements = {}
        date_diff = (text.date_of_next_send - today).days
        if date_diff == 0:
            date_diff = 'Today'
        elif date_diff == 1:
            date_diff = 'Tomorrow'
        elements['entry_title'] = text.entry_title
        elements['text_content'] = text.text_content
        elements['days'] = date_diff
        elements['id'] = text.id
        category = Category.query.filter_by(id=text.category_id).first()
        if category == None:
            elements['category'] = None
        else:
            elements['category'] = category.title
        texts.append(elements)

    return texts
