# Multiple Choice Grader
A basic grading system for a 100-question multiple choice bubble sheet, written in Python.


![Example 6]("Examples/Example 6.jpg")

I wrote this for grading bubblesheets for practice Physics GRE exams, but it will work for any 100-question multiple choice bubble sheet similar to printable one provided ("BOLD 100 Question Bordered Bubble Sheet Printable.pdf"). More efficient borders may also work, though a thicker one seems to have more recognizable boundaries.


Requirements:
* [OpenCV](https://pypi.org/project/opencv-python/)
* [imutils](https://github.com/jrosebr1/imutils)


Additionally, there are a number of known issues and improvements to make, however I've set this project aside for the time being. I figure physical bubble sheets will be less popular until COVID-19 restrictions can be lifted.

Common Issues and Future Plans:
* Obtaining a proper image of a bubble sheet can be difficult. I have had good experience with [FastScanner](https://play.google.com/store/apps/details?id=com.coolmobilesolution.fastscannerfree). If available, I also recommend using a dedicated scanner rather than a phone camera.
* Currently, the grader relies on recognizing all the bubbles on the page. This is usually fine for a small number of questions, but with 100 questions/500 bubbles, it is easy to have an image where one or more bubbles are not recognized correctly. Unfortunately, this breaks the process. In the future, I plan on modifying the approach to allow for partial grading rather than total failure if part of the image is unreadable.
* Questions left blank or with more than one answer bubbled need to be marked as incorrect. (Perhaps this can be done by checking if there is no single bubble at a sufficiently distinct grayscale level from the other 4.)


I credit the approach to a blog post by Adrian Rosebrock at PyImageSearch:

Adrian Rosebrock, Bubble sheet multiple choice scanner and test grader using OMR, Python and OpenCV, PyImageSearch, https://www.pyimagesearch.com/2016/10/03/bubble-sheet-multiple-choice-scanner-and-test-grader-using-omr-python-and-opencv/, accessed on January 2020

https://www.pyimagesearch.com/faqs/single-faq/what-is-the-code-license-associated-with-your-examples/
