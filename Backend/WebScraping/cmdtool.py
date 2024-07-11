from webscrape import ScrapeReviews
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import argparse

def __define_arguments__():
	global parser
	parser = argparse.ArgumentParser(
                    prog=""" 
 ____                             
/ ___|  ___ _ __ __ _ _ __  _   _ 
\\___ \\ / __| '__/ _` | '_ \\| | | |
 ___) | (__| | | (_| | |_) | |_| |
|____/ \\___|_|  \\__,_| .__/ \\__, |
                     |_|    |___/ """,
                    description='This program scrapes IMDB and returns sentiment analysis of recent IMDB reviews of the movie.',
                    epilog='Make sure you increase the width of the terminal to make it legible')
	parser.add_argument('-t', '--title', required=True)
	parser.add_argument('-n', '--review_number', default=0)
	parser.add_argument('-c', '--command', choices=["analyze", "graph-polarity", "graph-subjectivity"], default="dataframe")
	parser.add_argument('-m', '--mode', default="all", choices=["all", "single"])

def __parse_args__():
	__define_arguments__()
	global title, review_num, command, mode
	args = parser.parse_args()
	title = args.title
	review_num = args.review_number
	command = args.command
	mode = args.mode.lower()

def __get_dataframe__(mode):
	scrape = ScrapeReviews(title)
	sentiment = []
	if mode == "all":
		sentiment = scrape.get_total_sentiment()
	else:
		sentiment = scrape.get_review_sentiment(review_num)
	return pd.DataFrame(sentiment, columns =['Sentence', 'Polarity', 'Subjectivity'])

def graph(dataframe, type_of_graph):
	sns.displot(dataframe[type_of_graph], height= 5, aspect=1.8)
	plt.xlabel(f"Sentence {type_of_graph} (Textblob)")
	plt.show()

def main():
	__parse_args__()
	df_sentiment = __get_dataframe__(mode)

	if command.lower() == "analyze":
		print(df_sentiment)
	
	elif command.lower() == "graph-subjectivity":
		graph(df_sentiment, "Subjectivity")
	
	elif command.lower() == "graph-polarity":
		graph(df_sentiment, "Polarity")

	elif command.lower() == "general-info":
		__general_info__(df_sentiment)

	else:
		print(f"No command of name {command} found")

if __name__ == "__main__":
	main()