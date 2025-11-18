FROM public.ecr.aws/lambda/nodejs:22@sha256:da86ccaed75c763b3b89d3da2e04d41af3c1b219e83212143769c79ccc1820c7

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
