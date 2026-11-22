---
title: Resume and Portfolio
summary: How to write a resume people will want to finish reading and build a portfolio that works for you.
order: 1
duration: 40 min
difficulty: intermediate
tags: resume, portfolio, github, star, job-search
---

Your resume is not an autobiography — it's a marketing document. A recruiter spends 7–10 seconds on the first read before deciding whether to keep going. So your job in those seconds is to show that you solve real problems and know how to drive them to results.

## Resume structure

A classic structure for a Python developer:

- **Header**: name, city, phone, email, links to GitHub and LinkedIn.
- **Summary paragraph**: 2–3 sentences about who you are and what you're looking for.
- **Work experience**: in reverse chronological order.
- **Projects**: a separate block if you have little experience.
- **Skills**: your stack by category, no "knows everything".
- **Education**: briefly, at the end.

## Numbers convince

The most common mistake is "solved tasks", "participated in development". Compare:

- Weak: "Optimized database queries."
- Strong: "Cut report generation time from 12 to 2 seconds by rewriting 3 heavy SQL queries: server load dropped by 35%."

Numbers are proof. Try to put a number in every bullet: a percentage, time, user count, data volume. If you don't remember exact figures, give an estimate ("roughly 2x", "up to 40% lower").

## Action verbs

Start each bullet with a verb: built, implemented, automated, designed, optimized, reduced, set up. Avoid passive phrasing like "was involved in", "was responsible for".

## The STAR method in project descriptions

STAR is a scheme for telling any story: **S**ituation → **T**ask → **A**ction → **R**esult. It will come in handy both in your portfolio and in behavioral interviews — more on that in Lesson 5.

Example:

- S: "The team deployed the service manually; releases took the whole day."
- T: "we needed to automate the rollout."
- A: "I wrote a 6-step CI/CD pipeline on GitHub Actions: tests, build, deploy."
- R: "release time dropped from 6 hours to 15 minutes, and people stopped doing night shifts."

## Tailoring to each vacancy

Don't send the same file to everyone. Highlight the technologies and projects that appear in the vacancy description: recruiters and applicant-tracking systems (ATS) look for keywords. Spend 15–20 minutes adjusting your resume per vacancy.

## What not to include

- Reasons for leaving previous jobs.
- Negativity about former employers.
- Hobbies and personal details (unless related to the profession).
- The phrase "professional qualities: stress resistance" — it proves nothing.
- Lies: any number can be checked at the interview.

## Format

Prepare your resume as a PDF — it opens the same everywhere. A Word file often "drifts" on another computer, while a PDF always looks identical. Length: one page for a junior or mid-level, two for a senior.

## Portfolio

A good portfolio is a tidy GitHub. What it should contain:

- 3–5 best projects, not every experiment;
- a README for each project: why it exists, the stack, how to run it, a usage example, screenshots;
- clean commits with meaningful messages;
- no one else's code without crediting the source.

A portfolio shows initiative: what you do beyond work tasks. For a junior, this is often more important than theory itself. A small lifehack: you can count the words in your resume with a script — you'll write such a script in Task 3.

## Summary

A good resume is specific, full of numbers, tailored to the vacancy, and saved as a PDF. A portfolio is 3–5 well-kept GitHub projects with READMEs. Together, these are your "sales kit" before the interview.

<!--TASK-->
### Task 1
Write a 60–80 word self-introduction, "About me". It should answer three questions: who you are, what your main result is, and what you're looking for. Remove all clichés like "responsible", "communicative", "goal-oriented" — replace them with specifics: stack, years of experience, one standout result with a number. An example for inspiration: "Python developer with 1.5 years of experience: wrote parsers and FastAPI APIs, automated reports, saving the team 10 hours a week. Looking for a backend developer position in a product team." Write your version and check that it fits within 80 words.

### Task 2
Here are three weak resume bullets:

1. "Answered user requests."
2. "Worked with a database."
3. "Participated in developing a new feature."

Rewrite each using the scheme: action verb + what exactly you did + how + a measurable result. If you don't have real numbers, invent plausible but honest estimates. Check that every bullet contains a number or an exact measure, and that the bullet fits on one line.

### Task 3
Write a script `resume_check.py` that checks a resume for required sections. The script reads the file `resume.txt` (UTF-8 encoding) and looks for the keywords in the text: `name`, `contacts`, `skills`, `experience`, `education`. For each section it prints `[OK] Section name` if the word is found and `[MISSING] Section name` if not. At the end, print a summary: the number of sections found out of five. If `resume.txt` doesn't exist, the program should print `File resume.txt not found` and exit.

### Task 4
Create a `README.md` file for one of your projects (real or educational). It should contain these sections: project name, description (2–3 sentences on why it's needed), tech stack, how to run it (commands), a usage example, a screenshot or a hint about where it will live in the repository, and a license. Aim for 5–7 sections. Write it so that someone seeing the project for the first time can run it within two minutes.

### Task 5
Describe three of your projects using the STAR method. For each, write one paragraph: the situation (how it all began), the task (what exactly needed to be done), the actions (what exactly you did), and a result in numbers. If you have no project yet, use an educational one: for example, automating your own routine, a Telegram bot, or a parser. Remember: the result must contain a measurable indicator.

<!--/TASK-->

<!--HINT-->
### Hint 1
Count the words in your draft: in a text, a word is a sequence of letters between spaces or line breaks. Write the text, then put it in a variable and use `split()` to check `len()`. Remove everything that doesn't answer "who am I / what did I do / what am I looking for".

### Hint 2
Use the formula: "[verb] + [what] + [how] + [metric]". For example: "Cut user response time from 3 hours to 20 minutes by introducing auto-replies and triggers in the ticket system." Invent your own metric for each bullet: time, percentage, number of processed requests.

### Hint 3
Read the file with `open("resume.txt", encoding="utf-8")` and `read()`. Convert the text to lowercase with `lower()` so you don't depend on capital letters. Use the `in` operator to check. Don't forget to handle a missing file with `try`/`except FileNotFoundError`.

### Hint 4
A README is Markdown: headings start with `##`, lists with `-`, and code goes in blocks with triple backticks. Prepare the structure in advance: `## Description`, `## Stack`, `## Run`, `## Example`, `## Screenshot`, `## License`. Wrap run commands in a code block so they're easy to copy.

### Hint 5
For each project, answer four questions in a row: "what situation was I in?", "what needed to be done?", "what exactly did I do?", "what measurable result came out?". If you don't remember the exact number, write "approximately", but always with a figure. Build each paragraph as a coherent story, not a list.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
An example of a good self-introduction:

> Python developer with 1.5 years of experience: wrote parsers and REST APIs with FastAPI, automated reporting, saving the team about 10 hours a week. I work confidently with PostgreSQL, Docker, and Git. Looking for a backend developer position in a product team where I can grow to mid-level.

What's going on here? Every sentence contains a fact and specifics: the period ("1.5 years"), the tools ("FastAPI", "PostgreSQL"), the result ("10 hours a week"), and the ask ("a backend developer position"). No clichés: instead of "responsible" — proof of value. If your version is longer than 80 words, trim the technology lists and keep only what matters for the role you want. Check that the text answers the three questions from the task: who you are, what result you have, what you're looking for.

### Solution 2
One way to rewrite them:

1. "Cut user response time from 3 hours to 20 minutes: implemented an auto-reply system and four ticket templates."
2. "Rewrote 5 frequently used SQL queries from JOINs to indexed lookups: execution time dropped from 1.2 s to 80 ms."
3. "Built a personal account in the new feature: authorization, profile, and order history; 2,000 users opened the feature in the first month."

What's going on here? Each bullet starts with an action verb, includes the method ("implemented templates", "rewrote queries"), and a metric ("from 3 hours to 20 minutes", "from 1.2 s to 80 ms"). Numbers make the contribution measurable — that's the main difference from "participated in development". If you don't have real figures, give a careful estimate and be ready to explain it at the interview: "approximately", "about", "up to".

### Solution 3
Solution:

```python
REQUIRED = ["name", "contacts", "skills", "experience", "education"]

try:
    with open("resume.txt", encoding="utf-8") as f:
        text = f.read().lower()
except FileNotFoundError:
    print("File resume.txt not found")
else:
    found = 0
    for section in REQUIRED:
        if section in text:
            print(f"[OK] {section}")
            found += 1
        else:
            print(f"[MISSING] {section}")
    print(f"Sections found: {found} out of {len(REQUIRED)}")
```

Run it:

```bash
python resume_check.py
```

If `resume.txt` contains the words "Name", "Contacts", "Skills", "Experience", "Education", the output will be:

```
[OK] name
[OK] contacts
[OK] skills
[OK] experience
[OK] education
Sections found: 5 out of 5
```

What's going on here? We convert the whole text to lowercase with `lower()` so the word "Name" matches the string `"name"`. The `in` operator searches for a substring. The `try`/`except FileNotFoundError` block handles a missing file gracefully. Such a script is handy to run before sending a resume: it will tell you which sections you forgot.

### Solution 4
An example README structure:

```markdown
# Jobs parser

Collects vacancies from several sites, filters them by keywords,
and saves them to CSV. Saves ~20 minutes of manual searching a day.

## Stack
Python, requests, BeautifulSoup, pandas

## Run
pip install -r requirements.txt
python main.py

## Example
python main.py --role "python developer" --city "Moscow"
The result will appear in the file vacancies.csv

## Screenshot
Example output: `screenshots/demo.png`

## License
MIT
```

What's going on here? A README answers four reader questions: what it is, what it consists of, how to run it, and what you'll see. Code blocks make commands copyable. The screenshot link uses a relative path, so it will work in the repository. If the project has no screenshot, describe the expected output instead — that's useful too.

### Solution 5
An example STAR story for an educational project:

> S: I spent 15 minutes a day manually checking prices in two online stores. T: I needed to automate collecting prices into one table. A: I wrote a Python script with requests and BeautifulSoup: it goes through both sites, extracts the price, and writes it to a CSV file, then runs on a schedule via the task scheduler. R: Checking time dropped to zero, and the data is always fresh; I published the script on GitHub and still use it.

What's going on here? Every STAR element is in place and connected: the situation explains the motivation, the task the goal, the actions the method, the result the value. Numbers ("15 minutes a day", "two sites") make the story concrete. Repeat this scheme for three projects: for each one you'll get a paragraph you can put in your portfolio or tell at an interview.

<!--/SOLUTION-->

<!--QUIZ-->
How much time does a recruiter usually spend on the first read of a resume?
- 7–10 seconds
- 5 minutes
- half an hour
- an hour
* Correct answer: 7–10 seconds
Resumes are skimmed quickly, so important facts should stand out immediately.

Which experience bullet sounds stronger?
- "Answered user requests"
- "Automated application processing: response time dropped from 3 hours to 20 minutes"
- "Helped colleagues"
- "Worked in a ticket system"
* Correct answer: "Automated application processing: response time dropped from 3 hours to 20 minutes"
An action verb, the method, and a measurable result are the most convincing combination.

What does the abbreviation STAR stand for?
- Situation, Task, Action, Result
- Simple, Technical, Advanced, Review
- Start, Test, Apply, Restart
- Script, Type, Answer, Request
* Correct answer: Situation, Task, Action, Result
STAR is a storytelling framework: situation, task, actions, result.

Why tailor your resume to each vacancy?
- To highlight skills relevant to the job and pass ATS filters
- To confuse the recruiter
- Because it's customary, but pointless
- To make the resume longer
* Correct answer: To highlight skills relevant to the job and pass ATS filters
Keywords from the vacancy raise the chance that both a person and an applicant-tracking system will notice your resume.

In what format is it best to send a resume?
- PDF
- DOCX
- TXT
- PNG
* Correct answer: PDF
PDF opens identically on any device and never "drifts" when viewed.

How many projects should you show in your portfolio?
- All of them, even unfinished ones
- Your best 3–5, each with a README
- Just your single best one
- The more, the better
* Correct answer: Your best 3–5, each with a README
A few quality projects make a better impression than dozens of abandoned ones.

What should be in the header of a resume?
- Name, role, contact details, GitHub/LinkedIn links, city
- Age, marital status, hobbies
- Only first and last name
- Passport number
* Correct answer: Name, role, contact details, GitHub/LinkedIn links, city
The header is the most-read part; key information should be visible at a glance.

What is an ATS?
- An applicant tracking system that filters resumes by keywords
- A program for creating PDFs
- A social network for finding jobs
- An email newsletter service
* Correct answer: An applicant tracking system that filters resumes by keywords
ATS parses resumes, so simple formats and keywords increase the chance of reaching a human.

<!--/QUIZ-->
