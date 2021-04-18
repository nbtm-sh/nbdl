import requests, mysql.connector, urlgen, youtube_dl, datetime, hashlib

class Backend:
    def __init__(self, sql_username, sql_password, sql_host, sql_database, download_output, content_host):
        self.sqldb = mysql.connector.connect(
            host=sql_host,
            user=sql_username,
            password=sql_password,
            database=sql_database
        )
        self.content_host = content_host
        self.output_dir = download_output
    
    def url_exists(self, url):
        query = f"SELECT count(*) FROM `urls` WHERE contentId='{url}';"
        sql_cursor = self.sqldb.cursor()
        sql_cursor.execute(query)

        sql_result = sql_cursor.fetchall()

        return sql_result[0][0] != 0
    
    def video_exists(self, video_id):
        query = f"SELECT count(*) FROM `urls` WHERE id='{video_id}';"
        print(query)
        sql_cursor = self.sqldb.cursor()
        sql_cursor.execute(query)

        sql_result = sql_cursor.fetchall()

        return sql_result[0][0] != 0

    def add_video(self, video_url, progress_hook=None):
        # Generate URL for the video
        while True:
            vid_url = urlgen.random_string(32)
            # Check if the video URL is already in the database
            if not self.url_exists(vid_url):
                break
        
        vid_int = hashlib.md5(video_url.encode()).hexdigest()
        if self.video_exists(vid_int):
            # get the video content id
            query = f"SELECT `contentId` FROM `urls` WHERE id='{vid_int}';"
            sql_cursor = self.sqldb.cursor()
            sql_cursor.execute(query)

            sql_result = sql_cursor.fetchall()

            return "http://" + self.content_host + "/" + sql_result[0][0]
            
        ytdl = youtube_dl.YoutubeDL({
            'outtmpl': self.output_dir + "/" + vid_url + ".mp4",
            'noplaylist': True
        })
        ytdl.extract_info(video_url, download=True)
        
        date_created = datetime.datetime.now()
        date_expire = date_created + datetime.timedelta(days=365)

        content_file_name = self.output_dir + "/" + vid_url + ".mp4"
        date_created = date_created.strftime('%Y-%m-%d %H:%M:%S')
        date_expire = date_expire.strftime('%Y-%m-%d %H:%M:%S')
        sql = f"INSERT INTO `urls` (`id`, `contentId`, `contentHost`, `dateCreated`, `dateExpire`, `contentFileName`) VALUES (\"{vid_int}\", \"{vid_url}\", \"cdn.nbti.net\", \"{date_created}\", \"{date_expire}\", \"{content_file_name}\");"

        print(sql)

        sql_cursor = self.sqldb.cursor()
        sql_cursor.execute(sql)

        return "http://" + self.content_host + "/" + vid_url
