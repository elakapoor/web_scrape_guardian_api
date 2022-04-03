import requests
from datetime import date
import pandas as pd
import plotly.express as px
import smtplib
import ssl
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM
from email.mime.image import MIMEImage as MI
import time
import datetime as dt


#### create a automatic scheduler
def getInfo(api_key, subject, receiver_email_address, sender_email_address, sender_password):
    """
    Every day the function will run and read the data from the Guardian API.
    It will process it in dataframe format.
    It will then select the date range and generate the graph. The graph will be saved in the directory.
    And it will be sent to the users in the email list
    :param api_key: The authentication required to read the data from API
    :param subject: The subject of the email to be sent
    :param receiver_email_address: The email address of the receiver
    :param sender_email_address: The email address of the sender
    :param sender_password: The password of the sender

    """
    # taking date as today date i.e the date when the program will run
    today = date.today()

    # specifying api endpoint
    endpoint = "http://content.guardianapis.com/search"

    # specifying the parameters along with the search term
    my_params = {
        'to-date': today,
        'order-by': "relevance",
        'show-fields': 'all',
        'page-size': 100,
        'api-key': api_key,
        "q": "\"Justin Trudeau\""

    }

    # defining the pages for the loop

    current_page = 1
    total_pages = 1

    # creating list to store results
    id_list = []
    headline_list = []
    sectionName_list = []
    webPublicationDate_list = []
    webUrl_list = []
    body_list = []

    # creating the while loop to go over every page
    while current_page <= total_pages:

        try:
            # specifying the current page
            my_params['page'] = current_page

            # creating a get request
            response = requests.get(endpoint, params=my_params).json()

            # selecting items from the page
            for j in response["response"]["results"]:
                id_ = j["id"]
                sectionName = j["sectionName"]
                webPublicationDate = j["webPublicationDate"]
                webUrl = j["webUrl"]
                body = j["fields"]["body"]
                headline = j["fields"]["headline"]

                # second check to select all the articles with the specified keyword only
                if 'Justin Trudeau' in body:

                    # appending all the list
                    id_list.append(id_)
                    webPublicationDate_list.append(webPublicationDate)
                    headline_list.append(headline)
                    webUrl_list.append(webUrl)
                    sectionName_list.append(sectionName)
                    body_list.append(body)

            # incrementing the current page till last page
            current_page += 1

            # calculating total pages containg the search term
            total_pages = response['response']['pages']

        except:
            break

    # dictionary of lists
    dict_ = {'id': id_list, "sectionName": sectionName_list, "webPublicationDate": webPublicationDate_list,
             "webUrl": webUrl_list, 'headline': headline_list, "body": body_list}

    # creating dataframe from the list
    df_new = pd.DataFrame(dict_)

    # creating a new date column
    df_new["Date"] = pd.to_datetime(df_new["webPublicationDate"]).dt.date

    # selecting specified date range
    startdate = pd.to_datetime("2018-01-01").date()
    today = date.today()

    mask = (df_new['Date'] >= startdate) & (df_new['Date'] <= today)

    df_filter = df_new.loc[mask]
    df_filter = df_filter.sort_values(by='Date')

    # creating a required format of date and article count
    df_filter_count = df_filter.groupby("Date").size().reset_index().rename(columns={
        0: "No. of articles"
    })

    # creating the graph
    fig = px.line(df_filter_count, x="Date", y="No. of articles",
                  color_discrete_sequence=["#2377a4"] * len(df_filter_count))

    fig.update_layout(
        plot_bgcolor="#ECECEC",
        yaxis_title="Articles Count",
        title="<b>Evolution of Articles Published</b>"
    )

    # saving the figure in same directory
    fig.write_image("article_numbers_" + str(today) +".jpeg")

    # creating
    receiver = receiver_email_address
    sender = sender_email_address
    sender_password = sender_password
    currnetdate = date.today()

    # create MIMEMultipart object
    msg = MM()
    msg["Subject"] = subject + " " + str(currnetdate)

    # assumes the image is in the current directory
    fp = open("article_numbers_" + str(today) + ".jpeg", 'rb')
    msgImage = MI(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image>')
    msgImage.add_header('Content-Disposition', 'inline', filename='article number')
    msg.attach(msgImage)

    # create the html for the message
    HTML = """
    <html>
        <body>
        <p><b> Number of Articles about Justin Trudeau over Time </b></p>
        </body>
    </html>
    """

    # create HTML MIMEtext object
    MTObj = MT(HTML, "html")

    # attach the MIMEtext object into the message container
    msg.attach(MTObj)

    # create a secure connection over the server and send the email
    # create secure socket layer (SSL) context object
    SSL_context = ssl.create_default_context()

    # create the secure Simple Mail Transfer Protocol (SMTP) connection
    server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, context=SSL_context)

    # login to the email account
    server.login(sender, sender_password)

    # send the email
    for r in receiver:
        server.sendmail(sender, r, msg.as_string())

    server.quit()

if __name__ == '__main__':


    MY_API_KEY = "API KEY"
    subject = "Articles about Canadian Prime Minister Justin Trudeau till"
    receiver_email_address = ["example1@gmail.com", "example2@gmail.com"]
    sender_email_address = "example1@gmail.com"
    sender_password = "example password"

    getInfo(MY_API_KEY, subject, receiver_email_address, sender_email_address, sender_password)
