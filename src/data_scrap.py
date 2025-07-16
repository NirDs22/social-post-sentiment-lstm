# data_scrap.py
# This script fetches posts from the "AmItheAsshole" subreddit using PRAW
# It collects posts with specific verdicts and saves them to a CSV file.
import praw
import pandas as pd
import time
from datetime import datetime
import random
from difflib import SequenceMatcher
import re

def create_reddit_instance():
    return praw.Reddit(
        # Create a Reddit instance with your credentials
        user_agent="",
        client_id="",
        client_secret="",
        username="",
        password="",
    )

def clean_text(text):
    """Clean text for comparison by removing common variations"""
    # Convert to lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    # Remove common formatting
    text = re.sub(r'\[.*?\]|\(.*?\)', '', text)
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split())
    return text

def fetch_posts(subreddit_name, verdict_target=6000):
    reddit = create_reddit_instance()
    # in order to override the default search limit, we need to use queries
    # and iterate over them, this is a list of common words that are used in the
    # titles of posts in the AmItheAsshole subreddit, we will use them to
    # search for posts that contain these words in the title
    # this will help us to find more posts that are relevant to the AmItheAsshole subreddit
    # and to avoid duplicates, we will use a set to keep track of the
    # post ids that we have already seen
    queries = [
    'a', 'about', 'accepted', 'advice', 'aita', 'afraid', 'after', 'afternoon', 'again', 'agree', 'ahead', 'am', 'angry',
    'annoyed', 'apartment', 'apologize', 'are', 'argued', 'around', 'arrived', 'ask', 'asked', 'ate', 'away',
    'baby', 'back', 'bad', 'bedroom', 'before', 'began', 'behind', 'believe', 'beside', 'best', 'better',
    'between', 'birthday', 'borrowed', 'boyfriend', 'brother', 'brought', 'bought', 'building', 'busy',
    'called', 'came', 'can', 'car', 'cat', 'celebrate', 'changed', 'children', 'christmas', 'chose', 'choose',
    'city', 'class', 'cleaned', 'close', 'college', 'conflict', 'confused', 'could', 'coworker', 'crazy',
    'decided', 'disagree', 'did', 'dinner', 'discussion', 'do', 'doctor', 'dog', 'done', 'door', 'down',
    'drama', 'dream', 'dressed', 'drink', 'drove', 'during', 'early', 'eaten', 'emotional', 'ended', 'entitled',
    'evening', 'every', 'everyone', 'everything', 'excited', 'expected', 'expensive', 'experience', 'fair',
    'family', 'far', 'father', 'feel', 'felt', 'few', 'fight', 'finally', 'first', 'food', 'for', 'found',
    'friend', 'friends', 'from', 'frustrated', 'fun', 'funny', 'future', 'gave', 'get', 'girlfriend', 'give',
    'good', 'got', 'great', 'had', 'happy', 'hard', 'has', 'have', 'he', 'health', 'hello', 'help', 'helped',
    'her', 'here', 'high', 'him', 'his', 'holiday', 'home', 'hope', 'hospital', 'house', 'how', 'however',
    'hurt', 'husband', 'I', 'if', 'important', 'in', 'inside', 'instead', 'into', 'invited', 'is', 'issue',
    'it', 'jealous', 'job', 'judgment', 'just', 'kids', 'kind', 'kitchen', 'knew', 'know', 'late', 'later',
    'laugh', 'left', 'lent', 'life', 'like', 'liked', 'listen', 'little', 'live', 'lived', 'long', 'looked',
    'love', 'loved', 'mad', 'made', 'make', 'marriage', 'married', 'me', 'meal', 'mean', 'meeting', 'message',
    'met', 'middle', 'might', 'mind', 'mine', 'money', 'month', 'more', 'morning', 'mother', 'move', 'moved',
    'movie', 'much', 'my', 'near', 'need', 'needed', 'neighbor', 'never', 'new', 'next', 'nice', 'night',
    'no', 'normal', 'not', 'now', 'of', 'office', 'oh', 'okay', 'old', 'on', 'once', 'one', 'only', 'opinion',
    'or', 'other', 'our', 'out', 'outside', 'over', 'own', 'paid', 'parents', 'park', 'part', 'partner',
    'party', 'past', 'pet', 'phone', 'picked', 'place', 'plan', 'played', 'please', 'problem', 'put',
    'quick', 'quiet', 'quite', 'random', 'rather', 'read', 'ready', 'reasonable', 'reddit', 'refused',
    'relationship', 'remember', 'right', 'road', 'room', 'rude', 'run', 'sad', 'said', 'same', 'saved',
    'saw', 'say', 'school', 'selfish', 'sent', 'serious', 'she', 'should', 'sister', 'situation', 'small',
    'so', 'sold', 'some', 'someone', 'something', 'soon', 'sorry', 'spent', 'spoke', 'started', 'stay',
    'stayed', 'still', 'stop', 'store', 'story', 'street', 'stress', 'stressed', 'student', 'such',
    'suddenly', 'summer', 'sure', 'take', 'talk', 'talked', 'teacher', 'tell', 'texted', 'than', 'thank',
    'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'think', 'this', 'thought', 'through',
    'time', 'tired', 'to', 'today', 'together', 'told', 'tomorrow', 'tonight', 'too', 'took', 'toward',
    'trip', 'true', 'trust', 'try', 'turned', 'under', 'unfair', 'unreasonable', 'until', 'up', 'upset',
    'us', 'use', 'used', 'vacation', 'very', 'wait', 'walk', 'walked', 'want', 'wanted', 'was', 'watched',
    'way', 'we', 'wedding', 'week', 'weekend', 'well', 'went', 'were', 'what', 'when', 'where', 'whether',
    'which', 'while', 'who', 'why', 'wibtah', 'wife', 'will', 'with', 'within', 'without', 'work', 'worked', 'worried',
    'would', 'wrong', 'year', 'yes', 'yesterday', 'yet', 'you', 'young', 'your', 'yours', 'yourself', 'yourselves'

]

    sort_types = ['hot', 'top', 'relevance', 'new']
    time_filters = ['all', 'year', 'month', 'week']
    flairs = ['Asshole', 'Not the A-hole']
    
    # Track posts and content
    seen_post_ids = set()
    posts_by_flair = {flair: [] for flair in flairs}
    
    # Progress tracking
    start_time = time.time()
    duplicate_count = 0
    
    def print_progress():
        elapsed = time.time() - start_time
        print("\nProgress after {:.1f} minutes:".format(elapsed / 60))
        for flair, posts in posts_by_flair.items():
            print(f"{flair}: {len(posts)}/{verdict_target}")
        print(f"Total unique posts: {sum(len(posts) for posts in posts_by_flair.values())}")
        print(f"Duplicates avoided: {duplicate_count}\n")
    
    try:
        subreddit = reddit.subreddit(subreddit_name)
        
        for query in queries:
            for sort_by in sort_types:
                for time_filter in time_filters:
                    if all(len(posts) >= verdict_target for posts in posts_by_flair.values()):
                        print("\nAll targets reached!")
                        break
                    
                    print(f"\nSearching with: query='{query}', sort={sort_by}, time={time_filter}")
                    
                    try:
                        submissions = subreddit.search(
                            query=query,
                            sort=sort_by,
                            time_filter=time_filter,
                            limit=None
                        )
                        
                        for submission in submissions:
                            # Skip if we've seen this ID
                            if submission.id in seen_post_ids:
                                duplicate_count += 1
                                continue
                            
                            flair = submission.link_flair_text
                            title = submission.title
                            
                            if flair in flairs and len(posts_by_flair[flair]) < verdict_target and 'update' not in title.lower() \
                                    and title.lower() != "[ Removed by Reddit ]":
                                try:
                                    post_data = {
                                        "pid": submission.id,
                                        "title": title,
                                        "post": submission.selftext,
                                        "verdict": flair,
                                    }
                                    
                                    posts_by_flair[flair].append(post_data)
                                    seen_post_ids.add(submission.id)
                                    
                                    print_progress()

                                        
                                except Exception as e:
                                    print(f"Error processing post {submission.id}: {str(e)}")
                            
                            time.sleep(0.1)
                    
                    except Exception as e:
                        print(f"Error during search: {str(e)}")
                        time.sleep(5)
                        continue
        
        # Combine and save results
        all_posts = []
        for flair_posts in posts_by_flair.values():
            all_posts.extend(flair_posts)
        
        df = pd.DataFrame(all_posts)
        filename = f"../data/aita_verdicts_unique_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"\nSaved {len(df)} unique posts to {filename}")
        print(f"Total duplicates avoided: {duplicate_count}")
        
        return df
    
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = fetch_posts("AmItheAsshole")