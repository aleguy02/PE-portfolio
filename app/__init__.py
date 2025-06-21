import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
url = os.getenv("URL")


@app.route("/")
def index():
    work_experience = [
        {
            "title": "Site Reliability Engineering Fellow",
            "meta": {
                "company": "Meta x Major League Hacking",
                "dates": "Jun. 2025 – Sep. 2025",
            },
            "bullets": [
                "Learned SRE best practices from MLH mentors and Meta engineers, on topics such as containerization, CI/CD, monitoring and debugging, deployment, and cloud technologies"
            ],
        },
        {
            "title": "TA - Programming Fundamentals 2",
            "meta": {
                "company": "The University of Florida",
                "dates": "Jan. 2025 – May 2025",
            },
            "bullets": [
                "Led weekly discussions to 30+ students teaching fundamental topics such as debugging, memory management, and basic data structures by creating slides and interactive demos written in C++",
                "Hosted office hours debugging ~7 projects and providing 1:1 assistance to ~10 students every week",
            ],
        },
        {
            "title": "UX/UI Designer",
            "meta": {
                "company": "UF Software Engineering Club",
                "dates": "Sep. 2023 – May 2025",
            },
            "bullets": [
                "Designed and prototyped 19 pages and 18 reusable components in Figma for Clubfinity, a mobile app streamlining club communication, enabling efficient, scalable development for a 6-member engineering team",
                "Collaborated on a team of 4, aligning with 3 other teams in bi-weekly Agile meetings to deliver key UI features",
            ],
        },
    ]
    hobbies = [
        {
            "img": {
                "src": "https://imgs.search.brave.com/v9nR7UvutdGmjnpfRFkWdC50p4KHI89GkefK1lkFPvY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvODQ1/NjU5ODc0L3Bob3Rv/L3BpY2FuaGEtdHJh/ZGl0aW9uYWwtYnJh/emlsaWFuLWJhcmJl/Y3VlLmpwZz9zPTYx/Mng2MTImdz0wJms9/MjAmYz10ekRJRnZh/dFlpODdRS3NibUFk/ei0wajM1NllTSS05/S1VhZjFWZDNSMko4/PQ",
                "alt": "Grilling Picanha",
            },
            "title": "Cooking",
            "one_liner": "Top two things I love to do are: grill picanha, put cherry tomatoes on everything",
        },
        {
            "img": {
                "src": "https://imgs.search.brave.com/ykH8G-8R_soLGwA0Ha1dfIK_y9K7TOdsyFtdoPTJS8A/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tLm1l/ZGlhLWFtYXpvbi5j/b20vaW1hZ2VzL1Mv/YXBsdXMtbWVkaWEt/bGlicmFyeS1zZXJ2/aWNlLW1lZGlhLzVm/M2RlZmJhLWFiMTQt/NGQ0Zi04MmZlLWY0/NDg0OTE3YmY0Yy5f/X0NSMCwwLDE5NDAs/MTIwMF9QVDBfU1g5/NzBfVjFfX18uanBn",
                "alt": "Sketchbook Drawing",
            },
            "title": "Drawing",
            "one_liner": "I keep a sketchbook filled with whatever comes to mind",
        },
        {
            "img": {
                "src": "https://imgs.search.brave.com/ttxYntZW8DMfw4oijWCfQxuYfviXk0GPk3uQXLZNSxo/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pLmV0/c3lzdGF0aWMuY29t/LzE5OTk5ODU0L2Mv/MTUzNS8xNTM1LzE1/LzAvaWwvMzljNGEw/LzU2MjQ1NTY3MDcv/aWxfNjAweDYwMC41/NjI0NTU2NzA3XzQw/dzkuanBn",
                "alt": "Mini Jade Bonsai",
            },
            "title": "Bonsai",
            "one_liner": "Of my 3 bonsai trees, 2 are mini-jades",
        },
    ]

    return render_template(
        "index.html",
        title="Alejandro Villate",
        url=url,
        work_experience=work_experience,
        hobbies=hobbies,
    )
