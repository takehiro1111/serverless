FROM public.ecr.aws/lambda/nodejs:24@sha256:180fb515d4af0e77558ee267457ac8bd59328bef89f4f21e5d2cec72be6fefff

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
