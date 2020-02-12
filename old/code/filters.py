import re

class CrossmodFilters:
    @staticmethod
    def get_urls(input_comment):
         return re.findall('((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)', 
                           input_comment)

    @staticmethod
    def get_subreddit_names(input_comment):
        return re.findall("r/([^\s/]+)", input_comment)

    @staticmethod
    def only_urls_filter(input_comment):
        """Returns True if the comment contains only a list of URLs"""
        urls_in_comment = CrossmodFilters.get_urls(input_comment)
        return len(urls_in_comment) > 0 and len(input_comment) == len(" ".join(urls_in_comment))
    
    @staticmethod
    def any_subreddit_name_filter(input_comment):
        """Returns True if the comment contains any subreddit names"""
        return len(CrossmodFilters.get_subreddit_names(input_comment)) > 0

    @staticmethod
    def only_subreddit_reference_filter(input_comment):
        """Returns True if the comment contains only a subreddit name"""
        # Potentially incomplete, could lead to false positives: for instance: "r/bullshit"
        subreddit_names_in_comment = CrossmodFilters.get_subreddit_names(input_comment)
        return len(subreddit_names_in_comment) == 1 and len(input_comment) == len("r/" + subreddit_names_in_comment[0])

    @staticmethod
    def apply_filters(input_comment):
        filters = [
                   CrossmodFilters.only_urls_filter, 
                   CrossmodFilters.only_subreddit_reference_filter,
                  ]

        for filter in filters:
            if filter(input_comment):
                return True

        return False
  
def main():
    test_input_comments = [ 
                            "add1 http://mit.edu.com you really kind of suck0",
                            "add2 https://facebook.jp.com.2. blah blah bleep bloop nooooo go away",
                            "add3 www.google.be. uvw",
                            "add4 https://www.google.be. 123",
                            "add5 www.website.gov.us test2",
                            "Hey bob on www.test.com." ,
                            "another test with ipv4 http://192.168.1.1/test.jpg. toto2",
                            "website with different port number www.test.com:8080/test.jpg not port 80",
                            "www.website.gov.us/login.html",
                            "test with ipv4 192.168.1.1/test.jpg.",
                            "search at google.co.jp/maps.",
                            "test with ipv6 2001:0db8:0000:85a3:0000:0000:ac1f:8001/test.jpg.",
                            "r/science",
                            "this post was also seen in r/science" 
                            "http://google.com http://youtube.com"
                            ]

    for input_comment in test_input_comments:
        print(CrossmodFilters.apply_filters(input_comment))        

if __name__ == '__main__':
    main()