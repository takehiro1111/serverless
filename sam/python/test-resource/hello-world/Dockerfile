FROM public.ecr.aws/lambda/nodejs:24@sha256:9d7dcad6de2f4bb85f65af1d70d14c936c671b0541a49566a2b5d3db51195b03

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
