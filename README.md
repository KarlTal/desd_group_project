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
2. Ensure that Docker Desktop is running.

3. Enter the django project directory and execute docker compose up --build.
```cmd
(.venv) C:\Users\talav\Desktop\New folder\desd_group_project>cd DESD_Project

(.venv) C:\Users\talav\Desktop\New folder\desd_group_project\DESD_Project>docker compose up --build 
+] Building 7.1s (10/10) FINISHED
 => [internal] load build definition from DockerFile                                                                     0.1s
 => => transferring dockerfile: 32B                                                                                      0.0s
```
4. Enter the Film Manager directory and execute docker compose up --build.
```cmd
(.venv) C:\Users\talav\Desktop\New folder\desd_group_project>cd FilmManager

(.venv) C:\Users\talav\Desktop\New folder\desd_group_project\FilmManager>docker compose up --build 
[+] Building 1.3s (10/10) FINISHED
 => [internal] load build definition from DockerFile                                             0.1s
 => => transferring dockerfile: 32B                                                              0.0s
```

5. Enter ```Docker Desktop``` and open the port in the browser and now the application should be running.

---
