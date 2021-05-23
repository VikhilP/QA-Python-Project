# Brief

I have been tasked with creating a CRUD application that is able to take a database instance and run a relationship between at least 2 tables using MySQL. 

To do this i used a variety of tools:
- Python
- Google Cloud Platform
- Jenkins
- MySQL/pymysql
- PyTest
- Trello Boards
- Gunicorn
- Flask/ Flask WTForms
- Git/ Github (for version control)
- Jinja2
- Selenium

## Idea

The idea behind the project was to create a CRUD application but in a way that would be fun to create and be relatable to me through hobbies and or work. 

The first idea was to create a DND database in which would store a characters/enemys details and allow dice rolls (using random.randint(1,20)) between the 2 to simulate attacks. I rejected this idea due to the complexity of the project being high. This is because i believed that while achiveable in the time frame, the work load of the project would not leave me enough time to finish other projects

The second idea was to create a Grades Calculator. It was a type of project i had done similiarly at univeristy in Java. All i had to do was convert the project using python. It would have used 3 tables, Modules, Course and University. However, i did not choose this project as i did not want to create the same project twice. Even though i would have been experienced with it, i would not have been as motivated

Lastly, the project i did start however was this, a database that would pair games and its series. Games would be added to the database and the software would dynamically update the corrosponding review(through mean) and series game count. The project was more fun to create and allowed me to easily create meaningful columns.

## CRUD

The functionality of the project entailed me to use CRUD (Create, Read, Update and Delete) aspects into the program. This includes

### Create

- Add a new Game (variables: Name, Series, Developer, Review)
- Add a new Series (only took a series name, the rest was dynamic)

### Read

- The user, after creating a new game would view its details on the readgame page
- similar with the series page

### Update

- The user could change the name of an existing series
- Changing series name would update all the games with that series in it
- Changing review score of a game would produce a different average review score for the series
- Adding a game to the series would affect the total game count of the series

### Delete

- Deleting a game would cause it to no longer appear and affect both the game count and review of the given series
- Deleting a series would also no longer appear and update the games that were previously not in that series to set its series to "N/A"

## Design Choices

### Database Architecture

As mentioned before, one of the requirements of the project was to create database using MySQL. So before creation, a database structure had to be agreed upon. 

![Initial DB Design](https://imgur.com/8Dr2kie.jpeg)

Initially, 4 tables had been created. Games, GameSeries, Developers and Publishers.

At first, there was an issue with the developers and publishers table. In reality there can be developers at multiple publishers e.g. Obisdian entertainment being freelancers in real life, and publishers having multiple developers under their belt. Then another issue arrises between publishers and game where there would be another many to many relationship. For the sake of complexity, publishers table was the first to go

As the deadline drew nearer, it became less viable to schedule the developers table into production. This was cut to scale down complexity while also entailing the Minimum Viable Product was surpassed. however, an aspect of the "Developers" table still lives on in the Game table through a not null column inputted by user entry.

### Trello

While in the QA training we have worked with Jira and the SCRUM devops style, the simplicity of trello and its less annoying UI drew me towards it. Kanban board still allowed me to create a to do board which would have been used in Jira also. I chose Trello because i did not see the Jira board being used to its fullest with a small, few day sprint.

![Imgur](https://i.imgur.com/oCDoNW9.png)

The Trello board has been seperated into sections:
- User Stories (The basis to my integration testing)
- Planning (This would be planning out potential features and how to implement them e.g. what i need to learn)
- To Do (Tasks that are 100% planned but not implemented)
- Doing (in the process of being completed)
- Done (Completed)

The goal is to get everything from to do, to done


### MoSCoW

*Must Have*
 
- CRUD functiolity
- Connect to cloud (GCP)
- Use jenkins build server
- Use git SCM

*Should Have*

- Release dates
- dynamically change the result of reviews based on games
- count number of games in a series

*Could have*

- Sorting methods
- mark favourite games for the sort method
- filter methods

*Wont Have*
- Nice looking UI (Do not have the time)
- Change to non relational (Would fail a requirement but i like them better practically)


### CI Pipeline

The Continuous Integration Pipeline is a major part of the Devops process

Starting with Python, i will create code for the project. After a feature is complete or i want to save work for someone else, i would push my code onto github. Through this the jenkins server will grab hold of the git webhook and automatically grab hold of the latest commit and perform the build. Here the build will come with automated Unit tests and integration tests (Unit to test functions and Integration to test user stories).

Jenkins will run several bash commands that i set in order to automate the process of grabbing the git web hooks, downloading requirements, creating databases and performing pytest. After it has run pytest i would get a coverage report and use that to work out what lines of code has not been tested to increase coverage rating.

Ideally once builds are finished i would create a seperate VM instance for production, this is so jenkins and the VM to not running in the same instance and have jenkins available to the public. However i am taking advantage of GCP free trial and do not want to be charged after having too many instances, i will use the same instance acknowledging cost and security concerns

Once tests are complete, Gunicorn will be used as the deployment server. This is a WSGI, it turns my development server/code which was accessed via "app.py" to be created deployed to a production server. This means multiple users can now use the system online and not stressout the development server.

### Risk Assessment

![Imgur](https://i.imgur.com/qmLycub.png)

This is the risk assessment for the project, i have linked to it also. I have also used a matrix for this part of the assessment

[Full link provided here](https://drive.google.com/file/d/1th_WwNNUO6eMiYGhmJPV46RvA0d1osBq/view?usp=sharing)

## Testing

I have utilised both Unit and Integration tests to produce test results. These tests are written as scripts and then carried out by the program pytest.

Unit Tests cover my functions and if they run well with one another. Integration testing is ran with my user stories in mind. If the integration test passes, this means that the user story has been completed. 

I have run these tests through the Jenkins build server.

### Steps
1) Create a VM instance
2) Open the ports 5000 and 8080 (8080 for jenkins, 5000 for a gunicorn server later)
3) Use the QA Community command to activate Jenkins
4) log in to Jenkins by excuting the script from task 3
5) Using jenkins, start a new build, input the git repository into the git project input box and set the right branch (if needed, tick the github webhook checkbox for automatic builds of recent pushes)
6) Input this command into the build settings (Using execute shell) 

```
#!/bin/bash
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
cd Tests
python3.6 -m pytest --cov=application --cov-report=term-missing
```

7) Open up the work space and retrieve the html file named "index", this will provide the coverage report of the build test

![Imgur](https://i.imgur.com/PodFWN6.png)
Proof of passed tests

![Imgur](https://i.imgur.com/DEC2h3Z.png)
HTML coverage report

### Reasons for the tests

I needed a way of testing if my functions worked. For a while i had an issue with my test coverage being less than 80%. I had fixed due to a wrong variable name in my unit test. However this had already taken significant time out of my project time trying to fix this issue.

i also made sure that the tests were provided on a local server, i did not what my real sql server on the cloud being affected by my tests. If on the cloud server, the test would be slow and reset the database every test.

On the picture labeled "proof of passed tests" there is a certain amount of lines missing from the report, this is due to the amount of tests i already made. i had at maximum 4 lines of code missing, i was sure i had those lines covered in the integration tests but a gap in knowledge provided me with a missed line, rendering me unable to rectify.

During these testing phases, an archive is created. the file contains the application folder and anything else not in a folder e.g. create.py and app.py as well as this readme and requirements

What was tested:

- Add series and Game functionality
- Update game functionality
- Delete game and series fuctionality 
- Updates when a game is deleted and added from a series e.g. the count of games, review and release years
- If the data is properly displayed on screen for the viewer
- Integration testing based on user stories ( shown on the Trello board)

What was not tested:

- 1 user story, this is due to not being able to create that feature yet. this would be the adding a favourite game feature.
- Update series, i had encounterd a bug late in development. this rendered me unable to fix during this sprint and had to be left incomplete. since i was able to still have an update game feature, i was sure i could still hit the MVP and move on to more important tests


## Front End




