---
title: Job Search and Growth to Senior
summary: Where to find vacancies, how to run an application funnel, negotiate offers, and chart the path from Junior to Senior.
order: 6
duration: 40 min
difficulty: intermediate
tags: job search, offer, growth, senior, career, negotiation
---

Job hunting is a process that can and should be systematized. If you act chaotically — "I applied a couple of times, silence, so I'm a bad candidate" — it's easy to get discouraged. It's far more reliable to build a funnel: many applications → a few interviews → one or two offers.

## Where to find vacancies

- **Recruiting platforms**: hh.ru, LinkedIn, and niche aggregators.
- **Direct contacts**: write to companies that interest you directly — even if there's no open position, you can offer yourself for the future.
- **Communities**: Telegram chats, meetups, conferences — many vacancies are filled through connections.
- **Career fairs and internships** — a fast entry for juniors.

## The application funnel

The working math: to get one offer, you need roughly 10–15 interviews, and for that — 50–100 applications. So a normal pace is 10–30 applications a week. Don't wait for an answer to each one: many companies go silent, and that's normal.

## Cover letter

A short letter of 3 paragraphs: who you are, why this particular company, and how you can be useful. Don't duplicate your resume — add the "their task ↔ your experience" connection.

## Hiring stages

The typical chain: HR screening → technical interview (language questions) → algorithmic problem → system design (for senior positions) → behavioral interview → offer. Each stage is a filter, and each is prepared for separately.

## Application tracking

Keep a table: company, date, stage, next action, link to the vacancy. Without it, it's easy to lose the thread across a dozen parallel processes. You'll write a tracker script in Task 1.

## Negotiating an offer

When you receive an offer:

1. Thank them and ask for time to think (usually 2–5 days).
2. Evaluate the whole compensation: salary, bonuses, options, training, equipment, remote work.
3. If the number is below your expectation — state your range and argue with market numbers.
4. Don't play a blunt "cold war" between offers — but honestly say you're comparing options.
5. Get the terms in writing before you start.

## Growth: Junior → Middle → Senior

Levels differ not in "amount of knowledge" but in zone of responsibility:

- **Junior**: does tasks under supervision, learns, asks questions.
- **Middle**: autonomously solves medium-sized tasks, takes part in planning, writes maintainable code.
- **Senior**: designs solutions, influences architecture, leads code review, mentors, thinks about business impact.

How to grow: take tasks slightly beyond your comfort zone, ask for feedback, sharpen communication, write articles, give talks, build side projects. Growth is not years but accumulated experience and changing responsibility.

## Summary

Systematic search: 10–30 applications a week, tracking, preparation for each stage, smart negotiations. And growth is conscious work on responsibility, not waiting for "someday I'll become a senior".

<!--TASK-->
### Task 1
Write a script `job_tracker.py` — an application tracker. It stores applications in a JSON file `jobs.json`: each application is a dict with fields `company`, `position`, `date`, `status` (status: sent, interview, offer, rejected). The script works in two modes: with the argument `add` — adds a new application (asks for data from the keyboard), without arguments — prints statistics: the number of applications per status. Use only the standard library.

### Task 2
Write a cover letter (120–180 words) for a fictional vacancy: "Python developer for an analytics team, stack: FastAPI, PostgreSQL, Docker, tasks: data pipelines and internal tools". Structure: greeting, who you are (1–2 sentences), the "company's task ↔ your experience" connection, what you can offer, closing. Don't repeat the resume verbatim.

### Task 3
Make a list of ten of your achievements with numbers: "speed up X by Y%", "automated Z, saving N hours a week", "trained N people". If you have little real experience, use educational projects, internships, volunteering. This is your building material for the resume and for interview answers. Check that every achievement has a number.

### Task 4
Make a 6-month growth plan from Junior to Middle. Break it down by month: for each month, state the goal, the tools (tasks, books, courses, projects), and the criterion by which you'll know the goal is met. At the end, add a list of five signs that you've "grown" to Middle: for example, colleagues come to you for reviews.

### Task 5
Imagine you received two offers. Offer A: salary 180,000 ₽, office work, Django stack, a product service, has a mentor. Offer B: salary 150,000 ₽, remote, FastAPI stack, a fast-growing startup, no mentor. Build a table of five criteria (salary, conditions, stack, growth, team), rate each offer on a 1–5 scale, and compute the total scores. Write which offer you'd choose and why.

<!--/TASK-->

<!--HINT-->
### Hint 1
Use the `json` module for storage: read the file at startup (`load`), append to the end (`dump`). For `add` mode, check `sys.argv`: if `len(sys.argv) > 1` and the argument equals `add` — ask for fields via `input()`. For statistics, count by status with a counter dict. Don't forget to handle the case when the file doesn't exist yet: start with an empty list.

### Hint 2
Start with specifics: "Hi! My name is..." then immediately the connection: "I have experience... and I see it can help your team with...". Mention 2–3 technologies from the stack. End with a sentence about being ready to hop on a call. Count the words: 120–180.

### Hint 3
The achievement formula: "Did X → got Y". Examples: "Set up CI/CD, cutting release time from 6 hours to 15 minutes", "Wrote a parser, saving 10 hours a week". Numbers work for educational projects too: "Built a dataset of 5,000 records". Don't forget the number must be concrete.

### Hint 4
Break the path into months: month 1 — close the gaps in Python and algorithms; month 2 — write 2 side projects and publish them; month 3 — take harder tasks at work/internship; month 4 — take a course on architecture; month 5 — help a beginner or write an article; month 6 — go through interviews and get an offer. Define a criterion for each month.

### Hint 5
You can take these criteria: salary, working conditions (office/remote), how interesting the stack is, growth prospects, team quality. Rate each criterion on a 5-point scale for both offers and sum them up. Don't forget to weigh importance for yourself: if money is critical for you, salary should carry more weight.

<!--/HINT-->

<!--SOLUTION-->
### Solution 1
Solution:

```python
import json
import sys
from datetime import date

FILENAME = "jobs.json"

def load_jobs():
    try:
        with open(FILENAME, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_jobs(jobs):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)

def add_job():
    company = input("Company: ")
    position = input("Position: ")
    status = input("Status (sent/interview/offer/rejected): ")
    jobs = load_jobs()
    jobs.append({"company": company, "position": position,
                 "date": date.today().isoformat(), "status": status})
    save_jobs(jobs)
    print("Application added")

def stats():
    jobs = load_jobs()
    counters = {}
    for job in jobs:
        counters[job["status"]] = counters.get(job["status"], 0) + 1
    if not counters:
        print("No applications yet")
    for status, count in counters.items():
        print(f"{status}: {count}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "add":
        add_job()
    else:
        stats()
```

Run it:

```bash
python job_tracker.py add
python job_tracker.py
```

What's going on here? The script stores applications in JSON — a convenient human-readable format. `load_jobs` reads the file, and if it doesn't exist, returns an empty list. The `add` mode asks for data from the keyboard and appends a record; the no-argument mode prints statistics by status. Such a tracker helps you see the funnel: how many applications were sent, how many reached the interview stage, how many became offers.

### Solution 2
An example cover letter:

> Hi! My name is Alexey, and I'm a Python developer with two years of experience. Your analytics team caught my eye: internal tools and data pipelines are exactly what I did in my last project. I wrote data collectors with FastAPI, designed PostgreSQL databases, and packaged services with Docker. I see that quickly collecting and updating data for analytics matters to you — I have experience cutting report processing time from 3 hours to 20 minutes through query optimization and parallel tasks. I can start right away and understand the current pipelines within the first two weeks. I'd be glad to hop on a call to discuss the details.

What's going on here? The letter is short and specific: greeting, who you are, the "their task ↔ your experience" connection, a result number, and a proposed next step. It doesn't repeat the resume but adds motivation. The main rule: every sentence should move the story forward, not fill space. The tone is confident, without bragging.

### Solution 3
An example achievements list:

1. Set up CI/CD, cutting release time from 6 hours to 15 minutes.
2. Wrote a vacancy parser, saving myself and the team 10 hours a week.
3. Optimized DB queries: API response time dropped by 40%.
4. Built a dataset of 5,000 records for an educational ML project.
5. Automated report generation: eliminated 8 hours of manual work a week.
6. Reviewed 20 pull requests in a month.
7. Trained two interns in the basics of Git and Python.
8. Deployed a service with Docker: environment setup time — 5 minutes instead of an hour.
9. Raised project test coverage from 30% to 75%.
10. Spoke at an internal meetup with a talk about asyncio.

What's going on here? Every achievement follows the "did → got" formula and contains a number. This is your base: from it come resume bullets, STAR stories, and negotiation arguments. If there's no number, figure out how to measure it: time, percentage, count, money. If a numeric metric is impossible, use a fact with volume ("20 pull requests", "two interns").

### Solution 4
A 6-month growth plan:

- **Month 1**: goal — close the gaps: Python, algorithms, SQL. Tools: LeetCode problems (2–3 a week), an SQL course, studying others' solutions. Criterion: you solve easy-medium problems without hints.
- **Month 2**: goal — two side projects on GitHub. Tools: FastAPI or Django, PostgreSQL, Docker, a README for each project. Criterion: repositories are public, run from instructions, have screenshots.
- **Month 3**: goal — harder tasks at work/internship. Tools: ask a mentor to assign tasks beyond your comfort zone. Criterion: you finished two tasks that used to seem too hard.
- **Month 4**: goal — understand architecture. Tools: a book/course on system design, analyzing your project's architecture. Criterion: you can draw a service diagram and explain technology choices.
- **Month 5**: goal — give back. Tools: mentoring a beginner, an article on habr or a Telegram post. Criterion: someone came to you for advice, the article got its first feedback.
- **Month 6**: goal — confirm the level. Tools: interviews at 2–3 companies, collecting feedback. Criterion: you get a Middle offer or feedback like "almost Middle, here's what's missing".

Five signs of Middle: 1) colleagues come to you for reviews; 2) tasks are taken without a detailed spec; 3) you estimate timelines yourself; 4) you influence technology choices; 5) you mentor juniors.

What's going on here? The plan turns abstract "I want to grow" into measurable steps. Every month has a goal, tools, and a criterion. The signs of Middle are not "learned more" but a change in responsibility: people come to you for decisions.

### Solution 5
A table with scores (on a 5-point scale):

| Criterion | Weight | Offer A | Offer B |
|---|---|---|---|
| Salary | 0.3 | 5 (180k) | 3 (150k) |
| Conditions | 0.2 | 3 (office) | 5 (remote) |
| Stack | 0.2 | 3 (Django) | 4 (FastAPI) |
| Growth | 0.15 | 4 (mentor) | 4 (startup) |
| Team | 0.15 | 4 | 3 |

Calculation: A = 0.3·5 + 0.2·3 + 0.2·3 + 0.15·4 + 0.15·4 = 1.5 + 0.6 + 0.6 + 0.6 + 0.6 = 3.9. B = 0.3·3 + 0.2·5 + 0.2·4 + 0.15·4 + 0.15·3 = 0.9 + 1.0 + 0.8 + 0.6 + 0.45 = 3.75.

Conclusion: offer A is slightly ahead thanks to salary and mentoring. But if remote work is critical to you, the weights change, and B can win.

What's going on here? Criteria and weights reflect your priorities, and an honest calculation helps you avoid getting carried away by the emotion "they pay more there". The mentor in offer A is a long-term asset: faster growth, fewer mistakes. And remote saves commute time. This approach makes the decision deliberate, not impulsive.

<!--/SOLUTION-->

<!--QUIZ-->
How many applications a week is a normal pace during an active job search?
- 1–2
- 10–30
- 100–200
- 0
* Correct answer: 10–30
To get one offer you need many applications: 10–30 a week is a working pace.

Why track applications?
- To not lose the thread across dozens of parallel processes
- To show the recruiter
- To spend time
- It's not necessary
* Correct answer: To not lose the thread across dozens of parallel processes
A table with stages and next actions keeps you from forgetting anything.

What's important to do when you receive an offer?
- Agree immediately
- Ask for time to think and evaluate the whole compensation
- State a counter number instantly
- Decline
* Correct answer: Ask for time to think and evaluate the whole compensation
An offer is the start of negotiations: calmly evaluate all conditions, not just salary.

How does a Senior differ from a Junior?
- Zone of responsibility and impact on architecture
- Only salary
- Number of years of experience
- Knowing more libraries
* Correct answer: Zone of responsibility and impact on architecture
Level is about responsibility: design, mentoring, business impact.

What should every resume achievement contain?
- A number or a measurable metric
- Emotional words
- Many adjectives
- Nothing special
* Correct answer: A number or a measurable metric
Numbers make achievements credible: "reduced by 40%", "saved 10 hours".

What's the best thing to do if a company goes silent after your application?
- Send 10 more identical applications to the same company
- Keep applying to other companies and politely follow up from time to time
- Wait and do nothing
- Consider yourself a bad candidate
* Correct answer: Keep applying to other companies and politely follow up from time to time
Silence is normal: keep the funnel wide; after a week or two you can politely follow up.

What should you do if your experience doesn't quite meet the vacancy requirements?
- Apply anyway, honestly highlighting adjacent skills and willingness to learn
- Don't apply at all
- Embellish your resume
- Wait for the perfect vacancy
* Correct answer: Apply anyway, honestly highlighting adjacent skills and willingness to learn
Descriptions often list a wishlist, not a hard threshold; adjacent experience counts too.

Why build a public "brand" — GitHub, articles, talks?
- Employers see your work, and it strengthens your negotiation position
- It fully replaces a resume
- It's mandatory for any position
- It's only for managers
* Correct answer: Employers see your work, and it strengthens your negotiation position
Public artifacts are living proof of skills that works before the interview.

<!--/QUIZ-->
