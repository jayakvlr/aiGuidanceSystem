from gensim import corpora, models
import asyncio
from scrapeService import ascrape_playwright
import nltk
from nltk.corpus import stopwords
# Download NLTK stop words data
nltk.download('stopwords')

# Get English stop words list
stop_words = set(stopwords.words('english'))
def topicmodelling():
    # Specify the path to your text file
    file_path = 'data.txt'

    # Open the file and read its contents
    with open(file_path, 'r') as file:
        document = file.read()
    # Tokenize and preprocess the text
    texts = [[word for word in document.lower().split() if word not in stop_words]]


    # Create dictionary and corpus
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Apply LDA model
    lda_model = models.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=20)
    # Get the main topic from the model
    main_topic = lda_model.print_topics()[0][1]

    print("Main Topic:", main_topic)
async def scrape_with_playwright(url: str, tags, **kwargs):

    topicmodelling()




if __name__ == "__main__":
    asyncio.run(scrape_with_playwright(
        url="https://towardsdatascience.com/connecting-datapoints-to-a-road-graph-with-python-efficiently-cb8c6795ad5f",
        tags=["p"]
    ))