FROM public.ecr.aws/lambda/nodejs:24@sha256:be67ba081682260b6a2b7c96f1baf5e3b7d55670349f2cb918cff770cec2be47

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
