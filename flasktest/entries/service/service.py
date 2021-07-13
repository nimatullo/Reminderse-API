from flasktest.models import Links
from flasktest.entries.repo.repo import LinkRepo, TextRepo
from flasktest.entries.repo.repo import get_category
from datetime import date


class EntryService:
    def __init__(self) -> None:
        self.link_repo = LinkRepo()
        self.text_repo = TextRepo()

    def generate_links_dict(self, user_id):
        all_links = self.link_repo.get_all_links_for_user(user_id)
        return map(lambda link: self.convert_to_dictionary, all_links)

    def convert_to_dictionary(self, link):
        date_diff = (link.date_of_next_send - date.today()).days
        if date_diff == 0:
            date_diff = "Today"
        elif date_diff == 1:
            date_diff = "Tomorrow"
        category = get_category(link.category_id)
        if category:
            category = ""
        else:
            category = category.title
        return {
            "id": link.id,
            "entry_title": link.entry_title,
            "days": date_diff,
            "category": category
        }
