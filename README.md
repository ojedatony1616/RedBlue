# RedBlue
**A political language classifier for news articles**

![RedBlue Word Cloud](results/wordcloud.png)

Here is a [presentation](http://www.slideshare.net/SamGoodgame/redblue-classifier-presentation?ref=https://www.linkedin.com/)
that provides a high-level overview of the project.

Here is a [report](http://www.slideshare.net/SamGoodgame/redblue-classifier-report?ref=https://www.linkedin.com/)
that goes over the entire project in detail.

## Quick Start

This quick start is intended to help you replicate our process.



1. Clone the repository:

    ```
$ git clone https://github.com/samgoodgame/RedBlue.git
$ cd redblue
    ```

2. Create a virtualenv and install the dependencies:

    ```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
    ```

3. Normally, you'd need to run the _dem_parse.py_ and _rep_parse.py_ scripts to
pull the training data from the internet and parse it into useable form. Since this
repository includes the training data in the _/data/debate_data/_ directory, you
don't need to run these scripts.

4. Build the models by running the classification script. Make sure that you modify the script
to pickle the models into the right directory (modify the paths in lines 68, 357, 365, and 371).

    ```
$ cd scripts
$ python classify_svm.py
    ```

    You'll receive a number of different results as your output. The most important
    number is the last one, which is the accuracy of the SVM model.

5. Classify the RSS data. You'll need to go into _predict.py_ and adjust the path to the
dataset (news source) that you wish to analyze, and you'll also need to make sure the
script is pulling the pickled models from the right directory (modify the paths in lines 51 and 81).

    ```
$ python predict.py
    ```

    Your results will appear in your CLI. To see results for each news source, simply redirect
    the _classify_svm.py_ script to run in each news source's directory, under _/data/sources/text/_.

## About

RedBlue is a political language classifier for news articles. It trains a
Support Vector Machine (SVM) algorithm using training data from the 2016 Democratic
and Republican presidential primary debates. It then uses [Baleen](https://github.com/bbengfort/baleen) to ingest RSS feeds into MongoDB, parse the feeds, remove stop words, and vectorize the data.

Once the RSS data is in the proper format (a sparse matrix with words as
features and documents as instances), we pass it to our fitted model, which predicts
if articles are "red" (Republican) or "blue" (Democratic).


## Attribution

We generated our word cloud from an [open-source Python word cloud package](https://github.com/amueller/word_cloud). The words are
from Democratic and Republican presidential primary debates.
