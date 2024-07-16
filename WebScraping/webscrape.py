from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from textblob import TextBlob
from selenium.webdriver.chrome.options import Options

class ScrapeReviews:
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36")
	driver = webdriver.Chrome(options=options)

	def __init__(self, query):
		self.query = query
		self.reviews = self.__get_reviews__()

	def __click_best_match__(self):
		# Get search page
		self.driver.get(f"https://www.imdb.com/find/?q={self.query}&ref_=nv_sr_sm")
		try:
			best_match = self.driver.find_element(By.CSS_SELECTOR, "a.ipc-metadata-list-summary-item__t")
			best_match.click()
		except:
			raise Exception(f"No movie of name {self.query} found.")
	
	def __click_review_page__(self):
		self.__click_best_match__()
		try:
			headings_links = self.driver.find_elements(By.CSS_SELECTOR, "a.ipc-title-link-wrapper")
			for heading_link in headings_links:
				try:
					heading_title = heading_link.find_element(By.TAG_NAME, "h3")
					# Dividing the first half and the second half of the heading text
					if heading_title.text.lower().split("\n")[0] == "user reviews":
						self.driver.execute_script("arguments[0].click();", heading_link)
						break
				except:
					pass
		except:
			raise Exception(f"No 'User Reviews' section found for {self.query}.")

	def __get_reviews__(self):
		self.__click_review_page__()
		result = []
		reviews = self.driver.find_elements(By.CSS_SELECTOR, "div.text")
		for review in reviews:
			result.append(review.text)
		return result

	def __calculate_sentiment__(self, review):
		reviews_sentiment = []
		for sentence in review.split(". "):
			if len(sentence.strip("\t\n ")) != 0:
				txt= TextBlob(sentence.strip("\t\n "))
				a= txt.sentiment.polarity
				b= txt.sentiment.subjectivity
				if a != 0:
					reviews_sentiment.append([sentence.strip("\t\n "),a,b])
		return reviews_sentiment

	def num_of_reviews(self):
		return len(self.reviews)

	def get_review_sentiment(self, review_number_str):
		review_number = int(review_number_str)
		num_of_reviews = self.num_of_reviews()
		if review_number > num_of_reviews:
			raise Exception(f"The review number exceeds the total number of reviews which is {num_of_reviews}.")
		review = self.reviews[review_number - 1]
		return self.__calculate_sentiment__(review)

	def get_review_text(self, review_number_str):
		review_number = int(review_number_str)
		num_of_reviews = self.num_of_reviews()
		if review_number > num_of_reviews:
			raise Exception(f"The review number exceeds the total number of reviews which is {num_of_reviews}.")
		return self.reviews[review_number - 1]

	def get_total_sentiment(self):
		review = ". ".join(self.reviews)
		return self.__calculate_sentiment__(review)

