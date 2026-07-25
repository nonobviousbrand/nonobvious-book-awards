"""2023 award data."""
YEAR = 2023
PREV_YEAR, NEXT_YEAR = 2022, 2024

HERO_SEAL = 'assets/badges/web/seal-inc-2023.png'
PARTNER = {
    'name': 'Inc.',
    'logo': 'assets/partners/inc-logo.svg',
    'url': 'https://www.inc.com/nonobviousbooks',
    'text': 'The 2023 awards were presented as the <b>Inc. Non-Obvious Book Awards</b> &mdash; a full media partnership with Inc. magazine that brought the year&rsquo;s best business books to Inc.&rsquo;s audience of entrepreneurs and business leaders, with the winners and longlist featured on Inc.com.',
}
VIDEO_ID = 'wpZa012owqc'
BOOKSHOP = 'https://bookshop.org/lists/2023-inc-non-obvious-book-awards-longlist-selections'

# Trends report (empty list = section omitted).
HERO_THEMES = "The year's biggest themes: finding the balance between AI and our humanity, redefining good work, celebrating the forgotten foundations of daily life, fixing broken healthcare — and looking beyond happiness itself."

TRENDS_INTRO = ("As part of our judging process, we curate the biggest trends from all the "
                "non-fiction books we evaluate throughout the year. Here are the six biggest "
                "trends we identified from books published during 2023.")
TRENDS_URL = ''
TRENDS = [
    ("#HumanAI", "A wave of AI books all circled one question: how do we find the balance between humanity and artificial intelligence — and teach the technology to respect the humans it serves."),
    ("#GoodWork", "Books about work took a deeper turn this year — intrinsic motivation, what a good job really means, and how we create more good jobs in the world."),
    ("#ForgottenFoundations", "From trees and roads to parking and underwater exploration, these books shined a light on the overlooked foundations of how we live."),
    ("#BrokenHealthcare", "Why is healthcare broken? These books examined the frayed doctor-patient connection, who pays for what, and where the fixing has to start."),
    ("#BeyondHappiness", "Instead of chasing happiness itself, these titles reframed what it takes to be happy — through awe, wonder and even awkwardness."),
    ("#FixTheFuture", "Optimistic books about a future that does not become a dystopia — and what it would actually take to create that future in reality."),
]




# Short summaries (blurb-mode layout)
WINNER_BLURBS = {
    'pockets': 'Hannah Carlson turns an everyday afterthought into a revelatory cultural history: who gets pockets, who doesn&rsquo;t, and what that says about power, gender and design.',
    'outragemachine': 'Tobias Rose-Stockwell maps how social media turned outrage into a business model, and gives readers practical tools to resist the machine and communicate better online.',
    'thetheoryofeverythingelse': 'From the co-host of No Such Thing As A Fish, a joyful tour of the world&rsquo;s weirdest theories and the brilliant eccentrics who believed them.',
    'yourbrainonart': 'Susan Magsamen and Ivy Ross share the new science of neuroaesthetics: how making and experiencing art measurably transforms our brains, bodies and lives.',
    'howbigthingsgetdone': 'Megaproject expert Bent Flyvbjerg distills a lifetime of data on why big projects fail, and the surprising factors behind the rare ones that succeed. Essential for anyone leading anything ambitious.',
}
SHORTLIST_BLURBS = {
    'againsttechnoableism': 'Disabled scholar Ashley Shew dismantles the assumption that technology&rsquo;s job is to &ldquo;fix&rdquo; disabled people. A bracing, funny corrective to how we talk about bodies and tech.',
    'foolmeonce': 'Forensic accounting professor Kelly Richmond Pope has spent a career studying fraud. Here she maps the perpetrators, whistleblowers and victims behind the biggest scams in America.',
    'howworkworks': 'Michelle King decodes the unwritten rules that actually determine who gets ahead at work, the informal systems no employee handbook will ever tell you about.',
    'onceuponatome': 'Antiquarian bookseller Oliver Darkshire&rsquo;s charming, very funny memoir of life in one of London&rsquo;s oldest rare bookshops. A love letter to the strangest corners of the book trade.',
    'pavedparadise': 'Henry Grabar makes parking, yes parking, one of the most fascinating lenses on American life, showing how the quest to store cars shaped our cities, housing and climate.',
    'thefourworkarounds': 'Paulo Savaget studied how scrappy organizations solve impossible problems without permission or resources, then distilled their four repeatable workarounds for the rest of us.',
    'thelongview': 'BBC journalist Richard Fisher argues our civilization&rsquo;s defining flaw is short-termism, and shows how to stretch our thinking across decades and generations.',
    'thestatusrevolution': 'Chuck Thompson&rsquo;s witty investigation of how status flipped: why the old markers of prestige lost their power and what quietly replaced them.',
    'unmaskingai': 'Algorithmic Justice League founder Joy Buolamwini recounts discovering bias baked into facial recognition, and her fight to make AI accountable.',
    'yourstruly': 'Longtime Wall Street Journal obituary writer James R. Hagerty on what writing hundreds of life stories teaches about living one, and how to tell your own before someone else does.',
}

WINNERS = [
    ("Most Original",     "blue",    "Pockets",                     "Hannah Carlson"),
    ("Most Useful",       "teal",    "Outrage Machine",             "Tobias Rose-Stockwell"),
    ("Most Entertaining", "orange",  "The Theory of Everything Else","Dan Schreiber"),
    ("Most Shareable",    "magenta", "Your Brain on Art",           "Susan Magsamen and Ivy Ross"),
    ("Most Important",    "purple",  "How Big Things Get Done",     "Bent Flyvbjerg and Dan Gardner"),
]

SHORTLIST = [
    ("Against Technoableism", "Ashley Shew"),
    ("Fool Me Once", "Kelly Richmond Pope"),
    ("How Work Works", "Michelle P. King, PhD"),
    ("Once Upon a Tome", "Oliver Darkshire"),
    ("Paved Paradise", "Henry Grabar"),
    ("The Four Workarounds", "Paulo Savaget"),
    ("The Long View", "Richard Fisher"),
    ("The Status Revolution", "Chuck Thompson"),
    ("Unmasking AI", "Joy Buolamwini"),
    ("Yours Truly", "James R. Hagerty"),
]

LONGLIST = [
    ("A City on Mars","Zach Weinersmith"),("Afrofuturism","Kevin M. Strait and Kinshasha Holman Conwill"),
    ("Against Technoableism","Ashley Shew"),("Awaken Your Genius","Ozan Varol"),("Back to the Futures","Scott Irwin"),
    ("Big Bets","Rajiv Shah"),("Black Founder","Stacy Spikes"),("Breaking Free","Marcie Bianco"),
    ("Build a Better Business Book","Josh Bernoff"),("Building","Mark Ellison"),("Centered","Kaleena Sales"),
    ("Clear Thinking","Shane Parrish"),("Code to Joy","Michael L. Littman"),("Crossings","Ben Goldfarb"),
    ("Do Interesting","Russell Davies"),("Doppelganger","Naomi Klein"),("Emotional Labor","Rose Hackman"),
    ("Encounterism","Andy Field"),("Everyday Dharma","Suneel Gupta"),("Excellent Advice for Living","Kevin Kelly"),
    ("Extremely Online","Taylor Lorenz"),("Fool Me Once","Kelly Richmond Pope"),("For the Culture","Marcus Collins"),
    ("Generations","Jean M. Twenge"),("Happiness Is Overrated","Cuong Lu"),("Hidden Genius","Polina Marinova Pompliano"),
    ("Hidden Potential","Adam Grant"),("How Big Things Get Done","Bent Flyvbjerg and Dan Gardner"),
    ("How to Make Money","Nafisa Bakkar"),("How to Protect Bookstores","Danny Caine"),
    ("How to Think Like a Woman","Regan Penaluna"),("How to Work with Almost Anyone","Michael Bungay Stanier"),
    ("How Work Works","Michelle P. King"),("I Hope You Fail","Pinky Cole"),("Knowing What We Know","Simon Winchester"),
    ("Look","Christian Madsbjerg"),("Magic Words","Jonah Berger"),("MCU","Gavin Edwards"),("Misbelief","Dan Ariely"),
    ("Mixed Signals","Uri Gneezy"),("More Numbers Every Day","Micael Dahlen"),("NFTs Are a Scam","Bobby Hundreds"),
    ("Nobody's Fool","Christopher Chabris"),("On Being Unreasonable","Kirsty Sedgman"),
    ("Once Upon a Tome","Oliver Darkshire"),("Ordinary Notes","Christina Sharpe"),
    ("Outrage Machine","Tobias Rose-Stockwell"),("Outsmart Your Brain","Daniel T. Willingham"),
    ("Paved Paradise","Henry Grabar"),("Pockets","Hannah Carlson"),("Poverty, by America","Matthew Desmond"),
    ("Quiet Street","Nick McDonell"),("Radical Inclusion","David Moinina Sengeh"),("Reimagine Inclusion","Mita Mallick"),
    ("Right Kind of Wrong","Amy C. Edmondson"),("Saving Time","Jenny Odell"),
    ("Saying No to a Farm-Free Future","Chris Smaje"),("Selfless","Brian Lowery"),("Size","Vaclav Smil"),
    ("Slay the Bully","Rebecca Zung"),("Soul Boom","Rainn Wilson"),("STFU","Dan Lyons"),
    ("The Anxious Achiever","Morra Aarons-Mele"),("The Canceling of the American Mind","Greg Lukianoff"),
    ("The Case for Good Jobs","Zeynep Ton"),("The Coming Wave","Mustafa Suleyman with Michael Bhaskar"),
    ("The Defiant Optimist","Durreen Shahnaz"),("The Four Workarounds","Paulo Savaget"),
    ("The Future Is Disabled","Leah Lakshmi Piepzna-Samarasinha"),
    ("The Future of the Responsible Company","Vincent Stanley with Yvon Chouinard"),
    ("The Golden Screen","Jeff Yang"),("The Identity Trap","Yascha Mounk"),("The Long View","Richard Fisher"),
    ("The PARA Method","Tiago Forte"),("The Perennials","Mauro F. Guillén"),("The Power of Empathy","Michael Tennant"),
    ("The Power of One","Frances Haugen"),("The Power of Saying No","Vanessa Patrick"),
    ("The Power of Wonder","Monica C. Parker"),("The Problem of Twelve","John Coates"),
    ("The Real Work","Adam Gopnik"),("The Right Call","Sally Jenkins"),("The Song of Significance","Seth Godin"),
    ("The Status Revolution","Chuck Thompson"),("The Teachers","Alexandra Robbins"),
    ("The Theory of Everything Else","Dan Schreiber"),("The Wisdom of the Bullfrog","William H. McRaven"),
    ("Turnaround Time","Oscar Munoz"),("Unmasking AI","Joy Buolamwini"),("Upshift","Ben Ramalingam"),
    ("Walking with Sam","Andrew McCarthy"),("What Is ChatGPT Doing","Stephen Wolfram"),
    ("When Race Trumps Merit","Heather Mac Donald"),("Win Every Argument","Mehdi Hasan"),
    ("You Will Own Nothing","Carol Roth"),("Your Brain on Art","Susan Magsamen and Ivy Ross"),
    ("Your Face Belongs to Us","Kashmir Hill"),("Yours Truly","James R. Hagerty"),
]

OVERRIDES = {
    "The Canceling of the American Mind": "thecancelingoftheamericanmind",
    "The Future of the Responsible Company": "thefutureoftheresponsbilecompany",
    "How to Think Like a Woman": "howtothinkinglikeawoman",
    "How to Protect Bookstores": "howtoprotectbookstoresandwhy",
    "What Is ChatGPT Doing": "whatischatgptdoing",
}
