import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

# Function to handle user input and display the chat history
def user_input(user_question):
    # Get the response from the conversational chain
    response = st.session_state.conversation({'question': user_question})
    
    # Update the chat history in session state
    st.session_state.chatHistory = response['chat_history']
    
    # Display the chat history
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.write("User: ", message.content)  # Display user messages
        else:
            st.write("Reply: ", message.content)  # Display responses

# Main function to set up the Streamlit app
def main():
    # Configure the Streamlit page
    st.set_page_config(page_title="Information Retrieval")
    st.header("Information Retrieval System💁")

    # Input field for user questions
    user_question = st.text_input("Ask a Question from the PDF Files")

    # Initialize session state variables if not already set
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None

    # If there is a user question, process it
    if user_question:
        user_input(user_question)

    # Sidebar for PDF file upload and processing
    with st.sidebar:
        st.title("Menu:")
        
        # Upload PDF files
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        
        # Button to process uploaded PDF files
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                # Extract text from the PDF files
                raw_text = get_pdf_text(pdf_docs)
                
                # Chunk the text for processing
                text_chunks = get_text_chunks(raw_text)
                
                # Create a vector store from the text chunks
                vector_store = get_vector_store(text_chunks)
                
                # Initialize the conversational chain with the vector store
                st.session_state.conversation = get_conversational_chain(vector_store)
                
                # Notify the user that processing is complete
                st.success("Done")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
