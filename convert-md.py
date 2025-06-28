from pathlib import Path
import convert_markdown

# File paths
markdown_content = """
<h2> Section 1</h2>

---

### Question 1

A.

B.

C.

D.

---

### Question 2


A. 
B. 
C. 
D.  

---

### Question 3


A. 
B. 
C. 
D.  

---
### Question 4


A. 
B. 
C. 
D.  

---
### Question 5


A. 
B. 
C. 
D.  

---

### Question 6


A. 
B. 
C. 
D.  

---
### Question 7


A. 
B. 
C. 
D.  

---
### Question 8


A. 
B. 
C. 
D.  

---
### Question 9


A. 
B. 
C. 
D.  

---
### Question 10


A. 
B. 
C. 
D.  

---

<h2> Round 1 Answers</h2>

1.
2.
3.
4.
5.
6.
7.
8.
9.
10. 

---

<h2> Section 2</h2>

---
### Question 11


A. 
B. 
C. 
D.  

---
### Question 12


A. 
B. 
C. 
D.  

---
### Question 13


A. 
B. 
C. 
D.  

---
### Question 14


A. 
B. 
C. 
D.  

---
### Question 15


A. 
B. 
C. 
D.  

---
# Halftime



---
### Question 16


A. 
B. 
C. 
D.  

---
### Question 17


A. 
B. 
C. 
D.  

---
### Question 18


A. 
B. 
C. 
D.  

---
### Question 19


A. 
B. 
C. 
D.  

---
### Question 20


A. 
B. 
C. 
D.  

---

<h2> Round 2 Answers</h2>

11.
12.
13.
14.
15.
16.
17.
18.
19.
20.

---
<h2> Halftime Answers</h2>


---

<h2> Section 3</h2>

---
### Question 21


A. 
B. 
C. 
D.  

---
### Question 22


A. 
B. 
C. 
D.  

---
### Question 23


A. 
B. 
C. 
D.  

---
### Question 24


A. 
B. 
C. 
D.  

---
### Question 25


A. 
B. 
C. 
D.  

---
### Question 26


A. 
B. 
C. 
D.  

---
### Question 27


A. 
B. 
C. 
D.  

---
### Question 28


A. 
B. 
C. 
D.  

---
### Question 29


A. 
B. 
C. 
D.  

---
### Question 30


A. 
B. 
C. 
D.  

---

<h2> Round 3 Answers</h2>

21.
22.
23.
24.
25.
26.
27.
28.
29.
30.

---

<h2> Final Category</h2> 

---

Final Question here

---

<h2> Final Answer</h2>

Answer here

"""

# Add CSS for styling
css_styles = """
<style>
  body {
    font-family: Arial, sans-serif;
    background-color: #301f6e;
    color: #D82F86;
    margin: 0;
    padding: 0;
  }
  h1, h2, h3 {
    color: #00AEEF;
    text-align: center; /* Center headers */
    margin-top: 50px; /* Add spacing above headers */
  }
  section {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 100vh;
  }
  .answers {
    font-size: 25px;
  }
</style>
"""

# Method 1: Get bytes and save manually
output = convert_markdown.to(
    markdown=markdown_content,
    style='css_styles', # default: 'style', 'style1', 'style2', 'style3', 'custom'
    format='pdf'    # default: 'pdf', 'docx', 'pptx', 'html'
)
with open(r'/Users/muneer78/Documents/Projects/trivia-night/output.pdf', 'wb') as f:
    f.write(output)