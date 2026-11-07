# Advanced Calculator

A desktop-based multifunctional calculator built with **Python** and
**Tkinter**. The application combines basic arithmetic, scientific
functions, unit conversion, graph plotting, and selectable interface
color themes.

## Features

### 1. Basic calculator

-   Addition, subtraction, multiplication, division, modulus, and powers
-   Parentheses and decimal values
-   Clear (`C`), backspace (`⌫`), and calculate (`=`)
-   Keyboard support: Enter to calculate, Escape to clear, Backspace to
    delete

### 2. Scientific calculator

-   Trigonometric functions: `sin`, `cos`, `tan`
-   Inverse trigonometric functions: `asin`, `acos`, `atan`
-   Square root, common logarithm (`log`), natural logarithm (`ln`)
-   Factorial, absolute value, floor, ceiling, and exponential
-   Pi (`π`) and Euler's number (`e`)
-   Degree (`DEG`) and radian (`RAD`) angle modes

### 3. Unit conversion

-   **Length:** meter, kilometer, centimeter, millimeter, mile, foot,
    inch
-   **Mass:** kilogram, gram, milligram, pound, ounce
-   **Temperature:** Celsius, Fahrenheit, Kelvin
-   **Time:** second, minute, hour, day

### 4. Graph plotter

-   Horizontal bar, vertical bar, line, scatter, and pie charts
-   User-provided comma-separated X and Y values
-   Charts are embedded in the Tkinter application using Matplotlib

### 5. Color themes

Select a theme from the **Color theme** dropdown: - Midnight - Ocean -
Forest - Sunset - Light - Rose

The selected theme updates the application styling and the graph
appearance.

## Requirements

-   Python 3.9 or later recommended
-   Tkinter (included with most standard Python installations)
-   Matplotlib (optional for calculator operation, required for graph
    plotting)

## Installation

1.  Install Python and make sure it is available from your terminal.

2.  Download or clone this project.

3.  Open a terminal in the project folder.

4.  Install Matplotlib:

    ``` bash
    python -m pip install matplotlib
    ```

    If Matplotlib is not installed, the calculator's arithmetic and
    conversion features can still be used; graph plotting will be
    unavailable.

## Run the application

Save the program as `advanced_calculator_color_themes.py`, then run:

``` bash
python advanced_calculator_color_themes.py
```

## How to use

1.  Launch the application.
2.  Select **Basic**, **Scientific**, **Unit Conversion**, or **Graph
    Plotter**.
3.  Enter an expression or values and use the on-screen controls.
4.  In the scientific calculator, select `DEG/RAD` to switch the angle
    mode.
5.  In Unit Conversion, choose a category, enter a value, choose source
    and destination units, then click **Convert**.
6.  In Graph Plotter, enter comma-separated values, choose a chart type,
    and click **Draw Chart**.
7.  Change the appearance at any time using the **Color theme**
    dropdown.

## Example expressions

``` text
25 + 15
sqrt(81)
sin(30)       # in DEG mode
log(100)
factorial(5)
2^3
```

## Project structure

``` text
advanced-calculator/
├── advanced_calculator_color_themes.py
└── README.md
```

## Implementation notes

-   The interface is organized in a `Calculator` class.
-   Tkinter and `ttk` widgets provide the desktop interface.
-   Mathematical expressions are parsed with Python's `ast` module and
    evaluated using an allowlist of supported operators, constants, and
    functions rather than Python's general-purpose `eval()`.
-   Matplotlib's `FigureCanvasTkAgg` embeds charts in the application.
-   Theme colors are stored in the `THEMES` dictionary.

## Known notes

-   Graph plotting requires Matplotlib.
-   Pie charts use the entered X values as labels and Y values as slice
    sizes.
-   The calculator accepts the mathematical syntax and functions listed
    above; it is not a full computer algebra system.
-   The application displays validation and calculation errors in its
    result/status areas or message boxes.

## Author / submission details

-   **Project:** Advanced Calculator
-   **Organization:** NextHikes IT Solutions
-   **Student name:** Add your name here
-   **GitHub repository:** Add your repository URL here

## License

Add a license if you intend to distribute this project publicly.
