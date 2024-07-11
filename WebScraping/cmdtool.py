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
                    description='python3 <filename> --guided',
                    epilog='Make sure you increase the width of the terminal to make it legible')
	parser.add_argument('-t', '--title', default="movie", help="Title of the movie")
	parser.add_argument('-n', '--review_number', default=0, help="The nth review from the list of scraped reviews")
	parser.add_argument('-c', '--command', choices=["analyze", "graph-polarity", "graph-subjectivity", "general-info"], default="analyze")
	parser.add_argument('-m', '--mode', default="all", choices=["all", "single"])
	parser.add_argument('-g', '--guided', nargs='?', const='')


def __parse_args__():
	__define_arguments__()
	global title, review_num, command, mode, guided
	args = parser.parse_args()
	title = args.title
	review_num = args.review_number
	command = args.command
	mode = args.mode.lower()
	guided = args.guided

def __get_analysis__(mode):
	if guided == None:
		global scrape
		scrape = ScrapeReviews(title)
	sentiment = []
	if mode == "all":
		sentiment = scrape.get_total_sentiment()
	else:
		print(f"Review: {scrape.get_review_text(review_num)}")
		sentiment = scrape.get_review_sentiment(review_num)
	return pd.DataFrame(sentiment, columns =['Sentence', 'Polarity', 'Subjectivity'])

def __general_info__(dataframe):
	if mode == "all":
		mode_here = "Info of all the scraped reviews"
	else:
		mode_here = f"Info of scraped review number {review_num}"
	string = f"Mode: {mode_here}"
	print(f"""
{string}

Movie Title: {title}
Average Polarity: {dataframe["Polarity"].mean()}
Average Subjectivity: {dataframe["Subjectivity"].mean()}
Number of reviews scraped: {scrape.num_of_reviews()}
		""")

def __graph__(dataframe, type_of_graph):
	sns.displot(dataframe[type_of_graph], height= 5, aspect=1.8)
	plt.xlabel(f"Sentence {type_of_graph} (Textblob)")
	plt.show()

def __guided_mode__():
	global title, review_num, command, mode, scrape
	command_array = ["general-info","analyze", "graph-subjectivity", "graph-polarity"]
	print("\nEnter the title of the movie you want to analyze review sentiment of: ", end="")
	title = input()

	scrape = ScrapeReviews(title)

	print("""
Do you want to view:
1. General Info
2. In depth analysis
3. Subjectivity Graph
4. Polarity Graph

Enter (1,2,3,4): """, end="")
	number = input()
	command = command_array[int(number) - 1]


	print("\nDo you want to view review sentiment analysis of all the reviews? (Y/N) ", end="")
	mode = input()
	if mode == "Y":
		print("\nYou stated that you want to view sentiment analysis of all reviews\n")
		mode = "all"
	else:
		print(f"\nYou declined that you want to view sentiment analysis of all reviews.\n\nChose review number (0, {scrape.num_of_reviews()}): ", end="")
		review_num = input()
		mode = "single"

def main():
	__parse_args__()
	if guided != None:
		__guided_mode__()

	df_sentiment = __get_analysis__(mode)

	if command.lower() == "analyze":
		print(df_sentiment)
	
	elif command.lower() == "graph-subjectivity":
		__graph__(df_sentiment, "Subjectivity")
	
	elif command.lower() == "graph-polarity":
		__graph__(df_sentiment, "Polarity")

	elif command.lower() == "general-info":
		__general_info__(df_sentiment)

	else:
		print(f"No command of name {command} found")

if __name__ == "__main__":
	main()