# -*- coding: utf-8 -*-

from scrapy_splash import SplashRequest
from FPP.spiders import *

class IeeeSpider(scrapy.Spider):
    name = 'ieee'
    allowed_domains = ['ieeexplore.ieee.org']
    start_urls = ['http://ieeexplore.ieee.org/']
    words = ['A novel secure data transmission scheme in industrial internet of things']
    header = {

        'User-Agent': USER_AGENT,
    }
    cookie = {
        'ipCheck':'223.146.34.161',
        'fp':'0e57790f8988e6fea0d2370ff7825131',
        'AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg':'1',
        's_cc':'true',
        'TS01dcb973_26':'014082121d65c145c9859743669885f40041bc1c46209bf2b8d13a7294a951900837c44d8eba099acdd92468f9803280a8deb242525923cfefa7c868b10e00798b8d49a057',
        's_fid':'4804E13A0155BAA2-30BFAE72400C5049',
        's_sq':'%5B%5BB%5D%5D',
        'ieeeSSO':'oudaHe+T0WlGk9gnYShdhdowgeYy/r2do/HB6pNce3wUMGWbXkYd1A==',
        'PA.Global_Websession':'eyJ6aXAiOiJERUYiLCJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2Iiwia2lkIjoiOHMiLCJwaS5zcmkiOiJCbXowcElmWlJ0RHpJTzVBNzQ2Smtyb1R1NVkuVGtvIn0..jWwij8JHQFbZThHSly59Iw.j3XgyoAGg5-P2V9YDOBlrE3ECDWFOvaslR9cuNf5X_N4aY4DZT0sjRST1tBdwtxVFLxRnZvjSif0yS73ZvTGSStgFOMIJgJLUyGEqCbyxnVr9dI_F5ba_tGMZMfikjZLeAhpnlvNtcT7XxPSBOZNci-_ytmaIadYmrR-mT2_1IrH3yKabJDI8J-ue9Ye02TsN93UQt20UIBpYP0fqP4zgY__t-WSxFmDtStZRE-AfMb_eDad4NT4Sq5cxQMEUZh2GJ-yEV7QefhCl_iZdK0ZSTL3ugNpFP8XFyuiGOhMSWCo-8zKv51r2AHROHE8LSPGLjg0KnUUyEvHLdBZ8AgdwNvqjZFomoveUnboP9TBW5Zuto0j5JvoXuFYQtZ-cMyJLJewCeDsCYXTJDmt6bPvgOA-BmuE5FczNiyCsSpceN8.U3LN7fSjEQH56M-gtrZ2rw',
        'opentoken':'T1RLAQKAbH1c3hwJJtcBLC10BQK9iPEVDRC1-IygDNkg9bMP0l3TiFG6AACQwgrD7-7W7VW9TewjqcZ3KqBmduHFFH2626P1Wd42iuHfY4juxbhvbb2qxnkH2jEIqpme6thjPbjciquX-TLEwnI7qe6esDS_X98D1iWDaVPOmT6YpF3qIsXW3ZCSo2QzF-_L2fmXw0gNTff_X6GlPMwbW0pFL1Tt83kXuK6KStRaPvHLfSKhMLMvZIrqBMmY',
        'JSESSIONID':'t53o4t0aGrdjKzWsvODdwRXP3nx2hMqob2Kg957GMi0GEgy85Rzx!23286800',
        'ERIGHTS':'L0S2NodFfkOfeLZPfkv4wXnZpi4EF1Z2-18x2d4xxB0v5OF5Zjsoix2BefrHXeAx3Dx3D5bf6FqdfjiRmY2vuQN9bswx3Dx3D-seCuihlon4Yn6ravae9KzQx3Dx3D-x2BoJmAJK1Z3DbmTWzFvGVAAx3Dx3D',
        'WLSESSION':'220357260.20480.0000',
        'TS01dcb973':'012f35062361f3ddf16be361678e145f7407873c7becc75005c895652876933f3ea3bfe842837c88804947e01148c70e5cc02598c337b23f48a0cd2226a059895d7e7587d1678592385ccc6e071f5a6561b7b8b9d2',
        'ieeeUserInfoCookie':'%7B%22userInfoId%22%3A%2296841198%22%2C%22cartItemQty%22%3A0%2C%22name%22%3A%22Tu%20Ruwei%22%2C%22lastUpdated%22%3A8312628598785114270%2C%22env%22%3A%22pr%22%7D',
        'TS01f293bb':'012f35062354227b91ed89632367e55c25a47359a45eb11f9c27633b76e4e12e2ea670558aaa2655f4d5b53d9a0e5aea70e66ab0c03635eb0e319d5161a510057eb407cf04',
        'TS013304a6':'01c1c020dd5a7196eed344876522c09ea4050636b7a362f49ec90d8def646face7afed34f71e40c98154c4ed7aeb71b7852f7523c621f3922603cec66e5d8fa98df65ee68a82e02c94ead5940567c9a43d9d9be7557a5fdc02fc6c2eb535867267f201438d356a4847314436326eb579eb01fb04eef4c404325d70c94fa75a53d171a3b4b25ce8c52b29970678037fd8d95e7a3be884479a1e894b62ba2fcfa667ce29fb386bb4b3fd2aa2681e4844e04469513c554c8ef890260d8aca428bad12ad0f4a0fbb1c7e452248624a26b7f3a76813a653b1ef25e5303e0d279bd3f174a43e08d57250da3d54df25b60c0908face76331ecc800864f30ee20a37b4c7ea6746d9718e4b2546bf2758f6713a7c4edc99392f5be3bc01f2f78b7185b88015ccba10f174e0848bff81127ecb15a0fce0586567b57e2bf85647cf7c1dd045e1580c6a6f3891ffcfdca502231e842e858dc19cd1d281f5c4a603a23980133f1e8c34c9d8',
        'seqId':'7416987',
        'ipList':'223.146.34.161',
        'TS01109a32':'012f3506231e8a6a6aaeb31efa75854813983d438c039aa72427718562a5b6b19860327355ce8e85054aff93fcae5b455bcbc6c2b6e45ab99bfd1fe4e14ec96992620f81fc1e47ae8ebe073edc2d29a3d50d91214406f0b759568b37905bf9882b3e273cef63153c68eba09ec3ac47331a129e31252437db6c14556bbfacdfb2cfc857ed4017c77c5e1db15242e83358536ab223a09905cfce32e7cf4bd78ca29ac23f3b705cbe0b0065b5a748a4e45d17f797de0491d0b9d3c485290a75e225e9204c183e',
        'AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg':'1687686476%7CMCIDTS%7C18389%7CMCMID%7C09974804648066608877849651016791233829%7CMCAID%7CNONE%7CMCOPTOUT-1588757347s%7CNONE%7CvVersion%7C3.0.0',
        'utag_main':'v_id:0171e7e08def00142b4443e892c00307200a906a00c98$_sn:3$_ss:0$_st:1588751948285$vapi_domain:ieee.org$ses_id:1588750034311%3Bexp-session$_pn:2%3Bexp-session'

    }
    def start_requests(self):
        for word in self.words:
            url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText='+re.sub(' ','%20',word)
            print(url)
            yield scrapy.FormRequest(url,method='GET',headers=self.header,cookies=self.cookie,callback=self.parse)
            #yield SplashRequest(url=url,method='GET',args={'wait':10},headers=self.header,cookies=self.cookie,callback=self.parse)
    def parse(self, response):
        print(response.xpath("//body//div[@id='LayoutWrapper']//div[@class='col']//div[contains(@class,'global-content-wrapper')]//xpl-root").extract())
        #print(response.xpath("//div[contains(@class,'List-results-items')]//h2/a[contains(@class,'cyxy-trs-source')]").extract())
