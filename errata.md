# Errata, Corrections and Improvements
----------------------------------------------------
If you find any mistakes in the second edition of Python GUI Programming with Tkinter, or if you have suggestions for improvements, then please [raise an issue in this repository](https://github.com/PacktPublishing/Python-GUI-Programming-with-Tkinter-2E/issues), or email to us.

## Chapter01, Page 8 - Adding the missing alias name `tk` in the code lines

Incorrect code is:
```
root = Tk()

label = Label(root, text="Hello World")
```
Correct code is:
```
root = tk.Tk()

label = tk.Label(root, text="Hello World")
```
You can find this code correct in the file here: `Chapter01/hello_tkinter.py`
