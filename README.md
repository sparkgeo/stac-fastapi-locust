# stac-fastapi-locust
Locust load balancing for stac-fastapi


## Run stac-fastapi pgstac 
```$ docker-compose build```   
```$ docker-compose up```

## Ingest test data
```$ make ingest```

## Install
```$ pip install -e .```

## Start Locust
```$ locust```

## Run Load Balancing   
- go to ```http://localhost:8089``` and start with desired settings

## References  
  
- https://betterprogramming.pub/introduction-to-locust-an-open-source-load-testing-tool-in-python-2b2e89ea1ff
