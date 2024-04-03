Authors: Grigolato Giordano, Cischele Matteo, Mastrotto Enrico.
AI Project for social good regarding the AI Course lectured by professor Maria Silvia Pini at DEI (UniPD).

According to data provided by the National Alpine and
Cave Rescue Service , in 2023, over 3,000 mountain rescue
operations were conducted in Italy, with approximately 30
percent involving the search for missing persons. Moreover a problem that merges and often is part of the same
missing cases is the injury risk present in the mountain
environment: data from the Italian Alpine and Speleological
Rescue Service indicate that in 2023, there were over
4,000 reported incidents of mountain injuries , ranging
from minor sprains to more severe trauma with over 60
percent of them occurring due to falls, highlighting the need
for improved safety measures and risk awareness among
outdoor enthusiasts. (CNSAS 2022)

At the same time we also have to cite the always high
number of work-related injuries and deaths: over 1000
workers have sadly lost their lives in the past year. (INAIL
2024) Although these accidents can be caused by a variety
of reasons, explosions and fires remain some of the most
important ones and also remain some of the most solvable
ones: by fully automating the procedure following a fire
breakout the previously said numbers could be cut by an
important percentage. (PagineSicurezza 2024)

The main intuition laying the bases for the work in this paper
comes from the idea of reducing all the numbers previously
cited by creating an application capable of giving out precise
directions based on what the user actually wants, besides going for the shortest or fastest path. One of the first things that
we elaborated was a measure of safety for the multiple nodes
in a map deciding to opt for a point based system: ranging
from 1 to 5 a node can be as safe as possible if talking about
a town, for example, while it can be as risky as possible if
talking about some kind of natural obstacle, such as a swamp
or a room on fire. In the first study case we also designed
a parameter capable of taking into consideration the height
difference between two places, of course trying to make the
most stable path the most desirable: nobody would like to go
up and down in a steep path whenever a more even path can
be accessed. To summarize, the main idea has been to give
users the possibility to orient themselves with a more subjective and safety-centered view while, at the same time giving
them access to natural paths and points of interest otherwise
inaccessible at a first glance on more mainstream applications. Concerning the second study case we instead adapted
the application to make it sensible to the change of fire position, making it more suitable for real life applications.

USE:
LagoCarezza.py and Office.py are different python files to try and execute the applications. Nodes.txt is the database of the lake while Data1 is the database for the office, the user can just read all the points he has the possibilty to choose from those same txt files. There are also some PNGs as references
