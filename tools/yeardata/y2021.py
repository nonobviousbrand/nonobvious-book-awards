"""2021 award data."""
YEAR = 2021
PREV_YEAR, NEXT_YEAR = 2020, 2022
VIDEO_ID = 'QaiCpTSx4g4'
BOOKSHOP = 'https://bookshop.org/lists/2021-non-obvious-book-awards-longlist-selections'

LL_TITLE = 'The 75 Best Non-Fiction Books of 2021.'

HERO_SUB = ("Our most competitive year yet at the time — five winners, ten shortlist selections "
            "and a longlist of the 75 best non-fiction books of 2021, chosen from hundreds of "
            "titles and announced live in December 2021.")

HERO_THEMES = ("The year's biggest themes: the new world of work, shifting power, coming "
               "together as a society, facing an uncertain future, putting yourself first — "
               "and ending bias for good.")

TRENDS_INTRO = ("As part of our judging process, we curate the biggest trends from all "
                "non-fiction books that we evaluated throughout the year. Here are the six "
                "biggest trends we identified from books published during 2021.")
TRENDS_URL = 'https://www.linkedin.com/pulse/6-big-trends-from-2021-non-fiction-books-part-1-newwork-bhargava/'
TRENDS = [
    ("#newwork", "After a year of working virtually, the workplace is becoming more flexible for many people. As the way we work evolves rapidly, finding a better balance between work and life becomes key — and disruption leads to introspection about the dysfunction, nature and future of work itself."),
    ("#powershift", "The corrupt manipulators are winning, and a range of books delves into why and what can be done. As power changes hands, these books tell the story of how it is being reclaimed — and why choice and change remain two of the most popular non-fiction topics for yet another year."),
    ("#comingtogether", "How do we get along and heal our society? These books propose some intriguing theories and answers — helping you understand behavior and language to relate to others, and adopt a more balanced perspective by rejecting outrage and seeking the truth."),
    ("#uncertainfuture", "Save the earth, have more hope and imagine a more positive future. Learn from the distant and recent past to understand and create a better future — and explore the lives and achievements of the geniuses and creators who celebrate innovation."),
    ("#youfirst", "The path to happiness might start by being able to put yourself first. Conquer your imposter syndrome by leaning into doubt and giving yourself more confidence — success comes from learning new skills, focusing on the long term and choosing to always get better."),
    ("#endbias", "How can we end systemic bias that holds people back? These powerful books offer real answers — from achieving pay equity and ending workplace bias to actionable solutions that go beyond conversation to build a more inclusive world."),
]

# 2021: 6 MACRO trends, each explored through 3 micro-trends (writeups transcribed from trend images)
TRENDS_GROUPED = [
    ("#newwork", [
        ("#flexiblework", "After a year of working virtually, the workplace is becoming more flexible for many people."),
        ("#overload", "As the way we work evolves rapidly, finding a better balance between work and life becomes key."),
        ("#howwework", "Disruption leads to introspection and analysis about the dysfunction, nature and future of work itself."),
    ]),
    ("#powershift", [
        ("#corruptwinners", "The corrupt manipulators are winning, and this range of books delves into why and what can be done."),
        ("#reclaimcontrol", "As power changes hands, these books tell the story of how it is being reclaimed and what it means."),
        ("#choice&change", "Choice and change continue to be two of the most popular non-fiction book topics for yet another year."),
    ]),
    ("#comingtogether", [
        ("#healingsociety", "How do we get along and heal our society? These books propose some intriguing theories and answers."),
        ("#understandothers", "These books help you understand behavior and language to relate to others with more success."),
        ("#avoidextremism", "From rejecting outrage to seeking the truth, these books help you adopt a more balanced perspective."),
    ]),
    ("#uncertainfuture", [
        ("#savinghumanity", "Save the earth, have more hope and imagine a more positive future with these books."),
        ("#historylessons", "Learn from the distant and recent past to understand and create a better future."),
        ("#innovators", "Explore the lives and achievements of geniuses and creators in these books that celebrate innovation."),
    ]),
    ("#youfirst", [
        ("#prioritizeyou", "The path to happiness might start by being able to put yourself first, as these books suggest."),
        ("#innervoice", "Conquer your imposter syndrome by leaning into doubt, focusing and giving yourself more confidence."),
        ("#growthmindset", "These authors suggest success comes from learning new skills, focusing on the long term and choosing to always get better."),
    ]),
    ("#endbias", [
        ("#systemsofbias", "How can we end systemic bias that holds people back? These powerful books offer real answers."),
        ("#creatingequity", "Achieving pay equity, ending workplace bias and making the world fairer are what these books focus on."),
        ("#takeaction", "Going beyond just conversation, these actionable books suggest real solutions to build a more inclusive world."),
    ]),
]


# Short summaries (blurb-mode layout)
WINNER_BLURBS = {
    'whenweceasetounderstandtheworld': 'Benjam&iacute;n Labat&uacute;t&rsquo;s genre-defying account of the scientists whose discoveries brushed against madness. It reads like nothing else in the history of our awards.',
    'thinkagain': 'Adam Grant&rsquo;s blockbuster on the power of rethinking: why the smartest people update their views, and how intellectual humility beats being right. A modern classic of useful thinking.',
    'fourlostcities': 'Annalee Newitz tours four vanished metropolises, from &Ccedil;atalh&ouml;y&uuml;k to Cahokia, to uncover why cities die and what our own urban future can learn from theirs.',
    'move': 'Parag Khanna maps the forces of climate, economics and demographics that will make the next decades the most mobile in human history, and predicts where we will all go.',
    'thelonelycentury': 'Economist Noreena Hertz documents how loneliness became a defining condition of our age, reshaping our health, our economies and our politics, and what it takes to reconnect.',
}
SHORTLIST_BLURBS = {
    'backable': 'Suneel Gupta went from serial rejection to raising millions, then reverse-engineered why: people don&rsquo;t back ideas, they back people who make them believe.',
    'dirtywork': 'Eyal Press examines the morally troubling jobs society depends on but refuses to see, from drone operators to slaughterhouse workers, and asks who really bears the ethical cost.',
    'futureproof': 'Kevin Roose&rsquo;s nine rules for being human in the age of automation. Practical optimism for anyone worried about the robots.',
    'ninenastywords': 'Linguist John McWhorter takes profanity seriously, tracing how our forbidden words evolved and what swearing reveals about the way language and taboo actually work.',
    'spite': 'Psychologist Simon McCarthy-Jones explores our strangest motivation: the urge to hurt ourselves just to hurt someone else more, and why spite may secretly serve us.',
    'subtract': 'Engineer Leidy Klotz on the untapped science of less: why our instinct is always to add, and what becomes possible when we subtract instead.',
    'the1619project': 'Nikole Hannah-Jones expands her Pulitzer-winning work into a sweeping reframing of American history that placed slavery and its legacy at the center of the national story.',
    'theworldinaselfie': 'Marco D&rsquo;Eramo&rsquo;s provocative examination of the age of tourism, and what the industry that packages authenticity does to the places and people being visited.',
    'underawhitesky': 'Elizabeth Kolbert reports on the scientists engineering nature to fix the problems we created by engineering nature. Clear-eyed, wry and quietly alarming.',
    'usefuldelusions': 'Hidden Brain host Shankar Vedantam makes the counterintuitive case that self-deception is not always a bug: some illusions hold lives, relationships and societies together.',
}

WINNERS = [
    ("Most Original",     "blue",    "When We Cease to Understand the World", "Benjamin Labatut"),
    ("Most Useful",       "teal",    "Think Again",                           "Adam Grant"),
    ("Most Entertaining", "orange",  "Four Lost Cities",                      "Annalee Newitz"),
    ("Most Shareable",    "magenta", "Move",                                  "Parag Khanna"),
    ("Most Important",    "purple",  "The Lonely Century",                    "Noreena Hertz"),
]

SHORTLIST = [
    ("Backable", "Suneel Gupta with Carlye Adler"),
    ("Dirty Work", "Eyal Press"),
    ("Futureproof", "Kevin Roose"),
    ("Nine Nasty Words", "John McWhorter"),
    ("Spite", "Simon McCarthy-Jones"),
    ("Subtract", "Leidy Klotz"),
    ("The 1619 Project", "Nikole Hannah-Jones"),
    ("The World in a Selfie", "Marco D'Eramo"),
    ("Under a White Sky", "Elizabeth Kolbert"),
    ("Useful Delusions", "Shankar Vedantam and Bill Mesler"),
]

LONGLIST = [
    ("12 Bytes", "Jeanette Winterson"),
    ("An Illustrated Book of Loaded Language", "Ali Almossawi"),
    ("Arriving Today", "Christopher Mims"),
    ("Backable", "Suneel Gupta with Carlye Adler"),
    ("Bad News", "Batya Ungar-Sargon"),
    ("Battle for the Big Top", "Les Standiford"),
    ("Becoming Trader Joe", "Joe Coulombe with Patty Civalleri"),
    ("Beginners", "Tom Vanderbilt"),
    ("Black Futures", "Kimberly Drew"),
    ("Brand Hacks", "Dr. Emmanuel Probst"),
    ("CAPS LOCK", "Ruben Pater"),
    ("Chatter", "Ethan Kross"),
    ("Consumed", "Aja Barber"),
    ("Convergence", "Deb Westphal"),
    ("Corruptible", "Brian Klaas"),
    ("Cultish", "Amanda Montell"),
    ("Digital Body Language", "Erica Dhawan"),
    ("Dirty Work", "Eyal Press"),
    ("Extra Bold", "Ellen Lupton, Jennifer Tobias, Josh Halstead, Leslie Xia, Kaleena Sales, Farah Kafei, and Valentina Vergara"),
    ("Fair Pay", "David Buckmaster"),
    ("Fast Company Innovation by Design", "Stephanie Mehta and the Editors of Fast Company"),
    ("For Brown Girls with Sharp Edges and Tender Hearts", "Prisca Dorcas Mojica Rodriguez"),
    ("Four Lost Cities", "Annalee Newitz"),
    ("Futureproof", "Kevin Roose"),
    ("Fuzz", "Mary Roach"),
    ("High Conflict", "Amanda Ripley"),
    ("Hooked", "Michael Moss"),
    ("How Boards Work", "Dambisa Moyo"),
    ("How the Word Is Passed", "Clint Smith"),
    ("How to Resist Amazon and Why", "Danny Caine"),
    ("Humor, Seriously", "Jennifer Aaker and Naomi Bagdonas"),
    ("Laziness Does Not Exist", "Devon Price"),
    ("Math Without Numbers", "Milo Beckman"),
    ("Mine!", "Michael A. Heller and James Salzman"),
    ("Move", "Parag Khanna"),
    ("Nine Nasty Words", "John McWhorter"),
    ("Peak Mind", "Amishi P. Jha"),
    ("Per My Last Email", "Stephanie K. Wright"),
    ("Play Nice But Win", "Michael Dell"),
    ("Please Scream Inside Your Heart", "Dave Pell"),
    ("Rationality", "Steven Pinker"),
    ("Regeneration", "Paul Hawken"),
    ("Reset", "Johnny C. Taylor Jr."),
    ("Say Less, Get More", "Fotini Iconomopoulos"),
    ("Soundbite", "Sara Harberson"),
    ("Spite", "Simon McCarthy-Jones"),
    ("Subtract", "Leidy Klotz"),
    ("Technically Food", "Larissa Zimberoff"),
    ("The 1619 Project", "Nikole Hannah-Jones"),
    ("The 2000s Made Me Gay", "Grace Perry"),
    ("The Book of Hope", "Jane Goodall and Douglas Abrams"),
    ("The Conversation", "Robert Livingston"),
    ("The Data Detective", "Tim Harford"),
    ("The End of Bias: A Beginning", "Jessica Nordell"),
    ("The High 5 Habit", "Mel Robbins"),
    ("The Lonely Century", "Noreena Hertz"),
    ("The Long Game", "Dorie Clark"),
    ("The Ministry of Common Sense", "Martin Lindstrom"),
    ("The Pop-Up Pitch", "Dan Roam"),
    ("The Power of Nothing to Lose", "William L. Silber"),
    ("The Sea We Swim In", "Frank Rose"),
    ("The Sum of Us", "Heather McGhee"),
    ("The Whiteness of Wealth", "Dorothy A. Brown"),
    ("The Widest Net", "Pamela Slim"),
    ("The World in a Selfie", "Marco D'Eramo"),
    ("Think Again", "Adam Grant"),
    ("This Is How They Tell Me the World Ends", "Nicole Perlroth"),
    ("Trans", "Helen Joyce"),
    ("True Believer", "Abraham Riesman"),
    ("Under a White Sky", "Elizabeth Kolbert"),
    ("Useful Delusions", "Shankar Vedantam and Bill Mesler"),
    ("When We Cease to Understand the World", "Benjamin Labatut"),
    ("Will", "Will Smith"),
    ("Work Won't Love You Back", "Sarah Jaffe"),
    ("You Can't Be Serious", "Kal Penn"),
]

OVERRIDES = {}
