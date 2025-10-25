FROM public.ecr.aws/lambda/nodejs:20@sha256:d58766ca36227aedb3783925e3e9c29ea7a468ac18e3a7267804ff7dd9f24734

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
