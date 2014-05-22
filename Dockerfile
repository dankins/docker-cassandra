# Cassandra
#
# VERSION               0.0.1
# BUILD-USING:        docker build -t docker-cassandra .
# PUSH-USING:         docker tag docker-cassandra quay.io/queue/docker-cassandra  && docker push quay.io/queue/docker-cassandra

FROM      ubuntu
MAINTAINER Dan Kinsley <dan@queuenetwork.com>

# software-properties are so we can run "add-apt-repository"
RUN apt-get update && apt-get install -y curl unzip software-properties-common python-software-properties supervisor

# repository for java7
RUN add-apt-repository ppa:webupd8team/java
# accept license without requiring user intervention
RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
# and now install oracle java7
RUN sudo apt-get update && apt-get install -y \
	oracle-java7-installer \
	python-yaml

# add datastax apt repository
RUN echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
RUN curl --silent -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -

RUN sudo apt-get update && apt-get install -y \
	dsc20 \
	libjna-java

# Expose Cassandra ports
EXPOSE 7000 7199 9160 61620 61621

# add the launch script
ADD run.py /run.py
RUN chmod 700 /run.py
# Launch cassandra
CMD ["/run.py"]
