import json

from contextlib import contextmanager
from httmock import HTTMock, response, urlmatch


class PychexMock(object):
    def __init__(self, http_status=200):
        self.http_status = http_status


class FileMock(PychexMock):
    def build_response(self, file_name=None, content=''):
        if file_name:
            base_path = './features/files/templates/'
            with open('%s%s' % (base_path, file_name), 'rb') as file_obj:
                content = file_obj.read()
        return {'content': content, 'headers': self.headers,
                'status_code': self.http_status}

    @urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
              path=r'.*?Butterfly.gif$')
    def security_image_gif(self, *args):
        """ Mock for the URL that retrieves the Paychex security image """
        self.headers = {'content-type': 'image/gif'}
        return self.build_response('Butterfly.gif')


class HtmlMock(FileMock):
    headers = {'Content-Type': 'text/html; charset=utf-8'}

    @urlmatch(scheme='https', netloc=r'www\.mypaychex\.com$')
    def paychex_start(self, url, request):
        """ Mock requests to the Paychex login page URL """
        # Change the URL since this results in a redirect
        request.url = 'https://landing.paychex.com/ssologin/login.aspx?params'
        res = self.build_response('paychex_login.aspx')
        return response(200, res['content'], res['headers'], None, 5, request)

    @urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
              path=r'.*?ssologin_es$')
    def paychex_benefits_sso(self, *args):
        """ Mock requests to the benefits ssologin_es URL """
        return self.build_response('benefits_ssologin_es.html')

    @urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
              path=r'.*?401kstart$')
    def paychex_401k_start(self, *args):
        """ Mock requests to the retirement app 401kstart URL """
        return self.build_response('401kstart.html')

    @urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
              path=r'.*?LoginForm$')
    def paychex_401k_login(self, *args):
        """ Mock requests to the retirement app LoginForm URL """
        return self.build_response()

    @urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
              path=r'.*?accountSummary$')
    def paychex_401k_summary(self, *args):
        """ Mock requests to the retirement app accountSummary URL """
        return self.build_response('accountSummary.html')

    @urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
              path=r'.*?getBalanceTab$')
    def paychex_401k_balance(self, *args):
        """ Mock requests to the retirement app getBalanceTab URL """
        return self.build_response('getBalanceTab.html')


class XmlMock(FileMock):
    headers = {'content-type': 'application/xml; charset=utf-8'}


class JsonMock(object):
    headers = {'Content-Type': 'text/json; charset=utf-8'}

    def build_response(self, json_dict):
        content = json.dumps(json_dict).encode('utf8')
        return {'headers': self.headers, 'content': content}

    @urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
              path=r'.*?ProcessLogin$')
    def paychex_process_login(self, *args):
        """ Mock requests to the Paychex ProcessLogin URL """
        return self.build_response({'d': '/LandingRedirect.aspx'})


class ContextMock(PychexMock):
    def __init__(self, context):
        super(ContextMock, self).__init__()
        self.context = context


class ContextJsonMock(ContextMock, JsonMock):
    @urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
              path=r'.*?GetSecurityImage$')
    def paychex_security_image(self, *args):
        """
        Mock for the URL that retrieves the Paychex login security image
        """
        return self.build_response({'d': self.context.security_image_path})


class ContextHtmlMock(ContextMock, HtmlMock):
    @urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
              path=r'.*?login\.fcc$')
    def paychex_login(self, *args):
        """ Mock requests to the Paychex login.fcc URL """
        password = None
        if hasattr(self.context, 'paychex'):
            password = self.context.paychex.password
        if not password or password == self.context.password:
            return self.build_response(content='<html></html>')
        else:
            return self.build_response('paychex_login_invalid.fcc')

    @urlmatch(scheme='https', netloc=r'benefits\.paychex\.com',
              path=r'.*?login\.fcc$')
    def paychex_benefits_login(self, *args):
        """ Mock requests to the benefits login.fcc URL """
        password = None
        if hasattr(self.context, 'benefits_online'):
            password = self.context.benefits_online.password
        if not password or password == self.context.password:
            return self.build_response()
        else:
            return self.build_response('benefits_ssologin_es.html')


class ContextXmlMock(ContextMock, XmlMock):
    @urlmatch(scheme='https', netloc=r'landing\.paychex\.com',
              path=r'.*?OneSourceService.asmx$')
    def paychex_account_data(self, *args):
        """
        Mock requests to the Paychex SOAP endpoint for retrieving account data
        """
        postfix = '' if self.context.has_bol else '_no_BOL'
        return self.build_response(
            'GetUserApplicationAccountDataResponse%s.soap.xml' % postfix)


@contextmanager
def mock_request(context, *mock_func):
    """
    Helper method to mock the HTTP request when context.mock_requests is True,
    or otherwise do a real request.
    """

    if context.mock_requests:
        with HTTMock(*mock_func):
            yield
    else:
        yield


@contextmanager
def mock_login_requests(context):
    """ Helper method to mock all requests needed for logging in to paychex """
    with mock_request(context,
                      HtmlMock().paychex_start,
                      ContextJsonMock(context).paychex_security_image,
                      JsonMock().paychex_process_login,
                      ContextHtmlMock(context).paychex_login,
                      HtmlMock().paychex_benefits_sso,
                      ContextHtmlMock(context).paychex_benefits_login):
        yield


@contextmanager
def mock_benefits_requests(context, http_status=200):
    """ Helper to mock all requests made in the get_account_summary method """
    with mock_request(context,
                      HtmlMock(http_status).paychex_401k_start,
                      HtmlMock(http_status).paychex_401k_login,
                      HtmlMock(http_status).paychex_401k_summary,
                      HtmlMock(http_status).paychex_401k_balance):
        yield
