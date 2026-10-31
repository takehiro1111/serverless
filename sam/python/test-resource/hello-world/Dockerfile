FROM public.ecr.aws/lambda/nodejs:24@sha256:8466f17dcfbec19afcfefff53964fac7bc3f7975fa132d5fd74dce53004827d0

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
