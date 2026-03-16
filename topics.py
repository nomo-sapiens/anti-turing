import random

TOPICS = [
    "What's the most overrated programming language and why?",
    "Describe your ideal weekend in detail.",
    "What would you do with admin access to the entire internet for one hour?",
    "Is cereal a soup? Defend your position.",
    "What's a hill you'll die on that most people would disagree with?",
    "If you had to give up one sense, which would it be and why?",
    "What's something everyone seems to love that you genuinely don't get?",
    "Describe the perfect meal — every course.",
    "If you could fix one thing about how humans communicate, what would it be?",
    "What animal would make the best coworker and why?",
    "What's a piece of advice you were given that turned out to be wrong?",
    "If you could live in any fictional universe, which and why?",
    "What's the most underrated everyday experience people take for granted?",
    "Hot take: what technology has made human life *worse*?",
    "What would a truly fair society look like to you?",
    "If you could redesign one room in a house from scratch, which and how?",
    "What skill do you wish more people learned as children?",
    "Describe the worst possible job you can imagine.",
    "What's the most interesting thing about the time period you live in?",
    "If you had to live in the same city forever, what would make it bearable?",
    "What's something that seems simple but is actually incredibly complex?",
    "If you woke up with perfect memory, what would be the first thing you'd do?",
]


def get_random_topic() -> str:
    return random.choice(TOPICS)
