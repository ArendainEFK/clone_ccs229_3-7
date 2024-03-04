import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

def app():
    if "reset_app" not in st.session_state:
        st.session_state.reset_app = False

    if "user_inputs" not in st.session_state:
        st.session_state['user_inputs'] = []

    if "scaler" not in st.session_state:
        st.session_state["scaler"] = StandardScaler()

    if "clf" not in st.session_state:
        st.session_state["clf"] = []

    #initialize the slider variables
    if "initial_payment" not in st.session_state:        
        st.session_state['initial_payment'] = 200
    if "last_payment" not in st.session_state:
        st.session_state['last_payment'] = 12000
    if "credit_score" not in st.session_state:
        st.session_state['credit_score'] = 500
    if "house_number" not in st.session_state:
        st.session_state['house_number'] = 4000

    # Use session state to track the current form
    if "current_form" not in st.session_state:
        st.session_state["current_form"] = 1    

    # Display the appropriate form based on the current form state
    if st.session_state["current_form"] == 1:
        display_form1()
    elif st.session_state["current_form"] == 2:
        display_form2()
    elif st.session_state["current_form"] == 3:
        display_form3()

def display_form1():
    st.session_state["current_form"] = 1
    form1 = st.form("intro")

    # Display the DataFrame with formatting
    form1.title("Students' Adaptability Level Prediction in Online Education")
    text = """(c) 2024 Louie F. Cervantes, M.Eng. [Information Engineering] 
    CCS 229 - Intelligent Systems
    Computer Science Department
    College of Information and Communications Technology
    West Visayas State University"""
    form1.text(text)
                
    form1.subheader('The Decision Tree Algorithm')
    text = """The decision tree algorithm is a supervised learning technique 
    used for both classification and regression tasks. It works by building 
    a tree-like model with:
    \nNodes: These represent features (or questions) from your data.
    \nBranches: These represent the possible answers to those features (like "yes" or "no").
    \nLeaves: These represent the final predictions (like "spam" or "not spam").
    \nThe algorithm builds the tree by recursively splitting the data based on 
    the feature that best separates the data points into distinct groups. 
    This process continues until the data points at each leaf are sufficiently 
    similar, or some other stopping criteria is met."""
    form1.write(text)

    form1.write('Adatability Level Dataset')
    text = """The adaptability dataset contains information about 
    the adaptability of students in an online learning environment. 
    It has 1205 data points, representing individual students. 
    There are 14 features, including:
    Demographic information:
    Gender, Age, Education Level, Institution Type, Location
    \nLearning environment: IT Student, Load-shedding, 
    Financial Condition, Internet Type, Network Type, 
    Class Duration
    \nStudent behaviour: Self Lms, Device
    \nTarget variable: Adaptivity Level"""
    form1.write(text)
                                                                              
    submit1 = form1.form_submit_button("Start")

    if submit1:
        form1 = [];
        # Go to the next form        
        display_form2()

def display_form2():
    st.session_state["current_form"] = 2
    form2 = st.form("training")
    form2.subheader('Classifier Training')        

    #load the data and the labels
    dbfile = 'loan-repayment.csv'
    df = pd.read_csv(dbfile, header=0)

    #display the data set
    form2.write('Browse the dataset')
    form2.write(df)

    form2.write('The dataset descriptive stats')
    form2.write(df.describe().T)

    # Separate features and target variable
    X = df.drop('result', axis=1)  # Target variable column name
    y = df['result']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features using StandardScaler (recommended)
    scaler = st.session_state["scaler"] 
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    #save the scaler object for later use in prediction
    st.session_state["scaler"] = scaler
    
    fig, ax = plt.subplots(figsize=(6, 2))

    # Create the horizontal barplot
    sns.countplot(y='result', data=df, hue='result', palette='bright', ax=ax)

    # Add the title
    ax.set_title('Distribution of Paid/Not Paid')
    # Display the plot using Streamlit
    form2.pyplot(fig)
    form2.write("""Figure 1. The data shows that the debtors are almost equal between 
    those that paid their loans (yes) and those that did not (no).""")

    # Create a figure and an axis
    fig, ax = plt.subplots(figsize=(6, 6))

    # Create a scatter plot with color based on species
    sns.scatterplot(
        x="credit score",
        y="last payment",
        hue="result",
        palette="bright",
        data=df,
        ax=ax,
    )
    # Add labels and title
    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Last Payment")
    ax.set_title("Debtors Payment Status")

    # Add legend
    plt.legend(title="Paid the Loan")

    # Show the plot
    form2.pyplot(fig)

    form2.write("""\n\nFigure 2. The data shows that the groups paid
                and not paid is almost linearly separable based on their last payment.""")

    # Create and train the Decision Tree Classifier   
    clf = DecisionTreeClassifier(random_state=100, max_depth=3, min_samples_leaf=5)
    clf.fit(X_train_scaled, y_train)
    st.session_state["clf"] = clf

    # Make predictions on the test set
    y_test_pred = clf.predict(X_test_scaled)

    form2.subheader('Confusion Matrix')
    cm = confusion_matrix(y_test, y_test_pred)
    form2.text(cm)

    form2.subheader('Performance Metrics')
    form2.text(classification_report(y_test, y_test_pred))
        
    submit2 = form2.form_submit_button("Predict")
    if submit2:        
        display_form3()

def display_form3():
    st.session_state["current_form"] = 3
    form3 = st.form("prediction")
    form3.subheader('Prediction')
    form3.write('The trained model will predict if a debtor will repay the loan or not')

    initial_payment = form3.slider(
        label="Initial Payment:",
        min_value=100,
        max_value=500,
        on_change=update_values(),
        key="initial_payment",
        value = 300
    )

    last_payment = form3.slider(
        label="Last Payment:",
        min_value=10000,
        max_value=15000,
        on_change=update_values(),
        key="last_payment",
        value = 12000
    )

    credit_score = form3.slider(
        label="Credit Score:",
        min_value=100,
        max_value=1000,
        on_change=update_values(),
        key="credit_score",
        value = 500
    )

    house_number = form3.slider(
        label="House Number:",
        min_value=3000,
        max_value=5000,
        on_change=update_values(),
        key="house_number",
        value = 3700
    )

    update_values()

    predictbn = form3.form_submit_button("Predict")
    if predictbn:
        user_inputs = np.array(st.session_state['user_inputs'])

        scaler = st.session_state["scaler"]
        test_data_scaled =scaler.transform(user_inputs)
        test_data_scaled = np.array(test_data_scaled)

        form3.write(user_inputs)
        form3.write(test_data_scaled)

        predicted =  st.session_state["clf"].predict(test_data_scaled)
        result = 'Will the debtor pay? The model predicts: ' + predicted[0]
        form3.subheader(result)

    submit3 = form3.form_submit_button("Reset")
    if submit3:
        st.session_state.reset_app = True
        st.session_state.clear()
        form3.write('Click reset again to reset this app.')

def update_values():
    """Get the updated values from the sliders."""
    initial_payment = st.session_state['initial_payment']
    last_payment = st.session_state['last_payment']
    credit_score = st.session_state['credit_score']
    house_number = st.session_state['house_number']

    st.session_state['user_inputs'] = [[initial_payment, 
        last_payment, credit_score, house_number]]

if __name__ == "__main__":
    app()
