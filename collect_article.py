import requests
from datetime import date
import pandas as pd
import plotly.express as px

def getArticle(api_key):
    """
    The function will collect the articles and process them as per the case study
    :param api_key: The authentication required to read the data from API
    :return: two dataframe, one with all information about the articles and other
    with number of articles with date published
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

    # Checking if there is any article which does not contain Justin Trudeau
    #name = df_new[~df_new['body'].str.contains('Justin Trudeau')]
    #print("The number of rows which does not contain Justin Trudeau are: ", name[0])

    # Creating a new column
    df_new["Date"] = pd.to_datetime(df_new["webPublicationDate"]).dt.date

    # Count how many articles about Justin Trudeau have been posted since 01.01.2018 until today
    startdate = pd.to_datetime("2018-01-01").date()
    #today = date.today()

    mask = (df_new['Date'] >= startdate) & (df_new['Date'] <= today)

    df_filter = df_new.loc[mask]
    df_filter = df_filter.sort_values(by='Date')

    # checking total number of articles published in given time range
    print("Total articles published from 01.01.2018 till today: ", df_filter.shape[0])

    # creating a required format of date and article count
    df_filter_count = df_filter.groupby("Date").size().reset_index().rename(columns={
        0: "No. of articles"
    })

    # Calculate the average of all days for the above-mentioned period from “No. of articles”
    print("", df_filter_count["No. of articles"].mean())

    # In which section are most articles written?
    print("The section with most writen article is: ", df_new.sectionName.max())

    # Show the evolution of the "No. of articles" over time for the above period
    # creating the graph
    fig = px.line(df_filter_count, x="Date", y="No. of articles",
                  color_discrete_sequence=["#2377a4"] * len(df_filter_count))

    fig.update_layout(
        plot_bgcolor="#ECECEC",
        yaxis_title="Articles Count",
        title="<b>Evolution of Articles Published</b>"
    )
    # saving the graph
    fig.write_image("article_numbers_" + str(today) +".jpeg")

    # Are there any unusual events in the time series under investigation?
    # Yes, we can see the unsual events in the number of articles pulbished shown by the spikes in the chart.

    # If so, show these. Why are these unusual? (Define for yourself what you want to show by ordinary or
    # unusual).

    # Seeing the articles more than the mean article published
    fig = px.line(df_filter_count, x="Date", y="No. of articles",
                  color_discrete_sequence=["#2377a4"] * len(df_filter_count))

    fig.add_hline(y=df_filter_count["No. of articles"].mean(), line_width=2, line_dash="solid",
                  line_color="#ffd514")

    fig.update_layout(
        plot_bgcolor="#ECECEC",
        yaxis_title="Articles Count",
        title="<b>Mean and total Articles Published</b>"
    )

    fig.show()

    # saving the figure
    fig.write_image("articles_more_than_mean.jpeg")

    # Checking the articles based on outlier detection
    fig = px.box(df_filter_count, x="No. of articles")

    fig.update_layout(
        plot_bgcolor="#ECECEC",
        yaxis_title="Articles Count",
        title="<b>Articles Published Distribution</b>"
    )

    fig.show()
    # saving the figure
    fig.write_image("articles_with_outliers.jpeg")

    # counting articles which comes under outlier category
    outlier_article = df_filter_count[df_filter_count["No. of articles"] > 3]
    print("Total number of time when more than 3 articles were published: ", outlier_article.shape[0])

    # By visual speculation taking article with more than 6 articles per day
    visual_analysis = df_filter_count[df_filter_count["No. of articles"] > 6]
    print("Number of articles with more than 6 articles published daily: ",visual_analysis)

    # Based on question one. Show the cause of the unusual event.
    df_selected = pd.merge(visual_analysis, df_filter, on="Date", how="inner")
    df_section = df_selected[["sectionName", "Date", "No. of articles"]].groupby(["sectionName", "Date"]).agg("count")

    print("Categorization of articles as per the section: ", df_section)


    return df_new, df_filter_count


if __name__ == '__main__':
    today = date.today()
    MY_API_KEY = "API KEY"
    df_new, df_filter_count = getArticle(MY_API_KEY)
    print(df_new.shape)

    # saving the collected data into a csv file
    df_new.to_csv("articles_justin_trudeau_" + str(today) +".csv", index=False)
    df_filter_count.to_csv("number_of_articles_published.csv", index = False)
