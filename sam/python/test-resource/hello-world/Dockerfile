FROM public.ecr.aws/lambda/nodejs:20@sha256:08afe3709f257b95a5517438d0b7c829c8271e44a99eb9d95519922d63d49839

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
