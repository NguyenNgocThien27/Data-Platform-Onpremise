VERSION=latest

build:
	# build hadoop base services
	docker build -t hadoop-base:${VERSION} ./.docker/hadoop/hadoop-base
	# build hive base services
	docker build -t hive-base:${VERSION} ./.docker/hive/hive-base
	# build spark base services
	docker build -t spark-base:${VERSION} ./.docker/spark/spark-base
	
