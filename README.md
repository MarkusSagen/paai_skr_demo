
## Setup

1. Create Virtual environment

   ```shell
   pyenv virtualenv 3.8.5 skr
   ```

2. Install pre-requisites:

   ```shell
   git clone git@github.com:Peltarion/ai_skr_qa.git
   cd ai_skr_qa
   # pyenv local skr
   pip install -r requirements.txt
   ```

## Run the demo

1. Start the demo application

  ```
  streamlit run app.py
  ```

## Download PDFs and create topic model

1. Follow the setup instructions above
2. Download Swedish stopwords
   # Download  stopwords
   python -m nltk.downloader stopwords
   python -c "import stanza;stanza.download('sv')"
   ```

3. Download all the library plans and place as pandas DataFrames:

   ```shell
   python scraper/scrape.py
   python convert/pdf.py
   ```

4. Some of the PDFs are for some reason not saved correctly to the right format when one tries to open then. But have currently left that for a later date.

5. Create a topic model

  ```shell
  python topics/model.py \
      --input_dataframe biblioteksplaner.csv
      --model_name kb
      --num_topics 50
      --output models
  ```

6. Run the streamlit application
  ```shell
  streamlit run app.py
  ```

## Notes:
- mp seem slightly better than kb as topic models
- For deployment:
  - Don't save embedding model for BERTopic
  - Don't load the embedding model
  - Ensure python version >= 3.8

## DONE:
- [ ] Download most of the PDFs and made list of which ones are missing
- [ ] Create and compare different topic models
- [ ] Initial preprocessing of text
- [ ] Create stopwords splitter based on Swedish language
- [ ] Save and load the BERTopic model, topics, probs etc.
- [ ] Started with Streamlit application
- [ ] Multiselect on regions
- [ ] Style with custom css sheets
- [ ] Added custom stopwords (per, ska)
- [ ] Remove topcics
- [ ] Load and prepare topics_per_class
- [ ] Script for running and creating multiple different topic models
- [ ] Prep for doing lemmatization later
- [ ] Allow filtering the text based on region and topics
- [ ] Add option to filter in sidebar
- [ ] Adjust colors, layout, format, and functions (streamlit, css, javascript)

## Next Steps:
- [ ] Make region and municipalities plots
- [ ] Re-run and get feedback from Annika
- [ ] Add option to reset the multiselect bars in filter
- [ ] Do lemmatization and find the best topics
- [ ] Continue to clean up the text
- [ ] Load two different models (50 and 20 topics)
- [ ] Lemmatization in Swedish

  Example of using stanza
   ```
  nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma')
  doc = nlp('Barack Obama was born in Hawaii.')
  print(*[f'word: {word.text+" "}\tlemma: {word.lemma}' for sent in doc.sentences for word in sent.words], sep='\n')
  ```

## TODO:
- Find PDFs not downloaded correctly - check: `text/html` and add those PDFs
- Skip converting PDFs not with correct encoding to show up!
- Allow filtering based on more parameters (municiplaities, region size)
- Filtering should have a cut-off point to make searching faster
- Aggregate / Summarize / Cluster the most similar answers fond across documents.
- Remove weblinks in text (beautiful soup)
- Allow `annotated_text` to take in markdown for links and clickable buttons
- Remove Hashtags, weblinks, bulletpoints etc.
- Hyperparameter tune the topic models
