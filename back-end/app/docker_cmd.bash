# Create a new container with the name my-mongo and the image mongo:4.4.6
sudo docker run --name my-mongo -d -p 27017:27017 mongo:4.4.6

# Start the container with the name my-mongo
sudo docker start my-mongo

# Stop the container with the name my-mongo
sudo docker stop my-mongo

# Remove the container with the name my-mongo
sudo docker rm my-mongo
