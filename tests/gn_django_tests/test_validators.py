from django.test import TestCase

from gn_django.validators import YoutubeValidator, GamerNetworkImageValidator, DomainValidator
from django.core.exceptions import ValidationError

class TestYoutubeValidator(TestCase):
    def setUp(self):
        self.validator = YoutubeValidator()
        
    def test_youtube_urls(self):
        self.validator('http://www.youtube.com/watch?v=-wtIMTCHWuI')
        self.validator('http://www.youtube.com/v/-wtIMTCHWuI?version=3&autohide=1')
        self.validator('http://youtu.be/-wtIMTCHWuI')
        self.validator('https://www.youtube.com/embed/M7lc1UVf-VE')

    def test_non_youtube_url(self):
        try:
            self.validator('https://vimeo.com/237568588')
            self.assertTrue(False)
        except ValidationError:
            pass
    
    def test_non_url(self):
        try:
            self.validator('jkhajskdhakjshd')
            self.assertTrue(False)
        except ValidationError:
            pass
    
class TestGNImageValidator(TestCase):
    def setUp(self):
        self.validator = GamerNetworkImageValidator()
        
    def test_cnd_image(self):
        self.validator('https://cdn.gamer-network.net/2017/articles/2017-10-18-14-24/-1508333093795.jpg/EG11/thumbnail/200x200/format/jpg/quality/75')
        
    def test_eg_image(self):
        self.validator('https://images.eurogamer.net/2017/articles/2017-10-18-14-24/-1508333093795.jpg/EG11/thumbnail/200x200/format/jpg/quality/75')
        
    def test_non_gn_image(self):
        try:
            self.validator('https://images-eu.ssl-images-amazon.com/images/I/51Zo0d%2BRxpL._AC_SY200_.jpg')
            self.assertTrue(False)
        except ValidationError:
            pass
    
class TestDomainValidator(TestCase):
    
    def setUp(self):
        self.validator = DomainValidator()
        self.validator_www = DomainValidator(allow_www=True)
    
    def test_valid_slug(self):
        self.validator('eurogamer.net')
        self.validator('rockpapershotgun.com')
        self.validator('google123.co.uk')
        self.validator('gamer-network.net')
        self.validator('jelly.deals')
        self.validator('mail.google.com')
        
    def test_domain_with_protocol(self):
        try:
            self.validator('http://eurogamer.net')
            self.assertTrue(False)
        except ValidationError:
            pass

    def test_domain_with_www_invalid(self):
        try:
            self.validator('www.eurogamer.net')
            self.assertTrue(False)
        except ValidationError:
            pass
            
    def test_domain_with_slug(self):
        try:
            self.validator('eurogamer.net/about-us')
            self.assertTrue(False)
        except ValidationError:
            pass
            
    def test_domain_no_tld(self):
        try:
            self.validator('kjhaskjdhasd')
            self.assertTrue(False)
        except ValidationError:
            pass
            
    def test_domain_hypen_at_end(self):
        try:
            self.validator('somedomain-.net')
            self.assertTrue(False)
        except ValidationError:
            pass

    def test_domain_hypen_at_end(self):
        try:
            self.validator('-somedomain.net')
            self.assertTrue(False)
        except ValidationError:
            pass
            
    def test_allow_www(self):
        self.validator_www('www.eurogamer.net')
