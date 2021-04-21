import requests, mysql.connector, urlgen, youtube_dl, datetime, hashlib, os.path

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

        self.sql_host = sql_host
        self.sql_username = sql_username
        self.sql_password = sql_password
        self.sql_database = sql_database
    
    def sql_auth_recon(self):
        try:
            sql_cursor = self.sqldb.cursor()
            return True
        except mysql.connector.errors.OperationalError:
            self.sqldb = mysql.connector.connect(
                host=self.sql_host,
                user=self.sql_username,
                password=self.sql_password,
                database=self.sql_database
            )
            return False
    
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
    
    @staticmethod
    def check_if_mkv_version(filename):
        filename_no_ext = '.'.join(filename.split(".")[::-1][1:][::-1])
        filename_mkv = filename_no_ext + ".mkv"

        return filename_mkv if (os.path.isfile(filename_mkv)) else False
        

    def add_video(self, video_url, progress_hook=None):
        # Generate URL for the video
        self.sql_auth_recon()
        while True:
            vid_url = urlgen.random_string(32)
            # Check if the video URL is already in the database
            if not self.url_exists(vid_url):
                break
        
        vid_int = hashlib.md5(video_url.encode()).hexdigest()
        if self.video_exists(vid_int):
            # get the video content id
            query = f"SELECT * FROM `urls` WHERE id='{vid_int}';"
            sql_cursor = self.sqldb.cursor()
            sql_cursor.execute(query)

            sql_result = sql_cursor.fetchall()

            print(sql_result[0])

            return "http://" + self.content_host + "/" + sql_result[0][1] + "." + sql_result[0][5].split(".")[::-1][0]
            
        ytdl = youtube_dl.YoutubeDL({
            'outtmpl': self.output_dir + "/" + vid_url + ".%(ext)s",
            'noplaylist': True
        })
        vx = ytdl.extract_info(video_url, download=True)
        ext = vx["ext"]
        
        date_created = datetime.datetime.now()
        date_expire = date_created + datetime.timedelta(days=365)

        content_file_name = self.output_dir + "/" + vid_url + "." + ext
        if (self.check_if_mkv_version(content_file_name)):
            content_file_name = self.check_if_mkv_version(content_file_name)
            ext = "mkv"
        
        print(content_file_name)
        date_created = date_created.strftime('%Y-%m-%d %H:%M:%S')
        date_expire = date_expire.strftime('%Y-%m-%d %H:%M:%S')
        sql = f"INSERT INTO `urls` (`id`, `contentId`, `contentHost`, `dateCreated`, `dateExpire`, `contentFileName`) VALUES (\"{vid_int}\", \"{vid_url}\", \"cdn.nbti.net\", \"{date_created}\", \"{date_expire}\", \"{content_file_name}\");"

        print(sql)

        sql_cursor = self.sqldb.cursor()
        sql_cursor.execute(sql)

        self.sqldb.commit()

        return "http://" + self.content_host + "/" + vid_url + "." + ext
