import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import subprocess
from PIL import Image
import requests
from utils import lime_xai, login, model_predictions, preprocess_image
from skimage.segmentation import slic, mark_boundaries
       
# Title
st.title('HASH Project Dashboard')

# Sidebar
page = st.sidebar.selectbox('Navigation', ["Model Prediction", "Train Model", "Model Analysis"])
st.sidebar.markdown("""---""")
#st.sidebar.write("Created by [MARCONI LAB@MAK](https://marconilab.org/)")
st.sidebar.write("PROJECT PARTNERS")
st.sidebar.image("marc.jpg", width=100)
st.sidebar.image("ailab.jpg", width=100)
st.sidebar.image("mak.jpg", width=100)
st.sidebar.image("hash.jpg", width=100)

# Parameter initialization
submit = None
uploaded_file = None

if page == "Model Prediction":
    # Inputs
    st.markdown("Select input ultrasound image.")
    upload_columns = st.columns([2, 1])
    
    try:
        # File upload
        file_upload = upload_columns[0].expander(label="Upload an image file.")
        uploaded_file = file_upload.file_uploader("Choose an image file", type=['jpg','png','jpeg'])

        # Validity Check
        if uploaded_file is None:
            st.error("No image uploaded :no_entry_sign:")
        if uploaded_file is not None:
            st.info("Image uploaded successfully :ballot_box_with_check:")

            # Open the image using Pillow
            image = Image.open(uploaded_file)
            upload_columns[1].image(image,caption="Uploaded Image")
            submit = upload_columns[1].button("Submit Image")

    except Exception as e:
        st.error(f"Error during file upload: {str(e)}") 

    # Data Submission
    st.markdown("""---""")
    if submit:
        try:
            with st.spinner(text="Fetching model prediction..."):
                # Preprocess Input Image
                array = preprocess_image(image)
                # Predictions
                probabilities = model_predictions(array)
                prediction = [1 if pred > 0.5 else 0 for pred in probabilities]
                print("Probability: ",probabilities)

            # Ouputs
            outputs = st.columns([2, 1])
            outputs[0].markdown("Pathology Prediction: ")

            if prediction[0] == 0:
                outputs[1].success("No Myoma")
            elif prediction[0] == 1:
                outputs[1].success("Myoma Detected")
            else:
                outputs[1].error("Error: Invalid Outcome")

            prediction_details = st.expander(label="XAI using LIME")
            details = prediction_details.columns([3, 1])
            with st.spinner(text="Fetching prediction explanations..."):
                # All of this is mocked
                explanation_image_1,explanation_image_2,mask_1,mask_2,img,prediction = lime_xai(uploaded_file)
                
                # Image and Mask display (Example with matplotlib and Streamlit)
                fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 10))
                plt.subplots_adjust(wspace=0.01, hspace=0)
                ax1.imshow(img)
                ax1.set_title('Input Image')
                ax1.axis('off')
            
                ax2.imshow(mark_boundaries(explanation_image_2/255,mask_2))
                ax2.set_title('LIME Explanation')
                ax2.axis('off')

                ax3.imshow(mark_boundaries(explanation_image_1/255,mask_1))
                ax3.set_title('Regions of Focus')
                ax3.axis('off')
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")

elif page == "Train Model":
    st.header("Train Model")
    st.markdown("This page will be available soon :no_entry_sign:")
 
elif page == "Model Analysis":
    st.header("Model Comparison and Analysis")
    st.markdown("This page will be available soon :no_entry_sign:")

else:
    st.markdown("This page will be available soon :no_entry_sign:")


