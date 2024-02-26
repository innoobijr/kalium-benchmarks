FROM ghcr.io/openfaas/of-watchdog:0.9.15 as watchdog

FROM node:21-alpine3.18 as ship



COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

#RUN apk --no-cache add curl ca-certificates \
#    && addgroup -S app && adduser -S -g app app

RUN apt-get update
RUN apt-get install -y curl ca-certificates nodejs npm
RUN addgroup --system app && adduser --system --ingroup app app

#COPY ./libssl.so.1.1 ./libcrypto.so.1.1 /usr/lib/x86_64-linux-gnu/

WORKDIR /root/

# Turn down the verbosity to default level.
ENV NPM_CONFIG_LOGLEVEL warn

RUN mkdir -p /home/app

# Wrapper/boot-strapper
WORKDIR /home/app
COPY package.json ./

# This ordering means the npm installation is cached for the outer function handler.
RUN npm i

# Copy outer function handler
COPY index.js ./

# COPY function node packages and install, adding this as a separate
# entry allows caching of npm install
WORKDIR /home/app/function
COPY function/*.json ./
#COPY function/kv-store ./kv-store
RUN npm i || :

COPY ./libssl.so.1.0.0 ./libcrypto.so.1.0.0 /usr/lib/x86_64-linux-gnu/
# COPY function files and folders
COPY function/ ./

# Set correct permissions to use non root user
WORKDIR /home/app/

# chmod for tmp is for a buildkit issue (@alexellis)
RUN chown app:app -R /home/app \
    && chmod 777 /tmp

USER app

ENV cgi_headers="true"
ENV fprocess="node index.js"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:3000"

ENV exec_timeout="0s"
ENV write_timeout="15s"
ENV read_timeout="15s"

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]

