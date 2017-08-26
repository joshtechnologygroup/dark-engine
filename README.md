# dark-engine
Search Engine Functionality


Setup Steps
-----------


1. Environment Setup:

        * Create a virtual environment

                mkvirtualenv engine

        * Install the requirements by using command:
            * pip install -r `requirements.txt`

1. Database Setup:

        * Setup a database server and create new Database
        * Copy local.py.template to local.py and Fill in required values

1. Run Migrations:

        python manage.py migrate

1. Install NLP Corpus

    Open Django shell (`python manage.py shell`) and run `import nltk; nltk.download()`
    Download these files:
    * Models -> punkt
    * Corpora -> stopwords
    * Corpora -> wordnet
    * All packages -> averaged_perceptron_tagger

1. To Runserver Locally (Not for Prod or staging):

        python manage.py runserver 8000

        The above command will run the server on port 8000
