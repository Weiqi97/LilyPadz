# Cane Toads Visualization

## A LilyPADz Production

LilyPADz is a student-led software development project devoted to understanding the biomechanics of humans through the visual analysis of Cane Toads. The software application is hosted on Wheaton College's Department of Computer Science server. It is a web-based visualization demonstrating the relationship between the kinematic movements of Cane Toads and the forces exerted when they hop. The software also analyzes the impact of a toad's vision and lack of vision on the factors mentioned previously.

### The Software

The software application is built with a flask microframework. The backend is written in Python and utilizes the Pandas Dataframes library while the frontend is written in HTML5, CSS, and JavaScript. It was created to help a Wheaton College biology professor summarize her research and draw conclusions about the data she collected.

### Getting Started

The kinematic movements, forces, and time series data of five different Cane Toads have already been gathered and stored within the application. Users simply must visit [LilyPADz](http://cs.wheatoncollege.edu/lilypadz/) in order to visualize the data. They have the ability to choose between comparing the data of different toads or analyzing the data of a single toad.

### The Visualization

This visualization is a combination of time series and small multiples. The small multiples portion of the visualization consists of six different rows in which each row is a force from the force plate data (fore-aft force, lateral force, normal force) or a kinematic movement from the kinematic movement data (elbow flexion/extension, humeral protraction/retraction and humeral elevation/depression). Each row will have its own y-axis which measures that specific variable. However, all rows share the same x-axis which measures time in .01 second increments. Thus, this visualization incorporates small multiples and time series in order to help the user clearly understand the data and make informed conclusions about it.

In addition, the software implements two other methods of visualizing the data including linear regression and clustering analysis.

#### Acknowledgements
- Laura Ekstrom
- Doug Werry 

#### Team Members
- Arianna Alfiero
- Krissa Cusanelli
- Weiqi Feng
- Xinru Liu
