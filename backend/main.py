from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "quiz.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            answer TEXT NOT NULL,
            explanation TEXT NOT NULL
        )
    ''')
    
    # Check if we need to seed
    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]
    
    if count < 100:
        # Clear existing to ensure fresh 20 per subject if needed
        cursor.execute("DELETE FROM questions")
        
        all_q = []
        
        html_questions = [
            ("HTML", "What does HTML stand for?", "Hyper Text Markup Language", "Hyperlinks and Text Markup Language", "Home Tool Markup Language", "Hyper Text Main Language", "option1", "HTML is the standard markup language for documents designed to be displayed in a web browser."),
            ("HTML", "Who is making the Web standards?", "Mozilla", "Google", "The World Wide Web Consortium", "Microsoft", "option3", "The W3C is the main international standards organization for the World Wide Web."),
            ("HTML", "Choose the correct HTML element for the largest heading:", "<h6>", "<heading>", "<h1>", "<head>", "option3", "<h1> is the standard for the most important/largest heading."),
            ("HTML", "What is the correct HTML element for inserting a line break?", "<lb>", "<break>", "<br>", "<li>", "option3", "<br> is an empty tag used to produce a line break."),
            ("HTML", "What is the correct HTML for adding a background color?", "<body bg='yellow'>", "<body style='background-color:yellow;'>", "<background>yellow</background>", "<body color='yellow'>", "option2", "Modern HTML uses CSS styles for background colors."),
            ("HTML", "Choose the correct HTML element to define important text:", "<strong>", "<b>", "<i>", "<important>", "option1", "<strong> is used to indicate strong importance, whereas <b> is just for bold formatting."),
            ("HTML", "Choose the correct HTML element to define emphasized text:", "<italic>", "<i>", "<em>", "<emphasize>", "option3", "<em> is used to define emphasized text."),
            ("HTML", "What is the correct HTML for creating a hyperlink?", "<a name=''></a>", "<a href=''></a>", "<a></a>", "<link href=''></link>", "option2", "The <a> tag defines a hyperlink and uses 'href' for the destination."),
            ("HTML", "Which character is used to indicate an end tag?", "/", "<", "*", "^", "option1", "Tags are closed using the forward slash character."),
            ("HTML", "How can you make a numbered list?", "<ul>", "<ol>", "<dl>", "<list>", "option2", "Ordered List <ol> creates numbered items."),
            ("HTML", "How can you make a bulleted list?", "<ul>", "<ol>", "<dl>", "<list>", "option1", "Unordered List <ul> creates bulleted items."),
            ("HTML", "What is the correct HTML for making a checkbox?", "<checkbox>", "<input type='checkbox'>", "<check>", "<input type='check'>", "option2", "Checkbox is an input type."),
            ("HTML", "What is the correct HTML for making a text input field?", "<input type='textfield'>", "<input type='text'>", "<textinput>", "<textfield>", "option2", "The 'text' type is used for single-line text input."),
            ("HTML", "What is the correct HTML for making a drop-down list?", "<input type='dropdown'>", "<list>", "<select>", "<dropdown>", "option3", "<select> is used to create a drop-down list."),
            ("HTML", "What is the correct HTML for making a text area?", "<input type='textarea'>", "<textarea>", "<text>", "<input type='text-area'>", "option2", "<textarea> is used for multi-line text input."),
            ("HTML", "Which HTML element is used to specify a footer for a document or section?", "<section>", "<footer>", "<bottom>", "<aside>", "option2", "The <footer> element contains footer information."),
            ("HTML", "What is the correct HTML for inserting an image?", "<image src=''>", "<img src=''>", "<img href=''>", "<pic src=''>", "option2", "<img src='source'> is the standard way to embed images."),
            ("HTML", "What is the correct HTML for inserting a background image?", "<body background=''>", "<body style='background-image:url();'>", "<bg img=''>", "<background img=''>", "option2", "Background images are best set via CSS."),
            ("HTML", "Which HTML element defines the title of a document?", "<head>", "<meta>", "<title>", "<header>", "option3", "The <title> tag defines the document title shown in the browser tab."),
            ("HTML", "Which attribute is used to provide an alternative text for an image?", "alt", "title", "src", "longdesc", "option1", "The alt attribute provides alternative text for screen readers or broken images.")
        ]
        
        css_questions = [
            ("CSS", "What does CSS stand for?", "Colorful Style Sheets", "Cascading Style Sheets", "Creative Style Sheets", "Computer Style Sheets", "option2", "CSS stands for Cascading Style Sheets, describing how HTML elements are to be displayed."),
            ("CSS", "Which HTML attribute is used to define inline styles?", "class", "styles", "font", "style", "option4", "The style attribute allows you to apply CSS directly to an element."),
            ("CSS", "Which is the correct CSS syntax?", "{body:color=black;}", "body {color: black;}", "body:color=black;", "{body;color:black;}", "option2", "Selector { property: value; } is the standard format."),
            ("CSS", "How do you insert a comment in a CSS file?", "// comment", "/* comment */", "' comment", "// comment //", "option2", "Multi-line comments in CSS use /* ... */."),
            ("CSS", "Which property is used to change the background color?", "color", "background-color", "bgcolor", "background-image", "option2", "background-color sets the background color of an element."),
            ("CSS", "How do you add a background color for all <h1> elements?", "all.h1 {background-color: #FFFFFF;}", "h1 {background-color: #FFFFFF;}", "h1.all {background-color: #FFFFFF;}", "h1 {bg-color: #FFFFFF;}", "option2", "The h1 selector targets all h1 elements."),
            ("CSS", "Which CSS property is used to change the text color of an element?", "fgcolor", "color", "text-color", "font-color", "option2", "The 'color' property specifically refers to the text color."),
            ("CSS", "Which CSS property controls the text size?", "font-size", "text-style", "text-size", "font-weight", "option1", "font-size is used to adjust how large the text appears."),
            ("CSS", "What is the correct CSS syntax for making all the <p> elements bold?", "p {text-size:bold;}", "p {font-weight:bold;}", "p {font-style:bold;}", "p {bold:true;}", "option2", "font-weight controls the thickness of characters."),
            ("CSS", "How do you display hyperlinks without an underline?", "a {text-decoration:none;}", "a {underline:none;}", "a {decoration:no-underline;}", "a {text-decoration:no-underline;}", "option1", "text-decoration is used to add or remove underlines."),
            ("CSS", "How do you make each word in a text start with a capital letter?", "text-style:capitalize", "text-transform:capitalize", "font-transform:capitalize", "You cannot do that with CSS", "option2", "text-transform:capitalize forces every word's first letter to be uppercase."),
            ("CSS", "Which property is used to change the font of an element?", "font-family", "font-style", "font-variant", "font-weight", "option1", "font-family specifies the typeface."),
            ("CSS", "How do you make the text bold?", "font-weight:bold;", "font:bold;", "style:bold;", "text-weight:bold;", "option1", "font-weight:bold is the Standard."),
            ("CSS", "How do you display a border like this: The top border = 10px, bottom border = 5px, left border = 20px, right border = 1px?", "border-width:10px 5px 20px 1px;", "border-width:10px 1px 5px 20px;", "border-width:5px 20px 10px 1px;", "border-width:10px 20px 5px 1px;", "option2", "The border-width shorthand follows: top, right, bottom, left."),
            ("CSS", "Which property is used to change the left margin of an element?", "padding-left", "margin-left", "indent", "spacing-left", "option2", "margin-left adds space outside the element's border on the left."),
            ("CSS", "When using the padding property; are you allowed to use negative values?", "Yes", "No", "Depends on browser", "Only for specialized cases", "option2", "Padding cannot be negative, while margin can be."),
            ("CSS", "How do you make a list that lists its items with squares?", "list-style-type: square;", "list-type: square;", "list: square;", "bullet-style: square;", "option1", "list-style-type defines the marker for lists."),
            ("CSS", "How do you select an element with id 'demo'?", "demo", "#demo", ".demo", "*demo", "option2", "The hash (#) symbol is the ID selector."),
            ("CSS", "How do you select elements with class name 'test'?", ".test", "test", "#test", "*test", "option1", "The dot (.) symbol is the class selector."),
            ("CSS", "How do you select all p elements inside a div element?", "div p", "div.p", "div + p", "div ~ p", "option1", "Descendant selector selects all child/grandchild elements.")
        ]
        
        js_questions = [
            ("JavaScript", "Inside which HTML element do we put the JavaScript?", "<js>", "<script>", "<javascript>", "<scripting>", "option2", "<script> is used for embedding or referencing JS."),
            ("JavaScript", "What is the correct JavaScript syntax to change the content of the HTML element: <p id='demo'>Hello World!</p>?", "document.getElementByName('p').innerHTML = 'Hello World!';", "document.getElementById('demo').innerHTML = 'Hello World!';", "#demo.innerHTML = 'Hello World!';", "document.getElement('p').innerHTML = 'Hello World!';", "option2", "getElementById is the standard DOM selection method."),
            ("JavaScript", "Where is the correct place to insert a JavaScript?", "The <head> section", "The <body> section", "Both <head> and <body>", "None of the above", "option3", "JS can be placed in both, though end of body is often preferred for performance."),
            ("JavaScript", "What is the correct syntax for referring to an external script called 'xxx.js'?", "<script name='xxx.js'>", "<script href='xxx.js'>", "<script src='xxx.js'>", "<script file='xxx.js'>", "option3", "The 'src' attribute defines the external source."),
            ("JavaScript", "The external JavaScript file must contain the <script> tag.", "True", "False", "Only if it uses modules", "Depends on browser", "option2", "External files contain raw JS, no HTML tags."),
            ("JavaScript", "How do you write 'Hello World' in an alert box?", "msgBox('Hello World');", "alertBox('Hello World');", "msg('Hello World');", "alert('Hello World');", "option4", "The alert() function displays messages in a modal dialog."),
            ("JavaScript", "How do you create a function in JavaScript?", "function:myFunction()", "function = myFunction()", "function myFunction()", "create myFunction()", "option3", "Functions are defined using the 'function' keyword."),
            ("JavaScript", "How do you call a function named 'myFunction'?", "call myFunction()", "myFunction()", "call function myFunction()", "execute myFunction()", "option2", "Simply using the function name followed by parentheses calls it."),
            ("JavaScript", "How to write an IF statement in JavaScript?", "if i = 5 then", "if i == 5 then", "if (i == 5)", "if i = 5", "option3", "JS uses parentheses for conditions and curly braces for blocks."),
            ("JavaScript", "How to write an IF statement for executing some code if 'i' is NOT equal to 5?", "if (i <> 5)", "if i <> 5", "if (i != 5)", "if i != 5", "option3", "!= is the Inequality operator."),
            ("JavaScript", "How does a WHILE loop start?", "while i = 1 to 10", "while (i <= 10)", "while (i <= 10; i++)", "while i <= 10", "option2", "A while loop continues as long as a condition is true."),
            ("JavaScript", "How does a FOR loop start?", "for (i = 0; i <= 5; i++)", "for (i <= 5; i++)", "for i = 1 to 5", "for (i = 0; i <= 5)", "option1", "For loops take: initializer, condition, and increment."),
            ("JavaScript", "How can you add a comment in a JavaScript?", "' comment", "<!-- comment -->", "// comment", "* comment", "option3", "// is used for single-line comments in JS."),
            ("JavaScript", "How to insert a comment that has more than one line?", "<!-- comment -->", "/* comment */", "// comment //", "// comment", "option2", "/* ... */ is used for multi-line comments."),
            ("JavaScript", "What is the correct way to write a JavaScript array?", "var colors = 1 = ('red'), 2 = ('green'), 3 = ('blue')", "var colors = (1:'red', 2:'green', 3:'blue')", "var colors = ['red', 'green', 'blue']", "var colors = 'red', 'green', 'blue'", "option3", "Arrays are defined using square brackets."),
            ("JavaScript", "How do you round the number 7.25, to the nearest integer?", "round(7.25)", "Math.rnd(7.25)", "Math.round(7.25)", "rnd(7.25)", "option3", "Math.round() performs standard rounding."),
            ("JavaScript", "How do you find the number with the highest value of x and y?", "Math.max(x, y)", "ceil(x, y)", "top(x, y)", "Math.ceil(x, y)", "option1", "Math.max() returns the largest of its zero or more arguments."),
            ("JavaScript", "Which event occurs when the user clicks on an HTML element?", "onmouseover", "onchange", "onclick", "onmouseclick", "option3", "onclick is the standard click event."),
            ("JavaScript", "How do you declare a JavaScript variable?", "v carName;", "variable carName;", "var carName;", "declare carName;", "option3", "var, let, or const are used to declare variables."),
            ("JavaScript", "Which operator is used to assign a value to a variable?", "x", "-", "=", "*", "option3", "The equals sign (=) is the assignment operator.")
        ]
        
        python_questions = [
            ("Python", "What is the correct file extension for Python files?", ".pyth", ".pt", ".py", ".pyt", "option3", ".py is the standard extension for Python scripts."),
            ("Python", "How do you output 'Hello World' in Python?", "echo('Hello World');", "print('Hello World')", "p('Hello World')", "printf('Hello World')", "option2", "The print() function outputs data to the console."),
            ("Python", "How do you insert COMMENTS in Python code?", "// This is a comment", "# This is a comment", "/* This is a comment */", "-- This is a comment", "option2", "# is used for single-line comments in Python."),
            ("Python", "Which variable name is invalid in Python?", "my_var", "_myvar", "2myvar", "myVar", "option3", "Variable names cannot start with a digit."),
            ("Python", "How do you create a variable with the numeric value 5?", "x = 5", "x = int(5)", "Both of the above", "None of the above", "option3", "Direct assignment and int() constructor both work."),
            ("Python", "What is the correct syntax to output the type of a variable or object in Python?", "print(typeof(x))", "print(type(x))", "print(typeOf(x))", "print(kind(x))", "option2", "The type() function returns the class name of the object."),
            ("Python", "How do you create a function in Python?", "function myFunction():", "def myFunction():", "create myFunction():", "make myFunction():", "option2", "'def' keyword is used to define functions."),
            ("Python", "In Python, 'Hello', is the same as \"Hello\"", "True", "False", "Depends on version", "Only in Python 2", "option1", "Strings can be enclosed in single or double quotes."),
            ("Python", "What is a correct syntax to return the first character in a string?", "x = \"Hello\"[1]", "x = sub(\"Hello\", 0, 1)", "x = \"Hello\"[0]", "x = \"Hello\".first()", "option3", "Python uses 0-based indexing."),
            ("Python", "Which method can be used to remove any whitespace from both the beginning and the end of a string?", "strip()", "trim()", "ptrim()", "len()", "option1", "strip() removes leading and trailing characters (whitespace by default)."),
            ("Python", "Which method can be used to return a string in upper case?", "upperCase()", "toUpperCase()", "upper()", "uppercase()", "option3", "upper() returns the string in all caps."),
            ("Python", "Which method can be used to replace parts of a string?", "replace()", "sub()", "switch()", "repl()", "option1", "replace() replaces all occurrences of a substring."),
            ("Python", "Which operator is used to multiply numbers?", "%", "*", "#", "x", "option2", "Asterisk (*) is the multiplication operator."),
            ("Python", "Which operator can be used to compare two values?", "=", "==", "<>", "><", "option2", "Comparison for equality uses the double equals (==)."),
            ("Python", "Which collection is ordered, changeable, and allows duplicate members?", "SET", "LIST", "TUPLE", "DICTIONARY", "option2", "Lists are the most versatile built-in sequence type in Python."),
            ("Python", "Which collection does not allow duplicate members?", "LIST", "SET", "TUPLE", "ARRAY", "option2", "Sets are unordered collections of unique elements."),
            ("Python", "How do you start writing an if statement in Python?", "if x > y:", "if (x > y)", "if x > y then:", "if x > y", "option1", "Python uses colons to indicate the start of an indented block."),
            ("Python", "How do you start writing a while loop in Python?", "while (x > y)", "while x > y:", "while x > y {", "while x > y then:", "option2", "While loops use colons and indentation."),
            ("Python", "How do you start writing a for loop in Python?", "for x in y:", "for x > y:", "for each x in y:", "for (x in y)", "option1", "For loops iterate over sequences."),
            ("Python", "Which statement is used to stop a loop?", "stop", "exit", "break", "return", "option3", "The break statement terminates the current loop.")
        ]
        
        java_questions = [
            ("Java", "What is the correct syntax to output 'Hello World' in Java?", "System.out.println(\"Hello World\");", "Console.WriteLine(\"Hello World\");", "print(\"Hello World\");", "echo(\"Hello World\");", "option1", "Java uses the System.out object for standard output."),
            ("Java", "Java is short for 'JavaScript'.", "True", "False", "Depends on kontekts", "Only in the 90s", "option2", "Java and JavaScript are entirely different languages."),
            ("Java", "How do you insert COMMENTS in Java code?", "// This is a comment", "# This is a comment", "/* This is a comment", "** This is a comment", "option1", "// is the standard single-line comment."),
            ("Java", "Which data type is used to create a variable that should store text?", "String", "Txt", "string", "myString", "option1", "String is a non-primitive data type in Java."),
            ("Java", "How do you create a variable with the numeric value 5?", "num x = 5", "int x = 5;", "x = 5;", "float x = 5;", "option2", "Java is statically typed; int is a 32-bit signed integer."),
            ("Java", "How do you create a variable with the floating point number 2.8?", "num x = 2.8", "float x = 2.8f;", "byte x = 2.8", "int x = 2.8", "option2", "Float literals require an 'f' or 'F' suffix."),
            ("Java", "Which method can be used to find the length of a string?", "getSize()", "length()", "len()", "getLength()", "option2", "The length() method on String objects returns the number of characters."),
            ("Java", "Which operator is used to add together two values?", "+", "&", "*", "/", "option1", "The plus (+) operator is used for addition and string concatenation."),
            ("Java", "The value of a string variable can be surrounded by single quotes.", "False", "True", "Only for character literals", "Depends on compiler", "option1", "String literals must use double quotes; single quotes are for char literals."),
            ("Java", "Which method can be used to return a string in upper case?", "tUpperCase()", "toUpperCase()", "upperCase()", "tUpper()", "option2", "toUpperCase() is a method of the String class."),
            ("Java", "Which operator can be used to compare two values?", "=", "==", "<>", "><", "option2", "Primitive equality is checked with the double equals (==)."),
            ("Java", "To declare an array in Java, define the variable type with:", "[]", "{}", "()", "||", "option1", "Square brackets [] are used to declare arrays."),
            ("Java", "Array indexes start with:", "1", "0", "-1", "Depends on array", "option2", "Java arrays are 0-indexed."),
            ("Java", "How do you create a method in Java?", "methodName()", "methodName[]", "methodName{}", "(methodName)", "option1", "Methods are defined with parenthetical parameters."),
            ("Java", "How do you call a method in Java?", "methodName();", "methodName[];", "(methodName);", "methodName;", "option1", "Methods are invoked by their name followed by parentheses."),
            ("Java", "Which keyword is used to create a class in Java?", "class", "className", "MyClass", "class()", "option1", "The 'class' keyword defines a blueprint for objects."),
            ("Java", "What is the correct way to create an object called myObj of MyClass?", "class MyClass = new myObj();", "MyClass myObj = new MyClass();", "new myObj = MyClass();", "class myObj = new MyClass();", "option2", "Objects are instantiated using the 'new' keyword with a constructor."),
            ("Java", "Which keyword is used to import a package from the Java API library?", "lib", "package", "import", "get", "option3", "The 'import' keyword makes classes/packages available."),
            ("Java", "How do you start writing an if statement in Java?", "if x > y then:", "if (x > y)", "if x > y:", "if x > y then {", "option2", "If conditions must be enclosed in parentheses."),
            ("Java", "How do you start writing a while loop in Java?", "while (x > y)", "while x > y {", "while x > y:", "x > y while {", "option1", "While conditions are enclosed in parentheses.")
        ]
        
        all_q = html_questions + css_questions + js_questions + python_questions + java_questions
        
        cursor.executemany('''
            INSERT INTO questions (subject, question, option1, option2, option3, option4, answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', all_q)
    
    conn.commit()
    conn.close()

init_db()

class Subject(BaseModel):
    name: str
    icon: str

class QuestionSchema(BaseModel):
    id: int
    subject: str
    question: str
    option1: str
    option2: str
    option3: str
    option4: str

class AnswerSubmission(BaseModel):
    question_id: int
    selected_option: str

class SubmissionRequest(BaseModel):
    answers: List[AnswerSubmission]

class ResultDetail(BaseModel):
    question_id: int
    correct_answer: str
    selected_option: str
    is_correct: bool
    explanation: str

class SubmissionResponse(BaseModel):
    score: int
    total: int
    details: List[ResultDetail]

@app.get("/subjects", response_model=List[Subject])
async def get_subjects():
    return [
        Subject(name="HTML", icon="Layout"),
        Subject(name="CSS", icon="Palette"),
        Subject(name="JavaScript", icon="Code2"),
        Subject(name="Python", icon="Py"),
        Subject(name="Java", icon="Coffee")
    ]

@app.get("/questions/{subject}", response_model=List[QuestionSchema])
async def get_questions(subject: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, subject, question, option1, option2, option3, option4 FROM questions WHERE subject = ?", (subject,))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        raise HTTPException(status_code=404, detail="Subject not found")
        
    return [
        QuestionSchema(
            id=row[0],
            subject=row[1],
            question=row[2],
            option1=row[3],
            option2=row[4],
            option3=row[5],
            option4=row[6]
        ) for row in rows
    ]

@app.post("/submit", response_model=SubmissionResponse)
async def submit_quiz(submission: SubmissionRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    score = 0
    details = []
    
    for ans in submission.answers:
        cursor.execute("SELECT id, answer, explanation FROM questions WHERE id = ?", (ans.question_id,))
        row = cursor.fetchone()
        if row:
            correct_ans = row[1]
            explanation = row[2]
            is_correct = ans.selected_option == correct_ans
            if is_correct:
                score += 1
            details.append(ResultDetail(
                question_id=ans.question_id,
                correct_answer=correct_ans,
                selected_option=ans.selected_option,
                is_correct=is_correct,
                explanation=explanation
            ))
    
    conn.close()
    return SubmissionResponse(
        score=score,
        total=len(details),
        details=details
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
