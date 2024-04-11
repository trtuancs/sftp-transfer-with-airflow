<!-- PROJECT TITLE -->
<div align="center">
<h1 align="center">SFTP TRANSFER WITH AIRFLOW</h1>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#description-of-the-problem">Description of the problem</a>
      <ul>
        <li><a href="#examples">Examples</a></li>
      </ul>
    </li>
    <li>
        <a href="#the-architecture">The architecture</a>
    </li>
    <li>
        <a href="#project-structure">Project Structure</a>
    </li>
    <li>
        <a href="#getting-started">Getting Started</a>
        <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#start-project">Start project</a></li>
        <li><a href="#stop-project">Stop project</a></li>
      </ul>
    </li>
  </ol>
</details>

<!-- Description of the problem -->
## Description of the problem  
Develop an Apache Airflow DAG that facilitates the transfer of files from the SFTP server at `<source>` to the SFTP server at `<target>`
and ensures the preservation of the original directory structure.  
The synchronization process should be unidirectional; hence, any modification made on `<target>` must not impact the `<source>`.  
Deleted files on SFTP server at <source> must remain intact on <target> server.  

### Examples:  
* On March 1st, 2024, when a file named sftp://<source>/a/b/c/file_1.txt is detected on the source server, it should be replicated to sftp://<target>/a/b/c/file_1.txt on the destination server.  
* On March 2nd, 2024, a file named sftp://<source>/a/b/c/file_2.txt appears on the source server and subsequently should be transferred to sftp://<target>/a/b/c/file_2.txt on the destination server.  
* On March 3rd, 2024, a file named sftp://<source>/a/b/c/file_3.txt appears on the source server and should then be transferred to sftp://<target>/a/b/c/file_3.txt on the destination server.  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- The architecture -->
## The architecture  
![The architecture of project](images/the-architecture.drawio.png)  
Details of setting up project services can be found in the [docker-compose.yml](docker-compose.yml)

<!-- Project structure --> 
## Project structure  
```
|- dags/
|   |- configs/
|   |- libs/
|   |- sftp_file_transfer_dag.py    # sftp file transfer dag
|- images/
|- .gitignore
|- docker-compose.yml               # all services of project
|- Dockerfile                       # dockerfile for airflow image
|- README.md
|- requirements.txt                 # libs need install for project
```

<!-- Getting Started -->  
## Getting Started  

### Prerequisites  
To run the project, you need to have **Docker** and **Docker Compose** installed.  

### Start project  
To start project: ```docker-compose up -d```

### Stop project  
To stop project: ```docker-compose down```

