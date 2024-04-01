## What is the HTRC Dataset?
        - stockpile of books where we only get "features" about each book: words (an part-of-speech) appearing on the page in terms of courts, not the original text
        - lots of books: 17mil, multi-lingual

## What is the goal?
        - Determine similarity between every book and every other book


## What are our assumptions?
        - Books that use the same words are more similar than books that do not use the same words

## How do we do it?
        - Compute distance between each book according to the words used
                - When two books use mothly the same words, they wil be closer in distance
        - Gives a "query" book (either one we know about it the dataset or a new one), we can find the most similar books in the dataset

## Why is this challenging?
        - Large dataset, so must make aggressive use of indexes and sampling of data to get insights


## Procedure:
        - Take a random subset (small amount, 1000 books) and determine the most common words from that subset (say, 100k most frequent).
        	- These words ( sorted alphabetically, just to maintain an order) will become he vector columns/dimensions.
        	- Unknowns: Which words are 'good' words to keep? punctuations?: stop words (they/are/or/not/etc.)? Non-english words? Unicode/emoji characters? numbers? 
			- Use stemming / emmatization ( drop plurals, -ing, etc)?
		- save this word ordeing/list to a fie for later quarying.
	- Initialize fais index (blank)
	- Now, for each book:
		- Save book filename / id pair to a file
		- now for each book (in random order to get a good estimate of processing time per book):
		- Open the book's Data file, get the tokens (words) from the file, and make a binary vector representing the words ( from the most common ) that are found in this book
			- Binary = 1 or 0 for each word, not a count).
		- Save the vector into faiss:
			- what is faiss? An efficient vector store that can handle a large number of vectors, and in particular, has effcient algorithms for finding the most similar vectors fiven a query vector.
	- Save faiss index to disk.

## Querying: 
	- receive a book's filename as input, open the file, get the tokens
	- Make the vector using the pre-saved most common word list and ordering
	- Query faisee with this vector, ask for K most similar matches
		- Faiss will typically give you the row id of  the matching books
		- look up the row id in a file you saved ahead o time of book filename/id pair
	- Show the resulting cloest matching books/filenames

