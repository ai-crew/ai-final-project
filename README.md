# AI - Linear Regression Tool

### What is this project?
As the name suggests, this a linear regression tool, created as a single page application. It has been created using the [Dash](https://dash.plotly.com/), a python framework for web development. Visualizations were created using the [plotly library](https://github.com/plotly/plotly.py). The deployed app is hosted on Heroku, and you can find it [here](https://linear-regression-viz.herokuapp.com/).

### Team Members
* Ihsan Ahmed
* Elizabeth Aufzien
* Hussein Mohamed
* Ege Seyithanoglu
* Abdullah Yousuf
> Listed in last name A -> Z order

### Getting Started for Devs
* Clone the repository:
```
git clone https://github.com/ai-crew/ai-final-project.git
```

* Installing dependencies:
```
pip install -r requirements.txt
```
> Note: Additional 'convenience' packages such as the "black" code formatter need to be separately installed.

* Running the app:
```
python app.py
```

* Code clean up:
```
black app.py
```

* Saving new dependencies:
```
pipreqs --force
```
> Note: pipreqs only saves project dependencies, to save all environment dependencies use:
```
pip freeze > requirements.txt
```

### User Guide

When you first open the app, you will be given the choice to upload your own dataset or select a sample dataset.

If you opt into the second option (selecting a sample dataset), you will be taken to a page where you select a dataset using a dropdown. Then, you can select which variable in the dataset to use as the X variable and which variable to use as the Y variable. If you would like, you can specify an initial weight and bias for the linear regression model by toggling the "Specify initial weight and bias" option and entering values for the initial weight and bias.

You can specify values for the learning rate and iteration amount by entering values in their respective input fields. Note that when you change the learning rate or iteration amount, it may take several seconds to generate a new graph and recompute the values for the weight and bias in the linear regression model. Underneath the fields for the learning rate and iteration amount is the graph displaying a scatter plot of the points in the dataset and the regression line.

Then, underneath the graph are two panels. The panel on the left shows the equation of the linear regression line, the values for the weight and bias, and the final cost. The panel on the right shows a graph of the cost as a function of the number of iterations.

If you opt in the first choice, uploading your own dataset, you will be taken to a page that looks similar to the page taken by pressing "Select a sample dataset". At the top of the page, you have an option to download a sample dataset to your local computer. Underneath that is the place where you upload your own dataset which should either be a .csv or .xlsx file. Once the file is uploaded, a message with the text "File uploaded successfully" will be written under the upload area and the filename will be written under this message.

After that, the "Add Point" button allows you to optionally add points to your dataset. Once you press the "Add Point" button, a modal pops up. You can enter X and Y values for the points to be added in the fields in the modal. If you wish to add multiple points, you can press the "Add more points" button. Once you are done adding points, you can press the "Add" button, which will add the points and close the modal. Note that only valid inputs (i.e., points whose X and Y values are not empty) will actually be added to the dataset. At any time, you can press the "Add Point" button to edit the points you added.

If the dataset you uploaded does not have column labels as the first row, you should toggle the "Add custom labels to axes" option. Subsequently, you choose to label the X-axis and Y-axis with custom values or use the default values. The remainder portion of the page (specifying initial weight and bias, specifying learning rate and iteration amount, the graph, the panel with the computed linear regression line, and the panel with the cost graph) are the same as their corresponding elements as described above for the page taken to by pressing "Select a sample dataset". 

We hope you enjoy using our application!
