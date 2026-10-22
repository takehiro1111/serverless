FROM public.ecr.aws/lambda/nodejs:24@sha256:92b7cccd985332238af80ac8da42d6965d418552e88955e315da4e3c0c76ca79

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
