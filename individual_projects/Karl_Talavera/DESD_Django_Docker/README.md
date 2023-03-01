# Django and Docker Mini-project for DESD

A repository for the Django and Docker mini project for DESD. </br>

This repository contains a virtual environment ```.venv``` and a folder for the django/docker project, ```uweflix_project```.

# Author
<b> Name : Karl Talavera </b> <br/>
<b> ID : 20001879 </b>

## Prequisites
- Git Bash
- Docker Desktop

---

### Installation on local machine
1. Obtain the http link from the clone git lab repository.
2. Create a new bash shell.
3. Enter a folder and then in the bash shell enter : ```git clone '<http link>' ```

---

### Running the Django/Docker application
1. Enter the cloned repo.
```cmd
C:\Users\talav\Desktop\New folder\DESD_Django_Docker
```
2. In the command prompt/powershell enter the virtual environment.
```cmd
.venv\Scripts\activate
```
3. Enter the django project directory.
```cmd
(.venv) C:\Users\talav\Desktop\New folder\DESD_Django_Docker>cd uweflix_project

(.venv) C:\Users\talav\Desktop\New folder\DESD_Django_Docker\uweflix_project>
```
4. Before executing docker compuse up -d, ensure that the ```end of line sequence for the uweflix_project-entrypoint.sh``` is ```LF``` as GIT sometimes changes it CRLF which causes the docker cointainer to break as it cannot find the file.

5. Execute ```docker compose up -d ```to initialise the docker container.
```cmd
(.venv) C:\Users\talav\Desktop\New folder\DESD_Django_Docker\uweflix_project>docker compose up -d
[+] Running 2/2
 - Network uweflix_project_default              Created      0.9s 
 - Container uweflix_project-uweflix_project-1  Started      2.0s
```

6. Enter ```Docker Desktop``` and open the port in the browser and now the application should be running.

---
