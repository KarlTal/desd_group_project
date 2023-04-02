# desd_group_project

DESD Group Project based on the UWEFLIX case study. </br>

## Group 9

### Authors

<b> Daniel Hill - ```19014767```</b> <br/>
<b> Adrian Mitrea - ```20000146```</b> <br/>
<b> Alex Roussel-Smith - ```20019006``` </b><br/>
<b> Karl Talavera - ```20001879``` </b><br/> 

---

### Running the Django/Docker application

1. Enter the cloned repo.
```cmd
C:\Users\talav\Desktop\New folder\desd_group_project
```
2. In the command prompt/powershell enter the virtual environment.
```cmd
.venv\Scripts\activate
```
3. Enter the django project directory.
```cmd
(.venv) C:\Users\talav\Desktop\New folder\desd_group_project>cd DESD_Project

(.venv) C:\Users\talav\Desktop\New folder\desd_group_project\DESD_Project>
```
4. Run docker-compose up --build. 

5. Before executing docker compose --env-file .env up -d, ensure that the ```end of line sequence for the DESD_Project-entrypoint.sh``` is ```LF``` as ```GIT``` sometimes changes it ```CRLF``` which causes the docker cointainer to break as it cannot find the file.

5. Execute ```docker compose --env-file .env up -d```to initialise the docker container.
```cmd
(.venv) C:\Users\talav\Desktop\Group\desd_group_project\DESD_Project>docker compose --env-file .env up -d
[+] Running 0/1
 - desd_project Warning                      1.4s 
[+] Building 3.7s (11/11) FINISHED
[+] Running 3/3
 - Network desd_project_default           Create...                                0.8s
 - Container desd_project-mysql_db        Sta...                                   1.6s
 - Container desd_project-desd_project-1  Started                                  2.8s
```

6. Enter ```Docker Desktop``` and open the port in the browser and now the application should be running.

---
