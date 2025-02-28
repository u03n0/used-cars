# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Install any needed packages specified in requirements.txt
# It's a good idea to have a requirements.txt file that contains your app dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port the app runs on
EXPOSE 8501

# Step 6: Define environment variable (Optional but helps keep things clean)
ENV STREAMLIT_SERVER_PORT=8501

# Step 7: Run streamlit app when the container starts
CMD ["streamlit", "run", "frontend/app.py"]
