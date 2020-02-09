import crossmod
from crossmod.helpers.filters import CrossmodFilters
from crossmod.ml.classifiers import CrossmodClassifiers

def input_comments_tests():
    input_with_urls = [ "add1 http://mit.edu.com you really kind of suck0",
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
                        "test with ipv6 2001:0db8:0000:85a3:0000:0000:ac1f:8001/test.jpg." ]

    for input_comment in input_with_urls:
        print(CrossmodClassifiers.process_input_comment(input_comment))

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