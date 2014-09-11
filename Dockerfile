# Cassandra
#
# VERSION               0.0.1
# BUILD-USING:        docker build -t cassandra .
# PUSH-USING:         docker tag cassandra surf/cassandra  && docker push surf/cassandra

FROM      surf/base-jvm
MAINTAINER Dan Kinsley <dan@queuenetwork.com>

# add datastax apt repository
RUN echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
RUN curl --silent -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -

RUN sudo apt-get update && apt-get install -y \
	dsc20 \
	python-yaml

# Expose Cassandra ports
EXPOSE 7000 7199 9160 61620 61621

# add the launch script
ADD run.py /run.py
RUN chmod 700 /run.py
# Launch cassandra
CMD ["/run.py"]
