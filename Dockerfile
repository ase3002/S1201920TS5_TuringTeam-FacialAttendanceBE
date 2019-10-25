FROM caoliu98/face_recognition:latest

# Root directory in ther container
RUN mkdir /backend
WORKDIR /backend
COPY ./requirements.txt /backend/

# Install python packages
RUN pip install -r requirements.txt
COPY . /backend/
