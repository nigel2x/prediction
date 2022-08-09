import pickle
import streamlit as st
from sklearn.tree import DecisionTreeClassifier
with open('DT_model_pickle','rb') as file:
    clf = pickle.load(file)


def main():
    st.title('แบบรายงานคุณลักษณะการกำกับการเรียนรู้')
    sex_options = {
        1: "ชาย",
        2: "หญิง"}

    sex = st.radio( 
        label="เพศ : ",
        options= (1, 2,),
        format_func=lambda x: sex_options.get(x),)
    st.write(f'You have chosen {sex_options.get(sex)}'
        f' with the value {sex}.')

    sw = st.number_input('วิชาคณิตศาสตร์')
    pl = st.number_input('วิชาวิทยาศาสตร์')
    pw = st.number_input('วิชาภาษาไทย')
    
    #genre = st.radio(
     #"What's your favorite movie genre",
     #('Comedy', 'Drama', 'Documentary'))

    if st.button('Predict'):
        result = clf.predict([[sl,sw,pl,pw]])

        if result==0:
            st.success('Setosa')

        elif result == 1:
            st.success('Versicolor')

        else:
            st.success('Virginica')


if __name__=='__main__':
    main()
