Docker Scraper
==============

This repository is a dockerised image of a Python web scraper app, based on Linux Ubuntu. The image is hosted on the Docker Hub and can be found [here][1].

## Technologies

Below are the main technologies used for this project. Take some time to familiarise yourself.

[scrapy][5]: an open source and collaborative framework for scraping data from websites.

[scrapyd][6]: a web service for your Scrapy spiders. Allows deployment and control of spiders via HTTP Json API. 

[scrapyd-client][7]: a client for scrapyd. Provides the scrapyd-deploy utility needed to deploy your spider projects to the Scrapyd server.

[scrapy-splash][8]: Provides Scrapy + JavaScript integration using Splash.

[scrapyrt][9]: Allows easy integration of HTTP API to your existing Scrapy project.

[pillow][10]: A Python Imaging Library that supports the ImagesPipeline.

## How to run

First, you need to install and configure Docker on your system following this [installation guide][2].

Once Docker is successfully installed and configured on your system (you should be able to run ```$ docker run hello-world```), you are ready to download a copy of this docker image.

### Downlaod local copy

Download the Docker image by using the following (replace **:version** with desired tag or empty for latest).

```bash
$ docker pull nichelia/scraper[:version]
```

According the docker-compose file, the image can be run as a background-daemon for ```scrapyd``` and as an interactive-shell for ```scrapy```

#### docker-compose.yml

```yaml
scrapyd:
  image: nichelia/scraper:[version]
  ports:
    - "6800:6800"
  volumes:
    - ./data:/var/lib/scrapyd
    - /usr/local/lib/python2.7/dist-packages
  restart: always

scrapy:
  image: nichelia/scraper:[version]
  command: bash
  volumes:
    - ./data:/var/lib/scrapyd
    - .:/code
  working_dir: /code
  restart: always
```

### Develop and Install custom scraper (and nhsbot)

Run the image as an interactive-shell (provides an environment with all the packages required for you to develop a new scrapy scpider).

```bash
$ docker-compose run --rm scrapy
```

To create your own spider, I recommend going through the Scrapy [tutorial][3] and following the same file structure as the provided ```nhsbot``` scrapy project.

Once you are satisfied with your scraper project, you are ready to deploy it to the ```scrapyd``` web service. The following commands will run ```scrapyd``` service on the background, navigate to your scraper project, eggify it and then deploy it by using ```scrapyd``` REST API.

```
$ scrapyd &
$ cd [path_to_custom_scraper_project]
$ scrapyd-deploy
$ exit
```

If successful, you should see a reply like:

```
{"status": "ok", "project": "[project_id]", "version": "[generated_version_number]", "spiders": [number_of_spiders], "node_name": "[generated_node_name]"}
```

Follow the same procedure to deploy the ```nhsbot``` scraper project.

```
$ scrapyd &
$ cd nhsbot/
$ scrapyd-deploy
$ exit
```

Expect a similar reponse if successful:

```
{"status": "ok", "project": "nhsbot", "version": "1498181035", "spiders": 1, "node_name": "ee38aa1dbb62"}
```

### Run web server

Run the image as a background-daemon for ```scrapyd```.

```bash
$ docker-compose up -d scrapyd
```

On your prefered browser, go to http://0.0.0.0:6800 and make sure that your custom scraper appears in the list of projects (top of page: Available projects).

### Run custom scraper spider job (and nhsbot/nhsuk)

To run the crawling of your deployed scraper, you have to make a call to the ```scrapyd``` REST API.
Remember to replace **project_id**, **spider_name** and **filepath**.

```bash
$ curl http://0.0.0.0:6800/schedule.json -d project=[project_id] -d spider=[spider_name] -d setting=FEED_URI=[filepath]
```

For example, for ```nhsbot/nhsuk```:
```bash
$ curl http://0.0.0.0:6800/schedule.json -d project=nhsbot -d spider=nhsuk -d setting=FEED_URI=file:///var/lib/scrapyd/items/nhsbot/nhsuk/sample.json
```

If successful you should see a similar response:

```
{"status": "ok", "jobid": "3f899fc057b911e782ac0242ac110002", "node_name": "697a4864a95a"}
```

You can monitor jobs, logs and extracted items on http://0.0.0.0:6800/jobs, http://0.0.0.0:6800/logs/ and http://0.0.0.0:6800/items/ respectively.

Make note of the job id for future reference.

### Cancel custom scraper job

In order to cancel a custom scraper job, you must know the id of the job.
Remember to replace **project_id** and **job_id**.

```bash
$ curl http://0.0.0.0:6800/cancel.json -d project=[project_id] -d job=[job_id]

```

### Stop web server

To stop the web server (background-daemon) you need the id of the container (obtained by ```$ docker ps```) and excecute the following:
Remember to replace **docker_container_id**.

```bash
docker stop [docker_container_id]
```

## Clean-up

Current project will use Docker containers, images and volumes. Check out [this][11] handy cheat sheet on how to clean-up after you finished.

[1]:  https://cloud.docker.com/swarm/nichelia/repository/docker/nichelia/scraper
[2]:  https://docs.docker.com/engine/installation
[3]:  https://doc.scrapy.org/en/latest/intro/tutorial.html#creating-a-project
[4]:  https://scrapyd.readthedocs.io/en/stable/deploy.html
[5]:  https://github.com/scrapy/scrapy
[6]:  https://github.com/scrapy/scrapyd
[7]:  https://github.com/scrapy/scrapyd-client
[8]:  https://github.com/scrapinghub/scrapy-splash
[9]:  https://github.com/scrapinghub/scrapyrt
[10]: https://github.com/python-pillow/Pillow
[11]: https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes