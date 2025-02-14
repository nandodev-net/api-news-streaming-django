"""
    Base class for scraped data schemes. Every scheme should inherit this class
"""

# Local imports 
from sre_parse import CATEGORIES
from app.scraper.models import ArticleCategory, ArticleHeadline, MediaSite

# Python imports
import dataclasses
from typing import List, Optional, Tuple
import datetime
import parsedatetime

# Note that the use of dataclasses here is not optional since 
# scrapy requires to have an Item-like interface, which is provided 
# by using dataclasses: https://docs.scrapy.org/en/latest/topics/items.html#dataclass-objects
@dataclasses.dataclass
class BaseDataScheme:
    """
        Every data scheme should inherit this class 
        and implement the corresponding function to map to the canonical
        data type, the `as_headline` function
    """
    title : str 
    excerpt : str
    url : str
    date : str
    # image url
    img : str
    scraper : str
    scraped_date : datetime.datetime
    relevance : Optional[bool] = None
    categories : List[str] = dataclasses.field(default_factory=list)

    def as_headline(self) -> Tuple[ArticleHeadline, List[ArticleCategory]]:
        """
            Convert from this specific data scheme to an article headline object
            # Returns
                An `ArticleHeadline` object correctly mapped. For example, if there's a canonical 
                category called 'Nacionales' but such category is called 'nacional' for this site,
                then the resulting object will have the category correctly named as 'Nacionales'. 
                The same applies to every data field.
        """
        categories = [
                ArticleCategory.objects.get_or_create(name=category_name, defaults={"color" : "#808080"})[0]
                for category_name in self._map_categories(self.categories) 
            ]
        
        try:
            media_site = MediaSite.objects.all().filter(scraper=self.scraper).get()
        except Exception as e:
            raise AttributeError(f"Could not find media site related to scraper: {self.scraper}. Error: {e}")

        headline = ArticleHeadline(
            title   = self.title,
            excerpt = self.excerpt,
            url     = self.url,
            datetime    = self._map_datetime(self.date), # TODO Still don't know how to map dates in this site 
            scraped_date = self.scraped_date,
            source  = media_site, 
            image_url   = self.img,
            relevance = self.relevance
        )
        
        return headline, categories
    
    def _map_categories(self, categories : List[str]) -> List[str]:
        """
            Override this function to modify how categories are mapped in your specific site
        """

        return categories

    def _map_datetime(self, datetime_str : str) -> Optional[datetime.datetime]:
        """
            Map from a date in a string to an actual datetime, useful since most sites 
            have dates in natural language and might need a way to map it to a python object
        """
        constants = parsedatetime.Constants(localeID='es', usePyICU=False)
        calendar = parsedatetime.Calendar(constants)
        result, code = calendar.parse(datetime_str)

        # code == 0 means it could not parse the given date
        if code == 0:
            # try to parse in english
            constants = parsedatetime.Constants(localeID='en', usePyICU=False)
            calendar = parsedatetime.Calendar(constants)
            result, code = calendar.parse(datetime_str)
            if code == 0:
                return None 

        return datetime.datetime(*result[:6]) # some magic words