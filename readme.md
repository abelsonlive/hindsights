hindsights
==========
A simple, lightweight tracker for facebook insights data.

## Dependencies:
`hindsights` runs off of `boto`, `facepy`, and `requests`.  You'll need the development version of `facepy`, installed as follows:
```
git clone https://github.com/jgorset/facepy.git
cd facepy
sudo python setup.py install
sudo rm -r facepy
cd ..
```

## Configuration - `config.yml`
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
short_url: .*nyti\.ms.* # OPTIONAL: A regex to match a custom domain shortener (the app tries to unshorten most typical shorterning services)
limit: 200 # How many posts do you want to track at a time?
```

After you've generated this config file (remember it must be called `config.yml` and in the project's root directory), run this script:
```
python fb.py
```
This will generate a stable access token and insert it into `config.yml`

## CRON
Now just set `hindsights.py` on a cron and your done!
```
00,10,20,30,40,50 * * * * cd <hindsights directory> && python hindsights.py 
```