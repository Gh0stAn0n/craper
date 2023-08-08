import requests
from bs4 import BeautifulSoup
import re
import sys
import threading
import time
import os

def check_OS():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
check_OS()

def loading_animation():
    symbols = "|/-\\"
    i = 0
    while not loading_animation.done:
        sys.stdout.write(symbols[i % len(symbols)])
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")
        i += 1

def get_gb_value(text):
    gb_pattern = r'(\d+(\.\d+)?)\s*(GB|GBytes|Gigabytes)'
    mb_pattern = r'(\d+(\.\d+)?)\s*(MB|MBytes|Megabytes)'

    gb_match = re.search(gb_pattern, text, re.IGNORECASE)
    mb_match = re.search(mb_pattern, text, re.IGNORECASE)

    if gb_match:
        value_in_gb = float(gb_match.group(1))
        value_in_mb = value_in_gb * 1024  # Convert GB to MB
        return value_in_gb if value_in_gb >= 1024 else value_in_mb

    if mb_match:
        value_in_mb = float(mb_match.group(1))
        return value_in_mb

    return 0

def is_query_present_in_link(raw_query, link):
    pattern = re.compile(r'\b{}\b'.format(re.escape(raw_query)), re.IGNORECASE)
    return bool(pattern.search(link))

def get_course_details(url, new_query):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for 4xx and 5xx status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()

        gb_value = get_gb_value(content)

        return {
            'url': url,
            'gb_value': gb_value,
            'query': new_query
        }

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching {url}: {e}")
        return None

def get_relevant_courses(new_query, raw_query, page_number=1):
    base_urls = [
        "https://freecoursesite.com/page/{page_number}/?s={new_query}",
        "https://gigacourse.com/?s={new_query}",
        "https://courseclub.me/page/{page_number}/?s={new_query}"
    ]
    relevant_courses = []

    try:
        for base_url in base_urls:
            current_page = page_number

            while True:
                url = base_url.format(page_number=current_page, new_query=new_query)
                response = requests.get(url)

                if response.status_code == 404:
                    print(f"Error: {url} not found. Skipping...")
                    break

                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                course_links = [link['href'] for link in soup.select('h2.title a.post-url')]

                if not course_links:
                    break

                for link in course_links:
                    if is_query_present_in_link(raw_query, link):
                        course_data = get_course_details(link, raw_query)
                        if course_data:
                            course_data['page_number'] = current_page
                            relevant_courses.append(course_data)

                next_link = soup.find('a', class_='next')
                if not next_link:
                    break

                current_page += 1

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching {url}: {e}")

    return relevant_courses

def main():
    if len(sys.argv) < 2:
        print("\nPlease provide search queries as arguments.")
        print("\nExample:\n\npython main.py matlab\npython main.py rust-and-crust\n")
        return

    queries = sys.argv[1:]

    for query in queries:
        raw_query = query.replace("*", "").replace("+", "").replace("#", "")
        new_query = query.replace("*", "x").replace("+", "p").replace("#", "sharp")

        changed_characters = [(old_ch, new_ch) for old_ch, new_ch in zip(raw_query, new_query) if old_ch != new_ch]

        for old_ch, _ in changed_characters:
            raw_query = new_query.replace(old_ch, "", 1)

        loading_animation.done = False
        loading_animation_thread = threading.Thread(target=loading_animation)
        print(f"\nSearched query: {query}")
        loading_animation_thread.start()

        try:
            relevant_courses = get_relevant_courses(new_query, raw_query)
        except KeyboardInterrupt:
            loading_animation.done = True
            loading_animation_thread.join()
            sys.exit(0)

        loading_animation.done = True
        loading_animation_thread.join()

        if relevant_courses:
            sorted_courses = sorted(relevant_courses, key=lambda x: x['gb_value'], reverse=True)

            total_courses = len(sorted_courses)
            total_size_gb = sum(course['gb_value'] for course in sorted_courses) / 1024

            print(f"\nTotal courses found: {total_courses}")
            print(f"Total size of courses: {total_size_gb:.2f} GB\n")

            for course in sorted_courses:
                size = course['gb_value'] / 1024 if course['gb_value'] >= 1024 else course['gb_value']
                print(f"Found on Page: {course['page_number']}")
                print(f"Course URL: {course['url']}")
                print(f"Content Size: {size:.2f} GB\n" if course['gb_value'] >= 1024 else f"Size: {size:.2f} MB\n")
        else:
            print(f"No relevant courses found for the search query: {query}")

if __name__ == "__main__":
    main()
