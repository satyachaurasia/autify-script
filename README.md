# autify-script

Autify-Script fetch web-pages and saves them to the disk for later retrieval and and browsing. 

### Running the Script

```sh
cd autify-script
docker build -t autify-script:v1 .
```

This will create the autify-script image and pull in the necessary dependencies.

Once done, run the Docker image to go inside the docker container.
```sh
docker run -it --rm autify-script:v1  sh
```

After running the above command, you can run the main script by passing required parameters. This command will fetch and store their html file on the disk, which you can verify by doing `ls` 

```sh
python3 main.py https://www.google.com https://autify.com 
```

To get the metadata of the files we can can pass optional parameter `-m` or `--metadata` with the above command. 

```sh
python3 main.py -m https://www.google.com https://autify.com
```
