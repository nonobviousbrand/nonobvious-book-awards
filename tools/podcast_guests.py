"""Guests of The Non-Obvious Show (from nonobvious.libsyn.com/rss, eps 1-83).
Used to add LISTEN TO EPISODE buttons for winner/shortlist authors."""

GUESTS = [
    'Sabina Nawaz', 'Nilofer Merchant', 'Mark Medley', 'Jenny Wood', 'Justin Gregg',
    'Nir Eyal', 'Melody Wilding', 'Tim Minshall', 'Kevin Plank', 'Amina AlTai',
    'Rosalind Chow', 'Tomas Chamorro-Premuzic', 'Kevin Ertell', 'Monica Nassif',
    'Eliot Stein', 'Marina Lopes', 'Mita Mallick', 'Minda Harts', 'AJ Wolfe',
    'Henry Coutinho-Mason', 'Simran Jeet Singh', 'Lew Frankfort', 'Ruchika T. Malhotra',
    'Nick Bostrom', 'Ranjay Gulati', 'Charles Melcher', 'Charlie Melcher', 'Dorie Clark',
    'Anne Libera', 'Brad Feld', 'Christopher Wong Michealson', 'Jennifer Tosti-Kharas',
    'Parag Khanna', 'Laura Ries', 'Damali Peterman', 'Tom Nash', 'Michael Tennant',
    'Paco Underhill', 'Sunita Sah', 'Rafi Kohan', 'A.J. Jacobs', 'Charles Duhigg',
    'Michelle P. King', 'Chuck Thompson', 'Ashley Shew', 'Brian Klaas', 'Richard Fisher',
    'Kelly Richmond Pope', 'Paulo Savaget', 'Tobias Rose-Stockwell', 'Michael Bungay Stanier',
    'Bent Flyvbjerg', 'Dan Gardner', 'Hannah Carlson', 'James R. Hagerty', 'Kevin Strait',
    'Marcus Collins', 'Jacquelyn Lane', 'Scott Osman', 'Amy Gallo', 'Zoe Chance',
    'Joey Coleman', 'Dolly Chugh', 'Neil Hoyne', 'The Band of Sisters', 'David Sax',
    'Barry J. Moltz', 'Ellen Lupton', 'Kaleena Sales', 'Valentine Vergara', 'Tom Fishburne',
    'Danielle Friedman', 'Priya Vulchi', 'Winona Guo', 'David W. Campt', 'Jeff Selingo',
    'Emmanuel Probst', 'Deepa Purushothaman', 'Erica Dhawan', 'Suneel Gupta', 'John Ruhlin',
    'Michael Heller', 'Jim Salzman', 'Martin Lindstrom', 'Safi Bahcall', 'Beth Comstock',
    'Daniel H. Pink', 'Guy Kawasaki',
]

import re

def _norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

_NG = [_norm(g) for g in GUESTS]

def was_guest(author_string):
    a = _norm(author_string)
    return any(g in a for g in _NG)
