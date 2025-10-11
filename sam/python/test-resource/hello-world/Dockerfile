FROM public.ecr.aws/lambda/nodejs:22@sha256:a13e332d46d6c93b83b23f60d080f1d50e43ce034bfef4e1f185f65cdc0f435f

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
