FROM public.ecr.aws/lambda/nodejs:26@sha256:a5ec3dfb14ceacb9276f95e36270f6cfd496ec798a26ae3f5dd045361b676245

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
