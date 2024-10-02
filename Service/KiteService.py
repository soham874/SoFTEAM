from Common.log_config import get_logger
from Common.config_reader import ConfigReader
import requests
import json, os, base64
import Common.constants as const

class KiteService:

    def __init__(self,totp = None):
        self.conf = ConfigReader()
        self.log = get_logger(__name__)

        self.__headers = None
        self.__kite_login(totp)

        self.__base_url = 'https://kite.zerodha.com'
        self.__extensions = {
            'holdings' : '/oms/portfolio/holdings',
            'positions' : '/oms/portfolio/positions',
            'orders' : '/oms/orders',
            'margins' : '/oms/user/margins',
            'buy_order' : '/oms/orders/regular',
            'triggers' : '/oms/gtt/triggers'
        }

    def __check_and_load_auth_from_file(self):
        
        if os.path.exists(const.KITE_AUTH_HEADERS):
            self.log.info("Pre-existing auth headers file found, loading")
            with open(const.KITE_AUTH_HEADERS, 'rb') as auth_file:
                encoded_data = auth_file.read()
                decoded_data = base64.b64decode(encoded_data)
                self.__headers = json.loads(decoded_data.decode('utf-8'))
                self.log.info("Auth headers loaded successfully")
                return 'Already logged in, auth headers loaded successfully'
        else:
            self.log.info("Auth file not found, need to authenticate")
            return None
            
    """
    Used to login to Kite. Accepts a 2FA OTP from the Kite app. If already logged in, the cached config will be loaded. If not, new 
    headers will be fetched, cached and loaded
    """
    def __kite_login(self,totp):
        
        res = self.__check_and_load_auth_from_file()

        if res is not None:
            return 
        
        if totp is None:
            raise Exception ('Not already logged in, manual OTP is required to authenticate')
        
        login_creds = {
            'user_id' : self.conf.get_config_from_env_or_file('KITE_USER_ID'),
            'password' : self.conf.get_config_from_env_or_file('KITE_PASSWORD'),
            "twofa_value" : totp
        }

        session = requests.Session() 
        self.log.info("Sending request to Kite to initiate 2FA")

        res1 = session.post(
            'https://kite.zerodha.com/api/login',
            data={
                "user_id": login_creds['user_id'], 
                "password": login_creds['password'], 
                "type": "user_id"}
        ) 
        loginRes = res1.json() 
        
        self.log.info(f"Response received -> {loginRes}")
        if not 200 <= res1.status_code < 300:
            raise Exception (res1.text)

        self.log.info("Sending request to fetch auth header with supplied OTP")

        finalRes = session.post(
            'https://kite.zerodha.com/api/twofa',
            data={
                "user_id": login_creds['user_id'], 
                "request_id": loginRes['data']['request_id'], 
                "twofa_value": login_creds['twofa_value'],
                "twofa_type": 'app_code'
            }
        ) 
        
        self.log.info(f"Response received -> {finalRes.json()}")
        if not 200 <= finalRes.status_code < 300:
            raise Exception (finalRes.text)

        session_info = session.cookies.get_dict()

        self.__headers = {
            "Content-Type" : "application/x-www-form-urlencoded",
            "cookie": f"kf_session={session_info['kf_session']}; __cf_bm={session_info['__cf_bm']}; _cfuvid={session_info['_cfuvid']}; public_token={session_info['public_token']}",
            "Authorization": f"enctoken {session_info['enctoken']}"
        }
        self.log.info("Auth headers cached successfully")

        json_string = json.dumps(self.__headers)
        encoded_data = base64.b64encode(json_string.encode('utf-8'))
        with open(const.KITE_AUTH_HEADERS, 'wb') as file:
            file.write(encoded_data)

        self.log.info("Auth headers fetched and cached successfully")
    
    """
    Generic private function to execute class to Kite backend.
    """
    def __execute_call(self,method,extension,data = None):

        # if self.__headers is None and self.__check_and_load_auth_from_file() is None:
        #     raise Exception ('Required auth headers not found. Please login to Kite first')

        return requests.request(
            method= method,
            url = f"{self.__base_url}{extension}",
            data=data,
            headers=self.__headers
        ).json()
    
    """
    Fetch different information from Kite profile
    """
    def execute_method(self,method):

        self.log.info(f"Fetching data for {method}")
        
        extension = self.__extensions[method]
        if extension is None:
            raise Exception (f'Requested method -> {method} does not have an extension registered')

        return self.__execute_call(
            method="GET",
            extension=extension
        )