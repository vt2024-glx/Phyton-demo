import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Demo Dashboard",
    page_icon="✨",   # munculin EMOJI: Windows + Titik(.)
    layout='wide'
)

st.title("Financial Insight Dashboard: Loan Performance & Trends")

st.markdown("---")   # Menambahkan garis

st.sidebar.header("Dashbord Filter and Features")

st.sidebar.markdown(
    '''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)


#loan=pd.read_csv('data_input/loan.csv)
#loan[issue_date']=pd.to.datetima(loan['issue_date'],dayfi)
loan = pd.read_pickle('data_input/loan_clean')
loan['purpose']=loan['purpose'].str.replace("_"," ")

st.metric('Total Loan',f"{loan['id'].count():,.0f}")

st.metric('Total Loan Amount',f"{loan['loan_amount'].sum():,.0f}")
#https://docs.streamlit.io/develop/api-reference --> REFERENSI

# Menambahkan Kotal/ Container pada dashboard --> supaya lebih estetik
with st.container(border=True):
    col1, col2, =st.columns(2)   #mendefinisikan NAMA KOLOM  
    #perhatikan indentasi (lakukan select --> tab untuk mengidentifikasi multi-line)

    with col1:
        st.metric('Total Loan',f"{loan['id'].count():,.0f}",help="Total Number of Loans")
        st.metric('Total Loan Amount',f"{loan['loan_amount'].sum():,.0f}",help="Total Amount of Loans")

    with col2:
        st.metric('Average Interest Rate',f"{loan['interest_rate'].mean():,.0f}",help="Average Number of Interest Rates")
        st.metric('Average Loan Amount',f"{loan['loan_amount'].mean():,.0f}",help="Average Amount of Loans")



import plotly.express as px  #--> untuk mulai masuk ke UPLOAD VISUALISASI
with st.container(border=True):
    tab1, tab2, tab3 =st.tabs(['Loans Issued Over Time',
                            'Loan Amount Overtime',
                            'Issue Data Analysis'])
    #gunakan list '[]' untuk memberikan NAMA tiap TABS

    with tab1:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()

        # Memasukkan hasil VISUALISASI yang kmrn sdh dibuat 
        line_count=px.line(
        loan_date_sum,
        markers=True,
        title="Number of Loans Issued Over Time",
        labels={
            "issue_date": "Issue Date",
            "value": "Number of Loans"
        }).update_traces(marker={'color':'red'}).update_layout(showlegend=False)
        
        st.plotly_chart(line_count)  #tampilkan fig ploty di dashboard


    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()

        line_sum=px.line(
        loan_date_sum,
        markers=True,
        labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
        },
        template='seaborn',
        title="Loans Amount Over Time",
        ).update_layout(showlegend = False).update_traces(marker={'color':'green'}).update_traces(line={'color':'red'})

        st.plotly_chart(line_sum)

    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()

        line_dist=px.bar(
        loan_day_count,
        category_orders={ 
            'issue_weekday':['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        },
        title='Distribution of Loans by Day of the Week',
        labels={
            'value':'Number of Loans',
            'issue_weekday':'Day of the Week'
        },
        template='seaborn'
        ).update_layout(showlegend=False)

        st.plotly_chart(line_dist)

with st.expander("click here to Expand Visualization"):
    col3, col4, =st.columns(2)

    with col3:
        pie = px.pie(
        loan,
        names='loan_condition',
        hole=0.4,
        title="Distribution of Loans by Condition",
        template='seaborn'
        ).update_traces(textinfo='percent+value')

        st.plotly_chart(pie)    
 
    with col4:
        grade = loan['grade'].value_counts().sort_index()

        loan_bar = px.bar(
        grade,
        labels={
            'index':'Grade',
            'value':'Number of Loans',
            'variable': 'Variable'
        },
        title='Distribution of Loans by Grade',
        template='seaborn'
        ).update_layout(showlegend=False)

        st.plotly_chart(loan_bar)    

condition=st.selectbox("Select Loan Condition",["Good Loan", "Bad Loan"])
loan_condition=loan[loan['loan_condition']==condition]

#buat 2 tab isi:
# -Loan amount Dist (histogram)
# -Loan amount Dist by Puspose (boxplot)

with st.container(border=True):
    tab4, tab5 =st.tabs(['Loan Amount Distribution',
                            'Loan Amount Distribution by Purpose'])
    #gunakan list '[]' untuk memberikan NAMA tiap TABS

    with tab4:
        loan_condition = loan[loan['loan_condition'] == 'Good Loan']

        histogram=px.histogram(
        loan,
        x='loan_amount',
        nbins=20,
        color='term',  # kolom pada dataframe untuk memecah/menentukan perbedaan warna
        color_discrete_sequence=['darkslateblue', 'tomato', 'lightsteelblue'],
        title='Loan Amount Distribution by Condition',
        labels={
            'loan_amount':'Loan Amount',
            'term':'Loan Term'
        },
            template='seaborn'
        )

        st.plotly_chart(histogram)    

    with tab5:
        By_Purpose=px.box(
        loan_condition,
        x = 'purpose',
        y = 'loan_amount',
        color = 'term',
        color_discrete_sequence=['darkslateblue', 'tomato','lightblue'],
        title='Loan Amount Distribution by Purpose',
        labels={
            'loan_amount': 'Loan Amount',
            'term': 'Loan Term',
            'purpose': 'Loan Purpose'
        }
        )
        st.plotly_chart(By_Purpose)

















