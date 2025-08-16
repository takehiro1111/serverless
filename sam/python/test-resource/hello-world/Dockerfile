FROM public.ecr.aws/lambda/nodejs:20@sha256:e579f6e33eb0b1e71d32e88336588c0d57e8bd11037a828693ac26bd1a80c6e6

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
