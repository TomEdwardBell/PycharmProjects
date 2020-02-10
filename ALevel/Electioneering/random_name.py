import random


def full():
    return first() + ' ' + last()


def first():
    firsts = ['Michael', 'Christopher', 'James', 'David', 'John', 'Robert', 'Jason', 'Brian', 'William', 'Matthew', 'Scott', 'Joseph', 'Kevin', 'Richard', 'Daniel', 'Eric', 'Jeffrey', 'Mark', 'Steven', 'Thomas', 'Timothy', 'Anthony', 'Charles', 'Paul', 'Chad', 'Gregory', 'Kenneth', 'Shawn', 'Stephen', 'Andrew', 'Todd', 'Ronald', 'Sean', 'Edward', 'Patrick', 'Donald', 'Jonathan', 'Keith', 'Ryan', 'Aaron', 'Gary', 'Jeremy', 'Douglas', 'George', 'Bryan', 'Craig', 'Larry', 'Peter', 'Troy', 'Jose', 'Adam', 'Dennis', 'Jerry', 'Raymond', 'Shane', 'Frank', 'Travis', 'Jeffery', 'Joshua', 'Justin', 'Bradley', 'Terry', 'Brandon', 'Benjamin', 'Rodney', 'Samuel', 'Derek', 'Tony', 'Russell', 'Randy', 'Marcus', 'Jamie', 'Juan', 'Johnny', 'Brent', 'Joel', 'Roger', 'Phillip', 'Nathan', 'Brett', 'Chris', 'Billy', 'Marc', 'Carlos', 'Carl', 'Erik', 'Danny', 'Jesse', 'Jon', 'Bobby', 'Derrick', 'Curtis', 'Antonio', 'Shannon', 'Corey', 'Christian', 'Jimmy', 'Walter', 'Nicholas', 'Lawrence', 'Joe', 'Gerald', 'Wayne', 'Philip', 'Vincent', 'Darren', 'Victor', 'Micheal', 'Willie', 'Alan', 'Tracy', 'Albert', 'Roy', 'Kyle', 'Frederick', 'Jay', 'Martin', 'Henry', 'Arthur', 'Randall', 'Bruce', 'Darrell', 'Allen', 'Luis', 'Lee', 'Lance', 'Ricky', 'Andre', 'Alexander', 'Louis', 'Dale', 'Harold', 'Ronnie', 'Glenn', 'Jermaine', 'Cory', 'Damon', 'Mario', 'Kelly', 'Gabriel', 'Reginald', 'Jack', 'Steve', 'Tyrone', 'Eugene', 'Tommy', 'Ernest', 'Barry', 'Brad', 'Eddie', 'Leonard', 'Manuel', 'Ricardo', 'Wesley', 'Dean', 'Jacob', 'Duane', 'Adrian', 'Ralph', 'Maurice', 'Jesus', 'Marvin', 'Dwayne', 'Kurt', 'Dustin', 'Jerome', 'Jeff', 'Howard', 'Clinton', 'Stanley', 'Melvin', 'Calvin', 'Greg', 'Miguel', 'Theodore', 'Roberto', 'Edwin', 'Mike', 'Mitchell', 'Kirk', 'Jody', 'Francisco', 'Harry', 'Ruben', 'Neil', 'Clifford', 'Jared', 'Earl', 'Ian', 'Heath', 'Clarence', 'Nathaniel', 'Daryl', 'Jorge', 'Casey', 'Alex', 'Ray', 'Norman', 'Karl', 'Alfred', 'Terrence', 'Glen', 'Darin', 'Hector', 'Oscar', 'Terrance', 'Lonnie', 'Trevor', 'Warren', 'Geoffrey', 'Wade', 'Bernard', 'Raul', 'Fred', 'Lamont', 'Dana', 'Leon', 'Marlon', 'Jaime', 'Ramon', 'Zachary', 'Francis', 'Don', 'Gilbert', 'Angel', 'Shaun', 'Byron', 'Fredrick', 'Roderick', 'Clayton', 'Franklin', 'Rafael', 'Leroy', 'Stacy', 'Clint', 'Mathew', 'Joey', 'Darryl', 'Javier', 'Cedric', 'Toby', 'Alvin', 'Kelvin', 'Seth', 'Vernon', 'Donnie', 'Darrin', 'Pedro', 'Leslie', 'Tyler', 'Isaac', 'Herbert', 'Lewis', 'Kent', 'Fernando', 'Armando', 'Dwight', 'Andy', 'Rene', 'Scotty', 'Jessie', 'Lloyd', 'Erick', 'Gene', 'Kerry', 'Tim', 'Guy', 'Marco', 'Gordon', 'Bryant', 'Kristopher', 'Eduardo', 'Trent', 'Jim', 'Ross', 'Alejandro', 'Ivan', 'Johnnie', 'Bill', 'Rick', 'Dan', 'Jackie', 'Alberto', 'Ted', 'Jimmie', 'Johnathan', 'Marshall', 'Omar', 'Sergio', 'Charlie', 'Edgar', 'Bret', 'Gregg', 'Orlando', 'Allan', 'Julian', 'Damian', 'Clifton', 'Nelson', 'Chadwick', 'Spencer', 'Julio', 'Marty', 'Floyd', 'Demetrius', 'Arturo', 'Enrique', 'Freddie', 'Ben', 'Lester', 'Alfredo', 'Stuart', 'Matt', 'Robbie', 'Dominic', 'Tom', 'Grant', 'Roland', 'Luke', 'Colin', 'Preston', 'Evan', 'Jonathon', 'Cameron', 'Herman', 'Leo', 'Nick', 'Perry', 'Stacey', 'Garrett', 'Noel', 'Angelo', 'Neal', 'Dewayne', 'Terence', 'Antoine', 'Felix', 'Lorenzo', 'Jarrod', 'Robin', 'Ethan', 'Rickey', 'Brendan', 'Kenny', 'Ron', 'Frankie', 'Sam', 'Cesar', 'Clyde', 'Israel', 'Milton', 'Cody', 'Dexter', 'Cecil', 'Arnold', 'Jennifer', 'Michelle', 'Lisa', 'Jimin', 'Kimberly', 'Amy', 'Angela', 'Melissa', 'Stephanie', 'Heather', 'Nicole', 'Tammy', 'Julie', 'Mary', 'Rebecca', 'Elizabeth', 'Christine', 'Laura', 'Tina', 'Tracy', 'Dawn', 'Karen', 'Shannon', 'Kelly', 'Susan', 'Cynthia', 'Christina', 'Patricia', 'Lori', 'Wendy', 'Andrea', 'Sandra', 'Maria', 'Stacy', 'Pamela', 'Denise', 'Michele', 'Tonya', 'Tara', 'Teresa', 'Rachel', 'Stacey', 'Melanie', 'Deborah', 'Brenda', 'Donna', 'Jessica', 'Monica', 'April', 'Sharon', 'Sarah', 'Linda', 'Dana', 'Carrie', 'Tanya', 'Robin', 'Cheryl', 'Kathleen', 'Barbara', 'Crystal', 'Rhonda', 'Tiffany', 'Nancy', 'Jill', 'Heidi', 'Catherine', 'Debra', 'Kristin', 'Theresa', 'Katherine', 'Sherry', 'Holly', 'Paula', 'Danielle', 'Christy', 'Leslie', 'Amanda', 'Renee', 'Gina', 'Jacqueline', 'Cindy', 'Melinda', 'Veronica', 'Diana', 'Tamara', 'Kristen', 'Erica', 'Anna', 'Tracey', 'Sheila', 'Yolanda', 'Ann', 'Suzanne', 'Erin', 'Shelly', 'Margaret', 'Alicia', 'Jodi', 'Laurie', 'Victoria', 'Valerie', 'Sara', 'Kristi', 'Kathryn', 'Regina', 'Diane', 'Carla', 'Deanna', 'Kathy', 'Carol', 'Carolyn', 'Janet', 'Kristina', 'Beth', 'Jamie', 'Allison', 'Katrina', 'Katina', 'Kim', 'Jenny', 'Traci', 'Tricia', 'Sonya', 'Colleen', 'Terri', 'Misty', 'Shelley', 'Kristine', 'Felicia', 'Sherri', 'Julia', 'Connie', 'Emily', 'Vanessa', 'Anne', 'Lynn', 'Anita', 'Samantha', 'Erika', 'Cassandra', 'Brandy', 'Brandi', 'Krista', 'Natalie', 'Carmen', 'Angel', 'Nichole', 'Sheri', 'Kerry', 'Yvonne', 'Martha', 'Kelli', 'Monique', 'Aimee', 'Sabrina', 'Annette', 'Bridget', 'Bonnie', 'Kristy', 'Stacie', 'Joy', 'Amber', 'Alison', 'Tracie', 'Virginia', 'Becky', 'Wanda', 'Marie', 'Kristie', 'Cathy', 'Natasha', 'Janice', 'Jody', 'Nikki', 'Shawna', 'Gloria', 'Vicki', 'Sonia', 'Toni', 'Leah', 'Megan', 'Penny', 'Debbie', 'Trina', 'Shawn', 'Beverly', 'Kari', 'Charlotte', 'Belinda', 'Yvette', 'Kerri', 'Jeanette', 'Christie', 'Robyn', 'Charlene', 'Sylvia', 'Kara', 'Meredith', 'Joanna', 'Darlene', 'Kendra', 'Ruth', 'Betty', 'Catina', 'Tammie', 'Claudia', 'Joyce', 'Peggy', 'Joanne', 'Shirley', 'Ginger', 'Rose', 'Jean', 'Hope', 'Rosa', 'Tami', 'Frances', 'Dorothy', 'Tonia', 'Kimberley', 'Judith', 'Judy', 'Gretchen', 'Candace', 'Kellie', 'Helen', 'Molly', 'Kelley', 'Marsha', 'Leigh', 'Rita', 'Alice', 'Latonya', 'Sonja', 'Ellen', 'Ashley', 'Bobbie', 'Maureen', 'Jane', 'Norma', 'Tasha', 'Juanita', 'Vickie', 'Melody', 'Karla', 'Christa', 'Keri', 'Joann', 'Dina', 'Ana', 'Billie', 'Caroline', 'Elaine', 'Staci', 'Evelyn', 'Sandy', 'Leticia', 'Rochelle', 'Loretta', 'Jackie', 'Angie', 'Raquel', 'Lauren', 'Candice', 'Teri', 'Cheri', 'Marcia', 'Gail', 'Lynette', 'Rachael', 'Roberta', 'Dena', 'Stefanie', 'Sheryl', 'Jeanne', 'Adrienne', 'Ronda', 'Jodie', 'Eileen', 'Audrey', 'Christi', 'Marcy', 'Sally', 'Jenifer', 'Rachelle', 'Kirsten', 'Lora', 'Roxanne', 'Eva', 'Gwendolyn', 'Jennie', 'Jana', 'Marilyn', 'Mindy', 'Candy', 'Deana', 'Tabitha', 'Lara', 'Shari', 'Cherie', 'Angelia', 'Ericka', 'Jeannie', 'Keisha', 'Antoinette', 'Shelia', 'Nina', 'Irene', 'Desiree', 'Bethany', 'Alisa', 'Lorraine', 'Dianna', 'Marla', 'Trisha', 'Katie', 'Priscilla', 'Shana', 'Shelby', 'Lydia', 'Terry', 'Brooke', 'Joan', 'Jo', 'Bobbi', 'Cara', 'Tammi', 'Sherrie', 'Latasha', 'Angelique', 'Wendi', 'Darla', 'Lee', 'Esther', 'Ramona', 'Audra', 'Lorie', 'Courtney', 'Jacquelyn', 'Karin', 'Angelica', 'Chandra', 'Marlene', 'Cristina', 'Lesley', 'Patrice', 'Marisol', 'Bernadette', 'Betsy', 'Naomi', 'Ruby', 'Melisa', 'Tamika', 'Alexandra', 'Tanisha', 'Lillia']
    name = random.choice(firsts)
    return name


def last():
    lasts = ['Smith', 'Jones', 'Taylor', 'Williams', 'Brown', 'Davies', 'Evans', 'Wilson', 'Thomas', 'Roberts', 'Johnson', 'Lewis', 'Walker', 'Robinson', 'Wood', 'Thompson', 'White', 'Watson', 'Jackson', 'Wright', 'Green', 'Harris', 'Cooper', 'King', 'Lee', 'Martin', 'Clarke', 'James', 'Morgan', 'Hughes', 'Edwards', 'Hill', 'Moore', 'Clark', 'Harrison', 'Scott', 'Young', 'Morris', 'Hall', 'Ward', 'Turner', 'Carter', 'Phillips', 'Mitchell', 'Patel', 'Adams', 'Campbell', 'Anderson', 'Allen', 'Cook', 'Bailey', 'Parker', 'Miller', 'Davis', 'Murphy', 'Price', 'Bell', 'Baker', 'Griffiths', 'Kelly', 'Simpson', 'Marshall', 'Collins', 'Bennett', 'Cox', 'Richardson', 'Fox', 'Gray', 'Rose', 'Chapman', 'Hunt', 'Robertson', 'Shaw', 'Reynolds', 'Lloyd', 'Ellis', 'Richards', 'Russell', 'Wilkinson', 'Khan', 'Graham', 'Stewart', 'Reid', 'Murray', 'Powell', 'Palmer', 'Holmes', 'Rogers', 'Stevens', 'Walsh', 'Hunter', 'Thomson', 'Matthews', 'Ross', 'Owen', 'Mason', 'Knight', 'Kennedy', 'Butler', 'Saunders', 'Cole', 'Pearce', 'Dean', 'Foster', 'Harvey', 'Hudson', 'Gibson', 'Mills', 'Berry', 'Barnes', 'Pearson', 'Kaur', 'Booth', 'Dixon', 'Grant', 'Gordon', 'Lane', 'Harper', 'Ali', 'Hart', 'Mcdonald', 'Brooks', 'Ryan', 'Carr', 'Macdonald', 'Hamilton', 'Johnston', 'West', 'Gill', 'Dawson', 'Armstrong', 'Gardner', 'Stone', 'Andrews', 'Williamson', 'Barker', 'George', 'Fisher', 'Cunningham', 'Watts', 'Webb', 'Lawrence', 'Bradley', 'Jenkins', 'Wells', 'Chambers', 'Spencer', 'Poole', 'Atkinson', 'Lawson', 'Day', 'Woods', 'Rees', 'Fraser', 'Black', 'Fletcher', 'Hussain', 'Willis', 'Marsh', 'Ahmed', 'Doyle', 'Lowe', 'Burns', 'Hopkins', 'Nicholson', 'Parry', 'Newman', 'Jordan', 'Henderson', 'Howard', 'Barrett', 'Burton', 'Riley', 'Porter', 'Byrne', 'Houghton', 'John', 'Perry', 'Baxter', 'Ball', 'Mccarthy', 'Elliott', 'Burke', 'Gallagher', 'Duncan', 'Cooke', 'Austin', 'Read', 'Wallace', 'Hawkins', 'Hayes', 'Francis', 'Sutton', 'Davidson', 'Sharp', 'Holland', 'Moss', 'May', 'Bates', 'Morrison', 'Bob', 'Oliver', 'Kemp', 'Page', 'Arnold', 'Shah', 'Stevenson', 'Ford', 'Potter', 'Flynn', 'Warren', 'Kent', 'Alexander', 'Field', 'Freeman', 'Begum', 'Rhodes', "O'neill", 'Middleton', 'Payne', 'Stephenson', 'Pritchard', 'Gregory', 'Bond', 'Webster', 'Dunn', 'Donnelly', 'Lucas', 'Long', 'Jarvis', 'Cross', 'Stephens', 'Reed', 'Coleman', 'Nicholls', 'Bull', 'Bartlett', "O'brien", 'Curtis', 'Bird', 'Patterson', 'Tucker', 'Bryant', 'Lynch', 'Mackenzie', 'Ferguson', 'Cameron', 'Lopez', 'Haynes', 'Bolton', 'Hardy', 'Heath', 'Davey', 'Rice', 'Jacobs', 'Parsons', 'Ashton', 'Robson', 'French', 'Farrell', 'Walton', 'Gilbert', 'Mcintyre', 'Newton', 'Norman', 'Higgins', 'Hodgson', 'Sutherland', 'Kay', 'Bishop', 'Burgess', 'Simmons', 'Hutchinson', 'Moran', 'Frost', 'Sharma', 'Slater', 'Greenwood', 'Kirk', 'Fernandez', 'Garcia', 'Daniel', 'Beattie', 'Maxwell', 'Todd', 'Charles', 'Paul', 'Crawford', "O'connor", 'Park', 'Forrest', 'Love', 'Rowland', 'Connolly', 'Sheppard', 'Harding', 'Banks', 'Rowe', 'Humphreys', 'Garner', 'Glover', 'Sanderson', 'Jeffery', 'Goodwin', 'Hewitt', 'Daniels', 'David', 'Sullivan', 'Yates', 'Howe', 'Mackay', 'Hammond', 'Carpenter', 'Miles', 'Brady', 'Preston', 'Mcleod', 'Lambert', 'Knowles', 'Leigh', 'Hope', 'Atherton', 'Barton', 'Finch', 'Blake', 'Fuller', 'Henry', 'Coates', 'Hobbs', 'Morton', 'Howells', 'Davison', 'Owens', 'Gough', 'Dennis', 'Wilkins', 'Duffy', 'Woodward', 'Griffin', 'Bloggs', 'Paterson', 'Charlton', 'Vincent', 'Wall', 'Bowen', 'Browne', 'Donaldson', 'Rodgers', 'Christie', 'Gibbons', 'Wheeler', 'Smart', 'Steele', 'Bentley', 'Quinn', 'Hartley', 'Barnett', 'Randall', 'Sweeney', 'Fowler', 'Allan', 'Brennan', 'Douglas', 'Holt', 'Howell', 'Bowden', 'Cartwright', 'Baird', 'Watkins', 'Kerr', 'Dickson', 'Benson', 'Goddard', 'Millar', 'Broadhurst', 'Doherty', 'Holden', 'Singh', 'Tait', 'Reilly', 'Thorne', 'Wyatt', 'Power', 'Lord', 'Nelson', 'Hilton', 'Adam', 'Mcgregor', 'Mclean', 'Walters', 'Jennings', 'Lindsay', 'Nash', 'Hancock', 'Hooper', 'Carroll', 'Silva', 'Chadwick', 'Abbott', 'Stuart', 'Mellor', 'Seymour', 'Boyd', 'Perkins', 'Dale', 'Mann', 'Mac', 'Haines', 'Whelan', 'Peters', 'Obrien', 'Savage', 'Barlow', 'Sanders', 'Mohamed', 'Kenny', 'Baldwin', 'Mcgrath', 'Thornton', 'Joyce', 'Blair', 'Whitehouse', 'Weaver', 'Shepherd', 'Whitehead', 'Little', 'Cullen', 'Burrows', 'Mcfarlane', 'Sinclair', 'Swift', 'Fleming', 'Buckley', 'Welch', 'Vaughan', 'Bradshaw', 'Naylor', 'Summers', 'Briggs', 'Schofield', 'Osborne', 'Coles', 'Akhtar', 'Cassidy', 'Rossi', 'Giles', 'Whittaker', 'Herbert', 'Hicks', 'Bourne', 'Faulkner', 'Weston', 'Oneill', 'Bray', 'Humphrey', 'Spence', 'Partridge', 'Johns', 'Morley', 'Welsh', 'Kaye', 'Bush', 'Rooney', 'Craig', 'Fitzgerald', 'Gardiner', 'Whittle', 'Laing', 'Pollard', 'Mccann', 'Wilkes', 'Drew', 'Armitage', 'Bright', 'Hills', 'English', 'Devlin', 'Winter', 'Howarth', 'Horne', 'Singleton', 'Lovell', 'Best', 'Kavanagh', 'Appleton', 'Gibbs', 'Rawlings', 'Mckenna', 'Turnbull', 'Bernard', 'Stanton', 'Kirby', 'Wills', 'Carey', 'Sawyer', 'Crossley', 'Piper', 'Joseph', 'Fenton', 'Bruce', 'Connor', 'Reeves', 'Norris', 'Needham', 'Firth', 'Clarkson', 'Dyer', 'Brookes', 'Townsend', 'Cairns', 'Guest', 'Wallis', 'Thorpe', 'Parkinson', 'Sykes', 'Lees', 'Gale', 'Blackburn', 'Holloway', 'Hurst', 'Mcintosh', 'Smyth', 'Conway', 'Bowman', 'Mclaughlin', 'Senior', 'Bassett', 'Collier', 'Corbett', 'Heaton', 'Curry', 'Humphries', 'Copeland', 'Fitzpatrick', 'Sloan', 'Archer', 'Hough', 'Ireland', 'Tomlinson', 'Edge', 'Burt', 'Stokes', 'Cope', 'Tanner', 'Chandler', 'Tyler', 'Goodman', 'Mckay', 'Wickens', 'Horton', 'Stacey', 'Skinner', 'Shields', 'Reeve', 'Mccallum', 'Noble', 'Whyte', 'Barr', 'Muir', 'Kane', 'Simons', 'Cannon', 'Pope', 'Barry', 'Mckenzie', 'England', 'Dalton', 'Hanson', 'Mccormack', 'Rahman', 'Philip', 'Marriott', 'Barclay', 'Simon', 'Logan', 'Farrow', 'Hood', 'Flower', 'Matthams', 'Wardle', 'Sims', 'Woodcock', 'Crowther', 'Waters', 'Mooney', 'Gould', 'Malone', 'Peacock', 'Gunn', 'Mcneill', 'Davie', 'Donald', 'Healy', 'Mcgill', 'Hutton', 'Neal', 'Pegle']
    name = random.choice(lasts)
    return name


def party():
    nouns = ['Peace', 'Freedom', 'Democracy', 'Liberalism', 'Unity', 'Action', 'Hope', 'Socialism', 'Communism',
             'The Nation', 'The Country', 'The People', 'The Planet', 'Liberty', 'Welfare', 'Equality', 'Progress',
             'Change', 'Reform', 'Tradition', 'Science', 'Business', 'Justice', 'Respect', 'Law', 'Ecology',
             'Revolution', 'Labour', 'Rights', 'The Future', 'Social Justice', 'Independence', 'Renewal', 'Society']

    people = ['Workers', 'Citizens', 'Democrats', 'Liberals', 'Fishermen', 'Unionists', 'Nationalists',
              'Students', 'Pensioners', 'Christians', 'Catholics', 'Protestants', 'Farmers', 'Independents',
              'Republicans', 'Animals', 'Veterans', 'Miners', 'Voters', 'The Middle Class', 'The Working Class',
              'Socialists', 'Communists', 'Centrists', 'Royalists', 'Conservatives', 'Socialists', 'People']

    adjectives = ['Socialist', 'Communist', 'Republican', 'Democratic', 'United', 'Humanist', 'Pirate',
                  'Revolutionary', 'Libertarian', 'Christian', 'Conservative', 'Liberal', 'Progressive',
                  'Independent', 'Popular', 'National', 'Federal', 'Populist', 'Patriotic',
                  'Rural', 'Urban', 'Environmental', 'Green', 'Secular']

    structures = ['The [a] Party', 'The [a]-[a] Party', "The [p]'s Party", 'The [n] Party', '[a] Party',
                  'The [a] [pn] Party', 'The Party for [pn]', 'The [a] and [a] Party', 'The [a] [a] Party',
                  'The Party Against [pn]', 'The New [a] Party', 'The [a] Party for [pn]', 'The [a] Voice',
                  'The Coalition of [pn]', 'The [a] League', '[n]!', 'The [p]\'s Front', 'The [a] Front',
                  'The [a] Alliance of [p]', 'The [a] Alliance', 'The Alliance of [p] and [p]', 'The Alliance for [n]',
                  'The [a] Group for [n]', 'The [a] Group of [p]', '[f]\'s [a] Party', 'The [a] [p]', '[p] for [n]']

    name = random.choice(structures)
    while '[a]' in name:
        name = name.replace('[a]', random.choice(adjectives), 1)
    while '[n]' in name:
        name = name.replace('[n]', random.choice(nouns), 1)
    while '[p]' in name:
        name = name.replace('[p]', random.choice(people), 1)
    while '[pn]' in name:
        name = name.replace('[pn]', random.choice(people + nouns), 1)
    while '[f]' in name:
        name = name.replace('[f]', full(), 1)

    name = name.replace('The The', 'The')
    name = name.replace("s's", "s'")

    return name


def initials():
    name = ''
    for i in range(random.randint(2, 4)):
        name += chr(random.randint(65, 85))
    return name


def region():
    name = ''
    locations = ['North', 'South', 'East', 'West', 'NE', 'NW', 'SE', 'SW', 'Central', 'Upper', 'Lower',
                 'Park', 'Valley', 'Green', 'New']

    starts = ['Alder', 'Ash', 'Ban', 'Barn', 'Bath', 'Berken', 'Brent', 'Brom',  # As Bs
              'Charish', 'Cam', 'Car', 'Cal', 'Chel', 'Cope', 'Craw', 'Croy', 'Dews', 'Dud', 'Dor',  # Cs Ds
              'Eal', 'Eas', 'Edd', 'Ere', 'Exe', 'Fel', 'Fal', 'Fil', 'Folke',  # Es Fs
              'Gains', 'Gar', 'Grim', 'Guil', 'Green', 'Harr', 'Hack', 'Halt', 'Horn', 'Hen', 'Hex',  # Gs Hs
              'Is', 'Ip', 'Ken', 'Kings', 'Lei', 'Lew', 'Lewes', 'Ley', 'Lin', 'Lut', 'Lan',  # Is Js Ks Ls
              'Mal', 'Mel', 'Man', 'Mid', 'Mil', 'New', 'Nun', 'Ox', 'Orp',  # Ms Ns Os
              'Pen', 'Ply', 'Port', 'Ports', 'Pres', 'Put', 'Punt', 'Pud', 'Read', 'Red', 'Roch', 'Rug',  # Ps Qs Rs
              'Sail', 'Scar', 'Sur', 'Strat', 'Tam', 'Tat', 'Tel', 'Thor', 'Tun', 'Ux', 'Ul',  # Ss Ts Us
              'Vaux', 'Vex', 'Wal', 'Wans', 'War', 'Wasp', 'Wat', 'Well', 'Wick', 'Win'  # Vs Ws Xs Ys Zs
              ]

    suffixes = ['bridge', 'bury', 'by', 'cester', 'chester', 'cliffe', 'don', 'dif', 'erton', 'field', 'ford', 'ferry',
                'grove', 'ham', 'ick', 'ing', 'ington', 'itch', 'mouth', 'ney', 'pool', 'sea', 'tonshire', 'rith',
                'shire', 'sley', 'ter', 'ton', 'wood', 'worth', 'side', 'ring', 'neyshire', 'neyton', 'buryshire', 'ness']

    if prob(0.5):  # place name
        name = random.choice(starts) + random.choice(suffixes)
        if prob(0.5):
            name += ' ' + random.choice(locations)
        else:
            name = random.choice(locations) + ' ' + name


    elif prob(0.5): # Two short location names with "and" between them
        name = random.choice(starts) + random.choice(suffixes) + ' and ' + random.choice(starts) + random.choice(suffixes)

    else: # place name, place name + place name
        name = random.choice(starts) + random.choice(suffixes) + ', ' + \
               random.choice(starts) + random.choice(suffixes) + ' and ' + \
               random.choice(starts) + random.choice(suffixes)

    return name
    return name

def color():
    return '#' + ''.join([random.choice('0123456789ABCDEF') for i in range(6)])

def prob(p):
    return random.random() < p
