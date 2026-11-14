FROM public.ecr.aws/lambda/nodejs:20@sha256:a4440274d6f0fb4e6cb92cd5f2a97254efe6612f631d9974b197ecbd4a61fcab

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
