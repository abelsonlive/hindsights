```
         _,adP"'\  "Y,                       _____
       ,P"  d"Y,  \  8                  ,adP"""""""Yba,_
     ,d" /,d' `Yb, ,P'              ,adP"'           `""Yba,
     d'   d'    `"""         _,aadP"""""""Ya,             `"Ya,_
     8  | 8              _,adP"'                              `"Ya,
     8    I,           ,dP"           __              "baa,       "Yb,
     I,   Ya         ,db___           `"Yb,      a       `"         `"b,
     `Y, \ Y,      ,d8888888baa8a,_      `"      `"b,                 `"b,
      `Ya, `b,    d8888888888888888b,               "ba,                `8,
        "Ya,`b  ,d8888888888888888888,   d,           `"Ya,_             `Y,
          `Ybd8d8888888888888888888888b, `"Ya,            `""Yba,         `8,
             "Y8888888888888888888888888,   `Yb,               `"Ya        `b
              d8888888888888888888888888b,    `"'            ,    "b,       8,
              888888888888888888888888888b,                  b      "b      `b
              8888888888888888888888888888b    b,_           8       "       8
              I8888888888888888888888888888,    `"Yb,_       `b,             8
               Y888888888888888888888888888I        `Yb,       8,            8
                `Y8888888888888888888888888(          `8,       "b     a    ,P
                  "8888""Y88888888888888888I           `b,       `b    8    d'
                    "Y8b,  "Y888PPY8888888P'            `8,       P    8    8
                        `b   "'  __ `"Y88P'    b,        `Y       "    8    8
                       ""|      =""Y'   d'     `b,                     8    8
                        /         "' |  I       b             ,       ,P   ,P
                       (          _,"  d'       Y,           ,P       "    d'
                        |              I        `b,          d'            8
                        |              I          "         d,d'           8
                        |          ;   `b                  dP"          __,8_
                        |          |    `b                d"     _,,add8888888
                        ",       ,"      `b              d' _,ad88888888888888
                          \,__,a"          ",          _,add888888888888888888

```
hindsights
==========
A simple, lightweight tracker for facebook insights data. 
`hindsights` polls the [facebook graph api](https://developers.facebook.com/docs/reference/api/) every ten minutes and dumps highly comprehensive information about facebook activity on your page(s) to s3.


# installation

## dependencies:
`hindsights` runs off of `boto`, `pyyaml`, `pytz`, and `requests`.  
These are installed as follows:
```
pip install boto
pip install pyyaml
pip install requests
pip install pytz
```

You'll also need the development version of `facepy`, installed as follows:
```
git clone https://github.com/jgorset/facepy.git
cd facepy
sudo python setup.py install
sudo rm -r facepy
cd ..
```

## configuration - `config.yml`
`hindsights` works off of a config file that MUST BE NAMED `config.yml` and in the project's root directory

`config.yml` looks like this:
```
aws_access_key_id: ZZZZZZZZZZZZZZZZZZZZZZ  # YOUR AWS ACCESS KEY ID
aws_secret_access_key: ZZZZZZZZZZZZZZZZZZZZZZ # YOUR AWS ACCESS SECRET ACCESS KEY
fb_app_id: 111111111111111111111 # YOUR FB APP ID (from: https://developers.facebook.com/apps)
fb_app_secret: ZZZZZZZZZZZZZZZZZZZZZZ # YOUR FB APP SECRET (from: https://developers.facebook.com/apps)
fb_page_ids: [    # A list of facebook pages you have insights access to
  my_cool_page_1,
  my_cool_page_2
]
fb_temp_access_token: ZZZZZZZZZZZZZZZZZZZZZZ # A TEMPORARY FB ACCESS TOKEN WITH READ INSIGHTS PRIVELEGES (from: https://developers.facebook.com/tools/explorer/)
s3_bucket: my-cool-bucket # a s3 bucket you've created to deposit data into
time_zone: America/New_York # Your time zone (should be the one that you post facebook messages in)
short_url: .*nyti\.ms.* # OPTIONAL: A regex to match a custom domain shortener 
                        # (the app tries to unshorten most typical shorterning services, 
                        #   but won't know about your special one)
limit: 200 # How many posts do you want to track at a time?
```
Here's a blank one for your convenience:
```
fb_page_ids: []
fb_app_id: 
fb_app_secret: 
fb_temp_access_token:
aws_access_key_id: 
aws_secret_access_key:
s3_bucket: 
time_zone: 
short_url:
limit:
```
After you've generated this config file (remember it must be called `config.yml` and in the project's root directory), 
run this script:
```
python fb.py
```
This will generate a stable access token and insert it into `config.yml`

## crontab
Now just set `hindsights.py` on a cron and you're done!
Make sure to navigate to the `hindsights` directory or it won't be able to find
`config.yml`
```
00,10,20,30,40,50 * * * * cd <path/to/hindsights/dir/> && python hindsights.py 
```

## Sample datum:
```
{"comment": 32, "post_impressions_paid_unique": 0, "post_impressions_paid": 0, "page_likes": 3284819, 
"post_consumptions": 1415, "short_url": "__________________", "post_impressions_viral_unique": 922, 
"share": 45, "datetime": "2013-07-05 16:19:19", "post_negative_feedback": 90, "post_impressions_fan_unique": 88704, 
"year": 2013, "other clicks": 565, "message": "____________________________________.", "link clicks": 850, 
"xbutton": 47, "post_impressions_unique": 96736, "post_impressions_organic_unique": 95744, 
"post_negative_feedback_unique": 47, "other": 1794, "report_spam_clicks": 1, "post_impressions": 260893, 
"post_impressions_fan_paid": 0, "page_id": "_______", "status_type": "shared_story", "hide_clicks": 36, 
"unlike_page_clicks": 3, "timestamp": "1373055559", "post_impressions_fan_paid_unique": 0, 
"post_impressions_fan": 249489, "post_consumptions_unique": 1171, "post_id": "______________________", 
"post_engaged_users": 1291, "link": 36, "post_impressions_viral": 1898, "wkdy": 4, "month": 7, 
"post_story_adds": 257, "day": 5, "minute": 19, "post_impressions_organic": 258995, "like": 180, "hour": 16, 
"url": "___________________", "type": "link", "page_talking_about": 105178, "wknd": 0, "post_stories": 257, 
"post_story_adds_unique": 226, "fan": 56, "post_storytellers": 226, "hide_all_clicks": 3}
```
