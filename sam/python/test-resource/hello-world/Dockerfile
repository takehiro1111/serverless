FROM public.ecr.aws/lambda/nodejs:22@sha256:22e7b59e399e70f7195f986feceabce85e09d79cce8ff1452b7097984d2cde3e

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
