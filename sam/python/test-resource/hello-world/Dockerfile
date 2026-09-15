FROM public.ecr.aws/lambda/nodejs:24@sha256:2c0ff7196d00c51fb3a8bdc8cc98c7df5db21b5f144ad35330ec4efeb5dbd5b2

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
