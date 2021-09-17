# SATAY pipeline

SATAY makes use of containerization with Docker. Docker is an open platform for developing, shipping, and running applications. Docker provides the ability to package and run an application in a loosely isolated environment called a container. Containers are lightweight and contain everything needed to run the application, so you do not need to rely on what is currently installed on the host system. You can easily share containers while you work, and be sure that everyone you share with gets the same container that works in the same way.

![image](https://user-images.githubusercontent.com/15414938/123805382-52543b00-d8ee-11eb-8f76-ae598d6fdb83.png)

**Dockerfile** – is a text document that contains all the commands you would normally execute manually in order to build a Docker image. The instructions include a choice of operating system and all the libraries we need to install into it. Docker can build images automatically by reading the instructions from a Dockerfile.  
**Docker Images** – are the basis of containers. A Docker image is an immutable (unchangeable) file that contains the source code, libraries, dependencies, tools, and other files needed for an application to run.  
**Docker Container** – A container is, ultimately, just a running image.
