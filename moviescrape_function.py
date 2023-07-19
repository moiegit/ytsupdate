import requests
from bs4 import BeautifulSoup as bs
import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

#--declare variables
url = 'https://yts.mx/browse-movies/0/all/all/0/featured/0/all'
r = requests.get(url)
s = bs(r.content, 'html.parser')
movies = []

#--send email function
def send_email(list_items):
    #--load env
    current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
    envars = current_dir / ".env"
    load_dotenv(envars)
    
    email_sender = os.getenv('EMAIL')
    email_password = os.getenv('PASSWORD')
    email_receiver = os.getenv('RECIPIENT')
    today = date.today()

    subject = f"YTS Movies for {today.strftime('%B %d, %Y')}"
    body = f"""
        <html>
            <head></head>
            <body>
                <h1 style="font-family='Georgia', serif; font-size:40px; text-align:center;">YTS Movies</h1>
                <p>Check out these new movies for the week:</p>
                <ul>
                    <br>
                    {list_items}
                </ul>
                
                <p><i>Check out the full list of movies at <a href="https://yts.mx/browse-movies/0/all/all/0/featured/0/all">YTS featured movies page</a></i></p>
                <br><br>
                <p style="color:green; font-size:10px; text-align:center;">YTS Stay tuned next week for more movies! Credits @YTS</p>
            </body>
        </html>
        """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


#--scrape the latest page of yts
complete_list = s.find('section')
lists = complete_list.find_all('div', class_='browse-movie-bottom')

for movie_title in lists:
    movie_name = movie_title.find('a', class_='browse-movie-title').text
    movie_link = movie_title.find('a').attrs['href']
    movie_year = movie_title.find('div', class_='browse-movie-year').text
    movies.append([movie_name, movie_year, movie_link])

list_items = ''.join(
    f'<li><a href="{movie[2]}">{movie[0]} ({movie[1]})</a></li>'
    for movie in movies
)


send_email(list_items)
