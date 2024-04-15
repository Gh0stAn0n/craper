# About 'craper'

<p align="center">
   </a>
      <a href="https://github.com/Gh0stAn0n/packdoor">
      <img src="https://img.shields.io/badge/Version-2.0.0-darkgreen">
        <img src="https://img.shields.io/badge/Release%20Date-august%202023-purple">
  <img src="https://shields.io/badge/Python-100%25-066da5">
  <img src="https://shields.io/badge/Platform-Linux/Windows/Mac-darkred">
    </a>
  </p>
</p>

craper (courses scraper) is a Python script that allows users to search and retrieve free courses links from various websites.

The script uses web scraping techniques to extract relevant course information. The user can provide search queries as arguments to find the courses of interest.

### Project features:

Searches for free available courses on the following websites: "freecoursesite.com," "gigacourse.com," and "courseclub.me."

Retrieves course details, including URL and content size (in GB or MB).

Supports multi-threading for faster search and loading animation.

### Usage:

Ensure you have Python 3 or more installed.

Install required dependencies: pip install requests beautifulsoup4.

Run the script with search queries as arguments.

    python3 craper.py Matlab
    python3 craper.py rust-and-crust

### Search multiple queries

    id=1; cat file | while read argv; do if [[ $id -lt 10 ]]; then id=0$id; fi; echo "$id : $argv"; python3 craper.py $argv >> ALL; ((id++)) ;done

![2024-04-11 16_27_51-Kali Linux  Running  - Oracle VM VirtualBox](https://github.com/Gh0stAn0n/craper/assets/102325071/523443f6-d65c-4ed9-a353-cbe3d16f7276)



### Filter using REGEX:



### Updates:

Update 2.0.0 allows the user to search for symbols inside the query.

If C++ was searched before, it would have interfered with the URL, causing it to give false-positive results.

The allowed symbols in the current craper version are: #, *, +, -

### Notes:

This script may rely on the structure of the target websites, so changes to those websites' layouts may affect the script's functionality.
Ensure you comply with the terms of use of the websites being scraped and respect their policies.
The previous mentionned websites propose free courses that were illegally downloaded. using illegal content may be tempting, but it's important to remember that it's against the law and can have serious consequences.
