# Name: Vi Nguyen
# Date: March 13, 2023
# Description: Unit Conversion functionality with
# Microservice to search for food recipes
# Ties in with health & fitness

import tkinter as tk
import tkinter.font as font
from tkinter import *
import json
import requests
from tkinter import messagebox
from tkinter import END

# Global variables for nav buttons or else throws errors while running
home_wind, search_wind, hist_wind, more_wind = None, None, None, None

def run_page():
    """
    Landing page once running foodie.py app
    Runs Home page
    """
    global convChange, unit_menu, convResults, storeHistory, landingPage, home_wind
    storeHistory = {}
    landingPage = Tk()
    landingPage.title('Food Conversion')
    landingPage.geometry('300x550')
    center_window(landingPage, 300, 550)

    moreFrame = Frame(landingPage)
    moreFrame.pack()

    ################# HOME TITLE TEXT ######################
    headerText(moreFrame, 'Home')
    ############################################################

    ###################### DROP DOWN MENU UNITS ###################
    menu_btn = ['grams to lbs', 'grams to oz', 'g fat to cals', 'g carbs to cals', 'g prot to cals',
                'cups to oz', 'quarts to cups', 'quarts to pints', 'gallons to quarts']
    clicked = StringVar()
    clicked.set("Select Measurement")
    unit_menu = clicked
    ################################################################

    conversion_entry = Frame(moreFrame)
    conversion_entry.pack(padx=10, pady=10)

    convChange = Entry(conversion_entry, width=10)
    convChange.pack(side=LEFT)

    unit_menu = OptionMenu(conversion_entry, clicked, *menu_btn, command=updateUnitMenu)
    unit_menu.pack(side=LEFT, padx=5)

    convert_button = Button(conversion_entry, text='Convert', command=convertUnits)
    convert_button.pack(side=LEFT, padx=5)

    convResults = Text(moreFrame, width=25, height=15)
    convResults.pack()

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(landingPage)
    ############################################################

    ################################# https://www.geeksforgeeks.org/dropdown-menus-tkinter/

    landingPage.mainloop()


def make_request():
    """
    Creates New Window with prompt to user asking them to enter an ingredient.
    Hitting "Submit" will send a GET request to my partner's microservice
    """
    global response_text

    input_box = Toplevel()
    input_box.title('Enter Ingredient Name')
    input_box.geometry('200x100')
    center_window(input_box, 200, 100)

    # Create text label 'Enter Ingredient'
    input_label = Label(input_box, text='Enter Ingredient:')
    input_label.pack()

    # Creates a manual text entry for user input
    input_entry = Entry(input_box)
    input_entry.pack()

    # Creates submit button under text entry with a get request to microservice by calling send_request(arg1) fxn
    submit_button = Button(input_box, text='Submit', command=lambda: send_request(input_entry.get()))
    submit_button.pack()


def send_request(arg1):
    """
    GET request which triggers this function.
    Data from request is sent as
            Name: ____
            Calories: ___
            Ingredient:
            -- Name: ____
               Quantity: __
               Units: ___
    """
    # Make HTTP request
    response = requests.get(f'http://localhost:5000/recipes?name={arg1}')

    recipe_reso = json.loads(response.text)

    output = ""
    for recipe_id, recipe_data in recipe_reso.items():
        output += f"Name: {recipe_data['name']}\n"
        output += f"Calories: {recipe_data['calories']}\n"
        output += "Ingredients:\n"
        for ingredient in recipe_data['ingredients']:
            output += f"- Name: {ingredient['name']}\n"
            output += f" Quantity: {ingredient['quantity']}\n"
            output += f" Units: {ingredient['units']}\n"

    # Update Text widget with response content
    response_text.delete('1.0', END)
    response_text.insert(END, output)


def updateProfile(name, weight, height):
    """
    Takes user input and returns edit by
    Name: __
    Weight: __ lbs
    Height: __ cms
    """
    userName.config(text=f'Name: {name}')
    userWeight.config(text=f'Weight: {weight} lbs')
    userHeight.config(text=f'Height: {height} cms')


def confirmBtn():
    """
    Pops up confirmation if user clicks "Save Changes"
    """
    prompt = messagebox.askyesno('Would You Like to Proceed?', icon='question')

    if prompt == True:
        updateProfile(nameEntry.get(), weightEntry.get(), heightEntry.get())
        editWindow.destroy()


def editBtn():  # https://www.youtube.com/watch?v=tpwu5Zb64lQ
    """
    New window prompt which allows new text entry for Name, Weight, & Height
    """
    global nameEntry, weightEntry, heightEntry, editWindow
    editWindow = Toplevel()
    editWindow.title('Edit Profile')
    editWindow.geometry('225x225')
    center_window(editWindow, 225, 225)

    # Create labels and entry fields for user input
    nameLabel = Label(editWindow, text='Name: ')
    nameLabel.grid(row=0, column=0, padx=10, pady=10)
    nameEntry = Entry(editWindow)
    nameEntry.grid(row=0, column=1)

    weightLabel = Label(editWindow, text='Weight: ')
    weightLabel.grid(row=1, column=0, padx=10, pady=10)
    weightEntry = Entry(editWindow)
    weightEntry.grid(row=1, column=1)

    heightLabel = Label(editWindow, text='Height: ')
    heightLabel.grid(row=2, column=0, padx=10, pady=10)
    heightEntry = Entry(editWindow)
    heightEntry.grid(row=2, column=1)

    # Button to save changes and update labels in the main window
    saveBtn = Button(editWindow, text='Save Changes', command=confirmBtn)
    saveBtn.grid(row=3, column=1, padx=3, pady=5)


def convertUnits():
    """
    Converts input from user into their perspective units chosen by user
    """
    global cvrtAns, storeHistory
    user_input = convChange.get()

    # Dictionary to store conversion functions and their labels
    conversion_funcs = {
        'grams to lbs': (lambda x: x * 0.00220462, 'grams', 'lbs'),
        'grams to oz': (lambda x: x * 0.035274, 'g prot', 'oz'),
        'g fat to cals': (lambda x: x * 9, 'g fat', 'cals'),
        'g carbs to cals': (lambda x: x * 4, 'g carbs', 'cals'),
        'g prot to cals': (lambda x: x * 4, 'g prot', 'cals'),
        'cups to oz': (lambda x: x * 8, 'cups', 'oz'),
        'quarts to cups': (lambda x: x * 4, 'qts', 'cups'),
        'quarts to pints': (lambda x: x * 2, 'qts', 'pints'),
        'gallons to quarts': (lambda x: x * 4, 'galns', 'qts')
    }

    # Check if selected unit is in the conversion dictionary
    if unit_menu in conversion_funcs:
        # Get the conversion function and labels
        conversion_func, input_label, output_label = conversion_funcs[unit_menu]

        # Perform the conversion
        result = conversion_func(int(user_input))
        cvrtAns = f"{round(result, 5)} {output_label}"

        # Update input label and display result
        user_input = user_input + f' {input_label}'
        convResults.delete(1.0, END)
        convResults.insert(END, cvrtAns)

    # Store user input in History Log to display
    storeHistory[user_input] = cvrtAns


def updateUnitMenu(selected):
    """
    Drop-down menu and returns unit selected in preparation for unit conversion
    """
    global unit_menu
    unit_menu = selected


def navigation_buttons(window):
    """
    Buttons created located at bottom of each page
    If you are at page Home and press Home, new Home window will not open and close old window
    Same applies to all other buttons
    """
    navFrame = Frame(window)
    navFrame.pack(side=BOTTOM, fill=X)
    textResize = font.Font(family='Helvetica', size=12, weight='bold')

    if window == landingPage:
        buttonHome = Button(navFrame, text='Home', font=textResize, fg='red')
    elif window == home_wind:
        buttonHome = Button(navFrame, text='Home', font=textResize, fg='red')
    else:
        buttonHome = Button(navFrame, text='Home', font=textResize, fg='red', command=lambda: navigate(window, homeWindow))
    buttonHome.grid(row=0, column=0, padx=1, pady=20)

    if window == search_wind:
        buttonSearch = Button(navFrame, text='Search', font=textResize, fg='red')
    else:
        buttonSearch = Button(navFrame, text='Search', font=textResize, fg='red', command=lambda: navigate(window, searchWindow))
    buttonSearch.grid(row=0, column=1, padx=1, pady=20)

    if window == hist_wind:
        buttonLog = Button(navFrame, text='History Log', font=textResize, fg='red')
    else:
        buttonLog = Button(navFrame, text='History Log', font=textResize, fg='red', command=lambda: navigate(window, historyWindow))
    buttonLog.grid(row=0, column=2, padx=1, pady=20)

    if window == more_wind:
        buttonMore = Button(navFrame, text='More', font=textResize, fg='red')
    else:
        buttonMore = Button(navFrame, text='More', font=textResize, fg='red', command=lambda: navigate(window, moreWindow))
    buttonMore.grid(row=0, column=3, padx=1, pady=20)

    ##### Not used -- If erased, makes Left arrow button look funky and distorted for some reason ?????
    rightArrow = Button(navFrame, font=textResize, text="\N{RIGHTWARDS BLACK ARROW}",
                        command=lambda: next_win())
    ######
    if window == landingPage:
        leftArrow = Button(navFrame, font=textResize, text="\N{LEFTWARDS BLACK ARROW}")
    elif window == home_wind:
        leftArrow = Button(navFrame, font=textResize, text="\N{LEFTWARDS BLACK ARROW}")
    else:
        leftArrow = Button(navFrame, font=textResize, text="\N{LEFTWARDS BLACK ARROW}",
                           command=lambda: prev_win(window))

    leftArrow.grid(row=1, column=0, pady=12)

def navigate(window, new_wind):
    """
    Retracts and Pops up appropriate window when buttons are pressed
    """
    window.withdraw()
    new_wind()

def center_window(window, w, h):
    """
    Takes current window and its sizes to centralize the window on your screen
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - w) // 2
    y = (screen_height - h) // 2
    window.geometry(f"{w}x{h}+{x}+{y}")


def prev_win(curr_win):
    """
    When left arrow is pressed, it destroys the window, thus simulating an arrow press
    """
    if curr_win == search_wind:
        curr_win.withdraw()
        homeWindow()
    if curr_win == hist_wind:
        curr_win.withdraw()
        homeWindow()
    if curr_win == more_wind:
        curr_win.withdraw()
        homeWindow()
    else:
        curr_win.withdraw()



def headerText(word, pageTitle):
    """
    Styling for header of each page
    """
    textResize = font.Font(family='Helvetica', size=36, weight='bold')
    label_frame1 = Label(word, text=pageTitle, font=textResize, bg='indian red', fg='white', anchor='center')
    label_frame1.pack(side='top', fill='x', padx=10, pady=10)


def homeWindow():
    """
    Home page that pops up when pressed
    Has units of conversion on primary page
    Any conversion is recorded and can be seen on the History Log
    """
    global convChange, unit_menu, convResults, home_wind
    home_wind = Toplevel()
    home_wind.title('Food Conversion')
    home_wind.geometry('300x550')
    center_window(home_wind, 300, 550)

    ################# HOME TITLE TEXT ######################
    headerText(home_wind, 'Home')
    ############################################################

    ###################### DROP DOWN MENU UNITS ###################
    menu_btn = ['grams to lbs', 'grams to oz', 'g fat to cals', 'g carbs to cals', 'g prot to cals',
                'cups to oz', 'quarts to cups', 'quarts to pints', 'gallons to quarts']
    clicked = StringVar()
    clicked.set("Select Measurement")
    unit_menu = clicked
    ################################################################

    conversion_entry = Frame(home_wind)
    conversion_entry.pack(padx=10, pady=10)

    convChange = Entry(conversion_entry, width=10)
    convChange.pack(side=LEFT)

    unit_menu = OptionMenu(conversion_entry, clicked, *menu_btn, command=updateUnitMenu)
    unit_menu.pack(side=LEFT, padx=5)

    convert_button = Button(conversion_entry, text='Convert', command=convertUnits)
    convert_button.pack(side=LEFT, padx=5)

    convResults = Text(home_wind, width=25, height=15)
    convResults.pack()

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(home_wind)
    ############################################################

    ################################# https://www.geeksforgeeks.org/dropdown-menus-tkinter/


def searchWindow():
    """
    Pops up search window when pressed which allows user to search for ingredients through Microservice
    created by partner
    """
    global response_text, search_wind
    search_wind = Toplevel()
    search_wind.title('Search')
    search_wind.geometry('300x550')
    center_window(search_wind, 300, 550)

    ################# SEARCH TITLE TEXT ######################
    headerText(search_wind, 'Search')
    ############################################################
    # Create text label 'Enter Ingredient'
    input_label = Label(search_wind, text='Enter Ingredient You Would Like To Search:')
    input_label.pack()

    ################# USER INPUT FOR SEARCH ####################
    # Creates a manual text entry for user input
    input_entry = Entry(search_wind)
    input_entry.pack()
    ############################################################

    # Creates submit button under text entry with a get request to microservice by calling send_request(arg1) fxn
    submit_button = Button(search_wind, text='Submit', command=lambda: send_request(input_entry.get()))
    submit_button.pack()

    response_text = Text(search_wind, width=25, height=15)
    response_text.pack()

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(search_wind)
    ############################################################


def historyWindow():
    """
    Pops up this window when History Log button is pressed
    Stores all units of conversions and can be seen here
    """
    global storeHistory, hist_wind
    hist_wind = Toplevel()
    hist_wind.title('History Log')
    hist_wind.geometry('300x550')
    center_window(hist_wind, 300, 550)

    ################# SEARCH TITLE TEXT ######################
    headerText(hist_wind, 'History Log')
    ############################################################

    # Stored conversion units displayed here
    response_text = Text(hist_wind, width=30, height=20)
    response_text.pack()

    for key, value in storeHistory.items():
        response_text.insert(END, f"{key} -> {value}\n")

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(hist_wind)
    ############################################################


def moreWindow():
    """
    Contains extra buttons which allows user to scavenge for more functionalities
    """
    global more_wind
    more_wind = Toplevel()
    more_wind.title('More')
    more_wind.geometry('300x550')
    center_window(more_wind, 300, 550)

    moreFrame = Frame(more_wind)
    moreFrame.pack()

    ################# SEARCH TITLE TEXT ######################
    headerText(moreFrame, 'More')
    ############################################################

    # Font Resizing for buttons
    textResize = font.Font(family='Helvetica', size=12, weight='bold')

    ################# BUTTONS FOR MORE PAGE #################
    profileBtn = Button(moreFrame, text='Profile', font=textResize, fg='red', command=profileWindow)
    profileBtn.pack()
    recipesBtn = Button(moreFrame, text='Recipes', font=textResize, fg='red', command=recipeWindow)
    recipesBtn.pack()
    goalsBtn = Button(moreFrame, text='Goals', font=textResize, fg='red', command=goalsWindow)
    goalsBtn.pack()
    eventsBtn = Button(moreFrame, text='Events', font=textResize, fg='red', command=eventsWindow)
    eventsBtn.pack()
    friendsBtn = Button(moreFrame, text='Friends', font=textResize, fg='red', command=friendsWindow)
    friendsBtn.pack()
    verBtn = Button(moreFrame, text='Verification', font=textResize, fg='red', command=verWindow)
    verBtn.pack()
    ##########################################################

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(more_wind)
    ############################################################


def profileWindow():
    """
    Displays Name, Weight, and Height of user
    Has edit button to change descriptions with confirmation of change
    """
    global userName, userWeight, userHeight, prof_wind
    prof_wind = Toplevel()
    prof_wind.title('Profile')
    prof_wind.geometry('300x550')
    center_window(prof_wind, 300, 550)

    editFrame = Frame(prof_wind)
    editFrame.pack(side=BOTTOM, fill=X)
    tryBtn = font.Font(family='Helvetica', size=18, weight='bold')
    editFont = font.Font(family='Helvetica', size=12, weight='bold')

    ################# SEARCH TITLE TEXT ######################
    headerText(prof_wind, 'Profile')
    ############################################################

    userName = Label(prof_wind, text='Name: John Doe', font=tryBtn)
    userName.pack()

    userWeight = Label(prof_wind, text='Weight: 180 lbs', font=tryBtn)
    userWeight.pack()

    userHeight = Label(prof_wind, text='Height: 182 cms.', font=tryBtn)
    userHeight.pack()

    affirm_button = Button(prof_wind, text='Edit Profile', font=editFont, command=editBtn)
    affirm_button.pack(padx=5, pady=100, anchor='center')

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(prof_wind)
    ############################################################


def recipeWindow():
    """
    Contains Microservice to search for recipe, developed by partner
    Also has 3 other buttons which displays recipes of Chicken Parm, Spaghetti, and Kun Pao Chkn
    REAL RECIPES BTW!!
    """
    global response_text, recipe_wind
    recipe_wind = Toplevel()
    recipe_wind.title('Recipes')
    recipe_wind.geometry('300x550')
    center_window(recipe_wind, 300, 550)

    moreFrame = Frame(recipe_wind)
    moreFrame.pack()

    ########################HEADER for Recipes Page ######################
    headerText(moreFrame, 'Recipes')
    ######################################################################

    ###################### Pre-Filled Recipes##########################

    # Font Resizing for buttons
    textResize = font.Font(family='Helvetica', size=12, weight='bold')
    tryBtn = font.Font(family='Helvetica', weight='bold')

    chickenParm = Button(moreFrame, text='Chicken Parmasean', font=textResize, fg='red', command=chknParm)
    chickenParm.pack()

    spaghetti = Button(moreFrame, text='Spaghetti', font=textResize, fg='red', command=spaghet)
    spaghetti.pack()

    kungpaoChkn = Button(moreFrame, text='Kung Pao Chicken', font=textResize, fg='red', command=kungpao)
    kungpaoChkn.pack()
    ##################################################################

    request_button = tk.Button(moreFrame, text='Try New Recipe!', font=tryBtn, command=make_request)
    request_button.pack()

    # Add Text widget to display response
    response_text = Text(moreFrame, width=50, height=10)
    response_text.pack()

    recipe_wind.resizable(True, True)

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(recipe_wind)
    ############################################################


def chknParm():
    """
    Pops up actual recipe of Chicken Parmasean
    """
    chkn_wind = Toplevel()
    chkn_wind.title('Chicken Parmasean')
    chkn_wind.geometry('700x600')
    center_window(chkn_wind, 700, 600)

    # Create text for recipe Chicken Parmasean
    input_label = Label(chkn_wind, text='Name: '
                                        '\nChicken Parmasean'
                                        '\n'
                                        '\nIngredients:'
                                        '\n'
                                        '\n4 skinless, boneless chicken breast halves'
                                        '\nsalt and freshly ground black pepper to taste'
                                        '\n2 large eggs'
                                        '\n1 cup panko bread crumbs, or more as needed'
                                        '\n¾ cup grated Parmesan cheese, divided'
                                        '\n2 tablespoons all - purpose flour, or more if needed'
                                        '\n½ cup olive oil for frying, or as needed'
                                        '\n½ cup prepared tomato sauce'
                                        '\n¼ cup fresh mozzarella, cut into small cubes'
                                        '\n¼ cup chopped fresh basil'
                                        '\n½ cup grated provolone cheese'
                                        '\n2 teaspoons olive oil'
                                        '\n'
                                        '\nInstructions:'
                                        '\n'
                                        '\n1. Preheat an oven to 450 degrees F (230 degrees C).'
                                        '\n2. Place chicken breasts between two sheets of heavy plastic (resealable freezer bags '
                                        '\nwork well) on a solid, level surface. Firmly pound chicken with the smooth side of a '
                                        '\nmeat mallet to a thickness of 1/2-inch.'
                                        '\n3. Season chicken thoroughly with salt and pepper. Using a sifter or strainer; sprinkle '
                                        '\nflour over chicken breasts, evenly coating both sides'
                                        '\n4. Beat eggs in a shallow bowl and set aside.'
                                        '\n5. Mix bread crumbs and 1/2 cup Parmesan cheese in a separate bowl, set aside.'
                                        '\n6. Dip a flour-coated chicken breast in beaten eggs. Transfer breast to the bread crumb mixture, '
                                        '\npressing crumbs into both sides. Repeat for each breast. Let chicken rest for 10 to 15 minutes.'
                                        '\n7. Heat 1/2 inch olive oil in a large skillet on medium-high heat until it begins to shimmer. '
                                        '\n Cook chicken in the hot oil until golden, about 2 minutes per side. The chicken will finish cooking in the oven.'
                                        '\n8. Transfer chicken to a baking dish. Top each breast with 2 tablespoons tomato sauce. Layer each chicken breast '
                                        '\nwith equal amounts of mozzarella cheese, fresh basil, and provolone cheese. Sprinkle remaining Parmesan over top '
                                        '\nand drizzle each with 1/2 teaspoon olive oil.'
                                        '\n9. Bake in the preheated oven until cheese is browned and bubbly and chicken breasts are no longer pink in the center, '
                                        '\n15 to 20 minutes. An instant-read thermometer inserted into the center should read at least 165 degrees F (74 degrees C).'
                                        '\nEnjoy!')
    input_label.pack()


def spaghet():
    """
    Pops up actual recipe of Spaghetti
    """
    spag_wind = Toplevel()
    spag_wind.title('Chicken Parmasean')
    spag_wind.geometry('550x400')
    center_window(spag_wind, 550, 400)

    # Create text for recipe Spaghetti
    input_label = Label(spag_wind, text='Name: '
                                        '\nSpaghetti'
                                        '\n'
                                        '\n Ingredients:'
                                        '\n'
                                        '\n 1 lb Hamburger'
                                        '\n 2 cubes beef bouillion'
                                        '\n 1 can tomato sauce 8 oz'
                                        '\n 1 can tomato paste 6 oz'
                                        '\n pepper to taste'
                                        '\n 2 cups hot water'
                                        '\n 2 teaspoon sugar'
                                        '\n 1/2 teaspoon dried basil'
                                        '\n 1/2 teaspoon dried oregano'
                                        '\n dash of garlic'
                                        '\n 16 oz spaghetti noodles'
                                        '\n'
                                        '\n'
                                        '\nInstructions:'
                                        '\n'
                                        '\n1. Brown your hamburger in a large pan.'
                                        '\n2. Once cooked, throw in salt, pepper, tomato sauce and paste, water (with the '
                                        '\nbouillon cubes in it), sugar, basil, oregano and garlic. Simmer on low for an hour.'
                                        '\n3. A few minutes before the hour is done, cook box of spaghetti noodles as directed on package.'
                                        '\n4. Once the noodles are cooked, drain and add to spaghetti sauce. ENJOY!')
    input_label.pack()


def kungpao():
    """
    Pops up actual recipe of Kung Pao Chicken
    """
    kpc_wind = Toplevel()
    kpc_wind.title('Chicken Parmasean')
    kpc_wind.geometry('550x500')
    center_window(kpc_wind, 550, 500)

    # Create text label for recipe Kung Pao Chicken
    input_label = Label(kpc_wind, text='Name: '
                                       '\nKung Pao Chicken'
                                       '\n'
                                       '\nIngredients:'
                                       '\n'
                                       '\n2 tablespoons cornstarch, dissolved in 2 tablespoons water'
                                       '\n2 tablespoons white wine, divided'
                                       '\n2 tablespoons soy sauce, divided'
                                       '\n2 tablespoons sesame oil, divided'
                                       '\n1 pound skinless, boneless chicken breast halves - cut into chunks'
                                       '\n1 ounce hot chile paste'
                                       '\n2 teaspoons brown sugar'
                                       '\n1 teaspoon distilled white vinegar'
                                       '\n1 (8 ounce) can water chestnuts'
                                       '\n4 ounces chopped peanuts'
                                       '\n4 green onions, chopped'
                                       '\n1 tablespoon chopped garlic'
                                       '\n'
                                       '\nInstructions:'
                                       '\n'
                                       '\n1.Combine water and cornstarch in a cup; set aside.'
                                       '\n2.Combine 1 tablespoon wine, 1 tablespoon soy sauce, 1 tablespoon sesame oil, '
                                       '\nand 1 tablespoon cornstarch/water mixture in a large glass bowl. Add chicken pieces '
                                       '\nand toss to coat. Cover the dish and refrigerate for about 30 minutes.'
                                       '\n3. Combine remaining 1 tablespoon wine, 1 tablespoon soy sauce, 1 tablespoon sesame '
                                       '\noil, and remaining cornstarch/water mixture in a medium bowl. Whisk in chile paste, brown'
                                       '\nsugar, and vinegar. Add water chestnuts, peanuts, green onions, and garlic and toss to coat.'
                                       '\n4. Transfer water chestnut mixture to a medium skillet. Heat slowly over medium heat until aromatic.'
                                       '\n5. Meanwhile, transfer chicken from marinade into a large skillet; cook over medium-high heat, '
                                       '\nstirring, until chicken is cooked through and juices run clear.'
                                       '\n6. Combine water chestnut mixture and sautéed chicken together in one skillet. Adjust '
                                       '\nheat and simmer together until sauce thickens. Enjoy!')
    input_label.pack()


def goalsWindow():
    """
    No functionalities here
    Displays text of goals
    Filler to make More page look more full
    """
    global goals_wind
    goals_wind = Toplevel()
    goals_wind.title('Goals')
    goals_wind.geometry('300x550')
    center_window(goals_wind, 300, 550)

    moreFrame = Frame(goals_wind)
    moreFrame.pack()

    ########################HEADER for Recipes Page ######################
    headerText(goals_wind, 'Goals')
    ######################################################################

    tryBtn = font.Font(family='Helvetica', size=16, weight='bold')

    goal1 = Label(goals_wind, text='Goal 1: ', fg='red', font=tryBtn)
    goal1.pack()
    goal1_5 = Label(goals_wind, text='Run 1 Mile every other day', font=tryBtn)
    goal1_5.pack()

    goal2 = Label(goals_wind, text='Goal 2: ', fg='red', font=tryBtn)
    goal2.pack()
    goal2_5 = Label(goals_wind, text='Drop 10 lbs by 5/20/23', font=tryBtn)
    goal2_5.pack()

    goal3 = Label(goals_wind, text='Goal 3: ', fg='red', font=tryBtn)
    goal3.pack()
    goal3_5 = Label(goals_wind, text='Drink 2 liters of water per day', font=tryBtn)
    goal3_5.pack()

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(goals_wind)
    ############################################################


def eventsWindow():
    """
    Displays actual events occuring
    No functionalities developed here
    Filler to make More page look more full
    """
    global events_wind
    events_wind = Toplevel()
    events_wind.title('Events')
    events_wind.geometry('300x550')
    center_window(events_wind, 300, 550)

    moreFrame = Frame(events_wind)
    moreFrame.pack()

    ########################HEADER for Recipes Page ######################
    headerText(events_wind, 'Events')
    ######################################################################

    tryBtn = font.Font(family='Helvetica', size=13, weight='bold')

    event1 = Label(events_wind, text='Event 1: ', fg='red', font=tryBtn)
    event1.pack()

    event1_2 = Label(events_wind, text='Improv Gym LA '
                                       '\n March 18, 2023'
                                       '\n Sat, 3:00 - 4:30 PM'
                                       '\n Glendale, CA', font=tryBtn)
    event1_2.pack()

    event2 = Label(events_wind, text='Event 2: ', fg='red', font=tryBtn)
    event2.pack()

    event2_2 = Label(events_wind, text='626 Night Market '
                                       '\n March 19, 2023'
                                       '\n Sun, 1 - 10 PM'
                                       '\n Santa Monica, CA', font=tryBtn)
    event2_2.pack()

    event3 = Label(events_wind, text='Event 3: ', fg='red', font=tryBtn)
    event3.pack()

    event3_2 = Label(events_wind, text='Beach Bootcamp '
                                       '\n April 1, 2023'
                                       '\n Sat, 8 - 9 AM'
                                       '\n Seal Beach, CA', font=tryBtn)
    event3_2.pack()

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(events_wind)
    ############################################################


def friendsWindow():
    """
    No functionalities
    Displays random names of 'friends'
    Filler to make More page look more full
    """
    global friends_wind
    friends_wind = Toplevel()
    friends_wind.title('Friends')
    friends_wind.geometry('300x550')
    center_window(friends_wind, 300, 550)

    moreFrame = Frame(friends_wind)
    moreFrame.pack()

    ########################HEADER for Recipes Page ######################
    headerText(friends_wind, 'Friends')
    ######################################################################

    tryBtn = font.Font(family='Helvetica', size=16, weight='bold')

    friend1 = Label(friends_wind, text='Shawn Smith', font=tryBtn)
    friend1.pack()

    friend2 = Label(friends_wind, text='Timmy Turner', font=tryBtn)
    friend2.pack()

    friend3 = Label(friends_wind, text='Petty Patty', font=tryBtn)
    friend3.pack()

    friend4 = Label(friends_wind, text="Laughin' Larry", font=tryBtn)
    friend4.pack()

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(friends_wind)
    ############################################################


def verWindow():
    """
    No functionalities developed
    Verification for users, just like twitter
    Filler to make More page look more full
    """
    global ver_wind
    ver_wind = Toplevel()
    ver_wind.title('Verification')
    ver_wind.geometry('300x550')
    center_window(ver_wind, 300, 550)

    moreFrame = Frame(ver_wind)
    moreFrame.pack()

    ########################HEADER for Recipes Page ######################
    headerText(ver_wind, 'Verification')
    ######################################################################
    tryBtn = font.Font(family='Helvetica', size=16, weight='bold')

    ver1 = Label(ver_wind, text="You are not currently Verified\n"
                                "Please apply Online.", font=tryBtn)
    ver1.pack()

    ################# BUTTONS AT BOTTOM ######################
    navigation_buttons(ver_wind)
    ############################################################


if __name__ == '__main__':
    run_page()
