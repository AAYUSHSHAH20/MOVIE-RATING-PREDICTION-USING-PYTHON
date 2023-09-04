import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics



def prediction(actor,votes,year):

    df = pd.read_csv("bollywood_full.csv", encoding="utf-8-sig")

    df.drop('tagline',axis = 1)

    df.dropna(subset=['actors'], inplace=True)

    # Read the CSV file
    df = pd.read_csv("bollywood_full.csv", encoding="utf-8-sig")

    # Drop rows with missing actor information
    df.dropna(subset=['actors'], inplace=True)

    # Create a new column with the modified actor names
    df['updated_actors'] = df.apply(lambda row: row['actors'].split('|')[0], axis=1)

    # # Print the new column containing modified actor names
    # print(df['updated_actors'])

    df.drop(columns=['actors'],inplace=True)

    df.drop(['title_x','imdb_id','poster_path','wiki_link','title_y','original_title','runtime','genres','story','summary','tagline','wins_nominations','release_date'],axis=1,inplace = True)

    processed_actors = set()
    data = {"imdb_votes": [votes], "year_of_release": [year],f"updated_actors_{actor}":[1]}
    sum = 0

    for i in range(len(df)):
        try:
            if i >= len(df):
                break

            actor_name = df['updated_actors'][i]
            if actor_name == actor or actor_name in processed_actors:
                continue

            processed_actors.add(actor_name)
            data[f"updated_actors_{actor_name}"] = [0]
            sum = sum + 1
        except:
            sum = sum + 1

    test_data = pd.DataFrame.from_dict(data)

    df = pd.get_dummies(data=df,drop_first=True)

    y = df["imdb_rating"]
    x = df.drop("imdb_rating",axis=1)

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=1)
    # print("x_train:",x_train.shape)
    # print("y_train:",y_train.shape)
    # print("x_test:",x_test.shape)
    # print("y_test:",y_test.shape)

    lm = LinearRegression()
    lm.fit(x_train, y_train)
    y_pred = lm.predict(x_test)

    print(metrics.mean_squared_error(y_test,y_pred))

    predict = lm.predict(test_data)
    return predict[0]  

# actor = input("Enter Actor:")
# votes = int(input("Enter votes:"))
# year = int(input("Enter Year:"))
